# Common challenges and questions and more

# Common challenges and questions

> Explore common challenges and questions related to Docker Compose.

# Common challenges and questions

   Table of contents

---

### Do I need to maintain a separate Compose file for my development, testing, and staging environments?

You don't necessarily need to maintain entirely separate Compose files for your
development, testing, and staging environments. You can define all your
services in a single Compose file (`compose.yaml`). You can use profiles to
group service configurations specific to each environment (`dev`, `test`,
`staging`).

When you need to spin up an environment, you can activate the corresponding
profiles. For example, to set up the development environment:

```console
$ docker compose --profile dev up
```

This command starts only the services associated with the `dev` profile,
leaving the rest inactive.

For more information on using profiles, see
[Using profiles with
Compose](https://docs.docker.com/compose/how-tos/profiles/).

### How can I enforce the database service to start up before the frontend service?

Docker Compose ensures services start in a specific order by using the
`depends_on` property. This tells Compose to start the database service before
even attempting to launch the frontend service. This is crucial since
applications often rely on databases being ready for connections.

However, `depends_on` only guarantees the order, not that the database is fully
initialized. For a more robust approach, especially if your application relies
on a prepared database (e.g., after migrations), consider
[health
checks](https://docs.docker.com/reference/compose-file/services/#healthcheck). Here, you can
configure the frontend to wait until the database passes its health check
before starting. This ensures the database is not only up but also ready to
handle requests.

For more information on setting the startup order of your services, see
[Control startup and shutdown order in Compose](https://docs.docker.com/compose/how-tos/startup-order/).

### Can I use Compose to build a Docker image?

Yes, you can use Docker Compose to build Docker images. Docker Compose is a
tool for defining and running multi-container applications. Even if your
application isn't a multi-container application, Docker Compose can make it
easier to run by defining all the `docker run` options in a file.

To use Compose, you need a `compose.yaml` file. In this file, you can specify
the build context and Dockerfile for each service. When you run the command
`docker compose up --build`, Docker Compose will build the images for each
service and then start the containers.

For more information on building Docker images using Compose, see the
[Compose
Build Specification](https://docs.docker.com/compose/compose-file/build/).

### What is the difference between Docker Compose and Dockerfile?

A Dockerfile provides instructions to build a container image while a Compose
file defines your running containers. Quite often, a Compose file references a
Dockerfile to build an image to use for a particular service.

### What is the difference between thedocker compose upanddocker compose runcommands?

The `docker compose up` command creates and starts all your services. It's
perfect for launching your development environment or running the entire
application. The `docker compose run` command focuses on individual services.
It starts a specified service along with its dependencies, allowing you to run
tests or perform one-off tasks within that container.

---

# Demo: set up and use Docker Compose

> Learn how to get started with Docker Compose.

# Demo: set up and use Docker Compose

---

This Docker Compose demo shows how to orchestrate a multi-container application
environment, streamlining development and deployment processes.

- Compare Docker Compose to the `docker run` command
- Configure a multi-container web app using a Compose file
- Run a multi-container web app using one command

---

# Why Docker Compose?

> Learn how Docker Compose can help you simplify app development.

# Why Docker Compose?

---

Docker Compose is an essential tool for defining and running multi-container
Docker applications. Docker Compose simplifies the Docker experience, making it
easier for developers to create, manage, and deploy applications by using YAML
files to configure application services.

Docker Compose provides several benefits:

- Lets you define multi-container applications in a single YAML file.
- Ensures consistent environments across development, testing, and production.
- Manages the startup and linking of multiple containers effortlessly.
- Streamlines development workflows and reduces setup time.
- Ensures that each service runs in its own container, avoiding conflicts.

---

# Defining and running multi

> Learn how to use Docker Compose to define and run multi-container Docker applications.

# Defining and running multi-container applications with Docker Compose

Table of contents

---

Developers face challenges with multi-container Docker applications, including
complex configuration, dependency management, and maintaining consistent
environments. Networking, resource allocation, data persistence, logging, and
monitoring add to the difficulty. Security concerns and troubleshooting issues
further complicate the process, requiring effective tools and practices for
efficient management.

Docker Compose solves the problem of managing multi-container Docker
applications by providing a simple way to define, configure, and run all the
containers needed for an application using a single YAML file. This approach
helps developers to easily set up, share, and maintain consistent development,
testing, and production environments, ensuring that complex applications can be
deployed with all their dependencies and services properly configured and
orchestrated.

## What you’ll learn

- What Docker Compose is and what it does
- How to define services
- Use cases for Docker Compose
- How things would be different without Docker Compose

## Who’s this for?

- Developers and DevOps engineers who need to define, manage, and orchestrate
  multi-container Docker applications efficiently across multiple environments.
- Development teams that want to increase productivity by streamlining
  development workflows and reducing setup time.

## Tools integration

Works well with Docker CLI, CI/CD tools, and container orchestration tools.

## Modules

1. [Why Docker Compose?](https://docs.docker.com/guides/docker-compose/why/)
  Learn how Docker Compose can help you simplify app development.
2. [Demo: set up and use Docker Compose](https://docs.docker.com/guides/docker-compose/setup/)
  Learn how to get started with Docker Compose.
3. [Common challenges and questions](https://docs.docker.com/guides/docker-compose/common-questions/)
  Explore common challenges and questions related to Docker Compose.

---

# Attestations

> Introduction to SBOM and provenance attestations with Docker Build, what they are, and why they exist

# Attestations

---

[Build attestations](https://docs.docker.com/build/metadata/attestations/) give you
detailed information about how an image was built and what it contains. These
attestations, generated by BuildKit during build-time, attach to the final
image as metadata, allowing you to inspect an image to see its origin, creator,
and contents. This information helps you make informed decisions about the
security and impact of the image on your supply chain.

Docker Scout uses these attestations to evaluate the image's security and
supply chain posture, and to provide remediation recommendations for issues. If
issues are detected, such as missing or outdated attestations, Docker Scout can
guide you on how to add or update them, ensuring compliance and improving
visibility into the image's security status.

There are two key types of attestations:

- SBOM, which lists the software artifacts within the image.
- Provenance, which details how the image was built.

You can create attestations by using `docker buildx build` with the
`--provenance` and `--sbom` flags. Attestations attach to the image index,
allowing you to inspect them without pulling the entire image. Docker Scout
leverages this metadata to give you more precise recommendations and better
control over your image's security.

---

# Common challenges and questions

> Explore common challenges and questions related to Docker Scout.

# Common challenges and questions

   Table of contents

---

### How is Docker Scout different from other security tools?

Docker Scout takes a broader approach to container security compared to
third-party security tools. Third-party security tools, if they offer
remediation guidance at all, miss the mark on their limited scope of
application security posture within the software supply chain, and often
limited guidance when it comes to suggested fixes. Such tools have either
limitations on runtime monitoring or no runtime protection at all. When they do
offer runtime monitoring, it’s limited in its adherence to key policies.
Third-party security tools offer a limited scope of policy evaluation for
Docker-specific builds. By focusing on the entire software supply chain,
providing actionable guidance, and offering comprehensive runtime protection
with strong policy enforcement, Docker Scout goes beyond just identifying
vulnerabilities in your containers. It helps you build secure applications from
the ground up.

### Can I use Docker Scout with external registries other than Docker Hub?

You can use Scout with registries other than Docker Hub. Integrating Docker Scout
with third-party container registries enables Docker Scout to run image
analysis on those repositories so that you can get insights into the
composition of those images even if they aren't hosted on Docker Hub.

The following container registry integrations are available:

- Artifactory
- Amazon Elastic Container Registry
- Azure Container Registry

Learn more about configuring Scout with your registries in
[Integrating Docker Scout with third-party registries](https://docs.docker.com/scout/integrations/#container-registries).

### Does Docker Scout CLI come by default with Docker Desktop?

Yes, the Docker Scout CLI plugin comes pre-installed with Docker Desktop.

### Is it possible to rundocker scoutcommands on a Linux system without Docker Desktop?

If you run Docker Engine without Docker Desktop, Docker Scout doesn't come
pre-installed, but you can
[install it as a standalone binary](https://docs.docker.com/scout/install/).

### How is Docker Scout using an SBOM?

An SBOM, or software bill of materials, is a list of ingredients that make up
software components.
[Docker Scout uses SBOMs](https://docs.docker.com/scout/concepts/sbom/) to
determine the components that are used in a Docker image. When you analyze an
image, Docker Scout will either use the SBOM that is attached to the image (as
an attestation), or generate an SBOM on the fly by analyzing the contents of
the image.

The SBOM is cross-referenced with the advisory database to determine if any of
the components in the image have known vulnerabilities.

---

# Docker Scout demo

> Learn about Docker Scout's powerful features for enhanced supply chain security.

# Docker Scout demo

---

Docker Scout has powerful features for enhancing containerized application
security and ensuring a robust software supply chain.

- Define vulnerability remediation
- Discuss why remediation is essential to maintain the security and integrity
  of containerized applications
- Discuss common vulnerabilities
- Implement remediation techniques: updating base images, applying patches,
  removing unnecessary packages
- Verify and validate remediation efforts using Docker Scout

---

# Remediation

> Learn how Docker Scout can help you improve your software quality automatically, using remediation

# Remediation

---

Docker Scout's
[remediation feature](https://docs.docker.com/scout/policy/remediation/)
helps you address supply chain and security issues by offering tailored
recommendations based on policy evaluations. These recommendations guide you in
improving policy compliance or enhancing image metadata, allowing Docker Scout
to perform more accurate evaluations in the future.

You can use this feature to ensure that your base images are up-to-date and
that your supply chain attestations are complete. When a violation occurs,
Docker Scout provides recommended fixes, such as updating your base image or
adding missing attestations. If there isn’t enough information to determine
compliance, Docker Scout suggests actions to help resolve the issue.

In the Docker Scout Dashboard, you can view and act on these recommendations by
reviewing violations or compliance uncertainties. With integrations like
GitHub, you can even automate updates, directly fixing issues from the
dashboard.

---

# Software supply chain security

> Learn about software supply chain security (S3C), what it means, and why it is important.

# Software supply chain security

   Table of contents

---

The term "software supply chain" refers to the end-to-end process of developing
and delivering software, from the development to deployment and maintenance.
Software supply chain security, or "S3C" for short, is the practice for
protecting the components and processes of the supply chain.

S3C is a fundamental change in how organizations approach software security.
Traditionally in the software industry, security and compliance has been mostly
an afterthought, left to the software delivery or release phase. With S3C,
security is integrated into the entire software development lifecycle, from the
inner loop of development and testing, to the outer loop of shipping and
monitoring.

Following industry best practices for software supply chain conduct is
important because it helps organizations protect their software from security
threats, compliance risks, and other vulnerabilities. Implementing a software
supply chain security framework improves visibility, collaboration, and
traceability of a project across stakeholders. This helps organizations detect,
respond to, and remediate threats more effectively.

## Securing the software supply chain

Building a secure software supply chain involves several key steps, such as:

- Identify the software components and dependencies you use to build and run
  your applications.
- Automate security testing throughout the software development lifecycle.
- Monitor your software supply chain for security threats.
- Implement security policies that govern how software is built, and the
  components it contains.

Managing the software supply chain is a complex task, especially in the modern
day where software is built using multiple components from different sources.
Organizations need to have a clear understanding of the software components
they use, and the security risks associated with them.

## How Docker Scout is different

Docker Scout is a platform designed to help organizations secure their software
supply chain. It provides tools and services for identifying and managing
software assets and policies, and automated remediation of security threats.

Unlike traditional security tools that focus on scheduled, point-in-time scans
at specific stages in the software development lifecycle, Docker Scout uses a
modern event-driven model that spans the entire software supply chain. This
means that when a new vulnerability affecting your images is disclosed, your
updated risk assessment is available within seconds, and earlier in the
development process.

Docker Scout works by analyzing the composition of your images to create a
Software Bill of Materials (SBOM). The SBOM is cross-referenced against the
security advisories to identify CVEs that affect your images. Docker Scout
integrates with
[over 20 different security
advisories](https://docs.docker.com/scout/deep-dive/advisory-db-sources/), and updates its
vulnerability database in real-time. This ensures that your security posture is
represented using the latest available information.

---

# Software Bill of Materials

> Learn about Software Bill of Materials (SBOM) and how Docker Scout uses it.

# Software Bill of Materials

   Table of contents

---

A Bill of Materials (BOM) is a list of materials, parts, and the quantities of
each needed to manufacture a product. For example, a BOM for a computer might
list the motherboard, CPU, RAM, power supply, storage devices, case, and other
components, along with the quantities of each that are needed to build the
computer.

A Software Bill of Materials (SBOM) is a list of all the components that make
up a piece of software. This includes open source and third-party components,
as well as any custom code that has been written for the software. An SBOM is
similar to a BOM for a physical product, but for software.

In the context of software supply chain security, SBOMs can help with
identifying and mitigating security and compliance risks in software. By
knowing exactly what components are used in a piece of software, you can
quickly identify and patch vulnerabilities in your components, or determine if
a component is licensed in a way that is incompatible with your project.

## Contents of an SBOM

An SBOM typically includes the following information:

- The name of the software, such as the name of a library or framework, that
  the SBOM describes.
- The version of the software.
- The license under which the software is distributed.
- A list of other components that the software depends on.

## How Docker Scout uses SBOMs

Docker Scout uses SBOMs to determine the components that are used in a Docker
image. When you analyze an image, Docker Scout will either use the SBOM that is
attached to the image as an attestation, or it will generate an SBOM on the fly
by analyzing the contents of the image.

The SBOM is cross-referenced with the
[advisory database](https://docs.docker.com/scout/deep-dive/advisory-db-sources/)
to determine if any of the components in the image have known vulnerabilities.

---

# Why Docker Scout?

> Learn how Docker Scout can help you secure your supply chain.

# Why Docker Scout?

---

Organizations face significant challenges from data breaches,
including financial losses, operational disruptions, and long-term damage to
brand reputation and customer trust. Docker Scout addresses critical problems
such as identifying insecure container images, preventing security breaches,
and reducing the risk of operational downtime due to vulnerabilities.

Docker Scout provides several benefits:

- Secure and trusted content
- A system of record for your Software Development Lifecycle (SDLC)
- Continuous security posture improvement

Docker Scout offers automated vulnerability detection and remediation, helping
organizations identify and fix security issues in container images early in the
development process. It also integrates with popular development tools like
Docker Desktop and GitHub Actions, providing seamless security management and
compliance checks within existing workflows.

---

# Securing your software supply chain with Docker Scout

> Learn how to use Docker Scout to enhance container security by automating vulnerability detection and remediation, ensuring compliance, and protecting your development workflow.

# Securing your software supply chain with Docker Scout

Table of contents

---

When container images are insecure, significant risks can arise. Around 60% of
organizations have reported experiencing at least one security breach or
vulnerability incident within a year, [resulting in operational
disruption](https://cloudsecurityalliance.org/blog/2023/09/21/2023-global-cloud-threat-report-cloud-attacks-are-lightning-fast). These incidents often result in considerable downtime, with
44% of affected companies experiencing over an hour of downtime per event. The
financial impact is substantial, with [the average data breach cost reaching
$4.45 million](https://www.ibm.com/reports/data-breach). This highlights the critical importance of maintaining
robust container security measures.

Docker Scout enhances container security by providing automated vulnerability
detection and remediation, addressing insecure container images, and ensuring
compliance with security standards.

## What you'll learn

- Define Secure Software Supply Chain (SSSC)
- Review SBOMs and how to use them
- Detect and monitor vulnerabilities

## Tools integration

Works well with Docker Desktop, GitHub Actions, Jenkins, Kubernetes, and
other CI solutions.

## Who’s this for?

- DevOps engineers who need to integrate automated security checks into CI/CD
  pipelines to enhance the security and efficiency of their workflows.
- Developers who want to use Docker Scout to identify and remediate
  vulnerabilities early in the development process, ensuring the production of
  secure container images.
- Security professionals who must enforce security compliance, conduct
  vulnerability assessments, and ensure the overall security of containerized
  applications.

## Modules

1. [Why Docker Scout?](https://docs.docker.com/guides/docker-scout/why/)
  Learn how Docker Scout can help you secure your supply chain.
2. [Demo](https://docs.docker.com/guides/docker-scout/demo/)
  Learn about Docker Scout's powerful features for enhanced supply chain security.
3. [Software supply chain security](https://docs.docker.com/guides/docker-scout/s3c/)
  Learn about software supply chain security (S3C), what it means, and why it is important.
4. [Software Bill of Materials](https://docs.docker.com/guides/docker-scout/sbom/)
  Learn about Software Bill of Materials (SBOM) and how Docker Scout uses it.
5. [Attestations](https://docs.docker.com/guides/docker-scout/attestations/)
  Introduction to SBOM and provenance attestations with Docker Build,
  what they are, and why they exist
6. [Remediation](https://docs.docker.com/guides/docker-scout/remediation/)
  Learn how Docker Scout can help you improve your software quality automatically, using remediation
7. [Common challenges and questions](https://docs.docker.com/guides/docker-scout/common-questions/)
  Explore common challenges and questions related to Docker Scout.

---

# Configure CI/CD for your .NET application

> Learn how to Configure CI/CD for your .NET application

# Configure CI/CD for your .NET application

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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
7. In your local repository on your machine, run the following command to rename
  the branch to main.
  ```console
  $ git branch -M main
  ```
8. Run the following commands to stage, commit, and then push your local
  repository to GitHub.
  ```console
  $ git add -A
  $ git commit -m "my first commit"
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
        - name: Build and test
          uses: docker/build-push-action@v6
          with:
            target: build
            load: true
        - name: Build and push
          uses: docker/build-push-action@v6
          with:
            platforms: linux/amd64,linux/arm64
            push: true
            target: final
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

In this section, you learned how to set up a GitHub Actions workflow for your application.

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

---

# Containerize a .NET application

> Learn how to containerize an ASP.NET application.

# Containerize a .NET application

   Table of contents

---

## Prerequisites

- You have installed the latest version of
  [Docker
  Desktop](https://docs.docker.com/get-started/get-docker/).
- You have a [git client](https://git-scm.com/downloads). The examples in this
  section use a command-line based git client, but you can use any client.

## Overview

This section walks you through containerizing and running a .NET
application.

## Get the sample applications

In this guide, you will use a pre-built .NET application. The application is
similar to the application built in the Docker Blog article, [Building a
Multi-Container .NET App Using Docker
Desktop](https://www.docker.com/blog/building-multi-container-net-app-using-docker-desktop/).

Open a terminal, change directory to a directory that you want to work in, and
run the following command to clone the repository.

```console
$ git clone https://github.com/docker/docker-dotnet-sample
```

## Initialize Docker assets

Now that you have an application, you can use `docker init` to create the
necessary Docker assets to containerize your application. Inside the
`docker-dotnet-sample` directory, run the `docker init` command in a terminal.
`docker init` provides some default configuration, but you'll need to answer a
few questions about your application. Refer to the following example to answer
the prompts from `docker init` and use the same answers for your prompts.

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? ASP.NET Core
? What's the name of your solution's main project? myWebApp
? What version of .NET do you want to use? 8.0
? What local port do you want to use to access your server? 8080
```

You should now have the following contents in your `docker-dotnet-sample`
directory.

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

To learn more about the files that `docker init` added, see the following:

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [compose.yaml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `docker-dotnet-sample` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple web application.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `docker-dotnet-sample` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple web application.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the
[Compose CLI
reference](https://docs.docker.com/reference/cli/docker/compose/).

## Summary

In this section, you learned how you can containerize and run your .NET
application using Docker.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore file reference](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [Docker Compose overview](https://docs.docker.com/compose/)

## Next steps

In the next section, you'll learn how you can develop your application using
Docker containers.

---

# Test your .NET deployment

> Learn how to deploy your application

# Test your .NET deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize
  a .NET application](https://docs.docker.com/guides/dotnet/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker
  Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your
application to a fully-featured Kubernetes environment on your development
machine. This allows you to test and debug your workloads on Kubernetes locally
before deploying.

## Create a Kubernetes YAML file

In your `docker-dotnet-sample` directory, create a file named
`docker-dotnet-kubernetes.yaml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your .NET application](https://docs.docker.com/guides/dotnet/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: server
  strategy: {}
  template:
    metadata:
      labels:
        service: server
    spec:
      initContainers:
        - name: wait-for-db
          image: busybox:1.28
          command:
            [
              "sh",
              "-c",
              'until nc -zv db 5432; do echo "waiting for db"; sleep 2; done;',
            ]
      containers:
        - image: DOCKER_USERNAME/REPO_NAME
          name: server
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              hostPort: 8080
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: db
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        service: db
    spec:
      containers:
        - env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_PASSWORD
              value: example
          image: postgres:18
          name: db
          ports:
            - containerPort: 5432
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  type: NodePort
  ports:
    - name: "8080"
      port: 8080
      targetPort: 8080
      nodePort: 30001
  selector:
    service: server
status:
  loadBalancer: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  ports:
    - name: "5432"
      port: 5432
      targetPort: 5432
  selector:
    service: db
status:
  loadBalancer: {}
```

In this Kubernetes YAML file, there are four objects, separated by the `---`. In addition to a Service and Deployment for the database, the other two objects are:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The container is
  created from the image built by GitHub Actions in [Configure CI/CD for your
  .NET application](https://docs.docker.com/guides/dotnet/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 8080 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to the `docker-dotnet-sample` directory
  and deploy your application to Kubernetes.
  ```console
  $ kubectl apply -f docker-dotnet-kubernetes.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```shell
  deployment.apps/db created
  service/db created
  deployment.apps/server created
  service/server created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```shell
  NAME     READY   UP-TO-DATE   AVAILABLE   AGE
  db       1/1     1            1           76s
  server   1/1     1            1           76s
  ```
  This indicates all of the pods are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```shell
  NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  db           ClusterIP   10.96.156.90    <none>        5432/TCP         2m8s
  kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          164m
  server       NodePort    10.102.94.225   <none>        8080:30001/TCP   2m8s
  ```
  In addition to the default `kubernetes` service, you can see your `server` service and `db` service. The `server` service is accepting traffic on port 30001/TCP.
3. Open a browser and visit your app at `localhost:30001`. You should see your
  application.
4. Run the following command to tear down your application.
  ```console
  $ kubectl delete -f docker-dotnet-kubernetes.yaml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)
