# Connecting services with Docker Compose and more

# Connecting services with Docker Compose

> Learn how to connect services with Docker Compose to monitor a Golang application with Prometheus and Grafana.

# Connecting services with Docker Compose

   Table of contents

---

Now that you have containerized the Golang application, you will use Docker Compose to connect your services together. You will connect the Golang application, Prometheus, and Grafana services together to monitor the Golang application with Prometheus and Grafana.

## Creating a Docker Compose file

Create a new file named `compose.yml` in the root directory of your Golang application. The Docker Compose file contains instructions to run multiple services and connect them together.

Here is a Docker Compose file for a project that uses Golang, Prometheus, and Grafana. You will also find this file in the `go-prometheus-monitoring` directory.

```yaml
services:
  api:
    container_name: go-api
    build:
      context: .
      dockerfile: Dockerfile
    image: go-api:latest
    ports:
      - 8000:8000
    networks:
      - go-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    develop:
      watch:
        - path: .
          action: rebuild

  prometheus:
    container_name: prometheus
    image: prom/prometheus:v2.55.0
    volumes:
      - ./Docker/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    networks:
      - go-network

  grafana:
    container_name: grafana
    image: grafana/grafana:11.3.0
    volumes:
      - ./Docker/grafana.yml:/etc/grafana/provisioning/datasources/datasource.yaml
      - grafana-data:/var/lib/grafana
    ports:
      - 3000:3000
    networks:
      - go-network
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password

volumes:
  grafana-data:

networks:
  go-network:
    driver: bridge
```

## Understanding the Docker Compose file

The Docker Compose file consists of three services:

- **Golang application service**: This service builds the Golang application using the Dockerfile and runs it in a container. It exposes the application's port `8000` and connects to the `go-network` network. It also defines a health check to monitor the application's health. You have also used `healthcheck` to monitor the health of the application. The health check runs every 30 seconds and retries 5 times if the health check fails. The health check uses the `curl` command to check the `/health` endpoint of the application. Apart from the health check, you have also added a `develop` section to watch the changes in the application's source code and rebuild the application using the Docker Compose Watch feature.
- **Prometheus service**: This service runs the Prometheus server in a container. It uses the official Prometheus image `prom/prometheus:v2.55.0`. It exposes the Prometheus server on port `9090` and connects to the `go-network` network. You have also mounted the `prometheus.yml` file from the `Docker` directory which is present in the root directory of your project. The `prometheus.yml` file contains the Prometheus configuration to scrape the metrics from the Golang application. This is how you connect the Prometheus server to the Golang application.
  ```yaml
  global:
    scrape_interval: 10s
    evaluation_interval: 10s
  scrape_configs:
    - job_name: myapp
      static_configs:
        - targets: ["api:8000"]
  ```
  In the `prometheus.yml` file, you have defined a job named `myapp` to scrape the metrics from the Golang application. The `targets` field specifies the target to scrape the metrics from. In this case, the target is the Golang application running on port `8000`. The `api` is the service name of the Golang application in the Docker Compose file. The Prometheus server will scrape the metrics from the Golang application every 10 seconds.
- **Grafana service**: This service runs the Grafana server in a container. It uses the official Grafana image `grafana/grafana:11.3.0`. It exposes the Grafana server on port `3000` and connects to the `go-network` network. You have also mounted the `grafana.yml` file from the `Docker` directory which is present in the root directory of your project. The `grafana.yml` file contains the Grafana configuration to add the Prometheus data source. This is how you connect the Grafana server to the Prometheus server. In the environment variables, you have set the Grafana admin user and password, which will be used to log in to the Grafana dashboard.
  ```yaml
  apiVersion: 1
  datasources:
  - name: Prometheus (Main)
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
  ```
  In the `grafana.yml` file, you have defined a Prometheus data source named `Prometheus (Main)`. The `type` field specifies the type of the data source, which is `prometheus`. The `url` field specifies the URL of the Prometheus server to fetch the metrics from. In this case, the URL is `http://prometheus:9090`. `prometheus` is the service name of the Prometheus server in the Docker Compose file. The `isDefault` field specifies whether the data source is the default data source in Grafana.

Apart from the services, the Docker Compose file also defines a volume named `grafana-data` to persist the Grafana data and a network named `go-network` to connect the services together. You have created a custom network `go-network` to connect the services together. The `driver: bridge` field specifies the network driver to use for the network.

