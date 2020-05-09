"""
ENVOY LOAD BALANCER DEEP DIVE, FROM LYFT
https://www.youtube.com/watch?v=gQF23Vw0keg
May 2018 tech talk at CloudNativeCon from CNCF Cloud Native Computing Foundation, sponsored by Google Cloud

Competitors - HAProxy, Nginx
--------------------------------------------------------------------------------

ENVOY DESIGN GOALS -

1) Envoy is at its core, an L3/L4 filter architecture, so it can be extended for multiple protocols.

2) HTTP L7 filter architecture

3) low latency, high perf, dev productivity

4) out of process architecture - to support multiple language services

5) HTTP/2 first

6) Service / config discovery

7) Active / passive health checking

8) Advanced load balancing

9) Best in class observability

10) Service / middle / edge proxy

11) Hot restart

--------------------------------------------------------------------------------
Before envoy, common pattern was:
Ppl deployed Nginx at the edge but HAproxy for internal services communication. It was a duplication.

--------------------------------------------------------------------------------
ENVOY THREADING MODEL - ref dig: app/orchestrator_load_balancer_proxy_scheduler/envoy-threading-model.png
Historically,
    Connection per thread doesnt scale
    Scaling requires many connections per thread: "c10k"
    Requires asnyc programing paradigms : harder. Async event loop.
----
1) Main thread handles non data-plane misc tasks
    xDS fetches - fetching from all the discovery services
2) Worker threads embarrassingly parallel and handle listeners, connections and proxying.
3) File flush threads avoid blocking
Designed to be 100% non-blocking & scale to massive parallelism (# of HW threads)

Easier to manage multiple threads in a process rather than managing processes.
No thread pools or connection pools or locking at all in envoy.

By default, 1 worker thread per hardware thread, so if there's a 4 core CPU, there will be 4 worker threads.

RCU = Read-Copy-Update
Synchronization primitive heavily used in Linux kernel.
Scales extremely well for R/W locking that is read heavy.
------
TLS = thread local storage
TLS slots can be allocated dynamically by objects
RCU is used to post shared read-only data from the main thread to workers
------
Envoy hot restart - full binary reload without dropping any connections.
Very useful in logacy/non-container scheduler worlds.
------

Envoy can work in both push mode and pull mode.

statsd = push mode
prometheus = pull mode


"""