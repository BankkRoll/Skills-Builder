# Automate your builds with GitHub Actions and more

# Automate your builds with GitHub Actions

> Learn how to configure CI/CD using GitHub Actions for your Vue.js application.

# Automate your builds with GitHub Actions

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize an Vue.js application](https://docs.docker.com/guides/vuejs/containerize/).

You must also have:

- A [GitHub](https://github.com/signup) account.
- A verified [Docker Hub](https://hub.docker.com/signup) account.

---

## Overview

In this section, you'll set up a CI/CD pipeline using [GitHub Actions](https://docs.github.com/en/actions) to automatically:

- Build your Vue.js application inside a Docker container.
- Run tests in a consistent environment.
- Push the production-ready image to [Docker Hub](https://hub.docker.com).

---

## Connect your GitHub repository to Docker Hub

To enable GitHub Actions to build and push Docker images, you’ll securely store your Docker Hub credentials in your new GitHub repository.

### Step 1: Generate Docker Hub Credentials and Set GitHub Secrets"

1. Create a Personal Access Token (PAT) from [Docker Hub](https://hub.docker.com)
  1. Go to your **Docker Hub account → Account Settings → Security**.
  2. Generate a new Access Token with **Read/Write** permissions.
  3. Name it something like `docker-vuejs-sample`.
  4. Copy and save the token — you’ll need it in Step 4.
2. Create a repository in [Docker Hub](https://hub.docker.com/repositories/)
  1. Go to your **Docker Hub account → Create a repository**.
  2. For the Repository Name, use something descriptive — for example: `vuejs-sample`.
  3. Once created, copy and save the repository name — you’ll need it in Step 4.
3. Create a new [GitHub repository](https://github.com/new) for your Vue.js project
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
  These secrets allow GitHub Actions to authenticate securely with Docker Hub during automated workflows.
5. Connect Your Local Project to GitHub
  Link your local project `docker-vuejs-sample` to the GitHub repository you just created by running the following command from your project root:
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
6. Push your source code to GitHub
  Follow these steps to commit and push your local project to your GitHub repository:
  1. Stage all files for commit.
    ```console
    $ git add -A
    ```
    This command stages all changes — including new, modified, and deleted files — preparing them for commit.
  2. Commit the staged changes with a descriptive message.
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
name: CI/CD – Vue.js App with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-deploy:
    name: Build, Test & Deploy
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout the codebase
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. Cache Docker layers
      - name: Cache Docker Layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm Dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. Generate build metadata
      - name: Generate Build Metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build Docker image for testing
      - name: Build Dev Docker Image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run unit tests inside container
      - name: Run Vue.js Tests
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npm run test -- --ci --runInBand"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Log in to Docker Hub
      - name: Docker Hub Login
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push production image
      - name: Build and Push Production Image
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

This workflow performs the following tasks for your Vue.js application:

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
  - Select "Commit changes…" in the GitHub editor.
  - This push will automatically trigger the GitHub Actions pipeline.
2. Monitor the workflow execution
  - Go to the Actions tab in your GitHub repository.
  - Click into the workflow run to follow each step: **build**, **test**, and (if successful) **push**.
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

In this section, you set up a complete CI/CD pipeline for your containerized Vue.js application using GitHub Actions.

Here's what you accomplished:

- Created a new GitHub repository specifically for your project.
- Generated a secure Docker Hub access token and added it to GitHub as a secret.
- Defined a GitHub Actions workflow that:
  - Build your application inside a Docker container.
  - Run tests in a consistent, containerized environment.
  - Push a production-ready image to Docker Hub if tests pass.
- Triggered and verified the workflow execution through GitHub Actions.
- Confirmed that your image was successfully published to Docker Hub.

With this setup, your Vue.js application is now ready for automated testing and deployment across environments — increasing confidence, consistency, and team productivity.

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

Next, learn how you can locally test and debug your Vue.js workloads on Kubernetes before deploying. This helps you ensure your application behaves as expected in a production-like environment, reducing surprises during deployment.

---

# Containerize an Vue.js Application

> Learn how to containerize an Vue.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.

# Containerize an Vue.js Application

   Table of contents

---

## Prerequisites

Before you begin, make sure the following tools are installed and available on your system:

- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
- You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

> **New to Docker?**
> Start with the
> [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide to get familiar with key concepts like images, containers, and Dockerfiles.

---

## Overview

This guide walks you through the complete process of containerizing an Vue.js application with Docker. You’ll learn how to create a production-ready Docker image using best practices that improve performance, security, scalability, and deployment efficiency.

By the end of this guide, you will:

- Containerize an Vue.js application using Docker.
- Create and optimize a Dockerfile for production builds.
- Use multi-stage builds to minimize image size.
- Serve the application efficiently with a custom Nginx configuration.
- Build secure and maintainable Docker images by following best practices.

---

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, navigate to the directory where you want to work, and run the following command
to clone the git repository:

```console
$ git clone https://github.com/kristiyan-velkov/docker-vuejs-sample
```

---

## Generate a Dockerfile

Docker provides an interactive CLI tool called `docker init` that helps scaffold the necessary configuration files for containerizing your application. This includes generating a `Dockerfile`, `.dockerignore`, `compose.yaml`, and `README.Docker.md`.

To begin, navigate to the root of your project directory:

```console
$ cd docker-vuejs-sample
```

Then run the following command:

```console
$ docker init
```

You’ll see output similar to:

```text
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

The CLI will prompt you with a few questions about your app setup.
For consistency, please use the same responses shown in the example below when prompted:

| Question | Answer |
| --- | --- |
| What application platform does your project use? | Node |
| What version of Node do you want to use? | 24.12.0-alpine |
| Which package manager do you want to use? | npm |
| Do you want to run "npm run build" before starting server? | yes |
| What directory is your build output to? | dist |
| What command do you want to use to start the app? | npm run build |
| What port does your server listen on? | 8080 |

After completion, your project directory will contain the following new files:

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## Build the Docker image

The default Dockerfile generated by `docker init` provides a solid foundation for typical Node.js applications. However, Vue.js is a front-end framework that compiles into static assets, which means the Dockerfile needs to be customized to align with how Vue.js applications are built and efficiently served in a production environment. Tailoring it properly ensures better performance, smaller image sizes, and a smoother deployment process.

### Step 1: Review the generated files

In this step, you’ll improve the Dockerfile and configuration files by following best practices:

- Use multi-stage builds to keep the final image clean and small
- Serve the app using Nginx, a fast and secure web server
- Improve performance and security by only including what’s needed

These updates help ensure your app is easy to deploy, fast to load, and production-ready.

> Note
>
> A `Dockerfile` is a plain text file that contains step-by-step instructions to build a Docker image. It automates packaging your application along with its dependencies and runtime environment.
> For full details, see the
> [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

### Step 2: Configure the Dockerfile

Before creating a Dockerfile, you need to choose a base image. You can either use the [Node.js Official Image](https://hub.docker.com/_/node) or a Docker Hardened Image (DHI) from the [Hardened Image catalog](https://hub.docker.com/hardened-images/catalog).

Choosing DHI offers the advantage of a production-ready image that is lightweight and secure. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

> Important
>
> This guide uses a stable Node.js LTS image tag that is considered secure when the guide is written. Because new releases and security patches are published regularly, the tag shown here may no longer be the safest option when you follow the guide. Always review the latest available image tags and select a secure, up-to-date version before building or deploying your application.
>
>
>
> Official Node.js Docker Images: [https://hub.docker.com/_/node](https://hub.docker.com/_/node)

Docker Hardened Images (DHIs) are available for Node.js in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/node). Docker Hardened Images are freely available to everyone with no subscription required. You can pull and use them like any other Docker image after signing in to the DHI registry. For more information, see the
[DHI quickstart](https://docs.docker.com/dhi/get-started/) guide.

1. Sign in to the DHI registry:
  ```console
  $ docker login dhi.io
  ```
2. Pull the Node.js DHI (check the catalog for available versions):
  ```console
  $ docker pull dhi.io/node:24-alpine3.22-dev
  ```
3. Pull the Nginx DHI (check the catalog for available versions):
  ```console
  $ docker pull dhi.io/nginx:1.28.0-alpine3.21-dev
  ```

In the following Dockerfile, the `FROM` instructions use `dhi.io/node:24-alpine3.22-dev` and `dhi.io/nginx:1.28.0-alpine3.21-dev` as the base images.

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
# Use a lightweight DHI Node.js image for building
FROM dhi.io/node:24-alpine3.22-dev AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

Replace the contents of your current `Dockerfile` with the optimized configuration below. This setup is tailored specifically for building and serving Vue.js applications in a clean, efficient, and production-ready environment.

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> Note
>
> We are using nginx-unprivileged instead of the standard Nginx image to follow security best practices.
> Running as a non-root user in the final image:
>
>
>
> - Reduces the attack surface
> - Aligns with Docker’s recommendations for container hardening
> - Helps comply with stricter security policies in production environments

### Step 3: Configure the .dockerignore file

The `.dockerignore` file plays a crucial role in optimizing your Docker image by specifying which files and directories should be excluded from the build context.

> Note
>
> This helps:
>
>
>
> - Reduce image size
> - Speed up the build process
> - Prevent sensitive or unnecessary files (like `.env`, `.git`, or `node_modules`) from being added to the final image.
>
>
>
> To learn more, visit the
> [.dockerignore reference](https://docs.docker.com/reference/dockerfile/#dockerignore-file).

Copy and replace the contents of your existing `.dockerignore` with the configuration below:

```dockerignore
# -------------------------------
# Dependency directories
# -------------------------------
node_modules/

# -------------------------------
# Production and build outputs
# -------------------------------
dist/
out/
build/
public/build/

# -------------------------------
# Vite, VuePress, and cache dirs
# -------------------------------
.vite/
.vitepress/
.cache/
.tmp/

# -------------------------------
# Test output and coverage
# -------------------------------
coverage/
reports/
jest/
cypress/
cypress/screenshots/
cypress/videos/

# -------------------------------
# Environment and config files
# -------------------------------
*.env*
!.env.production    # Keep production env if needed
*.local
*.log

# -------------------------------
# TypeScript artifacts
# -------------------------------
*.tsbuildinfo

# -------------------------------
# Editor and IDE config
# -------------------------------
.vscode/
.idea/
*.swp

# -------------------------------
# System files
# -------------------------------
.DS_Store
Thumbs.db

# -------------------------------
# Lockfiles (optional)
# -------------------------------
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# -------------------------------
# Git files
# -------------------------------
.git/
.gitignore

# -------------------------------
# Docker-related files
# -------------------------------
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml
```

### Step 4: Create thenginx.conffile

To serve your Vue.js application efficiently inside the container, you’ll configure Nginx with a custom setup. This configuration is optimized for performance, browser caching, gzip compression, and support for client-side routing.

Create a file named `nginx.conf` in the root of your project directory, and add the following content:

> Note
>
> To learn more about configuring Nginx, see the [official Nginx documentation](https://nginx.org/en/docs/).

```nginx
worker_processes auto;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    charset       utf-8;

    access_log    off;
    error_log     /dev/stderr warn;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    gzip on;
    gzip_comp_level 6;
    gzip_proxied any;
    gzip_min_length 256;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

    server {
        listen       8080;
        server_name  localhost;

        root   /usr/share/nginx/html;
        index  index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }

        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }

        error_page 404 /index.html;
    }
}
```

### Step 5: Build the Vue.js application image

With your custom configuration in place, you're now ready to build the Docker image for your Vue.js application.

The updated setup includes:

- The updated setup includes a clean, production-ready Nginx configuration tailored specifically for Vue.js.
- Efficient multi-stage Docker build, ensuring a small and secure final image.

After completing the previous steps, your project directory should now contain the following files:

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

Now that your Dockerfile is configured, you can build the Docker image for your Vue.js application.

> Note
>
> The `docker build` command packages your application into an image using the instructions in the Dockerfile. It includes all necessary files from the current directory (called the
> [build context](https://docs.docker.com/build/concepts/context/#what-is-a-build-context)).

Run the following command from the root of your project:

```console
$ docker build --tag docker-vuejs-sample .
```

What this command does:

- Uses the Dockerfile in the current directory (.)
- Packages the application and its dependencies into a Docker image
- Tags the image as docker-vuejs-sample so you can reference it later

#### Step 6: View local images

After building your Docker image, you can check which images are available on your local machine using either the Docker CLI or
[Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/). Since you're already working in the terminal, let's use the Docker CLI.

To list all locally available Docker images, run the following command:

```console
$ docker images
```

Example Output:

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-vuejs-sample       latest            8c9c199179d4   14 seconds ago   76.2MB
```

This output provides key details about your images:

- **Repository** – The name assigned to the image.
- **Tag** – A version label that helps identify different builds (e.g., latest).
- **Image ID** – A unique identifier for the image.
- **Created** – The timestamp indicating when the image was built.
- **Size** – The total disk space used by the image.

If the build was successful, you should see `docker-vuejs-sample` image listed.

---

## Run the containerized application

In the previous step, you created a Dockerfile for your Vue.js application and built a Docker image using the docker build command. Now it’s time to run that image in a container and verify that your application works as expected.

Inside the `docker-vuejs-sample` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple Vue.js web application.

Press `ctrl+c` in the terminal to stop your application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `docker-vuejs-sample` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see your Vue.js application running in the browser.

To confirm that the container is running, use `docker ps` command:

```console
$ docker ps
```

This will list all active containers along with their ports, names, and status. Look for a container exposing port 8080.

Example Output:

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
37a1fa85e4b0   docker-vuejs-sample-server     "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-vuejs-sample-server-1
```

To stop the application, run:

```console
$ docker compose down
```

> Note
>
> For more information about Compose commands, see the
> [Compose CLI
> reference](https://docs.docker.com/reference/cli/docker/compose/).

---

## Summary

In this guide, you learned how to containerize, build, and run an Vue.js application using Docker. By following best practices, you created a secure, optimized, and production-ready setup.

What you accomplished:

- Initialized your project using `docker init` to scaffold essential Docker configuration files.
- Replaced the default `Dockerfile` with a multi-stage build that compiles the Vue.js application and serves the static files using Nginx.
- Replaced the default `.dockerignore` file to exclude unnecessary files and keep the image clean and efficient.
- Built your Docker image using `docker build`.
- Ran the container using `docker compose up`, both in the foreground and in detached mode.
- Verified that the app was running by visiting [http://localhost:8080](http://localhost:8080).
- Learned how to stop the containerized application using `docker compose down`.

You now have a fully containerized Vue.js application, running in a Docker container, and ready for deployment across any environment with confidence and consistency.

---

## Related resources

Explore official references and best practices to sharpen your Docker workflow:

- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) – Learn how to separate build and runtime stages.
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
- [Build context in Docker](https://docs.docker.com/build/concepts/context/) – Learn how context affects image builds.
- [docker initCLI reference](https://docs.docker.com/reference/cli/docker/init/) – Scaffold Docker assets automatically.
- [docker buildCLI reference](https://docs.docker.com/reference/cli/docker/build/) – Build Docker images from a Dockerfile.
- [docker imagesCLI reference](https://docs.docker.com/reference/cli/docker/images/) – Manage and inspect local Docker images.
- [docker compose upCLI reference](https://docs.docker.com/reference/cli/docker/compose/up/) – Start and run multi-container applications.
- [docker compose downCLI reference](https://docs.docker.com/reference/cli/docker/compose/down/) – Stop and remove containers, networks, and volumes.

---

## Next steps

With your Vue.js application now containerized, you're ready to move on to the next step.

In the next section, you'll learn how to develop your application using Docker containers, enabling a consistent, isolated, and reproducible development environment across any machine.

---

# Test your Vue.js deployment

> Learn how to deploy locally to test and debug your Kubernetes deployment

# Test your Vue.js deployment

   Table of contents

---

## Prerequisites

Before you begin, make sure you’ve completed the following:

- Complete all the previous sections of this guide, starting with [Containerize Vue.js application](https://docs.docker.com/guides/vuejs/containerize/).
- [Enable Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

> **New to Kubernetes?**
> Visit the [Kubernetes basics tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/) to get familiar with how clusters, pods, deployments, and services work.

---

## Overview

This section guides you through deploying your containerized Vue.js application locally using
[Docker Desktop’s built-in Kubernetes](https://docs.docker.com/desktop/kubernetes/). Running your app in a local Kubernetes cluster closely simulates a real production environment, enabling you to test, validate, and debug your workloads with confidence before promoting them to staging or production.

---

## Create a Kubernetes YAML file

Follow these steps to define your deployment configuration:

1. In the root of your project, create a new file named: vuejs-sample-kubernetes.yaml
2. Open the file in your IDE or preferred text editor.
3. Add the following configuration, and be sure to replace `{DOCKER_USERNAME}` and `{DOCKERHUB_PROJECT_NAME}` with your actual Docker Hub username and repository name from the previous [Automate your builds with GitHub Actions](https://docs.docker.com/guides/vuejs/configure-github-actions/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vuejs-sample
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vuejs-sample
  template:
    metadata:
      labels:
        app: vuejs-sample
    spec:
      containers:
        - name: vuejs-container
          image: {DOCKER_USERNAME}/{DOCKERHUB_PROJECT_NAME}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
            requests:
              cpu: "250m"
              memory: "128Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: vuejs-sample-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: vuejs-sample
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

This manifest defines two key Kubernetes resources, separated by `---`:

- Deployment
  Deploys a single replica of your Vue.js application inside a pod. The pod uses the Docker image built and pushed by your GitHub Actions CI/CD workflow
  (refer to [Automate your builds with GitHub Actions](https://docs.docker.com/guides/vuejs/configure-github-actions/)).
  The container listens on port `8080`, which is typically used by [Nginx](https://nginx.org/en/docs/) to serve your production Vue.js app.
- Service (NodePort)
  Exposes the deployed pod to your local machine.
  It forwards traffic from port `30001` on your host to port `8080` inside the container.
  This lets you access the application in your browser at [http://localhost:30001](http://localhost:30001).

> Note
>
> To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

---

## Deploy and check your application

Follow these steps to deploy your containerized Vue.js app into a local Kubernetes cluster and verify that it’s running correctly.

### Step 1. Apply the Kubernetes configuration

In your terminal, navigate to the directory where your `vuejs-sample-kubernetes.yaml` file is located, then deploy the resources using:

```console
$ kubectl apply -f vuejs-sample-kubernetes.yaml
```

If everything is configured properly, you’ll see confirmation that both the Deployment and the Service were created:

```shell
deployment.apps/vuejs-sample created
  service/vuejs-sample-service created
```

This confirms that both the Deployment and the Service were successfully created and are now running inside your local cluster.

### Step 2. Check the Deployment status

Run the following command to check the status of your deployment:

```console
$ kubectl get deployments
```

You should see output similar to the following:

```shell
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  vuejs-sample         1/1     1            1           1m14s
```

This confirms that your pod is up and running with one replica available.

### Step 3. Verify the Service exposure

Check if the NodePort service is exposing your app to your local machine:

```console
$ kubectl get services
```

You should see something like:

```shell
NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
vuejs-sample-service     NodePort    10.98.233.59    <none>        8080:30001/TCP   1m
```

This output confirms that your app is available via NodePort on port 30001.

### Step 4. Access your app in the browser

Open your browser and navigate to [http://localhost:30001](http://localhost:30001).

You should see your production-ready Vue.js Sample application running — served by your local Kubernetes cluster.

### Step 5. Clean up Kubernetes resources

Once you're done testing, you can delete the deployment and service using:

```console
$ kubectl delete -f vuejs-sample-kubernetes.yaml
```

Expected output:

```shell
deployment.apps "vuejs-sample" deleted
  service "vuejs-sample-service" deleted
```

This ensures your cluster stays clean and ready for the next deployment.

---

## Summary

In this section, you learned how to deploy your Vue.js application to a local Kubernetes cluster using Docker Desktop. This setup allows you to test and debug your containerized app in a production-like environment before deploying it to the cloud.

What you accomplished:

- Created a Kubernetes Deployment and NodePort Service for your Vue.js app
- Used `kubectl apply` to deploy the application locally
- Verified the app was running and accessible at `http://localhost:30001`
- Cleaned up your Kubernetes resources after testing

---

## Related resources

Explore official references and best practices to sharpen your Kubernetes deployment workflow:

- [Kubernetes documentation](https://kubernetes.io/docs/home/) – Learn about core concepts, workloads, services, and more.
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/manuals) – Use Docker Desktop’s built-in Kubernetes support for local testing and development.
- [kubectlCLI reference](https://kubernetes.io/docs/reference/kubectl/) – Manage Kubernetes clusters from the command line.
- [Kubernetes Deployment resource](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – Understand how to manage and scale applications using Deployments.
- [Kubernetes Service resource](https://kubernetes.io/docs/concepts/services-networking/service/) – Learn how to expose your application to internal and external traffic.

---

# Use containers for Vue.js development

> Learn how to develop your Vue.js application locally using containers.

# Use containers for Vue.js development

   Table of contents

---

## Prerequisites

Complete [Containerize Vue.js application](https://docs.docker.com/guides/vuejs/containerize/).

---

## Overview

In this section, you'll set up both production and development environments for your Vue.js application using Docker Compose. This approach streamlines your workflow—delivering a lightweight, static site via Nginx in production, and providing a fast, live-reloading dev server with Compose Watch for efficient local development.

You’ll learn how to:

- Configure isolated environments: Set up separate containers optimized for production and development use cases.
- Live-reload in development: Use Compose Watch to automatically sync file changes, enabling real-time updates without manual intervention.
- Preview and debug with ease: Develop inside containers with a seamless preview and debug experience—no rebuilds required after every change.

---

## Automatically update services (Development Mode)

Leverage Compose Watch to enable real-time file synchronization between your local machine and the containerized Vue.js development environment. This powerful feature eliminates the need to manually rebuild or restart containers, providing a fast, seamless, and efficient development workflow.

With Compose Watch, your code updates are instantly reflected inside the container—perfect for rapid testing, debugging, and live previewing changes.

## Step 1: Create a development Dockerfile

Create a file named `Dockerfile.dev` in your project root with the following content:

```dockerfile
# =========================================
# Stage 1: Develop the Vue.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine

# Use a lightweight Node.js image for development
FROM node:${NODE_VERSION} AS dev

# Set environment variable to indicate development mode
ENV NODE_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies
RUN --mount=type=cache,target=/root/.npm npm install

# Copy the rest of the application source code into the container
COPY . .

# Change ownership of the application directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the port used by the Vite development server
EXPOSE 5173

# Use a default command, can be overridden in Docker compose.yml file
CMD [ "npm", "run", "dev", "--", "--host" ]
```

This file sets up a lightweight development environment for your Vue.js application using the dev server.

### Step 2: Update yourcompose.yamlfile

Open your `compose.yaml` file and define two services: one for production (`vuejs-prod`) and one for development (`vuejs-dev`).

Here’s an example configuration for an Vue.js application:

```yaml
services:
  vuejs-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-vuejs-sample
    ports:
      - "8080:8080"

  vuejs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - path: ./src
          target: /app/src
          action: sync
        - path: ./package.json
          target: /app/package.json
          action: restart
        - path: ./vite.config.js
          target: /app/vite.config.js
          action: restart
```

- The `vuejs-prod` service builds and serves your static production app using Nginx.
- The `vuejs-dev` service runs your Vue.js development server with live reload and hot module replacement.
- `watch` triggers file sync with Compose Watch.

> Note
>
> For more details, see the official guide:
> [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

After completing the previous steps, your project directory should now contain the following files:

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### Step 4: Start Compose Watch

Run the following command from the project root to start the container in watch mode

```console
$ docker compose watch vuejs-dev
```

### Step 5: Test Compose Watch with Vue.js

To confirm that Compose Watch is functioning correctly:

1. Open the `src/App.vue` file in your text editor.
2. Locate the following line:
  ```html
  <HelloWorld msg="You did it!" />
  ```
3. Change it to:
  ```html
  <HelloWorld msg="Hello from Docker Compose Watch" />
  ```
4. Save the file.
5. Open your browser at [http://localhost:5173](http://localhost:5173).

You should see the updated text appear instantly, without needing to rebuild the container manually. This confirms that file watching and automatic synchronization are working as expected.

---

## Summary

In this section, you set up a complete development and production workflow for your Vue.js application using Docker and Docker Compose.

Here’s what you accomplished:

- Created a `Dockerfile.dev` to streamline local development with hot reloading
- Defined separate `vuejs-dev` and `vuejs-prod` services in your `compose.yaml` file
- Enabled real-time file syncing using Compose Watch for a smoother development experience
- Verified that live updates work seamlessly by modifying and previewing a component

With this setup, you're now equipped to build, run, and iterate on your Vue.js app entirely within containers—efficiently and consistently across environments.

---

## Related resources

Deepen your knowledge and improve your containerized development workflow with these guides:

- [Using Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) – Automatically sync source changes during development
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) – Create efficient, production-ready Docker images
- [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/) – Write clean, secure, and optimized Dockerfiles.
- [Compose file reference](https://docs.docker.com/compose/compose-file/) – Learn the full syntax and options available for configuring services in `compose.yaml`.
- [Docker volumes](https://docs.docker.com/storage/volumes/) – Persist and manage data between container runs

## Next steps

In the next section, you'll learn how to run unit tests for your Vue.js application inside Docker containers. This ensures consistent testing across all environments and removes dependencies on local machine setup.