## Building and running the services

Now that you have the Docker Compose file, you can build the services and run them together using Docker Compose.

To build and run the services, run the following command in the terminal:

```console
$ docker compose up
```

The `docker compose up` command builds the services defined in the Docker Compose file and runs them together. You will see the similar output in the terminal:

```console
✔ Network go-prometheus-monitoring_go-network  Created                                                           0.0s
 ✔ Container grafana                            Created                                                           0.3s
 ✔ Container go-api                             Created                                                           0.2s
 ✔ Container prometheus                         Created                                                           0.3s
Attaching to go-api, grafana, prometheus
go-api      | [GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.
go-api      |
go-api      | [GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
go-api      |  - using env:     export GIN_MODE=release
go-api      |  - using code:    gin.SetMode(gin.ReleaseMode)
go-api      |
go-api      | [GIN-debug] GET    /metrics                  --> main.PrometheusHandler.func1 (3 handlers)
go-api      | [GIN-debug] GET    /health                   --> main.main.func1 (4 handlers)
go-api      | [GIN-debug] GET    /v1/users                 --> main.main.func2 (4 handlers)
go-api      | [GIN-debug] [WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.
go-api      | Please check https://pkg.go.dev/github.com/gin-gonic/gin#readme-don-t-trust-all-proxies for details.
go-api      | [GIN-debug] Listening and serving HTTP on :8000
prometheus  | ts=2025-03-15T05:57:06.676Z caller=main.go:627 level=info msg="No time or size retention was set so using the default time retention" duration=15d
prometheus  | ts=2025-03-15T05:57:06.678Z caller=main.go:671 level=info msg="Starting Prometheus Server" mode=server version="(version=2.55.0, branch=HEAD, revision=91d80252c3e528728b0f88d254dd720f6be07cb8)"
grafana     | logger=settings t=2025-03-15T05:57:06.865335506Z level=info msg="Config overridden from command line" arg="default.log.mode=console"
grafana     | logger=settings t=2025-03-15T05:57:06.865337131Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_DATA=/var/lib/grafana"
grafana     | logger=ngalert.state.manager t=2025-03-15T05:57:07.088956839Z level=info msg="State
.
.
grafana     | logger=plugin.angulardetectorsprovider.dynamic t=2025-03-15T05:57:07.530317298Z level=info msg="Patterns update finished" duration=440.489125ms
```

The services will start running, and you can access the Golang application at `http://localhost:8000`, Prometheus at `http://localhost:9090/health`, and Grafana at `http://localhost:3000`. You can also check the running containers using the `docker ps` command.

```console
$ docker ps
```

## Summary

In this section, you learned how to connect services together using Docker Compose. You created a Docker Compose file to run multiple services together and connect them using networks. You also learned how to build and run the services using Docker Compose.

Related information:

- [Docker Compose overview](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)

Next, you will learn how to develop the Golang application with Docker Compose and monitor it with Prometheus and Grafana.

## Next steps

In the next section, you will learn how to develop the Golang application with Docker. You will also learn how to use Docker Compose Watch to rebuild the image whenever you make changes to the code. Lastly, you will test the application and visualize the metrics in Grafana using Prometheus as the data source.

---

# Containerize a Golang application

> Learn how to containerize a Golang application.

# Containerize a Golang application

   Table of contents

---

Containerization helps you bundle the application and its dependencies into a single package called a container. This package can run on any platform without worrying about the environment. In this section, you will learn how to containerize a Golang application using Docker.

To containerize a Golang application, you first need to create a Dockerfile. The Dockerfile contains instructions to build and run the application in a container. Also, when creating a Dockerfile, you can follow different sets of best practices to optimize the image size and make it more secure.

## Creating a Dockerfile

Create a new file named `Dockerfile` in the root directory of your Golang application. The Dockerfile contains instructions to build and run the application in a container.

The following is a Dockerfile for a Golang application. You will also find this file in the `go-prometheus-monitoring` directory.

```dockerfile
# Use the official Golang image as the base
FROM golang:1.24-alpine AS builder

# Set environment variables
ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Set working directory inside the container
WORKDIR /build

# Copy go.mod and go.sum files for dependency installation
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the entire application source
COPY . .

# Build the Go binary
RUN go build -o /app .

# Final lightweight stage
FROM alpine:3.21 AS final

# Copy the compiled binary from the builder stage
COPY --from=builder /app /bin/app

# Expose the application's port
EXPOSE 8000

# Run the application
CMD ["bin/app"]
```

