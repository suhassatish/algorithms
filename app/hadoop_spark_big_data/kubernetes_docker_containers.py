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
TODO - https://spark.apache.org/docs/latest/running-on-kubernetes.html

Number of executors auto scaling - spark core scheduler decides that.

To re-provision executors on different cluster nodes, use kubernetes.
---------
helm is like apt-get for kubernetes.
**********************************************************************************

May 4, 2019  - tensorflow with kubernetes - ACM
Notes -

https://training.play-with-docker.com/
interactive browser based docker tutorial - free.

Linux containers require the Docker host to be running a Linux kernel. For example, Linux containers cannot run directly on Windows Docker hosts. The same is true of Windows containers - they need to run on a Docker host with a Windows kernel.
---------
https://katacoda.com/courses/kubernetes

https://kubernetes.io/docs/reference/kubectl/overview/

https://docs.bitnami.com/
cloud hosted kubernetes - ssh based login with pem file
------------------------
katacoda - deploying kubeflow tutorial

    export GITHUB_TOKEN=99510f2ccf40e496d1e97dbec9f31cb16770b884
    export KUBEFLOW_VERSION=0.2.5
    curl https://raw.githubusercontent.com/kubeflow/kubeflow/v${KUBEFLOW_VERSION}/scripts/deploy.sh | bash
    kubectl get pods
    kubectl apply -f ~/kubeflow/katacoda.yaml

complete example can be viewed at https://github.com/tensorflow/k8s/tree/master/examples/tf_sample

2) cat example.yaml
https://www.tensorflow.org/deploy/distributed

3) kubectl apply -f example.yaml

kubectl get tfjob
kubectl get pods | grep Completed
kubectl logs $(kubectl get pods | grep Completed | tr -s ' ' | cut -d ' ' -f 1)

kubectl get svc
kubectl get pods jupyter-admin

MODEL_COMPONENT=model-server
MODEL_NAME=inception
MODEL_PATH=/serving/inception-export

cd ~/kubeflow_ks_app
ks generate tf-serving ${MODEL_COMPONENT} --name=${MODEL_NAME}
ks param set ${MODEL_COMPONENT} modelPath $MODEL_PATH

ks param set ${MODEL_COMPONENT} modelServerImage katacoda/tensorflow_serving

ks param list

ks apply default -c ${MODEL_COMPONENT}

kubectl get pods

cat ~/model-client-job.yaml

kubectl apply -f ~/model-client-job.yaml

kubectl get pods

kubectl logs $(kubectl get pods | grep Completed | tail -n1 |  tr -s ' ' | cut -d ' ' -f 1)

More information on serving models via Kubernetes can be found at
https://github.com/kubeflow/kubeflow/tree/master/components/k8s-model-server
------
vagrant up - starts server on 10.10.10.10

"""