package answers.engine.precompute;

import java.io.DataOutputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Supplier;
import java.util.logging.Logger;

import com.google.common.collect.*;

import lib.logging.DiscoveryInfoLogRecord;

/**
 * AsynchronousWriter takes a collection of string preparation tasks and writes their outputs to an output stream
 * asynchronously. It is auto-closable.
 * 
 * <p>
 * Internal design: <br>
 * There are three queues: <br>
 * (a) processQueue: a blocking queue of Supplier<String> that keeps track of string preparation tasks to be
 *                   processed by processWorkers <br>
 * (b) writeQueue: a blocking queue of strings to be written to an output stream <br> 
 * (c) exceptionQueue: a buffer of exceptions encountered by any workers <br>
 * And the two kinds of workers: <br>
 * (a) processWorkers: each of which runs Supplier<String>.get(), and puts the output to writeQueue <br> 
 * (b) writeWorker: that dequeues strings in the writeQueue and writes them to the output stream <br>
 * 
 * This writer is not order preserving, meaning that the order of contents written to output stream is not
 * necessarily identical to that of supplier submissions (or even supplier completions). <br>
 * </p>
 * 
 * <pre>
 * Code pattern:
 * try (AsynchronousWriter writer = new AsynchronousWriter(outputStream, logger, degreeOfParallelism)) {
 *    while (...) {
 *       writer.write(() -> { return string}); // a string supplier
 *    }
 *    
 *    writer.await();
 *    BigInteger writeCount = writer.getTotalWriteCount();
 * }
 * </pre>
 *
 *
 *
 */
class AsynchronousWriter implements AutoCloseable {
    // global state
    private enum State {RUNNING, STOPPED};
    private final long QUEUE_WAIT_TIME_IN_MILLIS = 100;
    // given max String length is 2^31-1, packing 1000 strings (~1M double-bytes each) in a write is unlikely to hit overflow issue
    private final int BULK_WRITE_SIZE = 1000;
    private final DataOutputStream outputStream;
    private final Logger logger;
    
    // executor, queues and workers
    private final ExecutorService executor;                             // thread pool
    private final BlockingQueue<Supplier<List<String>>> processQueue;   // queue of suppliers that generate output strings
    private final BlockingQueue<String> writeQueue;                     // queue of strings to be written to an output stream
    private final BlockingQueue<Exception> exceptionQueue;              // a collection of exceptions encountered in any actor    
    private final List<CompletableFuture<Void>> processWorkers;         // references to process workers that take supplier outputs to write queue
    private CompletableFuture<Void> writeWorker;                        // a reference to a write worker that writes to an output stream

    // global state and statistics
    private volatile State processState = State.RUNNING;
    private volatile State writeState = State.RUNNING;
    private volatile BigInteger localProcessCounts[];
    private volatile BigInteger totalProcessCount = BigInteger.ZERO;
    private volatile BigInteger totalWriteCount = BigInteger.ZERO;
    private AtomicLong totalProcessingTimeInMs = new AtomicLong(0);
    private AtomicLong totalWriteTimeInMs = new AtomicLong(0);
    private final long startTime = System.currentTimeMillis();
    private Long endTime = null;    // null means the writer is in progress
    
    /**
     * Constructor
     * 
     * @param outputStream
     * @param logger
     * @param processCount
     */
    public AsynchronousWriter(final DataOutputStream outputStream,
                              final Logger logger,
                              final int processCount) {
        this(outputStream, logger, processCount, 1);
    }
    
    /**
     * Constructor
     * 
     * @param outputStream
     * @param logger
     * @param processCount       # process worker (not including writeWorker, which is already 1, since write is not thread-safe)
     * @param processOutputCount # average number of items output by each process
     */
    public AsynchronousWriter(final DataOutputStream outputStream, 
                              final Logger logger, 
                              final int processCount,                       // if processCount = 1, the writer becomes order-preserving, but of lowest throughput
                              final int expectedOutputCountPerProcess) {    // the expected number of strings output by each process
        this.outputStream = outputStream;
        this.logger = logger;

        // Initialize queues with bounds to avoid memory over-consumption        
        final int processThreadCount = Math.max(processCount, 1);   // aka N        
        this.writeQueue = new LinkedBlockingQueue<String>(processThreadCount * expectedOutputCountPerProcess);
        this.processQueue = new LinkedBlockingQueue<Supplier<List<String>>>(1);     // i.e., N+1 processes can be accommodated
        this.exceptionQueue = new LinkedBlockingQueue<Exception>();                 // unbound, but exception thrown back to caller to stop
        
        final int totalThreadCount = processThreadCount+1;                          // N process workers + 1 write worker
        this.executor = new ThreadPoolExecutor(totalThreadCount, totalThreadCount, 1L, TimeUnit.MINUTES, new SynchronousQueue<Runnable>());        
        this.writeWorker = CompletableFuture.runAsync(() -> writeLoop(), executor);        
        
        this.processWorkers = Lists.newArrayList();
        this.localProcessCounts = new BigInteger[processThreadCount];
        for (int t=0; t<processThreadCount; t++) {
            final int index = t;
            localProcessCounts[index] = BigInteger.ZERO;
            processWorkers.add(CompletableFuture.runAsync(() -> processLoop(index), executor));
        }
    }
    
