# -*- coding: utf-8 -*-
"""
Thread control block (TCB) is a data structure in the operating system kernel which contains
thread-specific information needed to manage it. It contains the following info -
1) thread_id
2) program_counter
3) stack_pointer : Points to thread's stack in the process
4) state of the thread (running, ready, waiting, start, done)
5) thread's register values
6) pointer to the process control block (PCB) of the process the thread lives on
-------------------------
Process control block (PCB) - aka Task controlling block, process table, task struct, switchframe
Its a data structure in the OS kernel with info needed to manage a process. Its the manifestation of
a process in the OS. 3 main types of info is contained by PCB -
a) Process state data b) process control data c) process identification data
It includes  -

1) Process scheduling state - Ready, suspended, etc. Priority value, time elapsed since last state
    change. Event the process is waiting on.

2) process_id, children_ids, sibling_ids related in some way - thru process pool, queue, ring etc

3) IPC info for inter process communication - various flags, signals, msgs wrt communicating
    independently with other processes.

4) Process privileges - allowed/disallowed access to system resources

5) Process state - new, ready, running, waiting, dead depending on CPU scheduling

6) process_id - unique

7) CPU registers - where process needs to be stored for execution for running state

8) CPU scheduling info - Used to schedule process run on CPU

9) Memory management info - Page tables, memory limits, segment table depending on memory used by OS

10) Accounting info - Includes the amount of CPU used for process execution, time limits, exeID, etc

11) IO Status info - Includes a list of I/O devices allocated to the process

Since PCB contains critical info for a process, it must be kept in an area of memory protected from
normal user access. In many OSes, beginning of the kernel stack of the process is a convenient
protected location.

-------------------------
Differences between process and thread -

1) Threads are used for small tasks, whereas processes are used for more heavyweight tasks –
 basically the execution of applications.

2) Threads within the same process share the same memory address space, whereas different processes
do not.

A process has a virtual address space, executable code, open handles to system objects, a security
context, a unique process identifier, environment variables, a priority class, minimum and maximum
working set sizes, and at least one thread of execution. Each process is started with a single
thread, often called the primary thread, but can create additional threads from any of its threads.

A thread is an entity within a process that can be scheduled for execution. All threads of a process
share its virtual address space and system resources. In addition, each thread maintains exception
handlers, a scheduling priority, thread local storage, a unique thread identifier, and a set of
structures the system will use to save the thread context until it is scheduled. The thread context
includes the thread's set of machine registers, the kernel stack, a thread environment block, and a
user stack in the address space of the thread's process. Threads can also have their own security
context, which can be used for impersonating clients.
--------
Taken from "Parallel and Distributed Programming Using C++" by Cameron Hughes and Tracey Hughes,
Table 4-1:

What is the difference between threads and processes?
The major differences between threads and processes are:

1) Threads have direct access to the data segment of its process; processes have their own copy of
the data segment of the parent process.

2) Threads can directly communicate with other threads of its process; processes must use
interprocess communication to communicate with sibling processes.

3) Threads have almost no overhead; processes have considerable overhead. This is because processes
    have different virtual address spaces which means they are on different pages and a different
    page table has to be context switched and brought into memory. For threads, there is no such
    overhead to context switch as they all share the same address space within the same page table.

4) New threads are easily created; new processes require duplication of the parent process.

5) Threads can exercise considerable control over threads of the same process; processes can only
exercise control over child processes.

6) Changes to the main thread (cancellation, priority change, etc.) may affect the behavior of the
other threads of the process; changes to the parent process do not affect child processes.


"""