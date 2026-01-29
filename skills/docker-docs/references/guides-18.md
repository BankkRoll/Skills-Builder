# Containerize a Node.js application and more

# Containerize a Node.js application

> Learn how to containerize a Node.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.

# Containerize a Node.js application

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

This guide walks you through the complete process of containerizing a Node.js application with Docker. You’ll learn how to create a production-ready Docker image using best practices that enhance performance, security, scalability, and operational efficiency.

By the end of this guide, you will:

- Containerize a Node.js application using Docker.
- Create and optimize a Dockerfile tailored for Node.js environments.
- Use multi-stage builds to separate dependencies and reduce image size.
- Configure the container for secure, efficient runtime using a non-root user.
- Follow best practices for building secure, lightweight, and maintainable Docker images.

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, change
directory to a directory that you want to work in, and run the following command
to clone the git repository:

```console
$ git clone https://github.com/kristiyan-velkov/docker-nodejs-sample
```

## Generate a Dockerfile

Docker provides an interactive CLI tool called `docker init` that helps scaffold the necessary configuration files for containerizing your application. This includes generating a `Dockerfile`, `.dockerignore`, `compose.yaml`, and `README.Docker.md`.

To begin, navigate to the root of your project directory:

```console
$ cd docker-nodejs-sample
```

Then run the following command:

```console
$ docker init
```

You’ll see output similar to:

```text
Welcome to the Docker Init CLI

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

The CLI will prompt you with a few questions about your app setup.
For consistency, use the same responses shown in the example following when prompted:

| Question | Answer |
| --- | --- |
| What application platform does your project use? | Node |
| What version of Node do you want to use? | 24.11.1-alpine |
| Which package manager do you want to use? | npm |
| Do you want to run "npm run build" before starting server? | yes |
| What directory is your build output to? | dist |
| What command do you want to use to start the app? | npm run dev |
| What port does your server listen on? | 3000 |

After completion, your project directory will contain the following new files:

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

## Create a Docker Compose file

While `docker init` generates a basic `compose.yaml` file, you'll need to create a more comprehensive configuration for this full-stack application. Replace the generated `compose.yaml` with a production-ready configuration.

Create a new file named `compose.yml` in your project root:

```yaml
# ========================================
# Docker Compose Configuration
# Modern Node.js Todo Application
# ========================================

services:
  # ========================================
  # Development Service
  # ========================================
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: todoapp-dev
    ports:
      - '${APP_PORT:-3000}:3000' # API server
      - '${VITE_PORT:-5173}:5173' # Vite dev server
      - '${DEBUG_PORT:-9229}:9229' # Node.js debugger
    environment:
      NODE_ENV: development
      DOCKER_ENV: 'true'
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: todoapp
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
      ALLOWED_ORIGINS: '${ALLOWED_ORIGINS:-http://localhost:3000,http://localhost:5173}'
    volumes:
      - ./src:/app/src:ro
      - ./package.json:/app/package.json
      - ./vite.config.ts:/app/vite.config.ts:ro
      - ./tailwind.config.js:/app/tailwind.config.js:ro
      - ./postcss.config.js:/app/postcss.config.js:ro
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - '**/*.test.*'
            - '**/__tests__/**'
        - action: rebuild
          path: ./package.json
        - action: sync
          path: ./vite.config.ts
          target: /app/vite.config.ts
        - action: sync
          path: ./tailwind.config.js
          target: /app/tailwind.config.js
        - action: sync
          path: ./postcss.config.js
          target: /app/postcss.config.js
    restart: unless-stopped
    networks:
      - todoapp-network

  # ========================================
  # Production Service
  # ========================================
  app-prod:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: todoapp-prod
    ports:
      - '${PROD_PORT:-8080}:3000'
    environment:
      NODE_ENV: production
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: todoapp
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
      ALLOWED_ORIGINS: '${ALLOWED_ORIGINS:-https://yourdomain.com}'
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: '${PROD_MEMORY_LIMIT:-2G}'
          cpus: '${PROD_CPU_LIMIT:-1.0}'
        reservations:
          memory: '${PROD_MEMORY_RESERVATION:-512M}'
          cpus: '${PROD_CPU_RESERVATION:-0.25}'
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - todoapp-network
    profiles:
      - prod

  # ========================================
  # PostgreSQL Database Service
  # ========================================
  db:
    image: postgres:18-alpine
    container_name: todoapp-db
    environment:
      POSTGRES_DB: '${POSTGRES_DB:-todoapp}'
      POSTGRES_USER: '${POSTGRES_USER:-todoapp}'
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
    volumes:
      - postgres_data:/var/lib/postgresql
    ports:
      - '${DB_PORT:-5432}:5432'
    restart: unless-stopped
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER:-todoapp} -d ${POSTGRES_DB:-todoapp}']
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 5s
    networks:
      - todoapp-network