    /**
     * Close the writer that involves stopping all workers and closing the output stream.
     */
    @Override
    public void close() {
        try {
            await();
        } finally {
            try {
                if (outputStream != null) {
                    outputStream.close();
                }
            } catch (IOException e) {
                if (logger != null) {
                    logger.log(new DiscoveryInfoLogRecord.Builder()
                            .setMessageDetail_dxlog("Failed to close writer.")
                            .setMessageSubDetail_dxlog(e.getMessage())
                            .build());
                }
            }
        }
    }

    /**
     * It takes a supplier to be executed at later time. The result of the supplier is to be written to
     * an output stream.
     * 
     * @param supplier
     * @return AsynchronousWriter
     */
    public AsynchronousWriter writeAsync(final Supplier<String> supplier) {
        return multiWriteAsync(() -> Lists.newArrayList(supplier.get()));
    }
    
    /**
     * It takes a supplier to be executed at later time. The result of the supplier is to be written to
     * an output stream.
     * 
     * @param supplier
     * @return AsynchronousWriter
     */
    public AsynchronousWriter multiWriteAsync(final Supplier<List<String>> supplier) {
        throwIfAny();
        if (processState != State.RUNNING) {
            throw new RuntimeException("The writer is no longer running.");
        }
        
        try {
            processQueue.put(supplier);            
        } catch (Exception e) {
            exceptionQueue.add(e);
            throwIfAny();
        }
        
        return this;        
    }
    
    /**
     * Get the latest totalProcessCount value, which may be updated by processLoop, during the call.
     * No concurrency control as it needs not be accurate while the writer is running.
     * 
     * return the number of written lines
     */
    public BigInteger getTotalProcessCount() {
        if (processState == State.RUNNING) {
            totalProcessCount = getTotalProcessCountInternal();
        }
        
        return totalProcessCount; 
    }

    /**
     * Get the latest totalWriteCount value, which may be updated by writeLoop, during the call.
     * No concurrency control as it needs not be accurate while the writer is running.
     * 
     * return the number of written lines
     */
    public BigInteger getTotalWriteCount() {
        return totalWriteCount;
    }
    
    /**
     * Get the latest accumulated processing time, which may be updated by processLoop, during the call.
     * No concurrency control as it needs not be accurate while the writer is running.
     * 
     * @return processing time
     */
    public long getProcessingTimeInMs() {
        return totalProcessingTimeInMs.get();
    }
    
    /**
     * Get the latest accumulated write time, which may be updated by writeLoop, during the call.
     * No concurrency control as it needs not be accurate while the writer is running.
     * 
     * @return write time
     */
    public long getWriteTimeInMs() {
        return totalWriteTimeInMs.get();
    }
    
    /**
     * Get the total elapsed time. If a writer is still running, endTime is NULL and elapsed time will keep changing.
     * @return elapsed time
     */
    public long getElapsedTime() {
        return (endTime != null ? endTime : System.currentTimeMillis()) - startTime;
    }
    
    public Map<String, String> getPerformance() {
        return ImmutableMap.<String,String>builder()
            .put("#writes", getTotalWriteCount().toString())
            .put("#processes", getTotalProcessCount().toString())
            .put("elapsedTimeInMs", Long.toString(getElapsedTime()))
            .put("processTimeInMs", Long.toString(getProcessingTimeInMs()))
            .put("writeTimeInMs", Long.toString(getWriteTimeInMs()))
            .build();
    }
    

    /**
     * Get all exceptions.
     * 
     * @return a collection of exceptions
     */
    public List<Exception> getExceptions() {
        return ImmutableList.copyOf(exceptionQueue);
    }
    
    /**
     * Barrier for the caller thread to wait for write completion.
     * Exception if any throws after all workers stop.  
     * 
     * return AsynchronousWriter
     */
    public synchronized AsynchronousWriter await() {
        return await(Duration.ofMinutes(3));
    }
    
