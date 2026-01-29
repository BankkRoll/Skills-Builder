# Use containers for Node.js development and more

# Use containers for Node.js development

> Learn how to develop your Node.js application locally using containers.

# Use containers for Node.js development

   Table of contents

---

## Prerequisites

Complete [Containerize a Node.js application](https://docs.docker.com/guides/nodejs/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Adding a local database and persisting data
- Configuring your container to run a development environment
- Debugging your containerized application

## Add a local database and persist data

The application uses PostgreSQL for data persistence. Add a database service to your Docker Compose configuration.

### Add database service to Docker Compose

If you haven't already created a `compose.yml` file in the previous section, or if you need to add the database service, update your `compose.yml` file to include the PostgreSQL database service:

```yaml
services:
  # ... existing app services ...

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

### Update your application service

Make sure your application service in `compose.yml` is configured to connect to the database:

compose.yml

```yaml
services:
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

volumes:
  postgres_data:
    name: todoapp-postgres-data
    driver: local

networks:
  todoapp-network:
    name: todoapp-network
    driver: bridge
```

1. The PostgreSQL database configuration is handled automatically by the application. The database is created and initialized when the application starts, with data persisted using the `postgres_data` volume.
2. Configure your environment by copying the example file:
  ```console
  $ cp .env.example .env
  ```
  Update the `.env` file with your preferred settings:
  ```env
  # Application Configuration
  NODE_ENV=development
  APP_PORT=3000
  VITE_PORT=5173
  DEBUG_PORT=9230
  # Database Configuration
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  POSTGRES_DB=todoapp
  POSTGRES_USER=todoapp
  POSTGRES_PASSWORD=todoapp_password
  # Security Configuration
  ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
  ```
3. Run the following command to start your application in development mode:
  ```console
  $ docker compose up app-dev --build
  ```
4. Open a browser and verify that the application is running at [http://localhost:5173](http://localhost:5173) for the frontend or [http://localhost:3000](http://localhost:3000) for the API. The React frontend is served by Vite dev server on port 5173, with API calls proxied to the Express server on port 3000.
5. Add some items to the todo list to test data persistence.
6. After adding some items to the todo list, press `CTRL + C` in the terminal to stop your application.
7. Run the application again:
  ```console
  $ docker compose up app-dev
  ```
8. Refresh [http://localhost:5173](http://localhost:5173) in your browser and verify that the todo items persisted, even after the containers were removed and ran again.

## Configure and run a development container

You can use a bind mount to mount your source code into the container. The container can then see the changes you make to the code immediately, as soon as you save a file. This means that you can run processes, like nodemon, in the container that watch for filesystem changes and respond to them. To learn more about bind mounts, see
[Storage overview](https://docs.docker.com/engine/storage/).

In addition to adding a bind mount, you can configure your Dockerfile and `compose.yaml` file to install development dependencies and run development tools.

### Update your Dockerfile for development

Your Dockerfile should be configured as a multi-stage build with separate stages for development, production, and testing. If you followed the previous section, your Dockerfile already includes a development stage that has all development dependencies and runs the application with hot reload enabled.

Here's the development stage from your multi-stage Dockerfile:

Dockerfile

```dockerfile
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
```

The development stage:

- Installs all dependencies including dev dependencies
- Exposes ports for the API server (3000), Vite dev server (5173), and Node.js debugger (9229)
- Runs `npm run dev` which starts both the Express server and Vite dev server concurrently
- Includes health checks for monitoring container status

Next, you'll need to update your Compose file to use the new stage.

### Update your Compose file for development

Update your `compose.yml` file to run the development stage with bind mounts for hot reloading:

compose.yml

```yaml
services:
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
```

Key features of the development configuration:

- **Multi-port exposure**: API server (3000), Vite dev server (5173), and debugger (9229)
- **Comprehensive bind mounts**: Source code, configuration files, and package files for hot reloading
- **Environment variables**: Configurable through `.env` file or defaults
- **PostgreSQL database**: Production-ready database with persistent storage
- **Docker Compose watch**: Automatic file synchronization and container rebuilds
- **Health checks**: Database health monitoring with automatic dependency management

### Run your development container and debug your application

Run the following command to run your application with the development configuration:

```console
$ docker compose up app-dev --build
```

Or with file watching for automatic updates:

```console
$ docker compose up app-dev --watch
```

For local development without Docker:

```console
$ npm run dev:with-db
```

Or start services separately:

```console
$ npm run db:start    # Start PostgreSQL container
$ npm run dev         # Start both server and client
```

### Using Task Runner (alternative)

The project includes a Taskfile.yml for advanced workflows:

```console
# Development
$ task dev              # Start development environment
$ task dev:build        # Build development image
$ task dev:run          # Run development container

# Production
$ task build            # Build production image
$ task run              # Run production container
$ task build-run        # Build and run in one step

# Testing
$ task test             # Run all tests
$ task test:unit        # Run unit tests with coverage
$ task test:lint        # Run linting

# Kubernetes
$ task k8s:deploy       # Deploy to Kubernetes
$ task k8s:status       # Check deployment status
$ task k8s:logs         # View pod logs

# Utilities
$ task clean            # Clean up containers and images
$ task health           # Check application health
$ task logs             # View container logs
```

The application will start with both the Express API server and Vite development server:

- **API Server**: [http://localhost:3000](http://localhost:3000) - Express.js backend with REST API
- **Frontend**: [http://localhost:5173](http://localhost:5173) - Vite dev server with hot module replacement
- **Health Check**: [http://localhost:3000/health](http://localhost:3000/health) - Application health status

Any changes to the application's source files on your local machine will now be immediately reflected in the running container thanks to the bind mounts.

Try making a change to test hot reloading:

1. Open `src/client/components/TodoApp.tsx` in an IDE or text editor.
2. Update the main heading text:
  ```diff
  - <h1 className="text-3xl font-bold text-gray-900 mb-8">
  -   Modern Todo App
  - </h1>
  + <h1 className="text-3xl font-bold text-gray-900 mb-8">
  +   My Todo App
  + </h1>
  ```
3. Save the file and the Vite dev server will automatically reload the page with your changes.

**Debugging support:**

You can connect a debugger to your application on port 9229. The Node.js inspector is enabled with `--inspect=0.0.0.0:9230` in the development script (`dev:server`).

### VS Code debugger setup

1. Create a launch configuration in `.vscode/launch.json`:
  ```json
  {
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Attach to Docker Container",
        "type": "node",
        "request": "attach",
        "port": 9229,
        "address": "localhost",
        "localRoot": "${workspaceFolder}",
        "remoteRoot": "/app",
        "protocol": "inspector",
        "restart": true,
        "sourceMaps": true,
        "skipFiles": ["<node_internals>/**"]
      }
    ]
  }
  ```
2. Start your development container:
  ```console
  docker compose up app-dev --build
  ```
3. Attach the debugger:
  - Open VS Code
  - From the Debug panel (Ctrl/Cmd + Shift + D), select **Attach to Docker Container** from the drop-down
  - Select the green play button or press F5

### Chrome DevTools (alternative)

You can also use Chrome DevTools for debugging:

1. Start your container (if not already running):
  ```console
  docker compose up app-dev --build
  ```
2. Open Chrome and go to `chrome://inspect`.
3. From the **Configure** option, add:
  ```text
  localhost:9229
  ```