# ========================================
# Volume Configuration
# ========================================
volumes:
  postgres_data:
    name: todoapp-postgres-data
    driver: local

# ========================================
# Network Configuration
# ========================================
networks:
  todoapp-network:
    name: todoapp-network
    driver: bridge
```

This Docker Compose configuration includes:

- **Development service** (`app-dev`): Full development environment with hot reload, debugging support, and bind mounts
- **Production service** (`app-prod`): Optimized production deployment with resource limits and security hardening
- **Database service** (`db`): PostgreSQL 16 with persistent storage and health checks
- **Networking**: Isolated network for secure service communication
- **Volumes**: Persistent storage for database data

## Create environment configuration

Create a `.env` file to configure your application settings:

```console
$ cp .env.example .env
```

Update the `.env` file with your preferred settings:

```env
# Application Configuration
NODE_ENV=development
APP_PORT=3000
VITE_PORT=5173
DEBUG_PORT=9229

# Production Configuration
PROD_PORT=8080
PROD_MEMORY_LIMIT=2G
PROD_CPU_LIMIT=1.0
PROD_MEMORY_RESERVATION=512M
PROD_CPU_RESERVATION=0.25

# Database Configuration
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=todoapp
POSTGRES_USER=todoapp
POSTGRES_PASSWORD=todoapp_password
DB_PORT=5432

# Security Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## Build the Docker image

The default Dockerfile generated by `docker init` provides a reliable baseline for standard Node.js applications. However, since this project is a full-stack TypeScript application that includes both a backend API and frontend React components, the Dockerfile should be customized to better support and optimize this specific architecture.

### Review the generated files

In the following step, you’ll improve the Dockerfile and configuration files by following best practices:

- Use multi-stage builds to keep the final image clean and small
- Improve performance and security by only including what’s needed

These updates make your app easier to deploy and faster to load.