    /**
     * Barrier for the caller thread to wait for write completion.
     * Exception if any throws after all workers stop.  
     * 
     * return AsynchronousWriter
     */
    public synchronized AsynchronousWriter await(final Duration timeout) {
        terminateProcessLoop(timeout);
        terminateWriteLoop(timeout);
        
        try {
            processQueue.clear();
            writeQueue.clear();                            
            executor.shutdownNow();
        } catch (Exception e) {
            exceptionQueue.add(e);
        }
        
        if (logger != null) {
            logger.log(new DiscoveryInfoLogRecord.Builder().setMessageDetail_dxlog(
                    "write completion; #exception=" + exceptionQueue.size())
                    .build());
        }
        
        // update the end time if needed
        endTime = endTime != null ? endTime : System.currentTimeMillis();
        return this;        
    }
    
    /**
     * Worker logic that iterates processQueue, executes every single dequeued supplier and forwards
     * each result to writeQueue.
     * 
     * @return number of processed supplier
     */
    private void processLoop(int i) {
        while (exceptionQueue.isEmpty() && (processState == State.RUNNING || !processQueue.isEmpty())) {
            try {
                final Supplier<List<String>> s = processQueue.poll(QUEUE_WAIT_TIME_IN_MILLIS, TimeUnit.MILLISECONDS);
                if (s != null) {
                    final long startTime = System.currentTimeMillis();  // start time count after process dequeue time
                    final List<String> outputs = s.get();
                    if (outputs == null) {
                        continue;
                    }
                    
                    for (String output: outputs) {
                        writeQueue.put(output);                            
                    }
                    
                    localProcessCounts[i] = localProcessCounts[i].add(BigInteger.ONE);
                    totalProcessingTimeInMs.addAndGet(System.currentTimeMillis() - startTime);                    
                }
            } catch (Exception e) {
                exceptionQueue.add(e);
            }
        }
    }

    /**
     * Terminate process workers
     */
    private void terminateProcessLoop(final Duration timeout) {
        if (processState == State.RUNNING) {
            processState = State.STOPPED;
            
            // wait until all processWorkers finish
            for (CompletableFuture<Void> processWorker : processWorkers) {
                try {
                    processWorker.get(timeout.toMillis(), TimeUnit.MILLISECONDS);
                } catch (Exception e) {
                    exceptionQueue.add(e);
                }
            }            
            totalProcessCount = getTotalProcessCountInternal();

            if (logger != null) {
                logger.log(new DiscoveryInfoLogRecord.Builder().setMessageDetail_dxlog(
                        "process completion; #process=" + totalProcessCount.toString())
                        .build());                    
            }
        }
    }
    
    /**
     * Worker logic that iterates writeQueue and writes every single dequeued string to outputStream.
     */
    private void writeLoop() {
        final List<String> buffer = Lists.newLinkedList();
        while (exceptionQueue.isEmpty() && (writeState == State.RUNNING || !writeQueue.isEmpty())) {
            try {
                String s = writeQueue.poll(QUEUE_WAIT_TIME_IN_MILLIS, TimeUnit.MILLISECONDS);
                if (s != null) {
                    long startTime = System.currentTimeMillis();
                    int writeCount = 1;
                    if (BULK_WRITE_SIZE > 1) {
                        buffer.clear();
                        writeQueue.drainTo(buffer, BULK_WRITE_SIZE-1); // get subsequent n-1 items to write together
                        buffer.add(0, s);
                        s = String.join("", buffer);
                        writeCount = buffer.size();
                    }
                    
                    outputStream.writeBytes(s);
                    totalWriteCount = totalWriteCount.add(BigInteger.valueOf(writeCount));
                    totalWriteTimeInMs.addAndGet(System.currentTimeMillis() - startTime);
                }
            } catch (Exception e) {
                exceptionQueue.add(e);
            }
        }
        
        buffer.clear();
    }

    /**
     * Terminate write worker
     */
    private void terminateWriteLoop(final Duration timeout) {
        if (writeState == State.RUNNING) {
            writeState = State.STOPPED;
            
            try {
                writeWorker.get(timeout.toMillis(), TimeUnit.MILLISECONDS);
                if (logger != null) {
                    logger.log(new DiscoveryInfoLogRecord.Builder().setMessageDetail_dxlog(
                            "write completion; #write=" + totalWriteCount.toString())
                            .build());                    
                }
            } catch (Exception e) {
                exceptionQueue.add(e);
            }
        }
    }
    
    /**
     * Aggregate all process counts
     * 
     * @return sum of all local process counts
     */
    private BigInteger getTotalProcessCountInternal() {
        BigInteger cnt = BigInteger.ZERO;
        for (BigInteger i : localProcessCounts) {
            cnt = cnt.add(i);
        }
        
        return cnt;
    }
    
    /**
     * Throw the head queued exception if any.
     * 
     * @throws Exception
     */
    private void throwIfAny() {
        final Exception exception = exceptionQueue.peek();
        if (exception != null) {
            throw new RuntimeException("internal exception", exception);
        }
    }
}
