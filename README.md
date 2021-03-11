# super-octo-chainsaw
Build status: [![Build Status](https://travis-ci.org/danitfk/super-octo-chainsaw.svg?branch=master)](https://travis-ci.org/danitfk/super-octo-chainsaw)
## Description
This app contains three different parts:
- Application's code itself with requirements (Python)
- Dockerfile
- Skaffold + Kubernetes manifests
## How to run chainsaw?
First you need to install some required tools:
- Install Docker
- Install Kubectl
- Install Skaffold
- Configure access to Kubernetes cluster and Docker Registry (eg: ECR, GCR, Dockerhub,..)
- Configure default context and namespace


### Install Docker
Installation of Docker can be different based on your machine's OS, Please follow official page in order to install Docker.
https://docs.docker.com/get-docker/

### Install kubectl
1. Download the latest release with the command:
```bash
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
```
2. Make the kubectl binary executable.
```bash
chmod +x ./kubectl
```
3. Move the binary in to your PATH.
```bash
sudo mv ./kubectl /usr/local/bin/kubectl
```
4. Test to ensure the version you installed is up-to-date:
```bash
kubectl version --client
```
### Install Skaffold
The latest stable binaries can be found here:
https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-arm64
Simply download the appropriate binary and add it to your PATH. Or, copy+paste one of the following commands in your terminal:

```bash
# For Linux AMD64
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/
```

### Configure access to Kubernetes Cluster & Docker Registry
Please configure access from your machine to kubernetes cluster according to your infrastructure.
More info can be found in bellow:

- GKE: https://cloud.google.com/sdk/gcloud/reference/container/clusters/get-credentials
- EKS: https://aws.amazon.com/premiumsupport/knowledge-center/eks-cluster-connection/

Also make sure you will have push access rights to your Docker registry such as GCR, ECR, Dockerhub, etc.. More info can be found in the provider documentation.

In order to set default repo in Skaffold please follow this:
```bash
 # EKS Example
 skaffold config set default-repo my-account-id.dkr.ecr.my-region.amazonaws.com/chainsaw -k my-kubernetes-context
 # GKE Example
 skaffold config set default-repo gcr.io/my-project-ID -k my-kubernetes-context
 # AKS Example
 skaffold config set default-repo registry-name.azurecr.io/chainsaw -k my-kubernetes-context
 ```
 ### Build and Deploy project
 After Install and configure requirements, it's time to Build and Deploy the project.
 ```bash
 skaffold run
```
Example:
```
➜  super-octo-chainsaw -> skaffold run
Generating tags...
 - chainsaw -> eu.gcr.io/XXXXX-XXX/chainsaw:XXXXX-XXX
Building [chainsaw]...
Sending build context to Docker daemon  4.608kB
Step 1/7 : FROM python:3.9
 ---> 254d4a8a8f31
Step 2/7 : CMD ["python","octo.py"]
 ---> Using cache
 ---> a03ca9277ede
Step 3/7 : WORKDIR /opt/app
 ---> Using cache
 ---> fb5c500532a0
Step 4/7 : COPY requirements.txt .
 ---> Using cache
 ---> 1b061338b98b
Step 5/7 : RUN pip3 install -r requirements.txt
 ---> Using cache
 ---> a67533050ab0
Step 6/7 : COPY octo.py .
 ---> Using cache
 ---> 23ef40cfba37
Step 7/7 : EXPOSE 80
 ---> Running in c69df76d5276
Removing intermediate container c69df76d5276
 ---> 69860d8cdc84
Successfully built 69860d8cdc84
Successfully tagged eu.gcr.io/XXXXX-XXX/chainsaw:XXXXX-XXX
The push refers to repository [eu.gcr.io/XXXXX-XXX/chainsaw]
345eb0f5e828: Preparing
9af00f90e3d7: Preparing
5e4384ede718: Preparing
10bf86ff9f6a: Waiting
7d999a918ae9: Layer already exists
909e93c71745: Layer already exists
7f03bfe4d6dc: Layer already exists
590f313-dirty: digest: sha256:XXXXX-XXX size: 3049
Tags used in deployment:
 - chainsaw -> eu.gcr.io/XXXXX-XXX/chainsaw:XXXXX-XXX@sha256:XXXXX-XXX
Starting deploy...
 - deployment.apps/chainsaw created
 - service/chainsaw created
 - configmap/chainsaw-csv created
Waiting for deployments to stabilize...
 - XXXXX-XXX:deployment/chainsaw: waiting for rollout to finish: 0 of 2 updated replicas are available...
 - XXXXX-XXX:deployment/chainsaw: waiting for rollout to finish: 1 of 2 updated replicas are available...
 - XXXXX-XXX:deployment/chainsaw is ready.
Deployments stabilized in 51.002 seconds
You can also run [skaffold run --tail] to get the logs
```
It's possible to run application in development mode by Skaffold:
```bash
skaffold dev --tail
```
Example:
```
➜  super-octo-chainsaw -> skaffold run --tail
Generating tags...
 - chainsaw -> eu.gcr.io/XXXXX-XXX/chainsaw:XXXXX-XXX
Checking cache...
 - chainsaw: Found Remotely
Tags used in deployment:
 - chainsaw -> eu.gcr.io/XXXXX-XXX/chainsaw:XXXXX-XXXy@sha256:XXXXX-XXX
Starting deploy...
 - deployment.apps/chainsaw created
 - service/chainsaw created
 - configmap/chainsaw-csv created
Waiting for deployments to stabilize...
 - XXXXX-XXX:deployment/chainsaw is ready.
Deployments stabilized in 45.487 seconds
Press Ctrl+C to exit
[chainsaw]  * Serving Flask app "octo" (lazy loading)
[chainsaw]  * Environment: production
[chainsaw]    WARNING: This is a development server. Do not use it in a production deployment.
[chainsaw]    Use a production WSGI server instead.
[chainsaw]  * Debug mode: off
[chainsaw]  * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:01] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:11] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:21] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:31] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:41] "GET /ready HTTP/1.1" 200 -
[chainsaw]  * Serving Flask app "octo" (lazy loading)
[chainsaw]  * Environment: production
[chainsaw]    WARNING: This is a development server. Do not use it in a production deployment.
[chainsaw]    Use a production WSGI server instead.
[chainsaw]  * Debug mode: off
[chainsaw]  * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:02] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:12] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:22] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:32] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:42] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:51] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [10/Mar/2021 23:59:52] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [11/Mar/2021 00:00:01] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [11/Mar/2021 00:00:02] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [11/Mar/2021 00:00:11] "GET /ready HTTP/1.1" 200 -
[chainsaw] 10.233.8.134 - - [11/Mar/2021 00:00:12] "GET /ready HTTP/1.1" 200 -
```
 ### Undeploy project
Project can be undeployed safely with bellow command:
```bash
skaffold delete
```
Example:
```
➜  super-octo-chainsaw ✗ skaffold delete
Cleaning up...
 - deployment.apps "chainsaw" deleted
 - service "chainsaw" deleted
 - configmap "chainsaw-csv" deleted
````