> Note
>
> A `Dockerfile` is a plain text file that contains step-by-step instructions to build a Docker image. It automates packaging your application along with its dependencies and runtime environment.
> For full details, see the
> [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

### Step 1: Configure the Dockerfile

Before creating a Dockerfile, you need to choose a base image. You can either use the [Node.js Official Image](https://hub.docker.com/_/node) or a Docker Hardened Image (DHI) from the [Hardened Image catalog](https://hub.docker.com/hardened-images/catalog).

Choosing DHI offers the advantage of a production-ready image that is lightweight and secure. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

> Important
>
> This guide uses a stable Node.js LTS image tag that is considered secure when the guide is written. Because new releases and security patches are published regularly, the tag shown here may no longer be the safest option when you follow the guide. Always review the latest available image tags and select a secure, up-to-date version before building or deploying your application.
>
>
>
> Official Node.js Docker Images: [https://hub.docker.com/_/node](https://hub.docker.com/_/node)

Docker Hardened Images (DHIs) are available for Node.js on [Docker Hub](https://hub.docker.com/hardened-images/catalog/dhi/node). Unlike using the Docker Official Image, you must first mirror the Node.js image into your organization and then use it as your base image. Follow the instructions in the
[DHI quickstart](https://docs.docker.com/dhi/get-started/) to create a mirrored repository for Node.js.

Mirrored repositories must start with `dhi-`, for example: `FROM <your-namespace>/dhi-node:<tag>`. In the following Dockerfile, the `FROM` instruction uses `<your-namespace>/dhi-node:24-alpine3.22-dev` as the base image.

```dockerfile
# ========================================
# Optimized Multi-Stage Dockerfile
# Node.js TypeScript Application (Using DHI)
# ========================================

FROM <your-namespace>/dhi-node:24-alpine3.22-dev AS base

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# Dependencies Stage
# ========================================
FROM base AS deps

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Build Dependencies Stage
# ========================================
FROM base AS build-deps

# Copy package files
COPY package*.json ./

# Install all dependencies with build optimizations
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# Create necessary directories and set permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# Build Stage
# ========================================
FROM build-deps AS build

# Copy only necessary files for building (respects .dockerignore)
COPY --chown=nodejs:nodejs . .

# Build the application
RUN npm run build

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Development Stage
# ========================================
FROM build-deps AS development

# Set environment
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# Copy source files
COPY . .

# Ensure all directories have proper permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# Switch to non-root user
USER nodejs

# Expose ports
EXPOSE 3000 5173 9229

# Start development server
CMD ["npm", "run", "dev:docker"]

# ========================================
# Production Stage
# ========================================
FROM <your-namespace>/dhi-node:24-alpine3.22-dev AS production

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# Set optimized environment variables
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# Copy production dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./
# Copy built application from build stage
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist

# Switch to non-root user for security
USER nodejs

# Expose port
EXPOSE 3000

# Start production server
CMD ["node", "dist/server.js"]

# ========================================
# Test Stage
# ========================================
FROM build-deps AS test

# Set environment
ENV NODE_ENV=test \
    CI=true

# Copy source files
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Run tests with coverage
CMD ["npm", "run", "test:coverage"]
```

Now you need to create a production-ready multi-stage Dockerfile. Replace the generated Dockerfile with the following optimized configuration:

```dockerfile
# ========================================
# Optimized Multi-Stage Dockerfile
# Node.js TypeScript Application
# ========================================

ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS base

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# Dependencies Stage
# ========================================
FROM base AS deps

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Build Dependencies Stage
# ========================================
FROM base AS build-deps

# Copy package files
COPY package*.json ./

# Install all dependencies with build optimizations
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# Create necessary directories and set permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# Build Stage
# ========================================
FROM build-deps AS build

# Copy only necessary files for building (respects .dockerignore)
COPY --chown=nodejs:nodejs . .

# Build the application
RUN npm run build

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Development Stage
# ========================================
FROM build-deps AS development

# Set environment
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# Copy source files
COPY . .

# Ensure all directories have proper permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# Switch to non-root user
USER nodejs

# Expose ports
EXPOSE 3000 5173 9229

# Start development server
CMD ["npm", "run", "dev:docker"]

# ========================================
# Production Stage
# ========================================
ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS production

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# Set optimized environment variables
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# Copy production dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./
# Copy built application from build stage
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist

# Switch to non-root user for security
USER nodejs

# Expose port
EXPOSE 3000

# Start production server
CMD ["node", "dist/server.js"]

# ========================================
# Test Stage
# ========================================
FROM build-deps AS test

# Set environment
ENV NODE_ENV=test \
    CI=true

# Copy source files
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Run tests with coverage
CMD ["npm", "run", "test:coverage"]
```

Key features of this Dockerfile:

- Multi-stage structure — Separate stages for dependencies, build, development, production, and testing to keep each phase clean and efficient.
- Lean production image — Optimized layering reduces size and keeps only what’s required to run the app.
- Security-minded setup — Uses a dedicated non-root user and excludes unnecessary packages.
- Performance-friendly design — Effective use of caching and well-structured layers for faster builds.
- Clean runtime environment — Removes files not needed in production, such as docs, tests, and build caches.
- Straightforward port usage — The app runs on port 3000 internally, exposed externally as port 8080.
- Memory-optimized runtime — Node.js is configured to run with a smaller memory limit than the default.

### Step 2: Configure the .dockerignore file

The `.dockerignore` file tells Docker which files and folders to exclude when building the image.

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

Copy and replace the contents of your existing `.dockerignore` with the optimized configuration:

```dockerignore
# Optimized .dockerignore for Node.js + React Todo App
# Based on actual project structure

# Version control
.git/
.github/
.gitignore

# Dependencies (installed in container)
node_modules/

# Build outputs (built in container)
dist/

# Environment files
.env*

# Development files
.vscode/
*.log
coverage/
.eslintcache

# OS files
.DS_Store
Thumbs.db

# Documentation
*.md
docs/

# Deployment configs
compose.yml
Taskfile.yml
nodejs-sample-kubernetes.yaml

# Non-essential configs (keep build configs)
*.config.js
!vite.config.ts
!esbuild.config.js
!tailwind.config.js
!postcss.config.js
!tsconfig.json
```

### Step 3: Build the Node.js application image

After creating all the configuration files, your project directory should now contain all necessary Docker configuration files:

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yml
│ └── README.Docker.md
```

Now you can build the Docker image for your Node.js application.

> Note
>
> The `docker build` command packages your application into an image using the instructions in the Dockerfile. It includes all necessary files from the current directory (called the
> [build context](https://docs.docker.com/build/concepts/context/#what-is-a-build-context)).

Run the following command from the root of your project:

```console
$ docker build --target production --tag docker-nodejs-sample .
```

What this command does:

- Uses the Dockerfile in the current directory (.)
- Targets the production stage of the multi-stage build
- Packages the application and its dependencies into a Docker image
- Tags the image as docker-nodejs-sample so you can reference it later

#### Step 4: View local images

After building your Docker image, you can check which images are available on your local machine using either the Docker CLI or
[Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/). Since you're already working in the terminal, use the Docker CLI.

To list all locally available Docker images, run the following command:

```console
$ docker images
```

Example Output:

```shell
REPOSITORY               TAG              IMAGE ID       CREATED         SIZE
docker-nodejs-sample     latest           423525528038   14 seconds ago  237.46MB
```

This output provides key details about your images:

- **Repository** – The name assigned to the image.
- **Tag** – A version label that helps identify different builds (e.g., latest).
- **Image ID** – A unique identifier for the image.
- **Created** – The timestamp indicating when the image was built.
- **Size** – The total disk space used by the image.

If the build was successful, you should see `docker-nodejs-sample` image listed.

---

## Run the containerized application

In the previous step, you created a Dockerfile for your Node.js application and built a Docker image using the docker build command. Now it’s time to run that image in a container and verify that your application works as expected.

Inside the `docker-nodejs-sample` directory, run the following command in a terminal.

```console
$ docker compose up app-dev --build
```

The development application will start with both servers:

- **API Server**: [http://localhost:3000](http://localhost:3000) - Express.js backend with REST API
- **Frontend**: [http://localhost:5173](http://localhost:5173) - Vite dev server with React frontend
- **Health Check**: [http://localhost:3000/health](http://localhost:3000/health) - Application health status

For production deployment, you can use:

```console
$ docker compose up app-prod --build
```

Which serves the full-stack app at [http://localhost:8080](http://localhost:8080) with the Express server running on port 3000 internally, mapped to port 8080 externally.

You should see a modern Todo List application with React 19 and a fully functional REST API.

Press `CTRL + C` in the terminal to stop your application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d` option. Inside the `docker-nodejs-sample` directory, run the following command in a terminal.

```console
$ docker compose up app-dev --build -d
```

Open a browser and view the application at [http://localhost:3000](http://localhost:3000) (API) or [http://localhost:5173](http://localhost:5173) (frontend). You should see the Todo application running.

To confirm that the container is running, use `docker ps` command:

```console
$ docker ps
```

This will list all active containers along with their ports, names, and status. Look for a container exposing ports 3000, 5173, and 9229 for the development app.

Example Output:

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                 PORTS                                                                                                                                   NAMES
93f3faee32c3   docker-nodejs-sample-app-dev   "docker-entrypoint.s…"   33 seconds ago   Up 31 seconds          0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp, 0.0.0.0:5173->5173/tcp, [::]:5173->5173/tcp, 0.0.0.0:9230->9229/tcp, [::]:9230->9229/tcp   todoapp-dev
```

### Run different profiles

You can run different configurations using Docker Compose profiles:

```console
# Run production
$ docker compose up app-prod -d

# Run tests
$ docker compose up app-test -d
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

In this guide, you learned how to containerize, build, and run a Node.js application using Docker. By following best practices, you created a secure, optimized, and production-ready setup.

What you accomplished:

- Initialized your project using `docker init` to scaffold essential Docker configuration files.
- Created a `compose.yml` file with development, production, and database services.
- Set up environment configuration with a `.env` file for flexible deployment settings.
- Replaced the default `Dockerfile` with a multi-stage build optimized for TypeScript and React.
- Replaced the default `.dockerignore` file to exclude unnecessary files and keep the image clean and efficient.
- Built your Docker image using `docker build`.
- Ran the container using `docker compose up`, both in the foreground and in detached mode.
- Verified that the app was running by visiting [http://localhost:8080](http://localhost:8080) (production) or [http://localhost:3000](http://localhost:3000) (development).
- Learned how to stop the containerized application using `docker compose down`.

You now have a fully containerized Node.js application, running in a Docker container, and ready for deployment across any environment with confidence and consistency.

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

With your Node.js application now containerized, you're ready to move on to the next step.

In the next section, you'll learn how to develop your application using Docker containers, enabling a consistent, isolated, and reproducible development environment across any machine.

---

# Deploy your Node.js application

> Learn how to deploy your containerized Node.js application to Kubernetes with production-ready configuration

# Deploy your Node.js application

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize a Node.js application](https://docs.docker.com/guides/nodejs/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to deploy your containerized Node.js application to Kubernetes using Docker Desktop. This deployment uses production-ready configurations including security hardening, auto-scaling, persistent storage, and high availability features.

You'll deploy a complete stack including:

- Node.js Todo application with 3 replicas.
- PostgreSQL database with persistent storage.
- Auto-scaling based on CPU and memory usage.
- Ingress configuration for external access.
- Security settings.

## Create a Kubernetes deployment file

Create a new file called `nodejs-sample-kubernetes.yaml` in your project root:

```yaml
# ========================================
# Node.js Todo App - Kubernetes Deployment
# ========================================

apiVersion: v1
kind: Namespace
metadata:
  name: todoapp
  labels:
    app: todoapp

---
# ========================================
# ConfigMap for Application Configuration
# ========================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: todoapp-config
  namespace: todoapp
data:
  NODE_ENV: 'production'
  ALLOWED_ORIGINS: 'https://yourdomain.com'
  POSTGRES_HOST: 'todoapp-postgres'
  POSTGRES_PORT: '5432'
  POSTGRES_DB: 'todoapp'
  POSTGRES_USER: 'todoapp'

---
# ========================================
# Secret for Database Credentials
# ========================================
apiVersion: v1
kind: Secret
metadata:
  name: todoapp-secrets
  namespace: todoapp
type: Opaque
data:
  postgres-password: dG9kb2FwcF9wYXNzd29yZA== # base64 encoded "todoapp_password"

---
# ========================================
# PostgreSQL PersistentVolumeClaim
# ========================================
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: todoapp
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard

---
# ========================================
# PostgreSQL Deployment
# ========================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todoapp-postgres
  namespace: todoapp
  labels:
    app: todoapp-postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todoapp-postgres
  template:
    metadata:
      labels:
        app: todoapp-postgres
    spec:
      containers:
        - name: postgres
          image: postgres:18-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: todoapp-secrets
                  key: postgres-password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - todoapp
                - -d
                - todoapp
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - todoapp
                - -d
                - todoapp
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
# ========================================
# PostgreSQL Service
# ========================================
apiVersion: v1
kind: Service
metadata:
  name: todoapp-postgres
  namespace: todoapp
  labels:
    app: todoapp-postgres
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
      protocol: TCP
      name: postgres
  selector:
    app: todoapp-postgres

---
# ========================================
# Application Deployment
# ========================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todoapp-deployment
  namespace: todoapp
  labels:
    app: todoapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todoapp
  template:
    metadata:
      labels:
        app: todoapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
      containers:
        - name: todoapp
          image: ghcr.io/your-username/docker-nodejs-sample:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              name: http
              protocol: TCP
          env:
            - name: NODE_ENV
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: NODE_ENV
            - name: ALLOWED_ORIGINS
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: ALLOWED_ORIGINS
            - name: POSTGRES_HOST
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_HOST
            - name: POSTGRES_PORT
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_PORT
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: todoapp-secrets
                  key: postgres-password
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              memory: '256Mi'
              cpu: '250m'
            limits:
              memory: '512Mi'
              cpu: '500m'
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

---
# ========================================
# Application Service
# ========================================
apiVersion: v1
kind: Service
metadata:
  name: todoapp-service
  namespace: todoapp
  labels:
    app: todoapp
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
  selector:
    app: todoapp

---
# ========================================
# Ingress for External Access
# ========================================
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todoapp-ingress
  namespace: todoapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
spec:
  tls:
    - hosts:
        - yourdomain.com
      secretName: todoapp-tls
  rules:
    - host: yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: todoapp-service
                port:
                  number: 80

---
# ========================================
# HorizontalPodAutoscaler
# ========================================
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todoapp-hpa
  namespace: todoapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todoapp-deployment
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

---
# ========================================
# PodDisruptionBudget
# ========================================
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: todoapp-pdb
  namespace: todoapp
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: todoapp
```

## Configure the deployment

Before deploying, you need to customize the deployment file for your environment:

1. **Image reference**: Replace `your-username` with your GitHub username or Docker Hub username:
  ```yaml
  image: ghcr.io/your-username/docker-nodejs-sample:latest
  ```
2. **Domain name**: Replace `yourdomain.com` with your actual domain in two places:
  ```yaml
  # In ConfigMap
  ALLOWED_ORIGINS: "https://yourdomain.com"
  # In Ingress
  - host: yourdomain.com
  ```
3. **Database password** (optional): The default password is already base64 encoded. To change it:
  ```console
  $ echo -n "your-new-password" | base64
  ```
  Then update the Secret:
  ```yaml
  data:
    postgres-password: <your-base64-encoded-password>
  ```
4. **Storage class**: Adjust based on your cluster (current: `standard`)

## Understanding the deployment

The deployment file creates a complete application stack with multiple components working together.

### Architecture

The deployment includes:

- **Node.js application**: Runs 3 replicas of your containerized Todo app
- **PostgreSQL database**: Single instance with 10Gi of persistent storage
- **Services**: Kubernetes services handle load balancing across application replicas
- **Ingress**: External access through an ingress controller with SSL/TLS support

### Security

The deployment uses several security features:

- Containers run as a non-root user (UID 1001)
- Read-only root filesystem prevents unauthorized writes
- Linux capabilities are dropped to minimize attack surface
- Sensitive data like database passwords are stored in Kubernetes secrets

### High availability

To keep your application running reliably:

- Three application replicas ensure service continues if one pod fails
- Pod disruption budget maintains at least one available pod during updates
- Rolling updates allow zero-downtime deployments
- Health checks on the `/health` endpoint ensure only healthy pods receive traffic

### Auto-scaling

The Horizontal Pod Autoscaler scales your application based on resource usage:

- Scales between 1 and 5 replicas automatically
- Triggers scaling when CPU usage exceeds 70%
- Triggers scaling when memory usage exceeds 80%
- Resource limits: 256Mi-512Mi memory, 250m-500m CPU per pod

### Data persistence

PostgreSQL data is stored persistently:

- 10Gi persistent volume stores database files
- Database initializes automatically on first startup
- Data persists across pod restarts and updates

## Deploy your application

### Step 1: Deploy to Kubernetes

Deploy your application to the local Kubernetes cluster:

```console
$ kubectl apply -f nodejs-sample-kubernetes.yaml
```

You should see output confirming all resources were created:

```shell
namespace/todoapp created
secret/todoapp-secrets created
configmap/todoapp-config created
persistentvolumeclaim/postgres-pvc created
deployment.apps/todoapp-postgres created
service/todoapp-postgres created
deployment.apps/todoapp-deployment created
service/todoapp-service created
ingress.networking.k8s.io/todoapp-ingress created
poddisruptionbudget.policy/todoapp-pdb created
horizontalpodautoscaler.autoscaling/todoapp-hpa created
```

### Step 2: Verify the deployment

Check that your deployments are running:

```console
$ kubectl get deployments -n todoapp
```

Expected output:

```shell
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
todoapp-deployment   3/3     3            3           30s
todoapp-postgres     1/1     1            1           30s
```

Verify your services are created:

```console
$ kubectl get services -n todoapp
```

Expected output:

```shell
NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
todoapp-service    ClusterIP   10.111.101.229   <none>        80/TCP     45s
todoapp-postgres   ClusterIP   10.111.102.130   <none>        5432/TCP   45s
```

Check that persistent storage is working:

```console
$ kubectl get pvc -n todoapp
```

Expected output:

```shell
NAME           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
postgres-pvc   Bound    pvc-12345678-1234-1234-1234-123456789012   10Gi       RWO            standard       1m
```

### Step 3: Access your application

For local testing, use port forwarding to access your application:

```console
$ kubectl port-forward -n todoapp service/todoapp-service 8080:80
```

Open your browser and visit [http://localhost:8080](http://localhost:8080) to see your Todo application running in Kubernetes.

### Step 4: Test the deployment

Test that your application is working correctly:

1. **Add some todos** through the web interface
2. **Check application pods**:
  ```console
  $ kubectl get pods -n todoapp -l app=todoapp
  ```
3. **View application logs**:
  ```console
  $ kubectl logs -f deployment/todoapp-deployment -n todoapp
  ```
4. **Check database connectivity**:
  ```console
  $ kubectl get pods -n todoapp -l app=todoapp-postgres
  ```
5. **Monitor auto-scaling**:
  ```console
  $ kubectl describe hpa todoapp-hpa -n todoapp
  ```

### Step 5: Clean up

When you're done testing, remove the deployment:

```console
$ kubectl delete -f nodejs-sample-kubernetes.yaml
```

## Summary

You've deployed your containerized Node.js application to Kubernetes. You learned how to:

- Create a comprehensive Kubernetes deployment file with security hardening
- Deploy a multi-tier application (Node.js + PostgreSQL) with persistent storage
- Configure auto-scaling, health checks, and high availability features
- Test and monitor your deployment locally using Docker Desktop's Kubernetes

Your application is now running in a production-like environment with enterprise-grade features including security contexts, resource management, and automatic scaling.

---

## Related resources

Explore official references and best practices to sharpen your Kubernetes deployment workflow:

- [Kubernetes documentation](https://kubernetes.io/docs/home/) – Learn about core concepts, workloads, services, and more.
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/) – Use Docker Desktop's built-in Kubernetes support for local testing and development.
- [kubectlCLI reference](https://kubernetes.io/docs/reference/kubectl/) – Manage Kubernetes clusters from the command line.
- [Kubernetes Deployment resource](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – Understand how to manage and scale applications using Deployments.
- [Kubernetes Service resource](https://kubernetes.io/docs/concepts/services-networking/service/) – Learn how to expose your application to internal and external traffic.
