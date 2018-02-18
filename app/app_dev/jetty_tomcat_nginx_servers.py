"""
https://socialcompare.com/en/comparison/comparison-of-web-servers

Jetty - SFDC uses it- used by java platforms
Limitations: No support for
    1) server side includes (but apache, nginx and tomcat application webservers support it)
    2) server-side javascript

Nginx has the highest adoption from the most heavily trafficed sites in the world like
Netflix, Spotify, Uber, Pinterest, Quora. Beacon app servers were migrated from Apache to Nginx for performance on
Ubuntu 14.04.
---------------------
TODO - read Nginx guide at
Dropbox://Tech_extras/app_dev_microservices/Microservices_Ref_Arch_Nginx.pdf
to learn about topics below:

1) How to implement three microservice architectures: the Proxy, Router Mesh, and Fabric models?

2) The circuit breaker pattern using NGINX Plus active health checks

3) How to design a microservices application to maintain 12-Factor App compliance

4) How to build a rich, user-experience-based frontend for microservices

"""