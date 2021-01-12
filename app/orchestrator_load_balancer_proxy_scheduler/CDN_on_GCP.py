"""
use case: low latency serving use cases such as ecommerce application to track user activity

ccccccccccccc

CDN = content delivery network, on GCP (google cloud platform) can cache content from 2 types of backend services-
1) VM instance groups
2) GCS buckets

CDN cache is populated from the 1st time response is served from a backend origin server.
For subsequent cache hits, still incur egress bandwidth.
For cache misses, also incur the cache fill bandwidth

Some responses cannot be cached such as - cache control no store, no cache or private directive, if response has a set-cookie header
HTTP PUTs and POSTs are not cacheable, it has to nbe a GET request. It has to be a specific response code.

CDN may decline to cache large content or if it has to evict more popular content.

Object stored in 1 cache doesnt replicate to another geo cache.

Pricing -
Cache egress: $0.02 - $0.20 per GB
cache fill: $0.04 - $0.15 per GB
HTTP(s) cache lookup requests $0.0075 per 10K requests
cache invalidation: $0.0005 per invalidation

"""