"""
Notes from book - BUILDING SECURE & RELIABLE SYSTEMS - best practices for designing, implementing and maintaining
systems - heather adkins, betsy beyer, paul blankinship, piotr lewandowski, ana oprea & adam stubblefield - Google Cloud

--------------------
Chapter 1 - Intersection of Security & Reliability

Reliability risks are primarily non-malicious in nature, unlike security where there can be an active adversary trying
to exploit vulnerabilities. Reliability introduces redundancy which increases the attack surface area. An adversary
only needs to find a vulnerability in one path to be successful.

Reliability vs Security Trade Offs
1) Incident management: you want to pull ppl with diverse perspectives vs looping in  ppl only on a need to know basis
    to avoid tipping off an attacker

2) Voluminous logs help vs being fodder for an attacker

******************************************************************************************************************

Chapter 2 - Understanding Adversaries

Designing for insider risk:
1) Principle of least privilege
2) Multi-person authorization - eg ; bank vaults, nuclear weapons need multiple approvers
3) Documenting business justifications
4) Auditing and detection - periodically reviewing logs
5) Recoverability - ability to recover systems after desctructive actions.
6) zero trust - time-based session expiry or token-based authentications, etc

******************************************************************************************************************

Chapter 3 - Case Study: Safe Proxies

1) Proxies are used to run risky cmds
2) App servers are configured to accept traffic only from safe proxies (no direct SSH)
3) Proxy has a cfg to check ACL that a particular ROLE can access a particular service before forwarding the request.
4) Additional business logic if downstream services are from 3rd parties taht cannot be modified, example to augment and
 massage the data.

----
Cons of proxies:
1) Increased round trip latency & cost of maintenance

******************************************************************************************************************

Chapter 4 : Design Tradeoffs
Google's design document template -

1) SCALABILITY - data size increase & traffic increase - plan for high utilization but requesting more resources will
    block expansion of your services

2) REDUNDANCY & RELIABILITY - data loss, transient errors (temp outages). how is data backed up and restored and what
    happens in between? (eg - serve static content on a website or a cached stale copy)

3) DEPENDENCY CONSIDERATIONS - what happens if your dependencies on other services are unavailable?
    Which services must be running for your app to start? DNS service, local time services. Are there dependency cycles?

4) DATA INTEGRITY - how will you find out about data corruption or loss in your data stores? what sources of data loss
    are detected (user errors, app bugs, data store platform bugs, site / replica disasters)

5) SLA REQUIREMENTS - tools for auditing & monitoring the SLAs? How will you guarantee stated level of reliability?

6) SECURITY & PRIVACY CONSIDERATIONS - describe worst-case impact and defenses to mitigate each attack, list any
    potentially insecure dependencies.
    Eg - credit card payment platform, can use 3rd party payment provider, but if their service unavailable, fall back
    to a different payment provider. You will have API wrapper layers to talk to 2 different API vendors.

    b) Maybe introduce queueing mechanism to buffer Tx data if payment service is unreachable.

    c) Can alternatively have a js client library from the vendor that redirects directly from the payment page to the
    vendor so you dont process any sensitive data. Vendor's lib runs with full privileges in the web origin of the app.

    d) A compromise of the server serving that library can lead to the app being compromised. Risk can be mitigated
    by running in a separate sandboxed iframe.  But have to secure cross-origin communications mechanisms.
    (Browsers restrict access to code from different web origins ie tuple(FQDN of server, port, protocol) )
    JavaScript running in the context of a given origin can observe or modify any information present in or available to
     that context. In contrast, browsers restrict access between content and code across different origins based on
     rules referred to as the same-origin policy.

    e) Vendor may instead offer a solution based on HTTP redirects. It maybe a less smooth user experience.

******************************************************************************************************************

Chapter 5 : Design for least privilege

1) Small functional APIs - pay attention to admin APIs for CRUD ops on an entity such as
    a) setup/teardown APIs to spin up containers , build , install and update S/W
    b) maintenance and emergency APIs to delete corrupted user data or state or to restart misbehaving processes

2) An authentication mechanism can range in complexity:
    a) Simple: Accepting a username passed in a URL parameter
        Example: /service?username=admin
    b) More complex: Presenting a preshared secret
        Examples: WPA2-PSK, an HTTP cookie
    c) Even more complex: Complex hybrid encryption and certificate schemes
        Examples: TLS 1.3, OAuth, X.509 certificate, OAuth2 token

3) Authorization - is this role authorized to perform the requested action?
    a) The specific action being requested
        Examples: URL, command being run, gRPC method

    b) Arguments to the requested action
        Examples: URL parameters, argv, gRPC request

    c) The source of the request
        Examples: IP address, client certificate metadata

    d) Metadata about the authenticated role
        Examples: geographic location, legal jurisdiction, machine learning evaluation of risk

    e) Server-side context
        Examples: rate of similar requests, available capacity

******************************************************************************************************************
Chapter 6: Design for Understandability

Desired properties of a system:

1) Only authenticated and authorized users can access a system's persistent store

2) All ops on sensitive data have audit logging

3) All values received from outside a system's trust boundary are validated before being passed to APIs -
    eg - sql injection attacks, APIs for constructing html markup

4) Queries to backend scale relative to queries received by system's front end

5) If backend query times out, gracefully degrate - eg - resopnding with an approximate answer
    a) If too much memory pressure leading to OS thrashing at virtual mem or heap/ garbage collector level, can cfg
    server to run w/o on-disk virtual memory swap space. So if prod service cant allocate enough memory, the failure is
    obvious.

6) If load / traffic is greater than the cmp can handle, server OVERLOAD error rather than crashing which can lead to
    cascading failures.

7) A system can only receive and send RPCs from and to a set of designated systems

--------------------
GMAIL SYSTEM DESIGN CASE STUDY

Requirements:
1) multiple front-ends / UIs - web browser , mobile browser, mobile app
2) Attachment service connected to google drive for storage & many different formats
3) spam filtering
4) APIs for 3rd party developers to customize
5) Mail sending and receiving APIs - IMAP & POP interfaces
6) offline capability for web client and underlying synchronization infrastructure
7) automatic message categorization
8) extracting structured info about flights, calendar events, etc
9) smart reply templates
10) reminders to reply to emails

--------------------------
API design considerations:

A) interfaces: prefer narrow interfaces & strong typing
    1) RESTful HTTP with json & open API
    2) gRPC
    3) thrift
    gRPC & thrift list the names of each RPC method they support & the types of inputs & outputs to that method.
    4) W3C (XML / SOAP / WSDL)

B) prefer idempotent ops
    1) eg: DB can ask client for UUID for each mutating PC. If its the same UUID, can send "duplicate" msg

C) prefer those that enforce a common object model - https://cloud.google.com/apis/design/resources
    Guidelines for designing resource-oriented APIs - TODO

D) Identities
    1) Harder to spoof a certificate with a private key backed by a hardware module like TPM used in a TLS session
    2) End user OAUth token can be exchanged inside backend auth system for an EUC ie end user context ticket. WIth that
    an attacker who has compromised the front end still wont be able to access teh backend payments system as he may
    not have access to every user's EUC. At most only a user currently using the application's data maybe compromised.
    eg - A malicious js script introduced thru an XSS vulnerability into 1 origin of the webUI can purchase as that user

Mitigation against sql injection & XSS attacks : use STRONG TYPES like Url type, SafeSql type, SafeHtml type, and do all
validations in those builders at construction time as well as runtime.

******************************************************************************************************************

Chapter 7: Design for a changing landscape

1) Periodic key rotation of encryption keys is a best practice.

2) Rollout planning trade-offs during migration :
start with the easiest use case, get teh most traction & prove value (better approach when seeking buy-in from executive sponsor)
vs
start with the hardest use case, where we'll find the most bugs and edge cases (better when there is already buy-in)
Pick a strategy with greatest risk reduction.

3) Eg: migration to HTTPS. Chrome team sent messaging to Japanese website owners that features such as push notifications
for their businesses and offline access, only worked with HTTPS. Tying it to business outcomes accelerated adoption,
since businesses prioritized the work for their developers.

******************************************************************************************************************

Chapter 8, 9: Design for resilience & recovery

1) If servers are geo-distributed across data centers, SHARE THE CERTIFICATE only among co-located server instances.

2) concept of LOAD SHEDDING when a server realizes its health is deteriorating, and only serves important requests
    while dropping others.

3) Example of home network security: If thief breaks in and cuts the internet, use backup hidden landline phone
    & call the emergency phone without relying on internet availability.


******************************************************************************************************************

Chapter 10: Mitigating denial of service (DOS) attacks

1) Several protocols like NTP, DNS, memcache allow amplification attacks in DDOS.
    Defense: Threat model w/ weakest link in the chain & layered approach as below
    a) Edge routers can throttle high B/W attacks & protect n/w backbone
    b) N/W load balancers can throttle packet flooding attacks to protect application load balancers
    c) App LBs can throttle app-specific attacks before traffic reaches service frontends

    Deploying caching proxies at the N/W edge can significantly reduce latency as well as provide significant cost
    savings.

2) Anti-pattern: stateful firewall rules. Con: state exhaustion attacks in which a large number of unused connections
    fill the memory of a firewall with connection tracking enabled. Instead, use router ACLs to restrict traffic to
    necessary ports without introducing a stateful system to the data path.

3)  a) Caching proxies to serve static content and images w/ cache-control HTTP header enabled
    b) Appln backend can send a larger image w/ many icons embedded which can be split client-side while rendering in
        the browser.
    c) Minimize egress B/W. Eg - resize images to only as large as they need to be. Also reduces page load times for
        users.

4) Outage resolution time directly proportional to MTTD (detect) + MTTR (recovery). Automated defenses:
    a) throttling top IP addresses
    b) serving a CAPTCHA javascript challenge  - no additional server state if using browser cookie. Track the following
        i) timestamp challenge was solved
        ii) type of challenge solved, harder challenges for more suspicious behavior
        iii) IP address it was solved from (different devices can share teh same IP if using NAT)
        iv) signature to ensure cookie cannot be forged

5) Google handles overload in the following ways -
    a) Blogger serves in read-only mode, disabling comments
    b) DNS servers serve as many requests as they can, designed not to crash under any amt of load
    c) google search continues serving with a reduced feature set

******************************************************************************************************************

Chapter 11: Designing, Implementing and Maintaining a publicly trusted certificate authority

1) Most orgs rely on 3rd parties for obtaining TLS trust certificates, signing certificates, etc

2) CSR ie certificate signing requests are inputs to CAs, can come from an internet user. Used GoLang to process it
    as its memory safe.

3) CA's keys are kept in a hardware security module (HSM) vault from a commercial vendor

4) Root keys are kept offline. Intermediary keys are kept online.

******************************************************************************************************************

Chapters 12 , 13 , 14 - coding, testing & deploying best practices

******************************************************************************************************************

Chapter 15 - investigating systems

1) Envoy proxy has a "fault injection HTTP filter" to return arbitrary errors from a % of traffic or to delay requests
    for a specific amt of time. Can use it to test system timeouts

"""