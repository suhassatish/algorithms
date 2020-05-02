"""
https://www.consul.io/discovery.html
1) CONSUL is a tool from HashiCorp for service discovery thats a modern way to replace proxy servers which work only with
static IP addresses. In the age of cloud, all resources are spot instances with dynamically changing IPaddresses.
So you need a real-time service discovery software that has a built-in DNS server to keep a routing table updated in
real-time with built-in health checks and HTTP interface / web-ui.

2) HTTP API with blocking & long polling support -  This allows
automation tools to react to services being registered or health status changes to change configurations or traffic
routing in real time.

3) MULTI DATACENTER
Consul supports multiple datacenters out of the box with no complicated configuration.
Look up services in other datacenters or keep the request local.
Advanced features like Prepared Queries enable automatic failover to other datacenters.

4) HEALTH CHECKS
Pairing service discovery with health checking prevents routing requests to unhealthy hosts and enables services to
easily provide circuit breakers.
"""