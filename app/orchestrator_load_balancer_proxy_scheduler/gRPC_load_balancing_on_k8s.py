"""
https://www.youtube.com/watch?time_continue=268&v=F2znfxn_5Hg&feature=emb_logo
Tech Talk - 2018 KubeCon - gRPC Load Balancing on Kubernetes

More grpc concepts at -
https://grpc.io/docs/guides/concepts/
----------------------------------------------------------------------
Connection based (L4) vs Stream-based L7 balancing -
1) L4 works fine for HTTP1.1/REST APIs

2) gRPC uses HTTP/2  : every RPC is a separate stream in the SAME TCP/IP connection.

3) L7 LB needed for gRPC traffic

4) Potential problem: Kubernetes LB is only L4 (= in service types ClusterIP and LoadBalancer)
----------------------------------------------------------------------

Proxy LB vs Client LB
Proxy Load Balancer - eg - envoy, nginx (full gRPC support from Mar 2018)
    Pros:
        simple client, untrusted clients are fine
    Cons:
        "sidecar" deployment possible on Kubernetes
        Higher latency and overhead

Client Load Balancer
    Pros:
        low latency, low overhead, no proxy management
    Cons:
        Usually only good for simple LB logic

gRPC implements RoundRobin and grpclb lookaside.
----------------------------------------------------------------------

Service Mesh LB - eg Linkerd, Istio Pilot Cluster Manager with or Lyft's Envoy Proxy
1) Proxy deployed as a service side-car
2) LB performed by proxy
3) 2 proxies add latency, but is needed for things like encryption in the service mesh, not in the LB itself.

----------------------------------------------------------------------
Envoy uses Universal data plane API to discover endpoints. gRPC plans to add support.

2 possible deployment scenarios -

1) Envoy proxy does lookaside load balancing
2) gRPC client consumes data plane API directly
----------------------------------------------------------------------
In kubernetes, use a "headless" service (ie w/clusterIP: None) to expose all replicas as DNS entries

----------------------------------------------------------------------

gRPC LB happens per-call. Potentially no balancing is happening for long-lived streaming calls. Difficult to assign
weights to streaming calls - we dont know how long they're gonna take.

What to do -
restart streaming calls periodically. Can set MAX_CONNECTION_AGE to limit lifetime of connections. Can keep this in mind
when designing APIs.
----------------------------------------------------------------------


"""