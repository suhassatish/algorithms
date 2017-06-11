"""
Kubernets - talk by Anirudh Ramanathan
1) Used for automating production deployment, scaling and management of containerized applications.

2) Containers give repeatable builds and workflows. Package with all dependencies in 1 place.

3) High degree of control over S/W ie versioning, author, etc. Done thru docker registry.

4) Way more efficient than VMS, so improved infra utilization.
-------------
Internally written in GoLang.

Users of kubernetes write yaml files and kubernetes reads out of it.
-------------
Kubernetes architecture -

1) Kubelet is like yarn NodeManager. Any operation local to node is handled by Kubelet.

2) Master runs - apiserverm etcd (this is current state of truth and desired state),
scheduler, controllers.

Etcd makes sure there's nothing waiting. Prepared for anything going down.

3) Each node runs pods. More than 1 pod can be run on 1 node. Pods have different IP addresses.
No need to take care of NAT N/W @ translation. Done seamlessly.

4) Pods are basic unit in kubernetes.
-------
Controllers -
Drive current state -> desired state

Examples -
1) StatefulSet - eg - MongoDB in prod => use statefulSet
2) DaemonSet - eg - HDFS need DN on every compute node

Features - rolling upgrades, roll backs, etc
-------
L4 vs L7 load balancer. Ingres. Specified declaratively with rules, plain and simple.

Kubenetes can be run in hybrid multiple cloud + on-prem environments. Gives 1 unified API.

Istio project - announced on May 24 by Google, IBM, Lyft. Declaratively specify interfaces and have
services talk to each other.
--------
Typical namespaces - dev, prod, test.
Test namespace can be no larger than 10 GB RAM and 5 CPUs. These cfgs can be specified with
Kubernetes.

You can also have user-namespaces.

RBAC - role-based access control.
Resource-quotas at namespace-level.

Containers dont guarantee isolation to the extent that VMs can. No good solution for it yet.
Soft or hard anti-affinity roles can be specified such as podA & podB consume lot of resources.
Dont put them together.
------------------------------
Spark on Kubernetes project recently announced to work at Spark Summit 2017.
Number of executors auto scaling - spark core scheduler decides that.

To re-provision executors on different cluster nodes, use kubernetes.
---------
helm is like apt-get for kubernetes.

"""