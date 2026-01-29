# Run vue.js tests in a container and more

# Run vue.js tests in a container

> Learn how to run your vue.js tests in a container.

# Run vue.js tests in a container

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize Vue.js application](https://docs.docker.com/guides/vuejs/containerize/).

## Overview

Testing is a critical part of the development process. In this section, you'll learn how to:

- Run unit tests using Vitest inside a Docker container.
- Use Docker Compose to run tests in an isolated, reproducible environment.

You’ll use [Vitest](https://vitest.dev) — a blazing fast test runner designed for Vite — together with [@vue/test-utils](https://test-utils.vuejs.org/) to write unit tests that validate your component logic, props, events, and reactive behavior.

This setup ensures your Vue.js components are tested in an environment that mirrors how users actually interact with your application.

---

## Run tests during development

`docker-vuejs-sample` application includes a sample test file at location:

```console
$ src/components/__tests__/HelloWorld.spec.ts
```

This test uses Vitest and Vue Test Utils to verify the behavior of the HelloWorld component.

---

### Step 1: Update compose.yaml

Add a new service named `vuejs-test` to your `compose.yaml` file. This service allows you to run your test suite in an isolated containerized environment.

| 1234567891011121314151617181920212223242526 | services:vuejs-prod:build:context:.dockerfile:Dockerfileimage:docker-vuejs-sampleports:-"8080:8080"vuejs-dev:build:context:.dockerfile:Dockerfile.devports:-"5173:5173"develop:watch:-action:syncpath:.target:/appvuejs-test:build:context:.dockerfile:Dockerfile.devcommand:["npm","run","test:unit"] |
| --- | --- |

The vuejs-test service reuses the same `Dockerfile.dev` used for [development](https://docs.docker.com/guides/vuejs/develop/) and overrides the default command to run tests with `npm run test`. This setup ensures a consistent test environment that matches your local development configuration.

After completing the previous steps, your project directory should contain the following files:

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### Step 2: Run the tests

To execute your test suite inside the container, run the following command from your project root:

```console
$ docker compose run --rm vuejs-test
```

This command will:

- Start the `vuejs-test` service defined in your `compose.yaml` file.
- Execute the `npm run test` script using the same environment as development.
- Automatically remove the container after the tests complete
  [docker compose run --rm](https://docs.docker.com/engine/reference/commandline/compose_run) command.

You should see output similar to the following:

```shell
Test Files: 1 passed (1)
Tests:      1 passed (1)
Start at:   16:50:55
Duration:   718ms
```

> Note
>
> For more information about Compose commands, see the
> [Compose CLI
> reference](https://docs.docker.com/reference/cli/docker/compose/).

---

## Summary

In this section, you learned how to run unit tests for your Vue.js application inside a Docker container using Vitest and Docker Compose.

What you accomplished:

- Created a `vuejs-test` service in `compose.yaml` to isolate test execution.
- Reused the development `Dockerfile.dev` to ensure consistency between dev and test environments.
- Ran tests inside the container using `docker compose run --rm vuejs-test`.
- Ensured reliable, repeatable testing across environments without depending on your local machine setup.

---

## Related resources

Explore official references and best practices to sharpen your Docker testing workflow:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) – Understand all Dockerfile instructions and syntax.
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
- [Compose file reference](https://docs.docker.com/compose/compose-file/) – Learn the full syntax and options available for configuring services in `compose.yaml`.
- [docker compose runCLI reference](https://docs.docker.com/reference/cli/docker/compose/run/) – Run one-off commands in a service container.

---

## Next steps

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions to automatically build and test your Vue.js application in a containerized environment. This ensures your code is validated on every push or pull request, maintaining consistency and reliability across your development workflow.

---

# Vue.js language

> Containerize and develop Vue.js apps using Docker

# Vue.js language-specific guide

Table of contents

---

The Vue.js language-specific guide shows you how to containerize an Vue.js application using Docker, following best practices for creating efficient, production-ready containers.

[Vue.js](https://vuejs.org/) is a progressive and flexible framework for building modern, interactive web applications. However, as applications scale, managing dependencies, environments, and deployments can become complex. Docker simplifies these challenges by providing a consistent, isolated environment for both development and production.

> **Acknowledgment**
>
>
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide. As a Docker Captain and highly skilled Front-end engineer, Kristiyan brings exceptional expertise in modern web development, Docker, and DevOps. His hands-on approach and clear, actionable guidance make this guide an essential resource for developers aiming to build, optimize, and secure Vue.js applications with Docker.

---

## What will you learn?

In this guide, you will learn how to:

- Containerize and run an Vue.js application using Docker.
- Set up a local development environment for Vue.js inside a container.
- Run tests for your Vue.js application within a Docker container.
- Configure a CI/CD pipeline using GitHub Actions for your containerized app.
- Deploy the containerized Vue.js application to a local Kubernetes cluster for testing and debugging.

You'll start by containerizing an existing Vue.js application and work your way up to production-level deployments.

---

## Prerequisites

Before you begin, ensure you have a working knowledge of:

- Basic understanding of [TypeScript](https://www.typescriptlang.org/) and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
- Familiarity with [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm) for managing dependencies and running scripts.
- Familiarity with [Vue.js](https://vuejs.org/) fundamentals.
- Understanding of core Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the
  [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

Once you've completed the Vue.js getting started modules, you’ll be fully prepared to containerize your own Vue.js application using the detailed examples and best practices outlined in this guide.

## Modules

1. [Containerize](https://docs.docker.com/guides/vuejs/containerize/)
  Learn how to containerize an Vue.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.
2. [Develop your app](https://docs.docker.com/guides/vuejs/develop/)
  Learn how to develop your Vue.js application locally using containers.
3. [Run your tests](https://docs.docker.com/guides/vuejs/run-tests/)
  Learn how to run your vue.js tests in a container.
4. [Automate your builds with GitHub Actions](https://docs.docker.com/guides/vuejs/configure-github-actions/)
  Learn how to configure CI/CD using GitHub Actions for your Vue.js application.
5. [Test your deployment](https://docs.docker.com/guides/vuejs/deploy/)
  Learn how to deploy locally to test and debug your Kubernetes deployment

---

# Mocking API services in development and testing with WireMock

> Mocking API services in development and testing with WireMock

# Mocking API services in development and testing with WireMock

   Table of contents

---

During local development and testing, it's quite common to encounter situations where your app is dependent on the remote APIs. Network issues, rate limits, or even downtime of the API provider can halt your progress. This can significantly hinder your productivity and make testing more challenging. This is where WireMock comes into play.

WireMock is an open-source tool that helps developers to create a mock server that simulates the behavior of real APIs, providing a controlled environment for development and testing.

Imagine you have both an API and a frontend app, and you want to test how the frontend interacts with the API. Using WireMock, you can set up a mock server to simulate the API's responses, allowing you to test the frontend behavior without relying on the actual API. This can be particularly helpful when the API is still under development or when you want to test different scenarios without affecting the actual API. WireMock supports both HTTP and HTTPS protocols and can simulate various response scenarios, including delays, errors, and different HTTP status codes.

In this guide, you'll learn how to:

- Use Docker to launch up a WireMock container.
- Use mock data in the local development without relying on an external API
- Use a Live API in production to fetch real-time weather data from AccuWeather.

## Using WireMock with Docker

The official [Docker image for WireMock](https://hub.docker.com/r/wiremock/wiremock) provides a convenient way to deploy and manage WireMock instances. WireMock is available for various CPU architectures, including amd64, armv7, and armv8, ensuring compatibility with different devices and platforms. You can learn more about WireMock standalone on the [WireMock docs site](https://wiremock.org/docs/standalone/docker/).

### Prerequisites

The following prerequisites are required to follow along with this how-to guide:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Launching WireMock

Launch a quick demo of WireMock by using the following steps:

1. Clone the [GitHub repository](https://github.com/dockersamples/wiremock-node-docker) locally.
  ```console
  $ git clone https://github.com/dockersamples/wiremock-node-docker
  ```
2. Navigate to the `wiremock-endpoint` directory
  ```console
  $ cd wiremock-node-docker/
  ```
  WireMock acts as the mock API that your backend will communicate with to retrieve data. The mock API responses have already been created for you in the mappings directory.
3. Start the Compose stack by running the following command at the root of the cloned project directory
  ```console
  $ docker compose up -d
  ```
  After a moment, the application will be up and running.
  ![Diagram showing the WireMock container running on Docker Desktop ](https://docs.docker.com/guides/images/wiremock-using-docker.webp)  ![Diagram showing the WireMock container running on Docker Desktop ](https://docs.docker.com/guides/images/wiremock-using-docker.webp)
  You can check the logs by selecting the `wiremock-node-docker` container:
  ![Diagram showing the logs of WireMock container running on Docker Desktop ](https://docs.docker.com/guides/images/wiremock-logs-docker-desktop.webp)  ![Diagram showing the logs of WireMock container running on Docker Desktop ](https://docs.docker.com/guides/images/wiremock-logs-docker-desktop.webp)
4. Test the Mock API.
  ```console
  $ curl http://localhost:8080/api/v1/getWeather\?city\=Bengaluru
  ```
  It will return the following canned response with mock data:
  ```plaintext
  {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}
  ```
  With WireMock, you define canned responses using mapping files.
  For this request, the mock data is defined in the JSON file at
  `wiremock-endpoint/mappings/getWeather/getWeatherBengaluru.json`.
  For more information about stubbing canned responses, refer to the
  [WireMock documentation](https://wiremock.org/docs/stubbing/).

## Using WireMock in development

Now that you have tried WireMock, let’s use it in development and testing. In this example, you will use a sample application that has a Node.js backend. This app stack has the following configuration:

- Local Development Environment: The context in which the Node.js backend and WireMock are running.
- Node.js Backend: Represents the backend application that handles HTTP requests.
- External AccuWeather API: The real API from which live weather data is fetched.
- WireMock: The mock server that simulates the API responses during testing. It runs as a Docker container.

![Diagram showing the architecture of WireMock in development ](https://docs.docker.com/guides/images/wiremock-arch.webp)  ![Diagram showing the architecture of WireMock in development ](https://docs.docker.com/guides/images/wiremock-arch.webp)

- In development, the Node.js backend sends a request to WireMock instead of the actual AccuWeather API.
- In production, it connects directly to the live AccuWeather API for real data.

## Use mock data in local development

Let’s set up a Node app to send requests to the WireMock container instead of the actual AccuWeather API.

### Prerequisite

- Install [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- Ensure that WireMock container is up and running (see [Launching Wiremock](#launching-wiremock)

Follow the steps to setup a non-containerized Node application:

1. Navigate to the `accuweather-api` directory
  Make sure you're in the directory where your `package.json` file is located.
2. Set the environment variable.
  Open `.env` file placed under `accuweather-api/` directory. Remove the old entries and ensure that it just contains the following single line.
  ```plaintext
  API_ENDPOINT_BASE=http://localhost:8080
  ```
  This will tell your Node.js application to use the WireMock server for API calls.
3. Examine the Application Entry Point
  - The main file for the application is `index.js`, located in the `accuweather-api/src/api` directory.
  - This file starts the `getWeather.js` module, which is essential for your Node.js application. It uses the `dotenv` package to load environment variables from the`.env` file.
  - Based on the value of `API_ENDPOINT_BASE`, the application routes requests either to the WireMock server (`http://localhost:8080`) or the AccuWeather API. In this setup, it uses the WireMock server.
  - The code ensures that the `ACCUWEATHER_API_KEY` is required only if the application is not using WireMock, enhancing efficiency and avoiding errors.
  ```javascript
  require("dotenv").config();
  const express = require("express");
  const axios = require("axios");
  const router = express.Router();
  const API_ENDPOINT_BASE = process.env.API_ENDPOINT_BASE;
  const API_KEY = process.env.ACCUWEATHER_API_KEY;
  console.log('API_ENDPOINT_BASE:', API_ENDPOINT_BASE);  // Log after it's defined
  console.log('ACCUWEATHER_API_KEY is set:', !!API_KEY); // Log boolean instead of actual key
  if (!API_ENDPOINT_BASE) {
    throw new Error("API_ENDPOINT_BASE is not defined in environment variables");
  }
  // Only check for API key if not using WireMock
  if (API_ENDPOINT_BASE !== 'http://localhost:8080' && !API_KEY) {
    throw new Error("ACCUWEATHER_API_KEY is not defined in environment variables");
  }
  // Function to fetch the location key for the city
  async function fetchLocationKey(townName) {
    const { data: locationData } = await
  axios.get(`${API_ENDPOINT_BASE}/locations/v1/cities/search`, {
      params: { q: townName, details: false, apikey: API_KEY },
    });
    return locationData[0]?.Key;
  }
  ```
4. Start the Node server
  Before you start the Node server, ensure that you have already installed the node packages listed in the package.json file by running `npm install`.
  ```console
  npm install
  npm run start
  ```
  You should see the following output:
  ```plaintext
  > express-api-starter@1.2.0 start
  > node src/index.js
  API_ENDPOINT_BASE: http://localhost:8080
  ..
  Listening: http://localhost:5001
  ```
  The output indicates that your Node application has successfully started.
  Keep this terminal window open.
5. Test the Mocked API
  Open a new terminal window and run the following command to test the mocked API:
  ```console
  $ curl "http://localhost:5001/api/v1/getWeather?city=Bengaluru"
  ```
  You should see the following output:
  ```plaintext
  {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}%
  ```
  This indicates that your Node.js application is now successfully routing requests to the WireMock container and receiving the mocked responses
  You might have noticed that you’re trying to use `http://localhost:5001` as the URL instead of port `8080`. This is because your Node.js application is running on port `5001`, and it's routing requests to the WireMock container that's listening on port `8080`.
  > Tip
  >
  > Before you proceed to the next step, ensure that you stop the node application service.

## Use a Live API in production to fetch real-time weather data from AccuWeather

To enhance your Node.js application with real-time weather data, you can seamlessly integrate the AccuWeather API. This section of the guide will walk you through the steps involved in setting up a non-containerized Node.js application and fetching weather information directly from the AccuWeather API.

1. Create an AccuWeather API Key
  Sign up for a free AccuWeather developer account at[https://developer.accuweather.com/](https://developer.accuweather.com/). Within your account, create a new app by selecting `MY APPS` on the top navigation menu to get your unique API key.
  ![Diagram showing the AccuWeather Dashboard](https://docs.docker.com/guides/images/wiremock-accuweatherapi.webp)  ![Diagram showing the AccuWeather Dashboard](https://docs.docker.com/guides/images/wiremock-accuweatherapi.webp)
  [AccuWeather API](https://developer.accuweather.com/) is a web API that provides real-time weather data and forecasts. Developers can use this API to integrate weather information into their applications, websites, or other projects.
2. Change directory to `accuweather-api`
  ```console
  $ cd accuweather-api
  ```
3. Set your AccuWeather API key using the `.env` file:
  > Tip
  >
  > To prevent conflicts, ensure that any existing environment variables named `API_ENDPOINT_BASE` or `ACCUWEATHER_API_KEY` are removed before modifying the `.env` file.
  Run the following command on your terminal:
  ```console
  unset API_ENDPOINT_BASE
  unset ACCUWEATHER_API_KEY
  ```
  It’s time to set the environment variables in the `.env` file:
  ```plaintext
  ACCUWEATHER_API_KEY=XXXXXX
  API_ENDPOINT_BASE=http://dataservice.accuweather.com
  ```
  Make sure to populate `ACCUWEATHER_API_KEY` with the correct value.
4. Install the dependencies
  Run the following command to install the required packages:
  ```console
  $ npm install
  ```
  This will install all the packages listed in your `package.json` file. These packages are essential for the project to function correctly.
  If you encounter any warnings related to deprecated packages, you can ignore them for now for this demonstration.
5. Assuming that you don’t have a pre-existing Node server running on your system, go ahead and start the Node server by running the following command:
  ```console
  $ npm run start
  ```
  You should see the following output:
  ```plaintext
  > express-api-starter@1.2.0 start
  > node src/index.js
  API_ENDPOINT_BASE: http://dataservice.accuweather.com
  ACCUWEATHER_API_KEY is set: true
  Listening: http://localhost:5001
  ```
  Keep this terminal window open.
6. Run the curl command to send a GET request to the server URL.
  In the new terminal window, enter the following command:
  ```console
  $ curl "http://localhost:5000/api/v1/getWeather?city=Bengaluru"
  ```
  By running the command, you're essentially telling your local server to provide you with weather data for a city named `Bengaluru`. The request is specifically targeting the `/api/v1/getWeather` endpoint, and you're providing the query parameter `city=Bengaluru`. Once you execute the command, the server processes this request, fetches the data and returns it as a response, which `curl` will display in your terminal.
  When fetching data from the external AccuWeather API, you're interacting with live data that reflects the latest weather conditions.

## Recap

This guide has walked you through setting up WireMock using Docker. You’ve learned how to create stubs to simulate API endpoints, allowing you to develop and test your application without relying on external services. By using WireMock, you can create reliable and consistent test environments, reproduce edge cases, and speed up your development workflow.

---

# Using Docker with Zscaler

# Using Docker with Zscaler

   Table of contents

---

In many corporate environments, network traffic is intercepted and monitored
using HTTPS proxies, such as Zscaler. While Zscaler ensures security compliance
and network control, it can cause issues for developers using Docker,
particularly during build processes, where SSL certificate validation errors
might occur. This guide outlines how to configure Docker containers and builds
to properly handle Zscaler's custom certificates, ensuring smooth operation in
monitored environments.

## The role of certificates in Docker

When Docker builds or runs containers, it often needs to fetch resources from
the internet—whether it's pulling a base image from a registry, downloading
dependencies, or communicating with external services. In a proxied
environment, Zscaler intercepts HTTPS traffic and replaces the remote server's
certificate with its own. However, Docker doesn't trust this Zscaler
certificate by default, leading to SSL errors.

```plaintext
x509: certificate signed by unknown authority
```

These errors occur because Docker cannot verify the validity of the certificate
presented by Zscaler. To avoid this, you must configure Docker to trust
Zscaler's certificate.

## Configure Zscaler proxy for Docker Desktop

Depending on how Zscaler is deployed, you may need to configure Docker Desktop
proxy settings manually to use the Zscaler proxy.

If you're using Zscaler as a system-level proxy via the [Zscaler Client Connector](https://help.zscaler.com/zscaler-client-connector/what-is-zscaler-client-connector),
all traffic on the device is automatically routed through Zscaler, so Docker
Desktop uses the Zscaler proxy automatically with no additional configuration
necessary.

If you are not using Zscaler as a system-level proxy, manually configure proxy
settings in Docker Desktop. Set up proxy settings for all clients in the
organization using
[Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/),
or edit proxy configuration in the Docker Desktop GUI under
[Settings > Resources > Proxies](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

## Install root certificates in Docker images

To enable containers to use and trust the Zscaler proxy, embed the certificate
in the image and configure the image's trust store. Installing certificates at
image build time is the preferred approach, as it removes the need for
configuration during startup and provides an auditable, consistent environment.

### Obtaining the root certificate

The easiest way to obtain the root certificate is to export it from a machine
where an administrator has already installed it. You can use either a web
browser or the system's certificate management service (for example, Windows
Certificate Store).

#### Example: Exporting the certificate using Google Chrome

1. In Google Chrome, navigate to `chrome://certificate-manager/`.
2. Under **Local certificates**, select **View imported certificates**.
3. Find the Zscaler root certificate, often labeled **Zscaler Root CA**.
4. Open the certificate details and select **Export**.
5. Save the certificate in ASCII PEM format.
6. Open the exported file in a text editor to confirm it includes `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`.

When you have obtained the certificate, store it in an accessible repository,
such as JFrog Artifactory or a Git repository. Alternatively, use generic
storage like AWS S3.

### Building with the certificate

To install these certificates when building images, copy the certificate into
the build container and update the trust store. An example Dockerfile looks
like this:

```dockerfile
FROM debian:bookworm
COPY zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
```

Here, `zscaler-root-ca.crt` is the root certificate, located at the root of the
build context (often within the application's Git repository).

If you use an artifact repository, you can fetch the certificate directly using
the `ADD` instruction. You can also use the `--checksum` flag to verify that
the content digest of the certificate is correct.

```dockerfile
FROM debian:bookworm
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://artifacts.example/certs/zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
```

#### Using multi-stage builds

For multi-stage builds where certificates are needed in the final runtime
image, ensure the certificate installation occurs in the final stage.

```dockerfile
FROM debian:bookworm AS build
WORKDIR /build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git
RUN --mount=target=. cmake -B output/

FROM debian:bookworm-slim AS final
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://artifacts.example/certs/zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
WORKDIR /app
COPY --from=build /build/output/bin .
ENTRYPOINT ["/app/bin"]
```

## Conclusion

Embedding the Zscaler root certificate directly into your Docker images ensures
that containers run smoothly within Zscaler-proxied environments. By using this
approach, you reduce potential runtime errors and create a consistent,
auditable configuration that allows for smooth Docker operations within a
monitored network.
