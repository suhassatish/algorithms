"""
Shortcomings of DCOS that leads to mass migration to its competitor Kubernetes since 2014
****************************************************************************************
1) COMMUNITY SUPPORT & DOCUMENTATION: DCOS documentation has quirks and race conditions, work arounds not readily
documented in the community.

2) AVAILABILITY: If a node leaves the cluster, the cluster can go into recovery mode for 10 * 2^n minutes where
n = number of nodes that have left the cluster. Its hard to have a node leave the cluster gracefully.

3) RELIABILITY: Job deployment can fall into "Delayed" state if it fails multiple times. Then, it has to be reset
manually even if issue is resolved. This creates lot of operational overhead.

4) UPGRADES: Given the above, patching is tedious and took 3 weeks to manually patch all DC/OS clusters.

5) LOGGING, METRICS AND IAM ROLE MANAGEMENT features are non-existent in free version.
Instead we used, datadog-agent for metric collection, sumo-agent for log aggregation,  AMPROXY (in-house tool) for IAM
role management, and service proxy for exposing DC/OS API. These in-house hacks are running as daemon process on the
hosts, but since DC/OS doesnt support daemon workloads, work around is to run the agents on every node. But this
requires manual operations to keep them up and running.

6) AUTHENTICATION: Although DC/OS has internal authentication, its minimal. User emails can be added in DC/OS but it
still relies on google sign-in or github authentication. No support for SSO or Role-Based Access Control. Moreover,
user can be added via Zookeeper, bypassing DC/OS hence posing security risk.

7) SERVICE DEPLOYMENTS: Deployment is managed by an internal (legacy) tool called WebIQ. It creates a new Marathon job
in DC/OS and then creates load balancers.

8) AMPROXY: This sets up an IAM role in AWS and the application container needs to assume this IAM role and look up
credentials in Crypter (another in-house tool). Often, the IAM role doesnt have the correct permissions to read from
crypter and crypter then errors out with a cryptic error msg.
"""