## Understanding the Dockerfile

The Dockerfile consists of two stages:

1. **Build stage**: This stage uses the official Golang image as the base and sets the necessary environment variables. It also sets the working directory inside the container, copies the `go.mod` and `go.sum` files for dependency installation, downloads the dependencies, copies the entire application source, and builds the Go binary.
  You use the `golang:1.24-alpine` image as the base image for the build stage. The `CGO_ENABLED=0` environment variable disables CGO, which is useful for building static binaries. You also set the `GOOS` and `GOARCH` environment variables to `linux` and `amd64`, respectively, to build the binary for the Linux platform.
2. **Final stage**: This stage uses the official Alpine image as the base and copies the compiled binary from the build stage. It also exposes the application's port and runs the application.
  You use the `alpine:3.21` image as the base image for the final stage. You copy the compiled binary from the build stage to the final image. You expose the application's port using the `EXPOSE` instruction and run the application using the `CMD` instruction.
  Apart from the multi-stage build, the Dockerfile also follows best practices such as using the official images, setting the working directory, and copying only the necessary files to the final image. You can further optimize the Dockerfile by other best practices.

## Build the Docker image and run the application

One you have the Dockerfile, you can build the Docker image and run the application in a container.

To build the Docker image, run the following command in the terminal:

```console
$ docker build -t go-api:latest .
```

After building the image, you can run the application in a container using the following command:

```console
$ docker run -p 8000:8000 go-api:latest
```

The application will start running inside the container, and you can access it at `http://localhost:8000`. You can also check the running containers using the `docker ps` command.

```console
$ docker ps
```

## Summary

In this section, you learned how to containerize a Golang application using a Dockerfile. You created a multi-stage Dockerfile to build and run the application in a container. You also learned about best practices to optimize the Docker image size and make it more secure.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore file](https://docs.docker.com/reference/dockerfile/#dockerignore-file)

## Next steps

In the next section, you will learn how to use Docker Compose to connect and run multiple services together to monitor a Golang application with Prometheus and Grafana.

---

# Developing your application

> Learn how to develop the Golang application with Docker.

# Developing your application

   Table of contents

---

In the last section, you saw how using Docker Compose, you can connect your services together. In this section, you will learn how to develop the Golang application with Docker. You will also see how to use Docker Compose Watch to rebuild the image whenever you make changes to the code. Lastly, you will test the application and visualize the metrics in Grafana using Prometheus as the data source.

## Developing the application

Now, if you make any changes to your Golang application locally, it needs to reflect in the container, right? To do that, one approach is use the `--build` flag in Docker Compose after making changes in the code. This will rebuild all the services which have the `build` instruction in the `compose.yml` file, in your case, the `api` service (Golang application).

```console
docker compose up --build
```

But, this is not the best approach. This is not efficient. Every time you make a change in the code, you need to rebuild manually. This is not is not a good flow for development.

The better approach is to use Docker Compose Watch. In the `compose.yml` file, under the service `api`, you have added the `develop` section. So, it's more like a hot reloading. Whenever you make changes to code (defined in `path`), it will rebuild the image (or restart depending on the action). This is how you can use it:

| 1234567891011121314151617181920 | services:api:container_name:go-apibuild:context:.dockerfile:Dockerfileimage:go-api:latestports:-8000:8000networks:-go-networkhealthcheck:test:["CMD","curl","-f","http://localhost:8080/health"]interval:30stimeout:10sretries:5develop:watch:-path:.action:rebuild |
| --- | --- |

Once you have added the `develop` section in the `compose.yml` file, you can use the following command to start the development server:

```console
$ docker compose watch
```

Now, if you modify your `main.go` or any other file in the project, the `api` service will be rebuilt automatically. You will see the following output in the terminal:

```bash
Rebuilding service(s) ["api"] after changes were detected...
[+] Building 8.1s (15/15) FINISHED                                                                                                        docker:desktop-linux
 => [api internal] load build definition from Dockerfile                                                                                                  0.0s
 => => transferring dockerfile: 704B                                                                                                                      0.0s
 => [api internal] load metadata for docker.io/library/alpine:3.17                                                                                        1.1s
  .
 => => exporting manifest list sha256:89ebc86fd51e27c1da440dc20858ff55fe42211a1930c2d51bbdce09f430c7f1                                                    0.0s
 => => naming to docker.io/library/go-api:latest                                                                                                          0.0s
 => => unpacking to docker.io/library/go-api:latest                                                                                                       0.0s
 => [api] resolving provenance for metadata file                                                                                                          0.0s
service(s) ["api"] successfully built
```

## Testing the application

Now that you have your application running, head over to the Grafana dashboard to visualize the metrics you are registering. Open your browser and navigate to `http://localhost:3000`. You will be greeted with the Grafana login page. The login credentials are the ones provided in Compose file.

Once you are logged in, you can create a new dashboard. While creating dashboard you will notice that is default data source is `Prometheus`. This is because you have already configured the data source in the `grafana.yml` file.

![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/grafana-dash.png)  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/grafana-dash.png)

