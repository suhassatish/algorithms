"""
Mon, Feb 1, 2021
Security in container-based devops

Docker security best practices -
1) Update Docker and Host Regularly - latest OS & docker versions, update images the containers are based on

2) Configure Resource Quotas - set docker mem & CPU limits

3) Use Non-Root Users - avoid running container in privileged mode

4) Limit Capabilities - admin can add or drop docker's capabilities to run kernel-space OS cmds with --cap-add,
    --cap-drop args to docker

5) Prohibit New Privileges - docker run --no-new-privileges:true overwrites previous settings in cap-add, cap-drop
    This ensures the feature is not used for path traversal/injection, buffer overruns, and privilege escalation attacks

6) Use Trusted Images - stick to official Docker hub, avoid 3rd-party registries which lack control policies
    Use image scanning tools to search for vulnerabilities before downloading anything on the host system.

7) Keep Images and Containers Light -
    a) ignore pkging irrelevant content into docker images with a .dockerignore file in
    the same dir as your Dockerfile.

    b) use multi-stage builds that start with FROM keyword

    c) Only install main dependencies and not unnecessary ones
    RUN apt-get install --no-install-recommends [package-one]

    d) Each RUN instrn adds a new layer to the image, so cascade them with && like below -
    RUN apt-get update && apt-get install -y <pkg> && rm -rf /var/lib

8) Secure Registries
    a) Docker Trusted Registry (DTR). You can install the registry behind your firewall to help prevent potential
    breaches

9) Dont expose docker daemon socket
    a) Docker communicates with a UNIX domain socket called /var/run/docker.sock. This is the main entry point for the
    Docker API. Anyone who has access to the Docker daemon socket also has unrestricted root access.

    b) Allowing a user to write to /var/run/docker.sock or exposing the socket to a container is a great security risk
    to the rest of the system. Doing so essentially gives it root privileges.

    c) Mounting the Docker socket inside a container does not restrict it to privileged access within the container.
    It allows the container full control of the host and all other containers. Therefore, it is not a recommended
    practice.

---------------------------------

Docker container monitoring solutions -
https://phoenixnap.com/blog/docker-container-monitoring-tools

1) AppOptics Docker Monitoring with APM
2) SolarWinds Server & Application Monitor
3) Prometheus - 1 of the 3 OSS tools recommended by Docker
4) Docker API
5) ManageEngine Applications Manager

6) cAdvisor from Google, OSS.
    running daemon that collects, aggregates, and exports resource usage and performance data of targeted containers
    has web UI & REST API

7) SolarWinds Librato - customizable, ability to monitor a wide range of languages and frameworks through RPC calls,
    queues, and other sources

8) Dynatrace - out-of-the-box. No extensive storage space needed, in contrast to many other tools

9) datadog

10) sysdig

11) sumo logic - container-aware approach instead of others which do log monitoring.

---------------------------------


"""