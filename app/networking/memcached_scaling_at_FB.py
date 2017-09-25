"""
https://www.facebook.com/note.php?note_id=39391378919
Scaling Memcached at Facebook - (2008) FB's fork of memchached can do 200k QPS, up from 50k QPS.
Key Ideas -
    a) Memcached keeps a per-TCP-connection buffer to RD/WR data over the N/W. For 100k+ cnxns, this amounts to GBs of
    memory. To reclaim this memory for user data, FB implemented a per-thread shared connection buffer pool for TCP &
    UDP sockets.

    b) Moved from TCP to UDP for reduced N.W traffic (lesser acks).

    c) Under load on linux, UDP perf was horrible. This is due to lock contention on UDP socket lock by multiple threads.
    Breaking up the lock by fixing kernel is not easy. So used separate socket servers for replies, with separate socket
    per thread.

    d) Network interrupts on linux are handled by a single CPU core. This is distributed across all the cores
    e) In the scheduler's idle loop, check for NIO interrupts.

    f) Combine this with opportunistic polling of NIO whenever they enter N/W driver, typically for transmitting a
    packet

    g) Stats collection in memcached was using a single global lock hogging 30% of CPU. Moved this to stats-collection
    per thread and on-demand results-aggregation.

    h) Each N/W device has a transmit queue, which had a lock. Packets are enqueued for TX and dequeued by device driver
    This Q is managed by Linux's `netdevice` layer that site b/w IP & device drivers. Packets are enQd and deQd 1 @ a
    time. DeQ algo was changed to batch deQs for transmit, drop Q lock & TX batched packets. This change amortizes cost
    of lock acquisition over many packets and reduces lock-contention significantly, allowing to scale memcached to 8
    threads on an 8-core system.

------------------------------------------------------------------------------------------------------------------
"""