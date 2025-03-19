# IP Tool - Kubernetes Deployment

## Overview
This project contains a Python script (`ip_tool.py`) that collects configured IP networks and stores them in a shared file across multiple containers in a Kubernetes cluster.

The script supports:
- Collecting IP networks from the container.
- Writing IP network data to a shared Persistent Volume (`/data/ip_networks.txt`).
- Checking for **IP collisions** between different nodes.

## Setup & Usage

### 1. Build Docker Image
Since Kubernetes will use a local image, you need to build the container and load it into Minikube:

```
eval $(minikube docker-env)  # Use Minikube's Docker daemon
docker build -t ip-tool:latest .
```

### 2. Deploy to Kubernetes
Apply the deployment and persistent volume configuration:

```
kubectl apply -f k8s_deployment.yaml
```

### 3. Verify Deployment
Check if the pods are running:

```
kubectl get pods
```

Inspect logs:

```
kubectl logs -l app=ip-tool
```

### 4. Access IP Network Data
Check if all instances are writing to the shared file:

```
kubectl exec -it <pod-name> -- cat /data/ip_networks.txt
```

### 5. Collision Check
Since all containers exit after execution, a separate Kubernetes Job is used to check for IP collisions.

Apply the job:
```
kubectl apply -f ip-tool-check.yaml
```
Check the job logs:
```
kubectl logs -l job-name=ip-tool-check
```
\
### 6. Cleanup
To delete the deployment:

```
kubectl delete -f k8s_deployment.yaml
```

## Project Structure

```
📂 ip-tool
├── Dockerfile               # Container setup
├── ip_tool.py               # Python script for IP collection
├── k8s_deployment.yaml      # Kubernetes deployment file
└── README.txt               # Project documentation
```