4. When your Node.js target appears, select **inspect**.

### Debugging configuration details

The debugger configuration:

- **Container port**: 9230 (internal debugger port)
- **Host port**: 9229 (mapped external port)
- **Script**: `tsx watch --inspect=0.0.0.0:9230 src/server/index.ts`

The debugger listens on all interfaces (`0.0.0.0`) inside the container on port 9230 and is accessible on port 9229 from your host machine.

### Troubleshooting debugger connection

If the debugger doesn't connect:

1. Check if the container is running:
  ```console
  docker ps
  ```
2. Check if the port is exposed:
  ```console
  docker port todoapp-dev
  ```
3. Check container logs:
  ```console
  docker compose logs app-dev
  ```
  You should see a message like:
  ```text
  Debugger listening on ws://0.0.0.0:9230/...
  ```

Now you can set breakpoints in your TypeScript source files and debug your containerized Node.js application.

For more details about Node.js debugging, see the [Node.js documentation](https://nodejs.org/en/docs/guides/debugging-getting-started).

## Summary

You've set up your Compose file with a PostgreSQL database and data persistence. You also created a multi-stage Dockerfile and configured bind mounts for development.

Related information:

- [Volumes top-level element](https://docs.docker.com/reference/compose-file/volumes/)
- [Services top-level element](https://docs.docker.com/reference/compose-file/services/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll learn how to run unit tests using Docker.

---

# Run Node.js tests in a container

> Learn how to run your Node.js tests in a container.

# Run Node.js tests in a container

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a Node.js application](https://docs.docker.com/guides/nodejs/containerize/).

## Overview

Testing is a core part of building reliable software. Whether you're writing unit tests, integration tests, or end-to-end tests, running them consistently across environments matters. Docker makes this easy by giving you the same setup locally, in CI/CD, and during image builds.

## Run tests when developing locally

The sample application uses Vitest for testing, and it already includes tests for React components, custom hooks, API routes, database operations, and utility functions.

### Run tests locally (without Docker)

```console
$ npm run test
```

### Add test service to Docker Compose

To run tests in a containerized environment, you need to add a dedicated test service to your `compose.yml` file. Add the following service configuration:

```yaml
services:
  # ... existing services ...

  # ========================================
  # Test Service
  # ========================================
  app-test:
    build:
      context: .
      dockerfile: Dockerfile
      target: test
    container_name: todoapp-test
    environment:
      NODE_ENV: test
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: todoapp_test
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
    depends_on:
      db:
        condition: service_healthy
    command: ['npm', 'run', 'test:coverage']
    networks:
      - todoapp-network
    profiles:
      - test
```

This test service configuration:

- **Builds from test stage**: Uses the `test` target from your multi-stage Dockerfile
- **Isolated test database**: Uses a separate `todoapp_test` database for testing
- **Profile-based**: Uses the `test` profile so it only runs when explicitly requested
- **Health dependency**: Waits for the database to be healthy before starting tests

### Run tests in a container

You can run tests using the dedicated test service:

```console
$ docker compose up app-test --build
```

Or run tests against the development service:

```console
$ docker compose run --rm app-dev npm run test
```

For a one-off test run with coverage:

```console
$ docker compose run --rm app-dev npm run test:coverage
```

### Run tests with coverage

To generate a coverage report:

```console
$ npm run test:coverage
```

You should see output like the following:

```console
> docker-nodejs-sample@1.0.0 test
> vitest --run

 ✓ src/server/__tests__/routes/todos.test.ts (5 tests) 16ms
 ✓ src/shared/utils/__tests__/validation.test.ts (15 tests) 6ms
 ✓ src/client/components/__tests__/LoadingSpinner.test.tsx (8 tests) 67ms
 ✓ src/server/database/__tests__/postgres.test.ts (13 tests) 136ms
 ✓ src/client/components/__tests__/ErrorMessage.test.tsx (8 tests) 127ms
 ✓ src/client/components/__tests__/TodoList.test.tsx (8 tests) 147ms
 ✓ src/client/components/__tests__/TodoItem.test.tsx (8 tests) 218ms
 ✓ src/client/__tests__/App.test.tsx (13 tests) 259ms
 ✓ src/client/components/__tests__/AddTodoForm.test.tsx (12 tests) 323ms
 ✓ src/client/hooks/__tests__/useTodos.test.ts (11 tests) 569ms

 Test Files  9 passed (9)
      Tests  88 passed (88)
   Start at  20:57:19
   Duration  4.41s (transform 1.79s, setup 2.66s, collect 5.38s, tests 4.61s, environment 14.07s, prepare 4.34s)
```

### Test structure

The test suite covers:

- **Client Components** (`src/client/components/__tests__/`): React component testing with React Testing Library
- **Custom Hooks** (`src/client/hooks/__tests__/`): React hooks testing with proper mocking
- **Server Routes** (`src/server/__tests__/routes/`): API endpoint testing
- **Database Layer** (`src/server/database/__tests__/`): PostgreSQL database operations testing
- **Utility Functions** (`src/shared/utils/__tests__/`): Validation and helper function testing
- **Integration Tests** (`src/client/__tests__/`): Full application integration testing

## Run tests when building

To run tests during the Docker build process, you need to add a dedicated test stage to your Dockerfile. If you haven't already added this stage, add the following to your multi-stage Dockerfile:

```dockerfile
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

This test stage:

- **Test environment**: Sets `NODE_ENV=test` and `CI=true` for proper test execution
- **Non-root user**: Runs tests as the `nodejs` user for security
- **Flexible execution**: Uses `CMD` instead of `RUN` to allow running tests during build or as a separate container
- **Coverage support**: Configured to run tests with coverage reporting

### Build and run tests during image build

To build an image that runs tests during the build process, you can create a custom Dockerfile or modify the existing one temporarily:

```console
$ docker build --target test -t node-docker-image-test .
```

### Run tests in a dedicated test container

The recommended approach is to use the test service defined in `compose.yml`:

```console
$ docker compose --profile test up app-test --build
```

Or run it as a one-off container:

```console
$ docker compose run --rm app-test
```

### Run tests with coverage in CI/CD

For continuous integration, you can run tests with coverage:

```console
$ docker build --target test --progress=plain --no-cache -t test-image .
$ docker run --rm test-image npm run test:coverage
```

You should see output containing the following:

```console
✓ src/server/__tests__/routes/todos.test.ts (5 tests) 16ms
 ✓ src/shared/utils/__tests__/validation.test.ts (15 tests) 6ms
 ✓ src/client/components/__tests__/LoadingSpinner.test.tsx (8 tests) 67ms
 ✓ src/server/database/__tests__/postgres.test.ts (13 tests) 136ms
 ✓ src/client/components/__tests__/ErrorMessage.test.tsx (8 tests) 127ms
 ✓ src/client/components/__tests__/TodoList.test.tsx (8 tests) 147ms
 ✓ src/client/components/__tests__/TodoItem.test.tsx (8 tests) 218ms
 ✓ src/client/__tests__/App.test.tsx (13 tests) 259ms
 ✓ src/client/components/__tests__/AddTodoForm.test.tsx (12 tests) 323ms
 ✓ src/client/hooks/__tests__/useTodos.test.ts (11 tests) 569ms

 Test Files  9 passed (9)
      Tests  88 passed (88)
   Start at  20:57:19
   Duration  4.41s (transform 1.79s, setup 2.66s, collect 5.38s, tests 4.61s, environment 14.07s, prepare 4.34s)
```

## Summary

In this section, you learned how to run tests when developing locally using Docker Compose and how to run tests when building your image.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) – Understand all Dockerfile instructions and syntax.
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
- [Compose file reference](https://docs.docker.com/compose/compose-file/) – Learn the full syntax and options available for configuring services in `compose.yaml`.
- [docker compose runCLI reference](https://docs.docker.com/reference/cli/docker/compose/run/) – Run one-off commands in a service container.

## Next steps

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions.

---

# Node.js language

> Containerize and develop Node.js apps using Docker

# Node.js language-specific guide

Table of contents

---

[Node.js](https://nodejs.org/en) is a JavaScript runtime for building web applications. This guide shows you how to containerize a TypeScript Node.js application with a React frontend and PostgreSQL database.

The sample application is a modern full-stack Todo application featuring:

- **Backend**: Express.js with TypeScript, PostgreSQL database, and RESTful API
- **Frontend**: React.js with Vite and Tailwind CSS 4

> **Acknowledgment**
>
>
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide. As a Docker Captain and experienced Full-stack engineer, his expertise in Docker, DevOps, and modern web development has made this resource invaluable for the community, helping developers navigate and optimize their Docker workflows.

---

## What will you learn?

In this guide, you will learn how to:

- Containerize and run a Node.js application using Docker.
- Run tests inside a Docker container.
- Set up a development container environment.
- Configure GitHub Actions for CI/CD with Docker.
- Deploy your Dockerized Node.js app to Kubernetes.

To begin, you’ll start by containerizing an existing Node.js application.

---

## Prerequisites

Before you begin, make sure you're familiar with the following:

- Basic understanding of [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and [TypeScript](https://www.typescriptlang.org/).
- Basic knowledge of [Node.js](https://nodejs.org/en), [npm](https://docs.npmjs.com/about-npm), and [React](https://react.dev/) for modern web development.
- Understanding of Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the
  [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.
- Familiarity with [Express.js](https://expressjs.com/) for backend API development.

Once you've completed the Node.js getting started modules, you’ll be ready to containerize your own Node.js application using the examples and instructions provided in this guide.

## Modules

1. [Containerize](https://docs.docker.com/guides/nodejs/containerize/)
  Learn how to containerize a Node.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.
2. [Develop your app](https://docs.docker.com/guides/nodejs/develop/)
  Learn how to develop your Node.js application locally using containers.
3. [Run your tests](https://docs.docker.com/guides/nodejs/run-tests/)
  Learn how to run your Node.js tests in a container.
4. [Automate your builds with GitHub Actions](https://docs.docker.com/guides/nodejs/configure-github-actions/)
  Learn how to configure CI/CD using GitHub Actions for your Node.js application.
5. [Deploy your app](https://docs.docker.com/guides/nodejs/deploy/)
  Learn how to deploy your containerized Node.js application to Kubernetes with production-ready configuration

---

# Instrumenting a JavaScript App with OpenTelemetry

> Learn how to instrument a JavaScript application using OpenTelemetry in a Dockerized environment.

# Instrumenting a JavaScript App with OpenTelemetry

   Table of contents

---

OpenTelemetry (OTel) is an open-source observability framework that provides a set of APIs, SDKs, and tools for collecting telemetry data, such as metrics, logs, and traces, from applications. With OpenTelemetry, developers can obtain valuable insights into how their services perform in production or during local development.

A key component of OpenTelemetry is the OpenTelemetry Protocol (OTLP) a general-purpose, vendor-agnostic protocol designed to transmit telemetry data efficiently and reliably. OTLP supports multiple data types (traces, metrics, logs) over HTTP or gRPC, making it the default and recommended protocol for communication between instrumented applications, the OpenTelemetry Collector, and backends such as Jaeger or Prometheus.

This guide walks you through how to instrument a simple Node.js application with OpenTelemetry and run both the app and a collector using Docker. This setup is ideal for local development and testing observability before integrating with external observability platforms like Prometheus, Jaeger, or Grafana.

In this guide, you'll learn how to:

- How to set up OpenTelemetry in a Node.js app.
- How to run an OpenTelemetry Collector in Docker.
- How to visualize traces with Jaeger.
- How to use Docker Compose to manage the full observability stack.

## Using OpenTelemetry with Docker

The [Docker Official Image for OpenTelemetry](https://hub.docker.com/r/otel/opentelemetry-collector-contrib) provides a convenient way to deploy and manage Dex instances. OpenTelemetry is available for various CPU architectures, including amd64, armv7, and arm64, ensuring compatibility with different devices and platforms. Same for the [Jaeger docekr image](https://hub.docker.com/r/jaegertracing/jaeger).

## Prerequisites

[Docker Compose](https://docs.docker.com/compose/): Recommended for managing multi-container Docker applications.

Basic knowledge of Node.js and Docker.

## Project Structure

Create the project directory:

```bash
mkdir otel-js-app
cd otel-js-app
```

```bash
otel-js-app/
├── docker-compose.yaml
├── collector-config.yaml
├── app/
│   ├── package.json
│   ├── app.js
│   └── tracer.js
```

## Create a Simple Node.js App

Initialize a basic Node.js app:

```bash
mkdir app && cd app
npm init -y
npm install express @opentelemetry/api @opentelemetry/sdk-node \
            @opentelemetry/auto-instrumentations-node \
            @opentelemetry/exporter-trace-otlp-http
```

Now, add the application logic:

```js
// app/app.js
const express = require('express');
require('./tracer'); // Initialize OpenTelemetry

const app = express();

app.get('/', (req, res) => {
  res.send('Hello from OpenTelemetry demo app!');
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`App listening at http://localhost:${PORT}`);
});
```

## Configure OpenTelemetry Tracing

Create the tracer configuration file:

```js
// app/tracer.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://collector:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

## Configure the OpenTelemetry Collector

Create a collector-config.yaml file at the root:

```yaml
# collector-config.yaml
receivers:
  otlp:
    protocols:
      http:

exporters:
  logging:
    loglevel: debug
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging, jaeger]
```

## Add Docker Compose Configuration

Create the `docker-compose.yaml` file:

```yaml
version: '3.9'

services:
  app:
    build: ./app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      - collector

  collector:
    image: otel/opentelemetry-collector:latest
    volumes:
      - ./collector-config.yaml:/etc/otelcol/config.yaml
    command: ["--config=/etc/otelcol/config.yaml"]
    ports:
      - "4318:4318" # OTLP

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "14250:14250" # Collector gRPC
```

Now, add the `Dockerfile` inside the `app/` folder:

```dockerfile
# app/Dockerfile
FROM node:18

WORKDIR /usr/src/app
COPY . .
RUN npm install

CMD ["node", "app.js"]
```

## Start the Stack

Start all services with Docker Compose:

```bash
docker compose up --build
```

Once the services are running:

Visit your app at [http://localhost:3000](http://localhost:3000)

View traces at [http://localhost:16686](http://localhost:16686) in the Jaeger UI

## Verify Traces in Jaeger

After visiting your app's root endpoint, open Jaeger’s UI, search for the service (default is usually `unknown_service` unless explicitly named), and check the traces.

You should see spans for the HTTP request, middleware, and auto-instrumented libraries.

## Conclusion

You now have a fully functional OpenTelemetry setup using Docker Compose. You've instrumented a basic JavaScript app to export traces and visualized them using Jaeger. This architecture is extendable for more complex applications and observability pipelines using Prometheus, Grafana, or cloud-native exporters.

For advanced topics such as custom span creation, metrics, and logs, consult the OpenTelemetry JavaScript docs.

---

# Deployment and orchestration

> Get oriented on some basics of Docker and install Docker Desktop.

# Deployment and orchestration

   Table of contents

---

Containerization provides an opportunity to move and scale applications to
clouds and data centers. Containers effectively guarantee that those applications run the
same way anywhere, allowing you to quickly and easily take advantage of all
these environments. Additionally, as you scale your applications up, you need some
tooling to help automate the maintenance of those applications, enable the
replacement of failed containers automatically, and manage the roll-out of
updates and reconfigurations of those containers during their lifecycle.

Tools to manage, scale, and maintain containerized applications are called
orchestrators. Two of the most popular orchestration tools are Kubernetes and
Docker Swarm. Docker Desktop provides development environments for both of these
orchestrators.

The advanced modules teach you how to:

1. [Set up and use a Kubernetes environment on your development machine](https://docs.docker.com/guides/kube-deploy/)
2. [Set up and use a Swarm environment on your development machine](https://docs.docker.com/guides/swarm-deploy/)

## Turn on Kubernetes

Docker Desktop sets up Kubernetes for you quickly and easily. Follow the setup and validation instructions appropriate for your operating system:

### Mac

1. From the Docker Dashboard, navigate to **Settings**, and select the **Kubernetes** tab.
2. Select the checkbox labeled **Enable Kubernetes**, and select **Apply**. Docker Desktop automatically sets up Kubernetes for you. You'll know that Kubernetes has been successfully enabled when you see a green light beside 'Kubernetes *running*' in **Settings**.
3. To confirm that Kubernetes is up and running, create a text file called `pod.yaml` with the following content:
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: demo
  spec:
    containers:
      - name: testpod
        image: alpine:latest
        command: ["ping", "8.8.8.8"]
  ```
  This describes a pod with a single container, isolating a simple ping to 8.8.8.8.
4. In a terminal, navigate to where you created `pod.yaml` and create your pod:
  ```console
  $ kubectl apply -f pod.yaml
  ```
5. Check that your pod is up and running:
  ```console
  $ kubectl get pods
  ```
  You should see something like:
  ```shell
  NAME      READY     STATUS    RESTARTS   AGE
  demo      1/1       Running   0          4s
  ```
6. Check that you get the logs you'd expect for a ping process:
  ```console
  $ kubectl logs demo
  ```
  You should see the output of a healthy ping process:
  ```shell
  PING 8.8.8.8 (8.8.8.8): 56 data bytes
  64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
  64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
  64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
  ...
  ```
7. Finally, tear down your test pod:
  ```console
  $ kubectl delete -f pod.yaml
  ```

### Windows

1. From the Docker Dashboard, navigate to **Settings**, and select the **Kubernetes** tab.
2. Select the checkbox labeled **Enable Kubernetes**, and select **Apply**. Docker Desktop automatically sets up Kubernetes for you. You'll know that Kubernetes has been successfully enabled when you see a green light beside 'Kubernetes *running*' in the **Settings** menu.
3. To confirm that Kubernetes is up and running, create a text file called `pod.yaml` with the following content:
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: demo
  spec:
    containers:
      - name: testpod
        image: alpine:latest
        command: ["ping", "8.8.8.8"]
  ```
  This describes a pod with a single container, isolating a simple ping to 8.8.8.8.
4. In PowerShell, navigate to where you created `pod.yaml` and create your pod:
  ```console
  $ kubectl apply -f pod.yaml
  ```
5. Check that your pod is up and running:
  ```console
  $ kubectl get pods
  ```
  You should see something like:
  ```shell
  NAME      READY     STATUS    RESTARTS   AGE
  demo      1/1       Running   0          4s
  ```
6. Check that you get the logs you'd expect for a ping process:
  ```console
  $ kubectl logs demo
  ```
  You should see the output of a healthy ping process:
  ```shell
  PING 8.8.8.8 (8.8.8.8): 56 data bytes
  64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
  64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
  64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
  ...
  ```
7. Finally, tear down your test pod:
  ```console
  $ kubectl delete -f pod.yaml
  ```

## Enable Docker Swarm

Docker Desktop runs primarily on Docker Engine, which has everything you need to run a Swarm built in. Follow the setup and validation instructions appropriate for your operating system:

### Mac

1. Open a terminal, and initialize Docker Swarm mode:
  ```console
  $ docker swarm init
  ```
  If all goes well, you should see a message similar to the following:
  ```shell
  Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.
  To add a worker to this swarm, run the following command:
      docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377
  To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
  ```
2. Run a simple Docker service that uses an alpine-based filesystem, and isolates a ping to 8.8.8.8:
  ```console
  $ docker service create --name demo alpine:latest ping 8.8.8.8
  ```
3. Check that your service created one running container:
  ```console
  $ docker service ps demo
  ```
  You should see something like:
  ```shell
  ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
  463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
  ```
4. Check that you get the logs you'd expect for a ping process:
  ```console
  $ docker service logs demo
  ```
  You should see the output of a healthy ping process:
  ```shell
  demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
  demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
  demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
  demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
  ...
  ```
5. Finally, tear down your test service:
  ```console
  $ docker service rm demo
  ```

### Windows

1. Open a PowerShell, and initialize Docker Swarm mode:
  ```console
  $ docker swarm init
  ```
  If all goes well, you should see a message similar to the following:
  ```shell
  Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.
  To add a worker to this swarm, run the following command:
      docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377
  To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
  ```
2. Run a simple Docker service that uses an alpine-based filesystem, and isolates a ping to 8.8.8.8:
  ```console
  $ docker service create --name demo alpine:latest ping 8.8.8.8
  ```
3. Check that your service created one running container:
  ```console
  $ docker service ps demo
  ```
  You should see something like:
  ```shell
  ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
  463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
  ```
4. Check that you get the logs you'd expect for a ping process:
  ```console
  $ docker service logs demo
  ```
  You should see the output of a healthy ping process:
  ```shell
  demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
  demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
  demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
  demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
  ...
  ```
5. Finally, tear down your test service:
  ```console
  $ docker service rm demo
  ```

## Conclusion

At this point, you've confirmed that you can run simple containerized workloads in Kubernetes and Swarm. The next step is to write a YAML file that describes how to run and manage these containers.

- [Deploy to Kubernetes](https://docs.docker.com/guides/kube-deploy/)
- [Deploy to Swarm](https://docs.docker.com/guides/swarm-deploy/)

## CLI references

Further documentation for all CLI commands used in this article are available here:

- [kubectl apply](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
- [kubectl get](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)
- [kubectl logs](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [kubectl delete](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)
- [docker swarm init](https://docs.docker.com/reference/cli/docker/swarm/init/)
- [docker service *](https://docs.docker.com/reference/cli/docker/service/)

---

# Visualizing your PostgreSQL databases with pgAdmin

> Visualizing your PostgreSQL databases with pgAdmin

# Visualizing your PostgreSQL databases with pgAdmin

   Table of contents

---

Many applications use PostgreSQL databases in the application stack. However, not all developers are knowledgeable about navigating and working with PostgreSQL databases.

Fortunately, when you use containers in development, it is easy to add additional services to help with troubleshooting and debugging.

The [pgAdmin](https://www.pgadmin.org/) tool is a popular open-source tool designed to help administer and visualize PostgreSQL databases.

In this guide you will learn how to:

1. Add pgAdmin to your application stack
2. Configure pgAdmin to automatically connect to the development database

## Adding pgAdmin to your stack

1. In your `compose.yaml` file, add the `pgadmin` service next to your existing `postgres` service:
  ```yaml
  services:
    postgres:
      image: postgres:18
      environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: secret
        POSTGRES_DB: demo
    pgadmin:
      image: dpage/pgadmin4:9.8
      ports:
        - 5050:80
      environment:
        # Required by pgAdmin
        PGADMIN_DEFAULT_EMAIL: demo@example.com
        PGADMIN_DEFAULT_PASSWORD: secret
        # Don't require the user to login
        PGADMIN_CONFIG_SERVER_MODE: 'False'
        # Don't require a "master" password after logging in
        PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'
  ```
2. Start the Compose stack with the following command:
  ```console
  $ docker compose up
  ```
  After the image is downloaded the container starts, you will see output that looks similar to the following indicating pgAdmin is ready:
  ```console
  pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Starting gunicorn 23.0.0
  pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
  pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Using worker: gthread
  pgadmin-1   | [2025-09-22 15:52:47 +0000] [119] [INFO] Booting worker with pid: 119
  ```
3. Open pgAdmin by going to http://localhost:5050.
4. Once in the admin panel, select the **Add New Server** link to define a new server. Enter the following details:
  - **General** tab:
    - **Name**: `postgres`
  - **Connection** tab:
    - **Host name/address**: `postgres`
    - **Username**: `postgres`
    - **Password**: `secret`
    - Enable the **Save password?** field
  > Important
  >
  > These connection details assume you are using the previous Compose file snippet. If you are using an existing Compose file,
  > adjust the connection details as required. The **Host name/address** field should match the name of your postgres service.
5. Select the **Save** button to create the new database.

You now have pgAdmin setup and connected to your containerized database. Feel free to navigate around, view the tables, and explore your database.

## Configuring pgAdmin to auto-connect to the database

Although you have pgAdmin running, it would be nice if you could simply open the app without needing to configure the database connection. Reducing the setup steps would be a great way to make it easier for teammates to get value from this tool.

Fortunately, there is an ability to auto-connect to the database.

> Warning
>
> In order to auto-connect, the database credentials are shared using plaintext files. During local development, this is often acceptable as local data is not real customer data.
> However, if you are using production or sensitive data, this practice is strongly discouraged.

1. First, you need to define the server itself, which pgAdmin does using a `servers.json` file.
  Add the following to your `compose.yaml` file to define a config file for the `servers.json` file:
  ```yaml
  configs:
    pgadmin-servers:
      content: |
        {
          "Servers": {
            "1": {
              "Name": "Local Postgres",
              "Group": "Servers",
              "Host": "postgres",
              "Port": 5432,
              "MaintenanceDB": "postgres",
              "Username": "postgres",
              "PassFile": "/config/pgpass"
            }
          }
        }
  ```
2. The `servers.json` file defines a `PassFile` field, which is a reference to a [postgreSQL password files](https://www.postgresql.org/docs/current/libpq-pgpass.html). These are often referred to as a pgpass file.
  Add the following config to your `compose.yaml` file to define a pgpass file:
  ```yaml
  config:
    pgadmin-pgpass:
      content: |
        postgres:5432:*:postgres:secret
  ```
  This will indicate any connection requests to `postgres:5432` using the username `postgres` should provide a password of `secret`.
3. In your `compose.yaml`, update the `pgadmin` service to inject the config files:
  ```yaml
  services:
    pgadmin:
      ...
      configs:
        - source: pgadmin-pgpass
          target: /config/pgpass
          uid: "5050"
          gid: "5050"
          mode: 0400
        - source: pgadmin-servers
          target: /pgadmin4/servers.json
          mode: 0444
  ```
4. Update the application stack by running `docker compose up` again:
  ```console
  $ docker compose up
  ```
5. Once the application is restarted, open your browser to http://localhost:5050. You should be able to access the database without any logging in or configuration.

## Conclusion

Using containers makes it easy to not only run your application's dependencies, but also additional tools to help with troubleshooting and debugging.

When you add tools, think about the experience and possible friction your teammates might experience and how you might be able to remove it. In this case, you were able to take an extra step to add configuration to automatically configure and connect the databases, saving your teammates valuable time.
