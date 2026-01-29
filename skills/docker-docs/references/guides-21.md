# Automate your builds with GitHub Actions and more

# Automate your builds with GitHub Actions

> Learn how to configure CI/CD using GitHub Actions for your Python application.

# Automate your builds with GitHub Actions

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a Python application](https://docs.docker.com/guides/python/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

If you didn't create a [GitHub repository](https://github.com/new) for your project yet, it is time to do it. After creating the repository, don't forget to [add a remote](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories) and ensure you can commit and [push your code](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push) to GitHub.

1. In your project's GitHub repository, open **Settings**, and go to **Secrets and variables** > **Actions**.
2. Under the **Variables** tab, create a new **Repository variable** named `DOCKER_USERNAME` and your Docker ID as a value.
3. Create a new
  [Personal Access Token (PAT)](https://docs.docker.com/security/access-tokens/#create-an-access-token) for Docker Hub. You can name this token `docker-tutorial`. Make sure access permissions include Read and Write.
4. Add the PAT as a **Repository secret** in your GitHub repository, with the name
  `DOCKERHUB_TOKEN`.

## Overview

GitHub Actions is a CI/CD (Continuous Integration and Continuous Deployment) automation tool built into GitHub. It allows you to define custom workflows for building, testing, and deploying your code when specific events occur (e.g., pushing code, creating a pull request, etc.). A workflow is a YAML-based automation script that defines a sequence of steps to be executed when triggered. Workflows are stored in the `.github/workflows/` directory of a repository.

In this section, you'll learn how to set up and use GitHub Actions to build your Docker image as well as push it to Docker Hub. You will complete the following steps:

1. Define the GitHub Actions workflow.
2. Run the workflow.

## 1. Define the GitHub Actions workflow

You can create a GitHub Actions workflow by creating a YAML file in the `.github/workflows/` directory of your repository. To do this use your favorite text editor or the GitHub web interface. The following steps show you how to create a workflow file using the GitHub web interface.

If you prefer to use the GitHub web interface, follow these steps:

1. Go to your repository on GitHub and then select the **Actions** tab.
2. Select **set up a workflow yourself**.
  This takes you to a page for creating a new GitHub Actions workflow file in
  your repository. By default, the file is created under `.github/workflows/main.yml`, let's change it name to `build.yml`.

If you prefer to use your text editor, create a new file named `build.yml` in the `.github/workflows/` directory of your repository.

Add the following content to the file:

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Run pyright
        run: pyright

  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

Each GitHub Actions workflow includes one or several jobs. Each job consists of steps. Each step can either run a set of commands or use already [existing actions](https://github.com/marketplace?type=actions). The action above has three steps:

1. [Login to Docker Hub](https://github.com/docker/login-action): Action logs in to Docker Hub using the Docker ID and Personal Access Token (PAT) you created earlier.
2. [Set up Docker Buildx](https://github.com/docker/setup-buildx-action): Action sets up Docker [Buildx](https://github.com/docker/buildx), a CLI plugin that extends the capabilities of the Docker CLI.
3. [Build and push](https://github.com/docker/build-push-action): Action builds and pushes the Docker image to Docker Hub. The `tags` parameter specifies the image name and tag. The `latest` tag is used in this example.

## 2. Run the workflow

Commit the changes and push them to the `main` branch. This workflow is runs every time you push changes to the `main` branch. You can find more information about workflow triggers [in the GitHub documentation](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows).

Go to the **Actions** tab of you GitHub repository. It displays the workflow. Selecting the workflow shows you the breakdown of all the steps.

When the workflow is complete, go to your [repositories on Docker Hub](https://hub.docker.com/repositories). If you see the new repository in that list, it means the GitHub Actions workflow successfully pushed the image to Docker Hub.

## Summary

In this section, you learned how to set up a GitHub Actions workflow for your Python application that includes:

- Running pre-commit hooks for linting and formatting
- Static type checking with Pyright
- Building and pushing Docker images

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

In the next section, you'll learn how you can develop locally using kubernetes.

---

# Containerize a Python application

> Learn how to containerize a Python application.

# Containerize a Python application

   Table of contents

---

## Prerequisites

- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
- You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

## Overview

This section walks you through containerizing and running a Python application.

## Get the sample application

The sample application uses the popular [FastAPI](https://fastapi.tiangolo.com) framework.

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/estebanx64/python-docker-example && cd python-docker-example
```

## Initialize Docker assets

Now that you have an application, you can create the necessary Docker assets to
containerize your application. You can use Docker Desktop's built-in Docker Init
feature to help streamline the process, or you can manually create the assets.

Inside the `python-docker-example` directory, run the `docker init` command. `docker init` provides some default configuration, but you'll need to answer a few
questions about your application. For example, this application uses FastAPI to
run. Refer to the following example to answer the prompts from `docker init` and
use the same answers for your prompts.

Before editing your Dockerfile, you need to choose a base image. You can use the [Python Docker Official Image](https://hub.docker.com/_/python),
or a [Docker Hardened Image (DHI)](https://hub.docker.com/hardened-images/catalog/dhi/python).

Docker Hardened Images (DHIs) are minimal, secure, and production-ready base images maintained by Docker.
They help reduce vulnerabilities and simplify compliance. For more details, see
[Docker Hardened Images](https://docs.docker.com/dhi/).

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.12
? What port do you want your app to listen on? 8000
? What is the command to run your app? python3 -m uvicorn app:app --host=0.0.0.0 --port=8000
```

Create a file named `.gitignore` with the following contents.

.gitignore

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

If you don't have Docker Desktop installed or prefer creating the assets
manually, you can create the following files in your project directory.

Create a file named `Dockerfile` with the following contents.

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

Create a file named `compose.yaml` with the following contents.

compose.yaml

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

Create a file named `.dockerignore` with the following contents.

.dockerignore

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.DS_Store
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose.y*ml
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
```

Create a file named `.gitignore` with the following contents.

.gitignore

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

If you don't have Docker Desktop installed or prefer creating the assets
manually, you can create the following files in your project directory.

Create a file named `Dockerfile` with the following contents.

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/
ARG PYTHON_VERSION=3.12.12-debian13-fips-dev
FROM <your-workspace>/dhi-python:${PYTHON_VERSION}

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

#Add dependencies for adduser
RUN apt update -y && apt install adduser -y

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

Create a file named `compose.yaml` with the following contents.

compose.yaml

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

Create a file named `.dockerignore` with the following contents.

.dockerignore

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.DS_Store
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose.y*ml
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
```

Create a file named `.gitignore` with the following contents.

.gitignore

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

You should now have the following contents in your `python-docker-example`
directory.

```text
├── python-docker-example/
│ ├── app.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

To learn more about the files, see the following:

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [.gitignore](https://git-scm.com/docs/gitignore)
- [compose.yaml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `python-docker-example` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8000](http://localhost:8000). You should see a simple FastAPI application.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `python-docker-example` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:8000](http://localhost:8000).

To see the OpenAPI docs you can go to [http://localhost:8000/docs](http://localhost:8000/docs).

You should see a simple FastAPI application.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the
[Compose CLI
reference](https://docs.docker.com/reference/cli/docker/compose/).

## Summary

In this section, you learned how you can containerize and run your Python
application using Docker.

Related information:

- [Docker Compose overview](https://docs.docker.com/compose/)

## Next steps

In the next section, you'll take a look at how to set up a local development environment using Docker containers.

---

# Test your Python deployment

> Learn how to develop locally using Kubernetes

# Test your Python deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Use containers for Python development](https://docs.docker.com/guides/python/develop/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## Create a Kubernetes YAML file

In your `python-docker-dev-example` directory, create a file named `docker-postgres-kubernetes.yaml`. Open the file in an IDE or text editor and add
the following contents.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:18
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql
      volumes:
        - name: postgres-data
          persistentVolumeClaim:
            claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
spec:
  ports:
    - port: 5432
  selector:
    app: postgres
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: default
type: Opaque
data:
  POSTGRES_PASSWORD: cG9zdGdyZXNfcGFzc3dvcmQ= # Base64 encoded password (e.g., 'postgres_password')
```

In your `python-docker-dev-example` directory, create a file named
`docker-python-kubernetes.yaml`. Replace `DOCKER_USERNAME/REPO_NAME` with your
Docker username and the repository name that you created in [Configure CI/CD for
your Python application](https://docs.docker.com/guides/python/configure-github-actions/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-python-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: fastapi
  template:
    metadata:
      labels:
        service: fastapi
    spec:
      containers:
        - name: fastapi-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_SERVER
              value: postgres
            - name: POSTGRES_PORT
              value: "5432"
          ports:
            - containerPort: 8001
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: fastapi
  ports:
    - port: 8001
      targetPort: 8001
      nodePort: 30001
```

In these Kubernetes YAML file, there are various objects, separated by the `---`:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The
  container is created from the image built by GitHub Actions in [Configure CI/CD for
  your Python application](https://docs.docker.com/guides/python/configure-github-actions/).
- A Service, which will define how the ports are mapped in the containers.
- A PersistentVolumeClaim, to define a storage that will be persistent through restarts for the database.
- A Secret, Keeping the database password as an example using secret kubernetes resource.
- A NodePort service, which will route traffic from port 30001 on your host to
  port 8001 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

> Note
>
> - The `NodePort` service is good for development/testing purposes. For production you should implement an [ingress-controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/).

## Deploy and check your application

1. In a terminal, navigate to `python-docker-dev-example` and deploy your database to
  Kubernetes.
  ```console
  $ kubectl apply -f docker-postgres-kubernetes.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```console
  deployment.apps/postgres created
  service/postgres created
  persistentvolumeclaim/postgres-pvc created
  secret/postgres-secret created
  ```
  Now, deploy your python application.
  ```console
  kubectl apply -f docker-python-kubernetes.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```console
  deployment.apps/docker-python-demo created
  service/service-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```console
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  docker-python-demo   1/1     1            1           48s
  postgres             1/1     1            1           2m39s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```console
  NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
  kubernetes           ClusterIP   10.43.0.1      <none>        443/TCP          13h
  postgres             ClusterIP   10.43.209.25   <none>        5432/TCP         3m10s
  service-entrypoint   NodePort    10.43.67.120   <none>        8001:30001/TCP   79s
  ```
  In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP and the internal `ClusterIP` `postgres` with the port `5432` open to accept connections from you python app.
3. In a terminal, curl the service. Note that a database was not deployed in
  this example.
  ```console
  $ curl http://localhost:30001/
  Hello, Docker!!!
  ```
4. Run the following commands to tear down your application.
  ```console
  $ kubectl delete -f docker-python-kubernetes.yaml
  $ kubectl delete -f docker-postgres-kubernetes.yaml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)

---

# Use containers for Python development

> Learn how to develop your Python application locally.

# Use containers for Python development

   Table of contents

---

## Prerequisites

Complete [Containerize a Python application](https://docs.docker.com/guides/python/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Adding a local database and persisting data
- Configuring Compose to automatically update your running Compose services as you edit and save your code

## Get the sample application

You'll need to clone a new repository to get a sample application that includes logic to connect to the database.

1. Change to a directory where you want to clone the repository and run the following command.
  ```console
  $ git clone https://github.com/estebanx64/python-docker-dev-example
  ```
2. In the cloned repository's directory, manually create the Docker assets or run `docker init` to create the necessary Docker assets.
  In the cloned repository's directory, run `docker init`. Refer to the
  following example to answer the prompts from `docker init`.
  ```console
  $ docker init
  Welcome to the Docker Init CLI!
  This utility will walk you through creating the following files with sensible defaults for your project:
    - .dockerignore
    - Dockerfile
    - compose.yaml
    - README.Docker.md
  Let's get started!
  ? What application platform does your project use? Python
  ? What version of Python do you want to use? 3.12
  ? What port do you want your app to listen on? 8001
  ? What is the command to run your app? python3 -m uvicorn app:app --host=0.0.0.0 --port=8001
  ```
  Create a file named `.gitignore` with the following contents.
  .gitignore
  ```text
  # Byte-compiled / optimized / DLL files
  __pycache__/
  *.py[cod]
  *$py.class
  # C extensions
  *.so
  # Distribution / packaging
  .Python
  build/
  develop-eggs/
  dist/
  downloads/
  eggs/
  .eggs/
  lib/
  lib64/
  parts/
  sdist/
  var/
  wheels/
  share/python-wheels/
  *.egg-info/
  .installed.cfg
  *.egg
  MANIFEST
  # Unit test / coverage reports
  htmlcov/
  .tox/
  .nox/
  .coverage
  .coverage.*
  .cache
  nosetests.xml
  coverage.xml
  *.cover
  *.py,cover
  .hypothesis/
  .pytest_cache/
  cover/
  # PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
  __pypackages__/
  # Environments
  .env
  .venv
  env/
  venv/
  ENV/
  env.bak/
  venv.bak/
  ```
  If you don't have Docker Desktop installed or prefer creating the assets
  manually, you can create the following files in your project directory.
  Create a file named `Dockerfile` with the following contents.
  Dockerfile
  ```dockerfile
  # syntax=docker/dockerfile:1
  # Comments are provided throughout this file to help you get started.
  # If you need more help, visit the Dockerfile reference guide at
  # https://docs.docker.com/go/dockerfile-reference/
  # Want to help us make this template better? Share your feedback here: https://   forms.gle/ybq9Krt8jtBL3iCk7
  ARG PYTHON_VERSION=3.12
  FROM python:${PYTHON_VERSION}-slim
  # Prevents Python from writing pyc files.
  ENV PYTHONDONTWRITEBYTECODE=1
  # Keeps Python from buffering stdout and stderr to avoid situations where
  # the application crashes without emitting any logs due to buffering.
  ENV PYTHONUNBUFFERED=1
  WORKDIR /app
  # Create a non-privileged user that the app will run under.
  # See https://docs.docker.com/go/dockerfile-user-best-practices/
  ARG UID=10001
  RUN adduser \
      --disabled-password \
      --gecos "" \
      --home "/nonexistent" \
      --shell "/sbin/nologin" \
      --no-create-home \
      --uid "${UID}" \
      appuser
  # Download dependencies as a separate step to take advantage of Docker's    caching.
  # Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
  # Leverage a bind mount to requirements.txt to avoid having to copy them into
  # into this layer.
  RUN --mount=type=cache,target=/root/.cache/pip \
      --mount=type=bind,source=requirements.txt,target=requirements.txt \
      python -m pip install -r requirements.txt
  # Switch to the non-privileged user to run the application.
  USER appuser
  # Copy the source code into the container.
  COPY . .
  # Expose the port that the application listens on.
  EXPOSE 8001
  # Run the application.
  CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8001"]
  ```
  Create a file named `compose.yaml` with the following contents.
  compose.yaml
  ```yaml
  # Comments are provided throughout this file to help you get started.
  # If you need more help, visit the Docker Compose reference guide at
  # https://docs.docker.com/go/compose-spec-reference/
  # Here the instructions define your application as a service called "server".
  # This service is built from the Dockerfile in the current directory.
  # You can add other services your application may depend on here, such as a
  # database or a cache. For examples, see the Awesome Compose repository:
  # https://github.com/docker/awesome-compose
  services:
    server:
      build:
        context: .
      ports:
        - 8001:8001
  # The commented out section below is an example of how to define a PostgreSQL
  # database that your application can use. `depends_on` tells Docker Compose to
  # start the database before your application. The `db-data` volume persists the
  # database data between container restarts. The `db-password` secret is used
  # to set the database password. You must create `db/password.txt` and add
  # a password of your choosing to it before running `docker compose up`.
  #     depends_on:
  #       db:
  #         condition: service_healthy
  #   db:
  #     image: postgres:18
  #     restart: always
  #     user: postgres
  #     secrets:
  #       - db-password
  #     volumes:
  #       - db-data:/var/lib/postgresql
  #     environment:
  #       - POSTGRES_DB=example
  #       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
  #     expose:
  #       - 5432
  #     healthcheck:
  #       test: [ "CMD", "pg_isready" ]
  #       interval: 10s
  #       timeout: 5s
  #       retries: 5
  # volumes:
  #   db-data:
  # secrets:
  #   db-password:
  #     file: db/password.txt
  ```
  Create a file named `.dockerignore` with the following contents.
  .dockerignore
  ```text
  # Include any files or directories that you don't want to be copied to your
  # container here (e.g., local build artifacts, temporary files, etc.).
  #
  # For more help, visit the .dockerignore file reference guide at
  # https://docs.docker.com/go/build-context-dockerignore/
  **/.DS_Store
  **/__pycache__
  **/.venv
  **/.classpath
  **/.dockerignore
  **/.env
  **/.git
  **/.gitignore
  **/.project
  **/.settings
  **/.toolstarget
  **/.vs
  **/.vscode
  **/*.*proj.user
  **/*.dbmdl
  **/*.jfm
  **/bin
  **/charts
  **/docker-compose*
  **/compose.y*ml
  **/Dockerfile*
  **/node_modules
  **/npm-debug.log
  **/obj
  **/secrets.dev.yaml
  **/values.dev.yaml
  LICENSE
  README.md
  ```
  Create a file named `.gitignore` with the following contents.
  .gitignore
  ```text
  # Byte-compiled / optimized / DLL files
  __pycache__/
  *.py[cod]
  *$py.class
  # C extensions
  *.so
  # Distribution / packaging
  .Python
  build/
  develop-eggs/
  dist/
  downloads/
  eggs/
  .eggs/
  lib/
  lib64/
  parts/
  sdist/
  var/
  wheels/
  share/python-wheels/
  *.egg-info/
  .installed.cfg
  *.egg
  MANIFEST
  # Unit test / coverage reports
  htmlcov/
  .tox/
  .nox/
  .coverage
  .coverage.*
  .cache
  nosetests.xml
  coverage.xml
  *.cover
  *.py,cover
  .hypothesis/
  .pytest_cache/
  cover/
  # PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
  __pypackages__/
  # Environments
  .env
  .venv
  env/
  venv/
  ENV/
  env.bak/
  venv.bak/
  ```

## Add a local database and persist data

You can use containers to set up local services, like a database. In this section, you'll update the `compose.yaml` file to define a database service and a volume to persist data.

In the cloned repository's directory, open the `compose.yaml` file in an IDE or text editor. `docker init` handled creating most of the instructions, but you'll need to update it for your unique application.

In the `compose.yaml` file, you need to uncomment all of the database instructions. In addition, you need to add the database password file as an environment variable to the server service and specify the secret file to use .

The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> Note
>
> To learn more about the instructions in the Compose file, see
> [Compose file
> reference](https://docs.docker.com/reference/compose-file/).

Before you run the application using Compose, notice that this Compose file specifies a `password.txt` file to hold the database's password. You must create this file as it's not included in the source repository.

In the cloned repository's directory, create a new directory named `db` and inside that directory create a file named `password.txt` that contains the password for the database. Using your favorite IDE or text editor, add the following contents to the `password.txt` file.

```text
mysecretpassword
```

Save and close the `password.txt` file.

You should now have the following contents in your `python-docker-dev-example`
directory.

```text
├── python-docker-dev-example/
│ ├── db/
│ │ └── password.txt
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

Now, run the following `docker compose up` command to start your application.

```console
$ docker compose up --build
```

Now test your API endpoint. Open a new terminal then make a request to the server using the curl commands:

Let's create an object with a post method

```console
$ curl -X 'POST' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

You should receive the following response:

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

Let's make a get request with the next curl command:

```console
curl -X 'GET' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json'
```

You should receive the same response as above because it's the only one object we have in database.

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

Press `ctrl+c` in the terminal to stop your application.

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you
edit and save your code. For more details about Compose Watch, see
[Use Compose
Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yaml` file in an IDE or text editor and then add the Compose
Watch instructions. The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

In a terminal, curl the application to get a response.

```console
$ curl http://localhost:8001
Hello, Docker!
```

Any changes to the application's source files on your local machine will now be immediately reflected in the running container.

Open `python-docker-dev-example/app.py` in an IDE or text editor and update the `Hello, Docker!` string by adding a few more exclamation marks.

```diff
-    return 'Hello, Docker!'
+    return 'Hello, Docker!!!'
```

Save the changes to `app.py` and then wait a few seconds for the application to rebuild. Curl the application again and verify that the updated text appears.

```console
$ curl http://localhost:8001
Hello, Docker!!!
```

Press `ctrl+c` in the terminal to stop your application.

## Summary

In this section, you took a look at setting up your Compose file to add a local
database and persist data. You also learned how to use Compose Watch to automatically rebuild and run your container when you update your code.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll learn how you can set up linting, formatting and type checking to follow the best practices in python apps.

---

# Linting, formatting, and type checking for Python

> Learn how to set up linting, formatting and type checking for your Python application.

# Linting, formatting, and type checking for Python

   Table of contents

---

## Prerequisites

Complete [Develop your app](https://docs.docker.com/guides/python/develop/).

## Overview

In this section, you'll learn how to set up code quality tools for your Python application. This includes:

- Linting and formatting with Ruff
- Static type checking with Pyright
- Automating checks with pre-commit hooks

## Linting and formatting with Ruff

Ruff is an extremely fast Python linter and formatter written in Rust. It replaces multiple tools like flake8, isort, and black with a single unified tool.

Before using Ruff, install it in your Python environment:

```bash
pip install ruff
```

If you're using a virtual environment, make sure it is activated so the `ruff` command is available when you run the commands below.

Create a `pyproject.toml` file:

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
```

### Using Ruff

Run these commands to check and format your code:

```bash
# Check for errors
ruff check .

# Automatically fix fixable errors
ruff check --fix .

# Format code
ruff format .
```

## Type checking with Pyright

Pyright is a fast static type checker for Python that works well with modern Python features.

Add `Pyright` configuration in `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```

### Running Pyright

To check your code for type errors:

```bash
pyright
```

## Setting up pre-commit hooks

Pre-commit hooks automatically run checks before each commit. The following `.pre-commit-config.yaml` snippet sets up Ruff:

```yaml
https: https://github.com/charliermarsh/ruff-pre-commit
  rev: v0.2.2
  hooks:
    - id: ruff
      args: [--fix]
    - id: ruff-format
```

To install and use:

```bash
pre-commit install
git commit -m "Test commit"  # Automatically runs checks
```

## Summary

In this section, you learned how to:

- Configure and use Ruff for linting and formatting
- Set up Pyright for static type checking
- Automate checks with pre-commit hooks

These tools help maintain code quality and catch errors early in development.

## Next steps

- [Configure GitHub Actions](https://docs.docker.com/guides/python/configure-github-actions/) to run these checks automatically
- Customize linting rules to match your team's style preferences
- Explore advanced type checking features

---

# Python language

> Containerize Python apps using Docker

# Python language-specific guide

---

> **Acknowledgment**
>
>
>
> This guide is a community contribution. Docker would like to thank
> [Esteban Maya](https://www.linkedin.com/in/esteban-x64/) and [Igor Aleksandrov](https://www.linkedin.com/in/igor-aleksandrov/) for their contribution
> to this guide.

The Python language-specific guide teaches you how to containerize a Python application using Docker. In this guide, you’ll learn how to:

- Containerize and run a Python application
- Set up a local environment to develop a Python application using containers
- Lint, format, typing and best practices
- Configure a CI/CD pipeline for a containerized Python application using GitHub Actions
- Deploy your containerized Python application locally to Kubernetes to test and debug your deployment

Start by containerizing an existing Python application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/python/containerize/)
  Learn how to containerize a Python application.
2. [Develop your app](https://docs.docker.com/guides/python/develop/)
  Learn how to develop your Python application locally.
3. [Linting and typing](https://docs.docker.com/guides/python/lint-format-typing/)
  Learn how to set up linting, formatting and type checking for your Python application.
4. [Automate your builds with GitHub Actions](https://docs.docker.com/guides/python/configure-github-actions/)
  Learn how to configure CI/CD using GitHub Actions for your Python application.
5. [Test your deployment](https://docs.docker.com/guides/python/deploy/)
  Learn how to develop locally using Kubernetes
