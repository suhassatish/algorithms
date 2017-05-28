"""
What happens under the hood when a unix cmdline call `ls -l` is made?
https://medium.com/meatandmachines/what-really-happens-when-you-type-ls-l-in-the-shell-a8914950fd73

1) The parser checks the syntax of the command and makes sure the exectuable is found in $PATH
Usually, its either in /usr/bin/ls or /usr/sbin/ls, etc

3 kernel syscalls are made.
2) The system call `fork()` is made to duplicate the shell parent process, creating a child process

3) The syscall `execve()` is made which does the following:
    a) The OS context switches the parent process with the child process and loads up the new
    `ls` program
    b) During context switch, `execve()` replaces defining parts of the current process' memory
    stack with the new stuff loaded from `ls` executable file

4) Meanwhile, the parent process contrinues to do other things, keeping track of its children as
    well, using the system call `wait()`

5) Lastly, after ls -l is executed, the shell executes shutdown commands, frees up memory, exits and
re-prompts the user for input.
"""