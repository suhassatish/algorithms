"""
http://blog.takipi.com/garbage-collectors-serial-vs-parallel-vs-cms-vs-the-g1-and-whats-new-in-java-8/
There are 4 TYPES OF GARBAGE COLLECTORS in Java.

1) Serial:  -XX:+UseSerialGC
    a) What it does: Uses a simple, single-threaded GC algo. For small (< 100 MB heaps)

2) Parallel: Use when appln can tolerate occasional long pauses & u want to maximize thruput, while
minimizing CPU usage.
    a) -XX:+UseParallelGC: Uses multiple threads to collect young gen while appln threads stopped
    b) -XX:+UseParallelOldGC: Uses multiple threads to collect old gen while appln threads stopped
    c) Parallel != Concurrent

3) CMS (Concurrent mark and sweep) - -XX:+UseConcMarkSweepGC
    a) Uses background threads to remove garbage from old gen with minimal pauses. Use when you
    have available CPU for the bg thread, you dont want long GC pauses, and have a relatively small
    heap.

    b) Amount of work performed in (cost of) a CMS cycle is proportional to number of live objects
        in tenured + time to process dead stuff & adjust the free lists

    c) Use -XX:+UseParNewGC in conjunction with above. Uses multiple threads to collect young gen
    when application threads are stopped.
Pros -
    a) Works reasonably well for small to medium sized heaps (< 2-4 GB heaps)
    b) Its still 1 of the most stable openJDK collectors with short pause times.(C4 from Azul aside)

Cons -
    a) Has some nasty stop-the-world (STW) GC pauses
    b) Configuration is too hard and clunky
----------------
4) G1: -XX:UseG1GC
G1 splits heap to regions = heap(size) / 2048
Types of regions =
    i) Eden ii) Survivor iii) Old gen iv) Humongous (>= 50% the size of a standard region)

    a) Uses multiple threads to collect young gen while appln threads are stopped, and bg threads to
    remove garbage from old gen with minimal pauses.

Pros -
    a) Low pause collector
    b) Low configuration overhead
    c) Can explicitly set pause-time goals

Cons -
    a) Requires large heaps.
    b) Support for G1 is stable only on java 1.8.0_40+ and is unstable in earlier Java versions
    c) It burns a lot of CPU
--------------------------------
Garbage collection goals -
1) Application throughput - What % of time are you willing to hand over to GC activity?
General thumb rule is 95%+ appln thruput. Conversely, GC thruput ~ < 5%

2) Pause time - How much are you willing to put up with? 2  ~3s pauses a day with the rest < 100ms

3) Memory footprint (JVM heapsize) - How much heap can you allocate/afford? Memory isn't always
cheap on virtualised envs.
----------------------------

HotSpot JVM: Architecture
    Top Layer: Class Loader Subsystem

    Runtime Data Areas:
        a) Method area
        b) Heap
        c) Java Threads
        d) Program Counter Registers
        e) Native Internal Threads

    Native Method Interface (to talk to Native Libraries)
    Execution Engine -
        a) JIT just in time compiler
        b) <>
----------------------------
Hotspot Heap Structure
    a) Eden (new objects) [Minor GC]  - Should run only for few ms.
    b) Survivor space - S0, S1
    c) Tenured - long-lived objects [Major GC]. Old generations are not moved around in-memory.
    d) Permanent Generation - classes, static member
----------------------------
jvisualVm with visualGC - Java Visual VM plugin to visualize GC.

Space is not compacted (when memory gets fragmented due to GC) unless there is full GC.

"""