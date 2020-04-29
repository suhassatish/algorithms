"""
Java NetworkIO
https://xunnanxu.github.io/2016/09/10/It-s-all-about-buffers-zero-copy-mmap-and-Java-NIO/
read(), write() and sendfile() syscalls make 2 copies - 1 from user space to
    kernel space and 2nd one is a DMA (direct memory access) from kernel space to hardware.

    But using mmap() call, avoids the 2nd copy and manipualtes data in memory directly without syscalls.
    The inverse of mmap() is munmap().

    Issues with Mmap on JVM:
        1) OS Page alignment
        2) Direct ByteBuffer Cleanup
        3) Limited number of mmap handles
        4) 32-bit signed integer addressing (2 GB limit)
https://xunnanxu.github.io/2016/09/10/It-s-all-about-buffers-zero-copy-mmap-and-Java-NIO/

"""