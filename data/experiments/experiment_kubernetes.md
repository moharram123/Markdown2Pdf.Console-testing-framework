# Kubernetes

Kubernetes, also known as K8s, is an open source system for automating deployment, scaling, and management of containerized applications.

## Introduction

Kubernetes is the world's most popular container orchestration platform designed by Google and maintained by the Cloud Native Computing Foundation.

## Features

- First item: Automatic bin packing based on resource requirements
- Second item: Self-healing restarts containers that fail
- Third item: Horizontal scaling with a simple command
- Fourth item: Service discovery and load balancing
- Fifth item: Automated rollouts and rollbacks
- Sixth item: Secret and configuration management
- Seventh item: Storage orchestration for all storage systems
- Eighth item: Batch execution for CI workloads

## Usage

Install kubectl:

```python
def install_kubectl():
    print("Installing kubectl...")
```

Create a deployment:

```python
def create_deployment():
    print("kubectl create deployment hello-node")
    def expose():
        print("kubectl expose deployment hello-node --port=8080")
```

Scale your application:

```javascript
function scaleDeployment() {
    console.log("kubectl scale deployment hello-node --replicas=3");
}
```

## Kubernetes Components

| Name | Role |
|------|------|
| Alice | Cluster Administrator |
| Bob | Developer |
| Carol | DevOps Engineer |
| Dave | Admin |

## Governance

| Name | Role |
|------|------|
| Alice | CNCF Technical Oversight |
| Bob | Kubernetes Steering Committee |

## Community

- First item: Slack at kubernetes.slack.com
- Second item: Stack Overflow with tag kubernetes
- Third item: Forum at discuss.kubernetes.io

## Support

| Name | Role |
|------|------|
| Alice | Enterprise Support |
| Bob | Community Maintainer |
| Carol | Admin |

## Security

```python
def report_security():
    print("Email: security@kubernetes.io")
    def encrypt():
        print("Use the Kubernetes PGP key")
```

## Architecture

- First item: Control Plane manages the overall state
- Second item: Worker Nodes run containerized applications
- Third item: etcd is the key-value store
- Fourth item: API Server is the control plane front end

```python
def get_architecture():
    print("Control Plane: kube-apiserver, etcd")
    def worker():
        print("Worker Node: kubelet, kube-proxy")
```