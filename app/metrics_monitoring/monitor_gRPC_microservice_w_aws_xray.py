"""
https://xunnanxu.github.io/2018/11/25/Monitor-gRPC-Microservices-in-Kubernetes-with-Amazon-X-Ray/

1) When a request enters the 1st service, usually the API gateway, , its responsible for creating the 1st segment and
generate a traceID (created by Xray SDK).

2) A "segment" represents the overall lifecycle of a request within * one * application.

3) A traceId represents the overall round trip of a request across * ALL * apps.

4) A service, when making requests to other services should generate corresponding "subsegment". This is useful for
tracing activities within 1 application.

5) A service, when accepting traffic from other services, should relay the traceId and the previous segmentID.


"""