You can use different panels to visualize the metrics. This guide doesn't go into details of Grafana. You can refer to the [Grafana documentation](https://grafana.com/docs/grafana/latest/) for more information. There is a Bar Gauge panel to visualize the total number of requests from different endpoints. You used the `api_http_request_total` and `api_http_request_error_total` metrics to get the data.

![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/grafana-panel.png)  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/grafana-panel.png)

You created this panel to visualize the total number of requests from different endpoints to compare the successful and failed requests. For all the good requests, the bar will be green, and for all the failed requests, the bar will be red. Plus it will also show the from which endpoint the request is coming, either it's a successful request or a failed request. If you want to use this panel, you can import the `dashboard.json` file from the repository you cloned.

## Summary

You've come to the end of this guide. You learned how to develop the Golang application with Docker. You also saw how to use Docker Compose Watch to rebuild the image whenever you make changes to the code. Lastly, you tested the application and visualized the metrics in Grafana using Prometheus as the data source.

---

# Monitor a Golang application with Prometheus and Grafana

> Containerize a Golang application and monitor it with Prometheus and Grafana.

# Monitor a Golang application with Prometheus and Grafana

Table of contents

---

The guide teaches you how to containerize a Golang application and monitor it with Prometheus and Grafana.

> **Acknowledgment**
>
>
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

## Overview

To make sure your application is working as intended, monitoring is important. One of the most popular monitoring tools is Prometheus. Prometheus is an open-source monitoring and alerting toolkit that is designed for reliability and scalability. It collects metrics from monitored targets by scraping metrics HTTP endpoints on these targets. To visualize the metrics, you can use Grafana. Grafana is an open-source platform for monitoring and observability that allows you to query, visualize, alert on, and understand your metrics no matter where they are stored.

In this guide, you will be creating a Golang server with some endpoints to simulate a real-world application. Then you will expose metrics from the server using Prometheus. Finally, you will visualize the metrics using Grafana. You will containerize the Golang application, and using the Docker Compose file, you will connect all the services: Golang, Prometheus, and Grafana.

## What will you learn?

- Create a Golang application with custom Prometheus metrics.
- Containerize a Golang application.
- Use Docker Compose to run multiple services and connect them together to monitor a Golang application with Prometheus and Grafana.
- Visualize the metrics using Grafana dashboards.

## Prerequisites

