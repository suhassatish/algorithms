# -*- coding: utf-8 -*-
"""
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

3) Threads have almost no overhead; processes have considerable overhead.

4) New threads are easily created; new processes require duplication of the parent process.

5) Threads can exercise considerable control over threads of the same process; processes can only
exercise control over child processes.

6) Changes to the main thread (cancellation, priority change, etc.) may affect the behavior of the
other threads of the process; changes to the parent process do not affect child processes.
"""