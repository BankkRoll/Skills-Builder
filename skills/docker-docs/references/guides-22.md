# Configure CI/CD for your R application and more

# Configure CI/CD for your R application

> Learn how to configure CI/CD using GitHub Actions for your R application.

# Configure CI/CD for your R application

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a R application](https://docs.docker.com/guides/r/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

## Overview

In this section, you'll learn how to set up and use GitHub Actions to build and test your Docker image as well as push it to Docker Hub. You will complete the following steps:

1. Create a new repository on GitHub.
2. Define the GitHub Actions workflow.
3. Run the workflow.

## Step one: Create the repository

Create a GitHub repository, configure the Docker Hub credentials, and push your source code.

1. [Create a new repository](https://github.com/new) on GitHub.
2. Open the repository **Settings**, and go to **Secrets and variables** >
  **Actions**.
3. Create a new **Repository variable** named `DOCKER_USERNAME` and your Docker ID as a value.
4. Create a new
  [Personal Access Token (PAT)](https://docs.docker.com/security/access-tokens/#create-an-access-token) for Docker Hub. You can name this token `docker-tutorial`. Make sure access permissions include Read and Write.
5. Add the PAT as a **Repository secret** in your GitHub repository, with the name
  `DOCKERHUB_TOKEN`.
6. In your local repository on your machine, run the following command to change
  the origin to the repository you just created. Make sure you change
  `your-username` to your GitHub username and `your-repository` to the name of
  the repository you created.
  ```console
  $ git remote set-url origin https://github.com/your-username/your-repository.git
  ```
7. Run the following commands to stage, commit, and push your local repository to GitHub.
  ```console
  $ git add -A
  $ git commit -m "my commit"
  $ git push -u origin main
  ```

## Step two: Set up the workflow

Set up your GitHub Actions workflow for building, testing, and pushing the image
to Docker Hub.

1. Go to your repository on GitHub and then select the **Actions** tab.
2. Select **set up a workflow yourself**.
  This takes you to a page for creating a new GitHub actions workflow file in
  your repository, under `.github/workflows/main.yml` by default.
3. In the editor window, copy and paste the following YAML configuration.
  ```yaml
  name: ci
  on:
    push:
      branches:
        - main
  jobs:
    build:
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
            platforms: linux/amd64,linux/arm64
            push: true
            tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
  ```
  For more information about the YAML syntax for `docker/build-push-action`,
  refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

## Step three: Run the workflow

Save the workflow file and run the job.

1. Select **Commit changes...** and push the changes to the `main` branch.
  After pushing the commit, the workflow starts automatically.
2. Go to the **Actions** tab. It displays the workflow.
  Selecting the workflow shows you the breakdown of all the steps.
3. When the workflow is complete, go to your
  [repositories on Docker Hub](https://hub.docker.com/repositories).
  If you see the new repository in that list, it means the GitHub Actions
  successfully pushed the image to Docker Hub.

## Summary

In this section, you learned how to set up a GitHub Actions workflow for your R application.

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

---

# Containerize a R application

> Learn how to containerize a R application.

# Containerize a R application

   Table of contents

---

## Prerequisites

- You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

## Overview

This section walks you through containerizing and running a R application.

## Get the sample application

The sample application uses the popular [Shiny](https://shiny.posit.co/) framework.

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git && cd r-docker-dev
```

You should now have the following contents in your `r-docker-dev`
directory.

```text
├── r-docker-dev/
│ ├── src/
│ │ └── app.R
│ ├── src_db/
│ │ └── app_db.R
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

To learn more about the files in the repository, see the following:

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [compose.yaml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `r-docker-dev` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:3838](http://localhost:3838). You should see a simple Shiny application.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `r-docker-dev` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:3838](http://localhost:3838).

You should see a simple Shiny application.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the
[Compose CLI
reference](https://docs.docker.com/reference/cli/docker/compose/).

## Summary

In this section, you learned how you can containerize and run your R
application using Docker.

Related information:

- [Docker Compose overview](https://docs.docker.com/compose/)

## Next steps

In the next section, you'll learn how you can develop your application using
containers.

---

# Test your R deployment

> Learn how to develop locally using Kubernetes

# Test your R deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize a R application](https://docs.docker.com/guides/r/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## Create a Kubernetes YAML file

In your `r-docker-dev` directory, create a file named
`docker-r-kubernetes.yaml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your R application](https://docs.docker.com/guides/r/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-r-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: shiny
  template:
    metadata:
      labels:
        service: shiny
    spec:
      containers:
        - name: shiny-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
          env:
            - name: POSTGRES_PASSWORD
              value: mysecretpassword
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: shiny
  ports:
    - port: 3838
      targetPort: 3838
      nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The
  container is created from the image built by GitHub Actions in [Configure CI/CD for
  your R application](https://docs.docker.com/guides/r/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 3838 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to `r-docker-dev` and deploy your application to
  Kubernetes.
  ```console
  $ kubectl apply -f docker-r-kubernetes.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```text
  deployment.apps/docker-r-demo created
  service/service-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  docker-r-demo   1/1     1            1           15s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```shell
  NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  kubernetes           ClusterIP   10.96.0.1       <none>        443/TCP          23h
  service-entrypoint   NodePort    10.99.128.230   <none>        3838:30001/TCP   75s
  ```
  In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP.
3. In a browser, visit the following address. Note that a database was not deployed in
  this example.
  ```console
  http://localhost:30001/
  ```
4. Run the following command to tear down your application.
  ```console
  $ kubectl delete -f docker-r-kubernetes.yaml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)

---

# Use containers for R development

> Learn how to develop your R application locally.

# Use containers for R development

   Table of contents

---

## Prerequisites

Complete [Containerize a R application](https://docs.docker.com/guides/r/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Adding a local database and persisting data
- Configuring Compose to automatically update your running Compose services as you edit and save your code

## Get the sample application

You'll need to clone a new repository to get a sample application that includes logic to connect to the database.

Change to a directory where you want to clone the repository and run the following command.

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git
```

## Configure the application to use the database

To try the connection between the Shiny application and the local database you have to modify the `Dockerfile` changing the `COPY` instruction:

```diff
-COPY src/ .
+COPY src_db/ .
```

## Add a local database and persist data

You can use containers to set up local services, like a database. In this section, you'll update the `compose.yaml` file to define a database service and a volume to persist data.

In the cloned repository's directory, open the `compose.yaml` file in an IDE or text editor.

In the `compose.yaml` file, you need to un-comment the properties for configuring the database. You must also mount the database password file and set an environment variable on the `shiny-app` service pointing to the location of the file in the container.

The following is the updated `compose.yaml` file.

```yaml
services:
  shiny-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 3838:3838
    environment:
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

You should now have the following contents in your `r-docker-dev`
directory.

```text
├── r-docker-dev/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ │ └── app.R
│ ├── src_db/
│ │ └── app_db.R
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

Now, run the following `docker compose up` command to start your application.

```console
$ docker compose up --build
```

Now test your DB connection opening a browser at:

```console
http://localhost:3838
```

You should see a pop-up message:

```text
DB CONNECTED
```

Press `ctrl+c` in the terminal to stop your application.

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you
edit and save your code. For more details about Compose Watch, see
[Use Compose
Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Lines 15 to 18 in the `compose.yaml` file contain properties that trigger Docker
to rebuild the image when a file in the current working directory is changed:

| 1234567891011121314151617181920212223242526272829303132333435363738394041 | services:shiny-app:build:context:.dockerfile:Dockerfileports:-3838:3838environment:-POSTGRES_PASSWORD_FILE=/run/secrets/db-passworddepends_on:db:condition:service_healthysecrets:-db-passworddevelop:watch:-action:rebuildpath:.db:image:postgres:18restart:alwaysuser:postgressecrets:-db-passwordvolumes:-db-data:/var/lib/postgresqlenvironment:-POSTGRES_DB=example-POSTGRES_PASSWORD_FILE=/run/secrets/db-passwordexpose:-5432healthcheck:test:["CMD","pg_isready"]interval:10stimeout:5sretries:5volumes:db-data:secrets:db-password:file:db/password.txt |
| --- | --- |

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Now, if you modify your `app.R` you will see the changes in real time without re-building the image!

Press `ctrl+c` in the terminal to stop your application.

## Summary

In this section, you took a look at setting up your Compose file to add a local
database and persist data. You also learned how to use Compose Watch to automatically rebuild and run your container when you update your code.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll take a look at how to set up a CI/CD pipeline using GitHub Actions.

---

# R language

> Containerize R apps using Docker

# R language-specific guide

---

The R language-specific guide teaches you how to containerize a R application using Docker. In this guide, you’ll learn how to:

- Containerize and run a R application
- Set up a local environment to develop a R application using containers
- Configure a CI/CD pipeline for a containerized R application using GitHub Actions
- Deploy your containerized R application locally to Kubernetes to test and debug your deployment

Start by containerizing an existing R application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/r/containerize/)
  Learn how to containerize a R application.
2. [Develop your app](https://docs.docker.com/guides/r/develop/)
  Learn how to develop your R application locally.
3. [Configure CI/CD](https://docs.docker.com/guides/r/configure-ci-cd/)
  Learn how to configure CI/CD using GitHub Actions for your R application.
4. [Test your deployment](https://docs.docker.com/guides/r/deploy/)
  Learn how to develop locally using Kubernetes

---

# Containerize a RAG application

> Learn how to containerize a RAG application.

# Containerize a RAG application

   Table of contents

---

## Overview

This section walks you through containerizing a RAG application using Docker.

> Note
>
> You can see more samples of containerized GenAI applications in the [GenAI Stack](https://github.com/docker/genai-stack) demo applications.

## Get the sample application

The sample application used in this guide is an example of RAG application, made by three main components, which are the building blocks for every RAG application. A Large Language Model hosted somewhere, in this case it is hosted in a container and served via [Ollama](https://ollama.ai/). A vector database, [Qdrant](https://qdrant.tech/), to store the embeddings of local data, and a web application, using [Streamlit](https://streamlit.io/) to offer the best user experience to the user.

Clone the sample application. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/mfranzon/winy.git
```

You should now have the following files in your `winy` directory.

```text
├── winy/
│ ├── .gitignore
│ ├── app/
│ │ ├── main.py
│ │ ├── Dockerfile
| | └── requirements.txt
│ ├── tools/
│ │ ├── create_db.py
│ │ ├── create_embeddings.py
│ │ ├── requirements.txt
│ │ ├── test.py
| | └── download_model.sh
│ ├── docker-compose.yaml
│ ├── wine_database.db
│ ├── LICENSE
│ └── README.md
```

## Containerizing your application: Essentials

Containerizing an application involves packaging it along with its dependencies into a container, which ensures consistency across different environments. Here’s what you need to containerize an app like Winy :

1. Dockerfile: A Dockerfile that contains instructions on how to build a Docker image for your application. It specifies the base image, dependencies, configuration files, and the command to run your application.
2. Docker Compose File: Docker Compose is a tool for defining and running multi-container Docker applications. A Compose file allows you to configure your application's services, networks, and volumes in a single file.

## Run the application

Inside the `winy` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Docker builds and runs your application. Depending on your network connection, it may take several minutes to download all the dependencies. You'll see a message like the following in the terminal when the application is running.

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8501
server-1  |
```

Open a browser and view the application at [http://localhost:8501](http://localhost:8501). You should see a simple Streamlit application.

The application requires a Qdrant database service and an LLM service to work properly. If you have access to services that you ran outside of Docker, specify the connection information in the `docker-compose.yaml`.

```yaml
winy:
  build:
    context: ./app
    dockerfile: Dockerfile
  environment:
    - QDRANT_CLIENT=http://qdrant:6333 # Specifies the url for the qdrant database
    - OLLAMA=http://ollama:11434 # Specifies the url for the ollama service
  container_name: winy
  ports:
    - "8501:8501"
  depends_on:
    - qdrant
    - ollama
```

If you don't have the services running, continue with this guide to learn how you can run some or all of these services with Docker.
Remember that the `ollama` service is empty; it doesn't have any model. For this reason you need to pull a model before starting to use the RAG application. All the instructions are in the following page.

In the terminal, press `ctrl`+`c` to stop the application.

## Summary

In this section, you learned how you can containerize and run your RAG
application using Docker.

## Next steps

In the next section, you'll learn how to properly configure the application with your preferred LLM model, completely locally, using Docker.

---

# Use containers for RAG development

> Learn how to develop your generative RAG application locally.

# Use containers for RAG development

   Table of contents

---

## Prerequisites

Complete [Containerize a RAG application](https://docs.docker.com/guides/rag-ollama/containerize/).

## Overview

In this section, you'll learn how to set up a development environment to access all the services that your generative RAG application needs. This includes:

- Adding a local database
- Adding a local or remote LLM service

> Note
>
> You can see more samples of containerized GenAI applications in the [GenAI Stack](https://github.com/docker/genai-stack) demo applications.

## Add a local database

You can use containers to set up local services, like a database. In this section, you'll explore the database service in the `docker-compose.yaml` file.

To run the database service:

1. In the cloned repository's directory, open the `docker-compose.yaml` file in an IDE or text editor.
2. In the `docker-compose.yaml` file, you'll see the following:
  ```yaml
  services:
    qdrant:
      image: qdrant/qdrant
      container_name: qdrant
      ports:
        - "6333:6333"
      volumes:
        - qdrant_data:/qdrant/storage
  ```
  > Note
  >
  > To learn more about Qdrant, see the [Qdrant Official Docker Image](https://hub.docker.com/r/qdrant/qdrant).
3. Start the application. Inside the `winy` directory, run the following command in a terminal.
  ```console
  $ docker compose up --build
  ```
4. Access the application. Open a browser and view the application at [http://localhost:8501](http://localhost:8501). You should see a simple Streamlit application.
5. Stop the application. In the terminal, press `ctrl`+`c` to stop the application.

## Add a local or remote LLM service

The sample application supports both [Ollama](https://ollama.ai/). This guide provides instructions for the following scenarios:

- Run Ollama in a container
- Run Ollama outside of a container

While all platforms can use any of the previous scenarios, the performance and
GPU support may vary. You can use the following guidelines to help you choose the appropriate option:

- Run Ollama in a container if you're on Linux, and using a native installation of the Docker Engine, or Windows 10/11, and using Docker Desktop, you
  have a CUDA-supported GPU, and your system has at least 8 GB of RAM.
- Run Ollama outside of a container if running Docker Desktop on a Linux Machine.

Choose one of the following options for your LLM service.

When running Ollama in a container, you should have a CUDA-supported GPU. While you can run Ollama in a container without a supported GPU, the performance may not be acceptable. Only Linux and Windows 11 support GPU access to containers.

To run Ollama in a container and provide GPU access:

1. Install the prerequisites.
  - For Docker Engine on Linux, install the [NVIDIA Container Toolkilt](https://github.com/NVIDIA/nvidia-container-toolkit).
  - For Docker Desktop on Windows 10/11, install the latest [NVIDIA driver](https://www.nvidia.com/Download/index.aspx) and make sure you are using the
    [WSL2 backend](https://docs.docker.com/desktop/features/wsl/#turn-on-docker-desktop-wsl-2)
2. The `docker-compose.yaml` file already contains the necessary instructions. In your own apps, you'll need to add the Ollama service in your `docker-compose.yaml`. The following is
  the updated `docker-compose.yaml`:
  ```yaml
  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  ```
  > Note
  >
  > For more details about the Compose instructions, see
  > [Turn on GPU access with Docker Compose](https://docs.docker.com/compose/how-tos/gpu-support/).
3. Once the Ollama container is up and running it is possible to use the `download_model.sh` inside the `tools` folder with this command:
  ```console
  . ./download_model.sh <model-name>
  ```

Pulling an Ollama model can take several minutes.

To run Ollama outside of a container:

1. [Install](https://github.com/jmorganca/ollama) and run Ollama on your host
  machine.
2. Pull the model to Ollama using the following command.
  ```console
  $ ollama pull llama2
  ```
3. Remove the `ollama` service from the `docker-compose.yaml` and update properly the connection variables in `winy` service:
  ```diff
  - OLLAMA=http://ollama:11434
  + OLLAMA=<your-url>
  ```

## Run your RAG application

At this point, you have the following services in your Compose file:

- Server service for your main RAG application
- Database service to store vectors in a Qdrant database
- (optional) Ollama service to run the LLM
  service

Once the application is running, open a browser and access the application at [http://localhost:8501](http://localhost:8501).

Depending on your system and the LLM service that you chose, it may take several
minutes to answer.

## Summary

In this section, you learned how to set up a development environment to provide
access all the services that your GenAI application needs.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Ollama Docker image](https://hub.docker.com/r/ollama/ollama)
- [GenAI Stack demo applications](https://github.com/docker/genai-stack)

## Next steps

See samples of more GenAI applications in the [GenAI Stack demo applications](https://github.com/docker/genai-stack).

---

# Build a RAG application using Ollama and Docker

> Containerize RAG application using Ollama and Docker

# Build a RAG application using Ollama and Docker

---

The Retrieval Augmented Generation (RAG) guide teaches you how to containerize an existing RAG application using Docker. The example application is a RAG that acts like a sommelier, giving you the best pairings between wines and food. In this guide, you’ll learn how to:

- Containerize and run a RAG application
- Set up a local environment to run the complete RAG stack locally for development

Start by containerizing an existing RAG application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/rag-ollama/containerize/)
  Learn how to containerize a RAG application.
2. [Develop your app](https://docs.docker.com/guides/rag-ollama/develop/)
  Learn how to develop your generative RAG application locally.

---

# Automate your builds with GitHub Actions

> Learn how to configure CI/CD using GitHub Actions for your React.js application.

# Automate your builds with GitHub Actions

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize React.js application](https://docs.docker.com/guides/reactjs/containerize/).

You must also have:

- A [GitHub](https://github.com/signup) account.
- A verified [Docker Hub](https://hub.docker.com/signup) account.

---

## Overview

In this section, you'll set up a **CI/CD pipeline** using [GitHub Actions](https://docs.github.com/en/actions) to automatically:

- Build your React.js application inside a Docker container.
- Run tests in a consistent environment.
- Push the production-ready image to [Docker Hub](https://hub.docker.com).

---

## Connect your GitHub repository to Docker Hub

To enable GitHub Actions to build and push Docker images, you’ll securely store your Docker Hub credentials in your new GitHub repository.

### Step 1: Connect your GitHub repository to Docker Hub

1. Create a Personal Access Token (PAT) from [Docker Hub](https://hub.docker.com)
  1. Go to your **Docker Hub account → Account Settings → Security**.
  2. Generate a new Access Token with **Read/Write** permissions.
  3. Name it something like `docker-reactjs-sample`.
  4. Copy and save the token — you’ll need it in Step 4.
2. Create a repository in [Docker Hub](https://hub.docker.com/repositories/)
  1. Go to your **Docker Hub account → Create a repository**.
  2. For the Repository Name, use something descriptive — for example: `reactjs-sample`.
  3. Once created, copy and save the repository name — you’ll need it in Step 4.
3. Create a new [GitHub repository](https://github.com/new) for your React.js project
4. Add Docker Hub credentials as GitHub repository secrets
  In your newly created GitHub repository:
  1. Navigate to:
    **Settings → Secrets and variables → Actions → New repository secret**.
  2. Add the following secrets:
  | Name | Value |
  | --- | --- |
  | DOCKER_USERNAME | Your Docker Hub username |
  | DOCKERHUB_TOKEN | Your Docker Hub access token (created in Step 1) |
  | DOCKERHUB_PROJECT_NAME | Your Docker Project Name (created in Step 2) |
  These secrets let GitHub Actions to authenticate securely with Docker Hub during automated workflows.
5. Connect Your Local Project to GitHub
  Link your local project `docker-reactjs-sample` to the GitHub repository you just created by running the following command from your project root:
  ```console
  $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
  ```
  > Important
  >
  > Replace `{your-username}` and `{your-repository}` with your actual GitHub username and repository name.
  To confirm that your local project is correctly connected to the remote GitHub repository, run:
  ```console
  $ git remote -v
  ```
  You should see output similar to:
  ```console
  origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
  origin  https://github.com/{your-username}/{your-repository-name}.git (push)
  ```
  This confirms that your local repository is properly linked and ready to push your source code to GitHub.
6. Push Your Source Code to GitHub
  Follow these steps to commit and push your local project to your GitHub repository:
  1. Stage all files for commit.
    ```console
    $ git add -A
    ```
    This command stages all changes — including new, modified, and deleted files — preparing them for commit.
  2. Commit your changes.
    ```console
    $ git commit -m "Initial commit"
    ```
    This command creates a commit that snapshots the staged changes with a descriptive message.
  3. Push the code to the `main` branch.
    ```console
    $ git push -u origin main
    ```
    This command pushes your local commits to the `main` branch of the remote GitHub repository and sets the upstream branch.

Once completed, your code will be available on GitHub, and any GitHub Actions workflow you’ve configured will run automatically.

> Note
>
> Learn more about the Git commands used in this step:
>
>
>
> - [Git add](https://git-scm.com/docs/git-add) – Stage changes (new, modified, deleted) for commit
> - [Git commit](https://git-scm.com/docs/git-commit) – Save a snapshot of your staged changes
> - [Git push](https://git-scm.com/docs/git-push) – Upload local commits to your GitHub repository
> - [Git remote](https://git-scm.com/docs/git-remote) – View and manage remote repository URLs

---

### Step 2: Set up the workflow

Now you'll create a GitHub Actions workflow that builds your Docker image, runs tests, and pushes the image to Docker Hub.

1. Go to your repository on GitHub and select the **Actions** tab in the top menu.
2. Select **Set up a workflow yourself** when prompted.
  This opens an inline editor to create a new workflow file. By default, it will be saved to:
  `.github/workflows/main.yml`
3. Add the following workflow configuration to the new file:

```yaml
name: CI/CD – React.js Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-push:
    name: Build, Test and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout source code
      - name: Checkout source code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Fetches full history for better caching/context

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. Cache Docker layers
      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-npm-

      # 5. Extract metadata
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build dev Docker image
      - name: Build Docker image for tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true # Load to local Docker daemon for testing
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run Vitest tests
      - name: Run Vitest tests and generate report
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npx vitest run --reporter=verbose"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Login to Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push prod image
      - name: Build and push production image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
```

This workflow performs the following tasks for your React.js application:

- Triggers on every `push` or `pull request` targeting the `main` branch.
- Builds a development Docker image using `Dockerfile.dev`, optimized for testing.
- Executes unit tests using Vitest inside a clean, containerized environment to ensure consistency.
- Halts the workflow immediately if any test fails — enforcing code quality.
- Caches both Docker build layers and npm dependencies for faster CI runs.
- Authenticates securely with Docker Hub using GitHub repository secrets.
- Builds a production-ready image using the `prod` stage in `Dockerfile`.
- Tags and pushes the final image to Docker Hub with both `latest` and short SHA tags for traceability.

> Note
>
> For more information about `docker/build-push-action`, refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

---

### Step 3: Run the workflow

After you've added your workflow file, it's time to trigger and observe the CI/CD process in action.

1. Commit and push your workflow file
  Select "Commit changes…" in the GitHub editor.
  - This push will automatically trigger the GitHub Actions pipeline.
2. Monitor the workflow execution
  1. Go to the Actions tab in your GitHub repository.
  2. Click into the workflow run to follow each step: **build**, **test**, and (if successful) **push**.
3. Verify the Docker image on Docker Hub
  - After a successful workflow run, visit your [Docker Hub repositories](https://hub.docker.com/repositories).
  - You should see a new image under your repository with:
    - Repository name: `${your-repository-name}`
    - Tags include:
      - `latest` – represents the most recent successful build; ideal for quick testing or deployment.
      - `<short-sha>` – a unique identifier based on the commit hash, useful for version tracking, rollbacks, and traceability.

> Tip
>
> To maintain code quality and prevent accidental direct pushes, enable branch protection rules:
>
>
>
> - Navigate to your **GitHub repo → Settings → Branches**.
> - Under Branch protection rules, click **Add rule**.
> - Specify `main` as the branch name.
> - Enable options like:
>   - *Require a pull request before merging*.
>   - *Require status checks to pass before merging*.
>
>
>
> This ensures that only tested and reviewed code is merged into `main` branch.

---

## Summary

In this section, you set up a complete CI/CD pipeline for your containerized React.js application using GitHub Actions.

Here's what you accomplished:

- Created a new GitHub repository specifically for your project.
- Generated a secure Docker Hub access token and added it to GitHub as a secret.
- Defined a GitHub Actions workflow to:
  - Build your application inside a Docker container.
  - Run tests in a consistent, containerized environment.
  - Push a production-ready image to Docker Hub if tests pass.
- Triggered and verified the workflow execution through GitHub Actions.
- Confirmed that your image was successfully published to Docker Hub.

With this setup, your React.js application is now ready for automated testing and deployment across environments — increasing confidence, consistency, and team productivity.

---

## Related resources

Deepen your understanding of automation and best practices for containerized apps:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/) – Learn how GitHub Actions automate your workflows
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/) – Set up container builds with GitHub Actions
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – Full reference for writing GitHub workflows
- [Compose file reference](https://docs.docker.com/compose/compose-file/) – Full configuration reference for `compose.yaml`
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) – Optimize your image for performance and security

---

## Next steps

Next, learn how you can locally test and debug your React.js workloads on Kubernetes before deploying. This helps you ensure your application behaves as expected in a production-like environment, reducing surprises during deployment.