- A good understanding of Golang is assumed.
- You must me familiar with Prometheus and creating dashboards in Grafana.
- You must have familiarity with Docker concepts like containers, images, and Dockerfiles. If you are new to Docker, you can start with the
  [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

## Next steps

You will create a Golang server and expose metrics using Prometheus.

## Modules

1. [Understand the application](https://docs.docker.com/guides/go-prometheus-monitoring/application/)
  Learn how to create a Golang server to register metrics with Prometheus.
2. [Containerize your app](https://docs.docker.com/guides/go-prometheus-monitoring/containerize/)
  Learn how to containerize a Golang application.
3. [Connecting services with Docker Compose](https://docs.docker.com/guides/go-prometheus-monitoring/compose/)
  Learn how to connect services with Docker Compose to monitor a Golang application with Prometheus and Grafana.
4. [Develop your app](https://docs.docker.com/guides/go-prometheus-monitoring/develop/)
  Learn how to develop the Golang application with Docker.

---

# Build your Go image

> Learn how to build your first Docker image by writing a Dockerfile

# Build your Go image

   Table of contents

---

## Overview

In this section you're going to build a container image. The image includes
everything you need to run your application – the compiled application binary
file, the runtime, the libraries, and all other resources required by your
application.

## Required software

To complete this tutorial, you need the following:

- Docker running locally. Follow the
  [instructions to download and install Docker](https://docs.docker.com/desktop/).
- An IDE or a text editor to edit files. [Visual Studio Code](https://code.visualstudio.com/) is a free and popular choice but you can use anything you feel comfortable with.
- A Git client. This guide uses a command-line based `git` client, but you are free to use whatever works for you.
- A command-line terminal application. The examples shown in this module are from the Linux shell, but they should work in PowerShell, Windows Command Prompt, or OS X Terminal with minimal, if any, modifications.

## Meet the example application

The example application is a caricature of a microservice. It is purposefully trivial to keep focus on learning the basics of containerization for Go applications.

The application offers two HTTP endpoints:

- It responds with a string containing a heart symbol (`<3`) to requests to `/`.
- It responds with `{"Status" : "OK"}` JSON to a request to `/health`.

It responds with HTTP error 404 to any other request.

The application listens on a TCP port defined by the value of environment variable `PORT`. The default value is `8080`.

The application is stateless.

The complete source code for the application is on GitHub: [github.com/docker/docker-gs-ping](https://github.com/docker/docker-gs-ping). You are encouraged to fork it and experiment with it as much as you like.

To continue, clone the application repository to your local machine:

```console
$ git clone https://github.com/docker/docker-gs-ping
```

The application's `main.go` file is straightforward, if you are familiar with Go:

```go
package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, "Hello, Docker! <3")
	})

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})

	httpPort := os.Getenv("PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

// Simple implementation of an integer minimum
// Adapted from: https://gobyexample.com/testing-and-benchmarking
func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
```

## Create a Dockerfile for the application

To build a container image with Docker, a `Dockerfile` with build instructions is required.

Begin your `Dockerfile` with the (optional) parser directive line that instructs BuildKit to
interpret your file according to the grammar rules for the specified version of the syntax.

You then tell Docker what base image you would like to use for your application:

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19
```

Docker images can be inherited from other images. Therefore, instead of creating
your own base image from scratch, you can use the official Go image that already
has all necessary tools and libraries to compile and run a Go application.

> Note
>
> If you are curious about creating your own base images, you can check out the following section of this guide:
> [creating base images](https://docs.docker.com/build/building/base-images/#create-a-base-image).
> Note, however, that this isn't necessary to continue with your task at hand.

Now that you have defined the base image for your upcoming container image, you
can begin building on top of it.

To make things easier when running the rest of your commands, create a directory
inside the image that you're building. This also instructs Docker to use this
directory as the default destination for all subsequent commands. This way you
don't have to type out full file paths in the `Dockerfile`, the relative paths
will be based on this directory.

```dockerfile
WORKDIR /app
```

Usually the very first thing you do once you’ve downloaded a project written in
Go is to install the modules necessary to compile it. Note, that the base image
has the toolchain already, but your source code isn't in it yet.

So before you can run `go mod download` inside your image, you need to get your
`go.mod` and `go.sum` files copied into it. Use the `COPY` command to do this.

In its simplest form, the `COPY` command takes two parameters. The first
parameter tells Docker what files you want to copy into the image. The last
parameter tells Docker where you want that file to be copied to.

Copy the `go.mod` and `go.sum` file into your project directory `/app` which,
owing to your use of `WORKDIR`, is the current directory (`./`) inside the
image. Unlike some modern shells that appear to be indifferent to the use of
trailing slash (`/`), and can figure out what the user meant (most of the time),
Docker's `COPY` command is quite sensitive in its interpretation of the trailing
slash.

```dockerfile
COPY go.mod go.sum ./
```

> Note
>
> If you'd like to familiarize yourself with the trailing slash treatment by the
> `COPY` command, see
> [Dockerfile
> reference](https://docs.docker.com/reference/dockerfile/#copy). This trailing slash can
> cause issues in more ways than you can imagine.

Now that you have the module files inside the Docker image that you are
building, you can use the `RUN` command to run the command `go mod download`
there as well. This works exactly the same as if you were running `go` locally
on your machine, but this time these Go modules will be installed into a
directory inside the image.

```dockerfile
RUN go mod download
```

At this point, you have a Go toolchain version 1.19.x and all your Go
dependencies installed inside the image.

The next thing you need to do is to copy your source code into the image. You’ll
use the `COPY` command just like you did with your module files before.

```dockerfile
COPY *.go ./
```

This `COPY` command uses a wildcard to copy all files with `.go` extension
located in the current directory on the host (the directory where the `Dockerfile`
is located) into the current directory inside the image.

Now, to compile your application, use the familiar `RUN` command:

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping
```

This should be familiar. The result of that command will be a static application
binary named `docker-gs-ping` and located in the root of the filesystem of the
image that you are building. You could have put the binary into any other place
you desire inside that image, the root directory has no special meaning in this
regard. It's just convenient to use it to keep the file paths short for improved
readability.

Now, all that is left to do is to tell Docker what command to run when your
image is used to start a container.

You do this with the `CMD` command:

```dockerfile
CMD ["/docker-gs-ping"]
```

Here's the complete `Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code. Note the slash at the end, as explained in
# https://docs.docker.com/reference/dockerfile/#copy
COPY *.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Optional:
# To bind to a TCP port, runtime parameters must be supplied to the docker command.
# But we can document in the Dockerfile what ports
# the application is going to listen on by default.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

# Run
CMD ["/docker-gs-ping"]
```

The `Dockerfile` may also contain comments. They always begin with a `#` symbol,
and must be at the beginning of a line. Comments are there for your convenience
to allow documenting your `Dockerfile`.

There is also a concept of Dockerfile directives, such as the `syntax` directive
you added. The directives must always be at the very top of the `Dockerfile`, so
when adding comments, make sure that the comments follow after any directives
that you may have used:

```dockerfile
# syntax=docker/dockerfile:1
# A sample microservice in Go packaged into a container image.

FROM golang:1.19

# ...
```

## Build the image

Now that you've created your `Dockerfile`, build an image from it. The `docker build` command creates Docker images from the `Dockerfile` and a context. A
build context is the set of files located in the specified path or URL. The
Docker build process can access any of the files located in the context.

The build command optionally takes a `--tag` flag. This flag is used to label
the image with a string value, which is easy for humans to read and recognize.
If you don't pass a `--tag`, Docker will use `latest` as the default value.

Build your first Docker image.

```console
$ docker build --tag docker-gs-ping .
```

The build process will print some diagnostic messages as it goes through the build steps.
The following is just an example of what these messages may look like.

```console
[+] Building 2.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => => transferring dockerfile: 701B                                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => => transferring context: 2B                                                                                                            0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                                 1.1s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14            0.0s
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/golang:1.19                                                                             0.7s
 => [1/6] FROM docker.io/library/golang:1.19@sha256:5d947843dde82ba1df5ac1b2ebb70b203d106f0423bf5183df3dc96f6bc5a705                       0.0s
 => [internal] load build context                                                                                                          0.0s
 => => transferring context: 6.08kB                                                                                                        0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                              0.0s
 => CACHED [3/6] COPY go.mod go.sum ./                                                                                                     0.0s
 => CACHED [4/6] RUN go mod download                                                                                                       0.0s
 => CACHED [5/6] COPY *.go ./                                                                                                              0.0s
 => CACHED [6/6] RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping                                                                  0.0s
 => exporting to image                                                                                                                     0.0s
 => => exporting layers                                                                                                                    0.0s
 => => writing image sha256:ede8ff889a0d9bc33f7a8da0673763c887a258eb53837dd52445cdca7b7df7e3                                               0.0s
 => => naming to docker.io/library/docker-gs-ping                                                                                          0.0s
```

Your exact output will vary, but provided there aren't any errors, you should
see the word `FINISHED` in the first line of output. This means Docker has
successfully built your image named `docker-gs-ping`.

## View local images

To see the list of images you have on your local machine, you have two options.
One is to use the CLI and the other is to use
[Docker
Desktop](https://docs.docker.com/desktop/). Since you're currently working in the
terminal, take a look at listing images with the CLI.

To list images, run the `docker image ls`command (or the `docker images` shorthand):

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   2 minutes ago   1.11GB
...
```

Your exact output may vary, but you should see the `docker-gs-ping` image with
the `latest` tag. Because you didn't specify a custom tag when you built your
image, Docker assumed that the tag would be `latest`, which is a special value.

## Tag images

An image name is made up of slash-separated name components. Name components may
contain lowercase letters, digits, and separators. A separator is defined as a
period, one or two underscores, or one or more dashes. A name component may not
start or end with a separator.

An image is made up of a manifest and a list of layers. In simple terms, a tag
points to a combination of these artifacts. You can have multiple tags for the
image and, in fact, most images have multiple tags. Create a second tag
for the image you built and take a look at its layers.

Use the `docker image tag` (or `docker tag` shorthand) command to create a new
tag for your image. This command takes two arguments; the first argument is the
source image, and the second is the new tag to create. The following command
creates a new `docker-gs-ping:v1.0` tag for the `docker-gs-ping:latest` you
built:

```console
$ docker image tag docker-gs-ping:latest docker-gs-ping:v1.0
```

The Docker `tag` command creates a new tag for the image. It doesn't create a
new image. The tag points to the same image and is just another way to reference
the image.

Now run the `docker image ls` command again to see the updated list of local
images:

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   6 minutes ago   1.11GB
docker-gs-ping                   v1.0      7f153fbcc0a8   6 minutes ago   1.11GB
...
```

You can see that you have two images that start with `docker-gs-ping`. You know
they're the same image because if you look at the `IMAGE ID` column, you can
see that the values are the same for the two images. This value is a unique
identifier Docker uses internally to identify the image.

Remove the tag that you just created. To do this, you’ll use the
`docker image rm` command, or the shorthand `docker rmi` (which stands for
"remove image"):

```console
$ docker image rm docker-gs-ping:v1.0
Untagged: docker-gs-ping:v1.0
```

Notice that the response from Docker tells you that the image hasn't been
removed but only untagged.

Verify this by running the following command:

```console
$ docker image ls
```

You will see that the tag `v1.0` is no longer in the list of images kept by your Docker instance.

```text
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   7 minutes ago   1.11GB
...
```

The tag `v1.0` has been removed but you still have the `docker-gs-ping:latest`
tag available on your machine, so the image is there.

## Multi-stage builds

You may have noticed that your `docker-gs-ping` image weighs in at over a
gigabyte, which is a lot for a tiny compiled Go application. You may also be
wondering what happened to the full suite of Go tools, including the compiler,
after you had built your image.

The answer is that the full toolchain is still there, in the container image.
Not only this is inconvenient because of the large file size, but it may also
present a security risk when the container is deployed.

These two issues can be solved by using
[multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

In a nutshell, a multi-stage build can carry over the artifacts from one build stage into another,
and every build stage can be instantiated from a different base image.

Thus, in the following example, you are going to use a full-scale official Go
image to build your application. Then you'll copy the application binary into
another image whose base is very lean and doesn't include the Go toolchain or
other optional components.

The `Dockerfile.multistage` in the sample application's repository has the
following content:

```dockerfile
# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Run the tests in the container
FROM build-stage AS run-test-stage
RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

Since you have two Dockerfiles now, you have to tell Docker what Dockerfile
you'd like to use to build the image. Tag the new image with `multistage`. This
tag (like any other, apart from `latest`) has no special meaning for Docker,
it's just something you chose.

```console
$ docker build -t docker-gs-ping:multistage -f Dockerfile.multistage .
```

Comparing the sizes of `docker-gs-ping:multistage` and `docker-gs-ping:latest`
you see a few orders-of-magnitude difference.

```console
$ docker image ls
REPOSITORY       TAG          IMAGE ID       CREATED              SIZE
docker-gs-ping   multistage   e3fdde09f172   About a minute ago   28.1MB
docker-gs-ping   latest       336a3f164d0f   About an hour ago    1.11GB
```

This is so because the ["distroless"](https://github.com/GoogleContainerTools/distroless)
base image that you have used in the second stage of the build is very barebones and is designed for lean deployments of static binaries.

There's much more to multi-stage builds, including the possibility of multi-architecture builds,
so feel free to check out
[multi-stage builds](https://docs.docker.com/build/building/multi-stage/). This is, however, not essential for your progress here.

## Next steps

In this module, you met your example application and built and container image
for it.

In the next module, you’ll take a look at how to run your image as a container.
