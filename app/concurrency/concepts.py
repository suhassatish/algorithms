"""
IK Instructor: nikhil.kolekar@gmail.com

Process has 10 threads and all threads have entered a deadlocked state. How can you recover them?
Ideas:
Is there some way to kill lower priority threads?
Can we attach the deadlocked process to a debugger and tinker with the state for the condition that
the threads were waiting on?

---------------------------------------------------------------------
Lazy initialization code:
Code will deadlock.
Class cannot execute any logic until its initialized.
THe run() in static {} will wait till an object is initialized.
The main() is waiting for static {} class initialization to be completed.
Hence, this is a code that will deadlock.

Solution:
Keep class init as simple as possible.
Allow main thread to finish init, before waiting for bg thread. This is error prone and NOT
recommended.
Remember: Waiting for bg thread during class init will lead to deadlock.

Solution code:

public class Lazy (

    static {
        thread.start()
    }
    public static void main(String[] args) {
        try {
            t.join();
        } catch (InterruptedException e) {
            throw new AssertionError(e);
        }
    }
}


TODO: Java threading API library - thread.start() - creates thread and gives it to scheduler.
 thread.run() - If its run(), its going to be only 1 thread.
If its start(),  then its unpredictable since we wont know which thread gets priority to execute.
---------------------------------------------------------------------
Synchronization:

Compiler thinks, there's a cost for me to read a variable.
In an infinite loop, I'm looking at a condition thats on an initialized value, which is not used in
the scope of that loop. Then compiler hardcodes the value to FALSE.

They dont see it in the context of a multi-threaded application. This technique is called hoisting.
So this code can run for ever, not just 1 second.

What is volatile?
Its a state that I intend to use across threads for inter-thread communication.
Its what I use to signal a value change from 1 thread to another.
Its more expensive than a regular variable read.
Some in-built protections kick in.
The moment its volatile, compiler wont cache it in system cache, nor will it try to optimize code.

Any critical section that needs a guarantee of single-threaded execution, the concern you're trying
to address is mutual exclusion.

The 2nd thing is inter-thread communication. How do you let another thread to wait, go-ahead etc?
Its an orthogonal concern to be managed. You need to know which concern you're handling, ie
inter-thread comm or mutual exclusion. Once you know which concern you're addressing, you'll
never go wrong.
---------------------------------------------------------------------
Publish-Subscribe Pattern

2 patterns commonly used -
1) Pub-Sub
2) Message Queue

Gang of 4 pattern called Observer.

Observable and observer: Used to decouple observable from lots of observers that come and go.

Final keyword - Once initialized to something, it cant be re-initialized to something else.
Final doesnt say its immutable. If you say observers = init_value1, and if you later do
observers = init_value2, then compiler will error out. But for observers.add(observer), it wont
error out.

Is synchronized a re-entrant lock? A thread goes into synchronized(observer) in notifyElementAdded()
and then calls removeObserver() which is in another synchronized block. The fact that thread1 held
the lock, it is re-entrant and can go into the other synchronized function since it already holds
the lock.

When you're iterating through a collection, you may get ConcurrentModificationException.

Take-aways:
1)
You should not write code within synchronized block that cedes control to a foreign method.
You have to move the foreign method outside of the synchronized block. By doing the notifications
through a snapshot copy.
This is a common pattern called copy-on-write. In more recent java versions, there's a collection
 called CopyOnWriteArrayList. Its a decorator.

2) When designing mutable class, evaluate internal synchronization.
3) Minimize amount of work performed within synchronized regions
4) Critical NOT to sync excessively
---------------------------------------------------------------------
In java , below 2 syntaxes are similar functionally.

void foo() {
    synchronized(this) {
    }
}

synchronized void foo() {
}
Using 'synchronized' is a huge serialization overhead. This comes at the cost of being thread-safe.
Thats why using very coarse-grained 'synchronized' construct at method level, is inefficient.
---------------------------------------------------------------------

java.lang.Object has a few methods inbuilt for concurrency to facilitate inter-thread communication:
void wait();  Pushes thread into wait mode and relinquishes control.

void notify(); Used to wake up a waiting thread. Only wakes up the next qualifying thread that
thread scheduler thinks is next in line.

void notifyAll(); This is a little dangerous. Wakes up all waiting threads.
Due to notifyAll causing spurious wake ups, you should always use the construct -
while (! condition_met){
    wait()
}
http://effbot.org/zone/thread-synchronization.htm
python equivalent of condition variable.
from threading import Condition
cond_var = Condition()

You should NOT use `if` instead of `while`.
 if (! condition_met) {
    wait()
} //this has risk of spurious wake-ups with NotifyAll

Try to use the constructs of Lock and Condition.
Having multiple instances of locks lets you control the granularity of your synchronization scope.
Have lock objects named appropriately for specific-purposes.

2nd is notion of Condition. Given any lock, you should be able to use
Lock newCondition(). You can create distinct wait sets. You get a wait() signal pair, that you
can limit to certain wait states.
---------------------------------------------------------------------
Double Check Locking - Popular phone interview question and controversial few years back, but now
controversy is dying down.

Object reference Escaping: 2 threads T1 and T2.
T1 acquires lock and goes into synchronized.
T2 is waiting outside of sync. What value will T2 see for var?

Using volatile works in java version > 1.4. Because compiler says expose the variable `var`
 only when you're done.
 eBay had PMD checks which would run lint against all known patterns and anti-patterns.

Is double-checked related to singleton design pattern?
In double-checked, we're trying to create a singleton guarantee.

3 volatile reads and 1 volatile write is expensive. How to fix it?

Having a 2nd non-volatile variable `result` = `var`. In all stable state, we only have 1 volatile
read and 1 volatile write.


Volatile never prevents mutual exclusion. It only enables inter-thread communication.

Poor man's version of single-check locking:

If you dont have singleton guarantee, its good enough.
---------------------------------------------------------------------
Count Down Latch - Making threads do real work

Initialize it to certain count, and then count down to 0.

Tips:
1) Make sure you dont have any busy-waits anywhere. ie, Important to do while(), outside the
synchronize.

Latch has 2 methods -
1) CountDown()
2) await()

def executor.execute(
    # provides executor definition (a runnable you can define)
    Runnable() {
        public void run():
            action.run()
    }
)

# need 3 latches -
# latch 1 - CountDownLatch(num_threads)
# latch2 - start (1-way comm from main thread to workers, with concurrency of 1) = CountDownLatch(1)
# latch3 - done - to comm back to main thread = CountDownLatch(num_threads)
---------------------------------------------------------------------

Producer consumer problem - bounded buffer or blocking queue
Simplest implementation = circular array with 2 pointers.

def produce(Item item):
    # blocks if inventory is full
    pass

def consume():
    # should block if empty
    # returns Item

http://www.dabeaz.com/usenix2009/concurrent/cond.py
---------------------------------------------------------------------
03/12/2017:

OS Synchronization primitives:

critical section: Allows only 1 thread to proceed, and all others block.
 Its an in-process primitive.

Mutex: works cross-process and provides exclusive access with wait() and signal().

Why have an in-process mutex? Overhead is lower, but only in a specific case,
when threads are uncontested. That is, I come into a critical section and no other thread
has it. I can take it fast  and as long as I can release it before the other thread comes along.
We dont have to do a kernel transition to take the lock.

Use in-process mutex when Most of the time, locks are uncontested.


Semaphores: Almost never use in practice. It keeps track of a count. If count < 0, it blocks.
Semaphore with count = 1 is a mutex.

When is a mutex faster than a semaphore?
They mean in-process mutex. When its an in-process mutex and lock is uncontested,
its faster. There are 2 things people call a mutex on linux. Out-of-process and in-process.

Interlocked operations or atomic operations: Take low-level operations like  swap, add,
load-linked-store-conditional (LL-SC) etc
and fuse the operations together by the hardware into 1 instruction.

like read from register, load from memory. Hardware locks that cache line and all other threads
have to spin. Its a spin lock. From the OS perspective, its just 1 thing to do.


"""





