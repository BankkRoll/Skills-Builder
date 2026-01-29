# Customize Compose Bridge and more

# Customize Compose Bridge

> Learn how to customize Compose Bridge transformations using Go templates and Compose extensions

# Customize Compose Bridge

   Table of contents

---

Requires: Docker Desktop 4.43.0 and later

You can customize how Compose Bridge converts your Docker Compose files into platform-specific formats.

This page explains how Compose Bridge uses templating to generate Kubernetes manifests and how you can customize these templates for your specific requirements and needs, or how you can build your own transformation.

## How it works

Compose bridge uses transformations to let you convert a Compose model into another form.

A transformation is packaged as a Docker image that receives the fully-resolved Compose model as `/in/compose.yaml` and can produce any target format file under `/out`.

Compose Bridge includes a default Kubernetes transformation using Go templates, which you can customize by replacing or extending templates.

### Template syntax

Compose Bridge makes use of templates to transform a Compose configuration file into Kubernetes manifests. Templates are plain text files that use the [Go templating syntax](https://pkg.go.dev/text/template). This enables the insertion of logic and data, making the templates dynamic and adaptable according to the Compose model.

When a template is executed, it must produce a YAML file which is the standard format for Kubernetes manifests. Multiple files can be generated as long as they are separated by `---`

Each YAML output file begins with custom header notation, for example:

```yaml
#! manifest.yaml
```

In the following example, a template iterates over services defined in a `compose.yaml` file. For each service, a dedicated Kubernetes manifest file is generated, named according to the service and containing specified configurations.

```yaml
{{ range $name, $service := .services }}
---
#! {{ $name }}-manifest.yaml
# Generated code, do not edit
key: value
## ...
{{ end }}
```

### Input model

You can generate the input model by running `docker compose config`.

This canonical YAML output serves as the input for Compose Bridge transformations. Within the templates, data from the `compose.yaml` is accessed using dot notation, allowing you to navigate through nested data structures. For example, to access the deployment mode of a service, you would use `service.deploy.mode`:

```yaml
# iterate over a yaml sequence
{{ range $name, $service := .services }}
 # access a nested attribute using dot notation
 {{ if eq $service.deploy.mode "global" }}
kind: DaemonSet
 {{ end }}
{{ end }}
```

You can check the [Compose Specification JSON schema](https://github.com/compose-spec/compose-go/blob/main/schema/compose-spec.json) for a full overview of the Compose model. This schema outlines all possible configurations and their data types in the Compose model.

### Helper functions

As part of the Go templating syntax, Compose Bridge offers a set of YAML helper functions designed to manipulate data within the templates efficiently:

| Function | Description |
| --- | --- |
| seconds | Converts adurationinto an integer (seconds). |
| uppercase | Converts a string to uppercase. |
| title | Capitalizes the first letter of each word. |
| safe | Converts a string into a safe identifier (replaces non-lowercase characters with-). |
| truncate | Removes the first N elements from a list. |
| join | Joins list elements into a single string with a separator. |
| base64 | Encodes a string as base64 (used for Kubernetes secrets). |
| map | Maps values using“value -> newValue”syntax. |
| indent | Indents string content by N spaces. |
| helmValue | Outputs a Helm-style template value. |

In the following example, the template checks if a healthcheck interval is specified for a service, applies the `seconds` function to convert this interval into seconds and assigns the value to the `periodSeconds` attribute.

```yaml
{{ if $service.healthcheck.interval }}
            periodSeconds: {{ $service.healthcheck.interval | seconds }}{{ end }}
{{ end }}
```

## Customize the default templates

As Kubernetes is a versatile platform, there are many ways
to map Compose concepts into Kubernetes resource definitions. Compose
Bridge lets you customize the transformation to match your own infrastructure
decisions and preferences, with varying level of flexibility and effort.

### Modify the default templates

You can extract templates used by the default transformation `docker/compose-bridge-kubernetes`:

```console
$ docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template
```

The templates are extracted into a directory named after your template name, in this case `my-template`. It includes:

- A Dockerfile that lets you create your own image to distribute your template
- A directory containing the templating files

Edit, [add](#add-your-own-templates), or remove templates as needed.

You can then use the generated Dockerfile to package your changes into a new transformation image, which you can then use with Compose Bridge:

```console
$ docker build --tag mycompany/transform --push .
```

Use your transformation as a replacement:

```console
$ docker compose bridge convert --transformations mycompany/transform
```

#### Model Runner templates

The default transformation also includes templates for applications that use LLMs:

- `model-runner-deployment.tmpl`
- `model-runner-service.tmpl`
- `model-runner-pvc.tmpl`
- `/overlays/model-runner/kustomization.yaml`
- `/overlays/desktop/deployment.tmpl`

These templates can be extended or replaced to change how Docker Model Runner is deployed or configured.

For more details, see [Use Model Runner](https://docs.docker.com/compose/bridge/use-model-runner/).

### Add your own templates

For resources that are not managed by Compose Bridge's default transformation,
you can build your own templates.

The `compose.yaml` model may not offer all
the configuration attributes required to populate the target manifest. If this is the case, you can
then rely on Compose custom extensions to better describe the
application, and offer an agnostic transformation.

For example, if you add `x-virtual-host` metadata
to service definitions in the `compose.yaml` file, you can use the following custom attribute
to produce Ingress rules:

```yaml
{{ $project := .name }}
#! {{ $name }}-ingress.yaml
# Generated code, do not edit
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virtual-host-ingress
  namespace: {{ $project }}
spec:
  rules:
{{ range $name, $service := .services }}
{{ range index $service "x-virtual-host" }}
  - host: ${{ . }}
    http:
      paths:
      - path: "/"
        backend:
          service:
            name: ${{ name }}
            port:
              number: 80
{{ end }}
{{ end }}
```

Once packaged into a Docker image, you can use this custom template
when transforming Compose models into Kubernetes in addition to other
transformations:

```console
$ docker compose bridge convert \
    --transformation docker/compose-bridge-kubernetes \
    --transformation mycompany/transform
```

### Build your own transformation

While Compose Bridge templates make it easy to customize with minimal changes,
you may want to make significant changes, or rely on an existing conversion tool.

A Compose Bridge transformation is a Docker image that is designed to get a Compose model
from `/in/compose.yaml` and produce platform manifests under `/out`. This simple
contract makes it easy to bundle an alternate transformation using
[Kompose](https://kompose.io/):

```Dockerfile
FROM alpine

# Get kompose from github release page
RUN apk add --no-cache curl
ARG VERSION=1.32.0
RUN ARCH=$(uname -m | sed 's/armv7l/arm/g' | sed 's/aarch64/arm64/g' | sed 's/x86_64/amd64/g') && \
    curl -fsL \
    "https://github.com/kubernetes/kompose/releases/download/v${VERSION}/kompose-linux-${ARCH}" \
    -o /usr/bin/kompose
RUN chmod +x /usr/bin/kompose

CMD ["/usr/bin/kompose", "convert", "-f", "/in/compose.yaml", "--out", "/out"]
```

This Dockerfile bundles Kompose and defines the command to run this tool according
to the Compose Bridge transformation contract.

---

# Use the default Compose Bridge transformation

> Learn how to use the default Compose Bridge transformation to convert Compose files into Kubernetes manifests

# Use the default Compose Bridge transformation

   Table of contents

---

Requires: Docker Desktop 4.43.0 and later

Compose Bridge includes a built-in transformation that automatically converts your Compose configuration into a set of Kubernetes manifests.

Based on your `compose.yaml` file, it produces:

- A [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) so all your resources are isolated and don't conflict with resources from other deployments.
- A [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) with an entry for each and every
  [config](https://docs.docker.com/reference/compose-file/configs/) resource in your Compose application.
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) for application services. This ensures that the specified number of instances of your application are maintained in the Kubernetes cluster.
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/) for ports exposed by your services, used for service-to-service communication.
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/) for ports published by your services, with type `LoadBalancer` so that Docker Desktop will also expose the same port on the host.
- [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) to replicate the networking topology defined in your `compose.yaml` file.
- [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for your volumes, using `hostpath` storage class so that Docker Desktop manages volume creation.
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) with your secret encoded. This is designed for local use in a testing environment.

It also supplies a Kustomize overlay dedicated to Docker Desktop with:

- `Loadbalancer` for services which need to expose ports on host.
- A `PersistentVolumeClaim` to use the Docker Desktop storage provisioner `desktop-storage-provisioner` to handle volume provisioning more effectively.
- A `Kustomization.yaml` file to link all the resources together.

If your Compose file defines a `models` section for a service, Compose Bridge automatically configures your deployment so your service can locate and use its models via Docker Model Runner.

For each declared model, the transformation injects two environment variables:

- `<MODELNAME>_URL`: The endpoint for Docker Model Runner serving that model
- `<MODELNAME>_MODEL`: The model’s name or identifier

You can optionally customize these variable names using `endpoint_var` and `model_var`.

The default transformation generates two different overlays - one for Docker Desktop whilst using a local instance of Docker Model Runner, and a `model-runner` overlay with all the relevant Kubernetes resources to deploy Docker Model Runner in a pod.

| Environment | Endpoint |
| --- | --- |
| Docker Desktop | http://host.docker.internal:12434/engines/v1/ |
| Kubernetes | http://model-runner/engines/v1/ |

For more details, see [Use Model Runner](https://docs.docker.com/compose/bridge/use-model-runner/).

## Use the default Compose Bridge transformation

To convert your Compose file using the default transformation:

```console
$ docker compose bridge convert
```

Compose looks for a `compose.yaml` file inside the current directory and generates Kubernetes manifests.

Example output:

```console
$ docker compose -f compose.yaml bridge convert
Kubernetes resource backend-deployment.yaml created
Kubernetes resource frontend-deployment.yaml created
Kubernetes resource backend-expose.yaml created
Kubernetes resource frontend-expose.yaml created
Kubernetes resource 0-my-project-namespace.yaml created
Kubernetes resource default-network-policy.yaml created
Kubernetes resource backend-service.yaml created
Kubernetes resource frontend-service.yaml created
Kubernetes resource kustomization.yaml created
Kubernetes resource backend-deployment.yaml created
Kubernetes resource frontend-deployment.yaml created
Kubernetes resource backend-service.yaml created
Kubernetes resource frontend-service.yaml created
Kubernetes resource kustomization.yaml created
Kubernetes resource model-runner-configmap.yaml created
Kubernetes resource model-runner-deployment.yaml created
Kubernetes resource model-runner-service.yaml created
Kubernetes resource model-runner-volume-claim.yaml created
Kubernetes resource kustomization.yaml created
```

All generated files are stored in the `/out` directory in your project.

## Deploy the generated manifests

> Important
>
> Before you deploy your Compose Bridge transformations, make sure you have
> [enabled Kubernetes](https://docs.docker.com/desktop/settings-and-maintenance/settings/#kubernetes) in Docker Desktop.

Once the manifests are generated, deploy them to your local Kubernetes cluster:

```console
$ kubectl apply -k out/overlays/desktop/
```

> Tip
>
> You can convert and deploy your Compose project to a Kubernetes cluster from the Compose file viewer.
>
>
>
> Make sure you are signed in to your Docker account, navigate to your container in the **Containers** view, and in the top-right corner select **View configurations** and then **Convert and Deploy to Kubernetes**.

## Additional commands

Convert a `compose.yaml` file located in another directory:

```console
$ docker compose -f <path-to-file>/compose.yaml bridge convert
```

To see all available flags, run:

```console
$ docker compose bridge convert --help
```

## What's next?

- [Explore how you can customize Compose Bridge](https://docs.docker.com/compose/bridge/customize/)
- [Use Model Runner](https://docs.docker.com/compose/bridge/use-model-runner/).

---

# Use Docker Model Runner with Compose Bridge

> How to use Docker Model Runner with Compose Bridge for consistent deployments

# Use Docker Model Runner with Compose Bridge

   Table of contents

---

Compose Bridge supports model-aware deployments. It can deploy and configure Docker Model Runner, a lightweight service that hosts and serves machine LLMs.

This reduces manual setup for LLM-enabled services and keeps deployments consistent across Docker Desktop and Kubernetes environments.

If you have a `models` top-level element in your `compose.yaml` file, Compose Bridge:

- Automatically injects environment variables for each model’s endpoint and name.
- Configures model endpoints differently for Docker Desktop vs Kubernetes.
- Optionally deploys Docker Model Runner in Kubernetes when enabled in Helm values

## Configure model runner settings

When deploying using generated Helm Charts, you can control the model runner configuration through Helm values.

```yaml
# Model Runner settings
modelRunner:
    # Set to false for Docker Desktop (uses host instance)
    # Set to true for standalone Kubernetes clusters
    enabled: false
    # Endpoint used when enabled=false (Docker Desktop)
    hostEndpoint: "http://host.docker.internal:12434/engines/v1/"
    # Deployment settings when enabled=true
    image: "docker/model-runner:latest"
    imagePullPolicy: "IfNotPresent"
    # GPU support
    gpu:
        enabled: false
        vendor: "nvidia" # nvidia or amd
        count: 1
    # Node scheduling (uncomment and customize as needed)
    # nodeSelector:
    #   accelerator: nvidia-tesla-t4
    # tolerations: []
    # affinity: {}

    # Security context
    securityContext:
        allowPrivilegeEscalation: false
    # Environment variables (uncomment and add as needed)
    # env:
    #   DMR_ORIGINS: "http://localhost:31246"
    resources:
        limits:
            cpu: "1000m"
            memory: "2Gi"
        requests:
            cpu: "100m"
            memory: "256Mi"
    # Storage for models
    storage:
        size: "100Gi"
        storageClass: "" # Empty uses default storage class
    # Models to pre-pull
    models:
        - ai/qwen2.5:latest
        - ai/mxbai-embed-large
```

## Deploying a model runner

### Docker Desktop

When `modelRunner.enabled` is `false`, Compose Bridge configures your workloads to connect to Docker Model Runner running on the host:

```text
http://host.docker.internal:12434/engines/v1/
```

The endpoint is automatically injected into your service containers.

### Kubernetes

When `modelRunner.enabled` is `true`, Compose Bridge uses the generated manifests to deploy Docker Model Runner in your cluster, including:

- Deployment: Runs the `docker-model-runner` container
- Service: Exposes port `80` (maps to container port `12434`)
- `PersistentVolumeClaim`: Stores model files

The `modelRunner.enabled` setting also determines the number of replicas for the `model-runner-deployment`:

- When `true`, the deployment replica count is set to 1, and Docker Model Runner is deployed in the Kubernetes cluster.
- When `false`, the replica count is 0, and no Docker Model Runner resources are deployed.

---

# Overview of Compose Bridge

> Learn how Compose Bridge transforms Docker Compose files into Kubernetes manifests for seamless platform transitions

# Overview of Compose Bridge

   Table of contents

---

Requires: Docker Desktop 4.43.0 and later

Compose Bridge converts your Docker Compose configuration into platform-specific deployment formats such as Kubernetes manifests. By default, it generates:

- Kubernetes manifests
- A Kustomize overlay

These outputs are ready for deployment on Docker Desktop with
[Kubernetes enabled](https://docs.docker.com/desktop/settings-and-maintenance/settings/#kubernetes).

Compose Bridge helps you bridge the gap between Compose and Kubernetes, making it easier to adopt Kubernetes while keeping the simplicity and efficiency of Compose.

It's a flexible tool that lets you either take advantage of the [default transformation](https://docs.docker.com/compose/bridge/usage/) or [create a custom transformation](https://docs.docker.com/compose/bridge/customize/) to suit specific project needs and requirements.

## How it works

Compose Bridge uses transformations to convert a Compose model into another form.

A transformation is packaged as a Docker image that receives the fully resolved Compose model as `/in/compose.yaml` and can produce any target format file under `/out`.

Compose Bridge provides its own transformation for Kubernetes using Go templates, so that it is easy to extend for customization by replacing or appending your own templates.

For more detailed information on how these transformations work and how you can customize them for your projects, see [Customize](https://docs.docker.com/compose/bridge/customize/).

Compose Bridge also supports applications that use LLMs via Docker Model Runner.

For more details, see [Use Model Runner](https://docs.docker.com/compose/bridge/use-model-runner/).

## What's next?

- [Use Compose Bridge](https://docs.docker.com/compose/bridge/usage/)
- [Explore how you can customize Compose Bridge](https://docs.docker.com/compose/bridge/customize/)

---

# Using the Compose SDK

> Integrate Docker Compose directly into your applications with the Compose SDK.

# Using the Compose SDK

   Table of contents

---

Requires: Docker Compose [5.0.0](https://github.com/docker/compose/releases/tag/v5.0.0) and later

The `docker/compose` package can be used as a Go library by third-party applications to programmatically manage
containerized applications defined in Compose files. This SDK provides a comprehensive API that lets you
integrate Compose functionality directly into your applications, allowing you to load, validate, and manage
multi-container environments without relying on the Compose CLI.

Whether you need to orchestrate containers as part of
a deployment pipeline, build custom management tools, or embed container orchestration into your application, the
Compose SDK offers the same powerful capabilities that drive the Docker Compose command-line tool.

## Set up the SDK

To get started, create an SDK instance using the `NewComposeService()` function, which initializes a service with the
necessary configuration to interact with the Docker daemon and manage Compose projects. This service instance provides
methods for all core Compose operations including creating, starting, stopping, and removing containers, as well as
loading and validating Compose files. The service handles the underlying Docker API interactions and resource
management, allowing you to focus on your application logic.

### Requirements

Before using the SDK, make sure you're using a compatible version of the Docker CLI.

```go
require (
    github.com/docker/cli v28.5.2+incompatible
)
```

Docker CLI version 29.0.0 and later depends on the new `github.com/moby/moby` module, whereas Docker Compose v5 currently depends on `github.com/docker/docker`. This means you need to pin `docker/cli v28.5.2+incompatible` to ensure compatibility and avoid build errors.

### Example usage

Here's a basic example demonstrating how to load a Compose project and start the services:

```go
package main

import (
    "context"
    "log"

	"github.com/docker/cli/cli/command"
	"github.com/docker/cli/cli/flags"
    "github.com/docker/compose/v5/pkg/api"
    "github.com/docker/compose/v5/pkg/compose"
)

func main() {
    ctx := context.Background()

	dockerCLI, err := command.NewDockerCli()
	if err != nil {
		log.Fatalf("Failed to create docker CLI: %v", err)
	}
	err = dockerCLI.Initialize(&flags.ClientOptions{})
	if err != nil {
		log.Fatalf("Failed to initialize docker CLI: %v", err)
	}

    // Create a new Compose service instance
    service, err := compose.NewComposeService(dockerCLI)
    if err != nil {
        log.Fatalf("Failed to create compose service: %v", err)
    }

    // Load the Compose project from a compose file
    project, err := service.LoadProject(ctx, api.ProjectLoadOptions{
        ConfigPaths: []string{"compose.yaml"},
        ProjectName: "my-app",
    })
    if err != nil {
        log.Fatalf("Failed to load project: %v", err)
    }

    // Start the services defined in the Compose file
    err = service.Up(ctx, project, api.UpOptions{
        Create: api.CreateOptions{},
        Start:  api.StartOptions{},
    })
    if err != nil {
        log.Fatalf("Failed to start services: %v", err)
    }

    log.Printf("Successfully started project: %s", project.Name)
}
```

This example demonstrates the core workflow - creating a service instance, loading a project from a Compose file, and
starting the services. The SDK provides many additional operations for managing the lifecycle of your containerized
application.

## Customizing the SDK

The `NewComposeService()` function accepts optional `compose.Option` parameters to customize the SDK behavior. These
options allow you to configure I/O streams, concurrency limits, dry-run mode, and other advanced features.

```go
// Create a custom output buffer to capture logs
    var outputBuffer bytes.Buffer

    // Create a compose service with custom options
    service, err := compose.NewComposeService(dockerCLI,
        compose.WithOutputStream(&outputBuffer),          // Redirect output to custom writer
        compose.WithErrorStream(os.Stderr),               // Use stderr for errors
        compose.WithMaxConcurrency(4),                    // Limit concurrent operations
        compose.WithPrompt(compose.AlwaysOkPrompt()),     // Auto-confirm all prompts
    )
```

### Available options

- `WithOutputStream(io.Writer)`: Redirect standard output to a custom writer
- `WithErrorStream(io.Writer)`: Redirect error output to a custom writer
- `WithInputStream(io.Reader)`: Provide a custom input stream for interactive prompts
- `WithStreams(out, err, in)`: Set all I/O streams at once
- `WithMaxConcurrency(int)`: Limit the number of concurrent operations against the Docker API
- `WithPrompt(Prompt)`: Customize user confirmation behavior (use `AlwaysOkPrompt()` for non-interactive mode)
- `WithDryRun`: Run operations in dry-run mode without actually applying changes
- `WithContextInfo(api.ContextInfo)`: Set custom Docker context information
- `WithProxyConfig(map[string]string)`: Configure HTTP proxy settings for builds
- `WithEventProcessor(progress.EventProcessor)`: Receive progress events and operation notifications

These options provide fine-grained control over the SDK's behavior, making it suitable for various integration
scenarios including CLI tools, web services, automation scripts, and testing environments.

## Tracking operations withEventProcessor

The `EventProcessor` interface allows you to monitor Compose operations in real-time by receiving events about changes
applied to Docker resources such as images, containers, volumes, and networks. This is particularly useful for building
user interfaces, logging systems, or monitoring tools that need to track the progress of Compose operations.

### UnderstandingEventProcessor

A Compose operation, such as `up`, `down`, `build`, performs a series of changes to Docker resources. The
`EventProcessor` receives notifications about these changes through three key methods:

- `Start(ctx, operation)`: Called when a Compose operation begins, for example `up`
- `On(events...)`: Called with progress events for individual resource changes, for example, container starting, image
  being pulled
- `Done(operation, success)`: Called when the operation completes, indicating success or failure

Each event contains information about the resource being modified, its current status, and progress indicators when
applicable (such as download progress for image pulls).

### Event status types

Events report resource changes with the following status types:

- Working: Operation is in progress, for example, creating, starting, pulling
- Done: Operation completed successfully
- Warning: Operation completed with warnings
- Error: Operation failed

Common status text values include: `Creating`, `Created`, `Starting`, `Started`, `Running`, `Stopping`, `Stopped`,
`Removing`, `Removed`, `Building`, `Built`, `Pulling`, `Pulled`, and more.

### Built-inEventProcessorimplementations

The SDK provides three ready-to-use `EventProcessor` implementations:

- `progress.NewTTYWriter(io.Writer)`: Renders an interactive terminal UI with progress bars and task lists
  (similar to the Docker Compose CLI output)
- `progress.NewPlainWriter(io.Writer)`: Outputs simple text-based progress messages suitable for non-interactive
  environments or log files
- `progress.NewJSONWriter()`: Render events as JSON objects
- `progress.NewQuietWriter()`: (Default) Silently processes events without producing any output

Using `EventProcessor`, a custom UI can be plugged into `docker/compose`.

---

# Docker Compose Quickstart

> Follow this hands-on tutorial to learn how to use Docker Compose from defining application dependencies to experimenting with commands.

# Docker Compose Quickstart

   Table of contents

---

This tutorial aims to introduce fundamental concepts of Docker Compose by guiding you through the development of a basic Python web application.

Using the Flask framework, the application features a hit counter in Redis, providing a practical example of how Docker Compose can be applied in web development scenarios.

The concepts demonstrated here should be understandable even if you're not familiar with Python.

This is a non-normative example that demonstrates core Compose functionality.

## Prerequisites

Make sure you have:

- [Installed the latest version of Docker Compose](https://docs.docker.com/compose/install/)
- A basic understanding of Docker concepts and how Docker works

## Step 1: Set up

1. Create a directory for the project:
  ```console
  $ mkdir composetest
  $ cd composetest
  ```
2. Create a file called `app.py` in your project directory and paste the following code in:
  ```python
  import time
  import redis
  from flask import Flask
  app = Flask(__name__)
  cache = redis.Redis(host='redis', port=6379)
  def get_hit_count():
      retries = 5
      while True:
          try:
              return cache.incr('hits')
          except redis.exceptions.ConnectionError as exc:
              if retries == 0:
                  raise exc
              retries -= 1
              time.sleep(0.5)
  @app.route('/')
  def hello():
      count = get_hit_count()
      return f'Hello World! I have been seen {count} times.\n'
  ```
  In this example, `redis` is the hostname of the redis container on the
  application's network and the default port, `6379` is used.
  > Note
  >
  > Note the way the `get_hit_count` function is written. This basic retry
  > loop attempts the request multiple times if the Redis service is
  > not available. This is useful at startup while the application comes
  > online, but also makes the application more resilient if the Redis
  > service needs to be restarted anytime during the app's lifetime. In a
  > cluster, this also helps handling momentary connection drops between
  > nodes.
3. Create another file called `requirements.txt` in your project directory and
  paste the following code in:
  ```text
  flask
  redis
  ```
4. Create a `Dockerfile` and paste the following code in:
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM python:3.10-alpine
  WORKDIR /code
  ENV FLASK_APP=app.py
  ENV FLASK_RUN_HOST=0.0.0.0
  RUN apk add --no-cache gcc musl-dev linux-headers
  COPY requirements.txt requirements.txt
  RUN pip install -r requirements.txt
  EXPOSE 5000
  COPY . .
  CMD ["flask", "run", "--debug"]
  ```
  This tells Docker to:
  - Build an image starting with the Python 3.10 image.
  - Set the working directory to `/code`.
  - Set environment variables used by the `flask` command.
  - Install gcc and other dependencies
  - Copy `requirements.txt` and install the Python dependencies.
  - Add metadata to the image to describe that the container is listening on port 5000
  - Copy the current directory `.` in the project to the workdir `.` in the image.
  - Set the default command for the container to `flask run --debug`.
  > Important
  >
  > Check that the `Dockerfile` has no file extension like `.txt`. Some editors may append this file extension automatically which results in an error when you run the application.
  For more information on how to write Dockerfiles, see the
  [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

## Step 2: Define services in a Compose file

Compose simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes in a single, comprehensible YAML configuration file.

Create a file called `compose.yaml` in your project directory and paste
the following:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5000"
  redis:
    image: "redis:alpine"
```

This Compose file defines two services: `web` and `redis`.

The `web` service uses an image that's built from the `Dockerfile` in the current directory.
It then binds the container and the host machine to the exposed port, `8000`. This example service uses the default port for the Flask web server, `5000`.

The `redis` service uses a public [Redis](https://registry.hub.docker.com/_/redis/)
image pulled from the Docker Hub registry.

For more information on the `compose.yaml` file, see [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/).

## Step 3: Build and run your app with Compose

With a single command, you create and start all the services from your configuration file.

1. From your project directory, start up your application by running `docker compose up`.
  ```console
  $ docker compose up
  Creating network "composetest_default" with the default driver
  Creating composetest_web_1 ...
  Creating composetest_redis_1 ...
  Creating composetest_web_1
  Creating composetest_redis_1 ... done
  Attaching to composetest_web_1, composetest_redis_1
  web_1    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
  redis_1  | 1:C 17 Aug 22:11:10.480 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
  redis_1  | 1:C 17 Aug 22:11:10.480 # Redis version=4.0.1, bits=64, commit=00000000, modified=0, pid=1, just started
  redis_1  | 1:C 17 Aug 22:11:10.480 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
  web_1    |  * Restarting with stat
  redis_1  | 1:M 17 Aug 22:11:10.483 * Running mode=standalone, port=6379.
  redis_1  | 1:M 17 Aug 22:11:10.483 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
  web_1    |  * Debugger is active!
  redis_1  | 1:M 17 Aug 22:11:10.483 # Server initialized
  redis_1  | 1:M 17 Aug 22:11:10.483 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
  web_1    |  * Debugger PIN: 330-787-903
  redis_1  | 1:M 17 Aug 22:11:10.483 * Ready to accept connections
  ```
  Compose pulls a Redis image, builds an image for your code, and starts the
  services you defined. In this case, the code is statically copied into the image at build time.
2. Enter `http://localhost:8000/` in a browser to see the application running.
  If this doesn't resolve, you can also try `http://127.0.0.1:8000`.
  You should see a message in your browser saying:
  ```text
  Hello World! I have been seen 1 times.
  ```
  ![hello world in browser](https://docs.docker.com/compose/images/quick-hello-world-1.png)  ![hello world in browser](https://docs.docker.com/compose/images/quick-hello-world-1.png)
3. Refresh the page.
  The number should increment.
  ```text
  Hello World! I have been seen 2 times.
  ```
  ![hello world in browser](https://docs.docker.com/compose/images/quick-hello-world-2.png)  ![hello world in browser](https://docs.docker.com/compose/images/quick-hello-world-2.png)
4. Switch to another terminal window, and type `docker image ls` to list local images.
  Listing images at this point should return `redis` and `web`.
  ```console
  $ docker image ls
  REPOSITORY        TAG           IMAGE ID      CREATED        SIZE
  composetest_web   latest        e2c21aa48cc1  4 minutes ago  93.8MB
  python            3.4-alpine    84e6077c7ab6  7 days ago     82.5MB
  redis             alpine        9d8fa9aa0e5b  3 weeks ago    27.5MB
  ```
  You can inspect images with `docker inspect <tag or id>`.
5. Stop the application, either by running `docker compose down`
  from within your project directory in the second terminal, or by
  hitting `CTRL+C` in the original terminal where you started the app.

## Step 4: Edit the Compose file to use Compose Watch

Edit the `compose.yaml` file in your project directory to use `watch` so you can preview your running Compose services which are automatically updated as you edit and save your code:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5000"
    develop:
      watch:
        - action: sync
          path: .
          target: /code
  redis:
    image: "redis:alpine"
```

Whenever a file is changed, Compose syncs the file to the corresponding location under `/code` inside the container. Once copied, the bundler updates the running application without a restart.

For more information on how Compose Watch works, see
[Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/). Alternatively, see
[Manage data in containers](https://docs.docker.com/engine/storage/volumes/) for other options.

> Note
>
> For this example to work, the `--debug` option is added to the `Dockerfile`. The `--debug` option in Flask enables automatic code reload, making it possible to work on the backend API without the need to restart or rebuild the container.
> After changing the `.py` file, subsequent API calls will use the new code, but the browser UI will not automatically refresh in this small example. Most frontend development servers include native live reload support that works with Compose.

## Step 5: Re-build and run the app with Compose

From your project directory, type `docker compose watch` or `docker compose up --watch` to build and launch the app and start the file watch mode.

```console
$ docker compose watch
[+] Running 2/2
 ✔ Container docs-redis-1 Created                                                                                                                                                                                                        0.0s
 ✔ Container docs-web-1    Recreated                                                                                                                                                                                                      0.1s
Attaching to redis-1, web-1
         ⦿ watch enabled
...
```

Check the `Hello World` message in a web browser again, and refresh to see the
count increment.

## Step 6: Update the application

To see Compose Watch in action:

1. Change the greeting in `app.py` and save it. For example, change the `Hello World!`
  message to `Hello from Docker!`:
  ```python
  return f'Hello from Docker! I have been seen {count} times.\n'
  ```
2. Refresh the app in your browser. The greeting should be updated, and the
  counter should still be incrementing.
  ![hello world in browser](https://docs.docker.com/compose/images/quick-hello-world-3.png)  ![hello world in browser](https://docs.docker.com/compose/images/quick-hello-world-3.png)
3. Once you're done, run `docker compose down`.

## Step 7: Split up your services

Using multiple Compose files lets you customize a Compose application for different environments or workflows. This is useful for large applications that may use dozens of containers, with ownership distributed across multiple teams.

1. In your project folder, create a new Compose file called `infra.yaml`.
2. Cut the Redis service from your `compose.yaml` file and paste it into your new `infra.yaml` file. Make sure you add the `services` top-level attribute at the top of your file. Your `infra.yaml` file should now look like this:
  ```yaml
  services:
    redis:
      image: "redis:alpine"
  ```
3. In your `compose.yaml` file, add the `include` top-level attribute along with the path to the `infra.yaml` file.
  ```yaml
  include:
     - infra.yaml
  services:
    web:
      build: .
      ports:
        - "8000:5000"
      develop:
        watch:
          - action: sync
            path: .
            target: /code
  ```
4. Run `docker compose up` to build the app with the updated Compose files, and run it. You should see the `Hello world` message in your browser.

This is a simplified example, but it demonstrates the basic principle of `include` and how it can make it easier to modularize complex applications into sub-Compose files. For more information on `include` and working with multiple Compose files, see
[Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/).

## Step 8: Experiment with some other commands

- If you want to run your services in the background, you can pass the `-d` flag (for "detached" mode) to `docker compose up` and use `docker compose ps` to see what is currently running:
  ```console
  $ docker compose up -d
  Starting composetest_redis_1...
  Starting composetest_web_1...
  $ docker compose ps
         Name                      Command               State           Ports
  -------------------------------------------------------------------------------------
  composetest_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp
  composetest_web_1     flask run                        Up      0.0.0.0:8000->5000/tcp
  ```
- Run `docker compose --help` to see other available commands.
- If you started Compose with `docker compose up -d`, stop your services once you've finished with them:
  ```console
  $ docker compose stop
  ```
- You can bring everything down, removing the containers entirely, with the `docker compose down` command.

## Where to go next

- Try the [Sample apps with Compose](https://github.com/docker/awesome-compose)
- [Explore the full list of Compose commands](https://docs.docker.com/reference/cli/docker/compose/)
- [Explore the Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Check out the Learning Docker Compose video on LinkedIn Learning](https://www.linkedin.com/learning/learning-docker-compose/)

---

# Build dependent images

> Build images for services with shared definition

# Build dependent images

   Table of contents

---

Requires: Docker Compose [2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0) and later

To reduce push/pull time and image weight, a common practice for Compose applications is to have services
share base layers as much as possible. You typically select the same operating system base image for
all services. But you can also get one step further by sharing image layers when your images share the same
system packages. The challenge to address is then to avoid repeating the exact same Dockerfile instruction
in all services.

For illustration, this page assumes you want all your services to be built with an `alpine` base
image and install the system package `openssl`.

## Multi-stage Dockerfile

The recommended approach is to group the shared declaration in a single Dockerfile, and use multi-stage features
so that service images are built from this shared declaration.

Dockerfile:

```dockerfile
FROM alpine as base
RUN /bin/sh -c apk add --update --no-cache openssl

FROM base as service_a
# build service a
...

FROM base as service_b
# build service b
...
```

Compose file:

```yaml
services:
  a:
     build:
       target: service_a
  b:
     build:
       target: service_b
```

## Use another service's image as the base image

A popular pattern is to reuse a service image as a base image in another service.
As Compose does not parse the Dockerfile, it can't automatically detect this dependency
between services to correctly order the build execution.

a.Dockerfile:

```dockerfile
FROM alpine
RUN /bin/sh -c apk add --update --no-cache openssl
```

b.Dockerfile:

```dockerfile
FROM service_a
# build service b
```

Compose file:

```yaml
services:
  a:
     image: service_a
     build:
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
```

Legacy Docker Compose v1 used to build images sequentially, which made this pattern usable
out of the box. Compose v2 uses BuildKit to optimise builds and build images in parallel
and requires an explicit declaration.

The recommended approach is to declare the dependent base image as an additional build context:

Compose file:

```yaml
services:
  a:
     image: service_a
     build:
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM service_a` will be resolved as a dependency on service "a" which has to be built first
         service_a: "service:a"
```

With the `additional_contexts` attribute, you can refer to an image built by another service without needing to explicitly name it:

b.Dockerfile:

```dockerfile
FROM base_image
# `base_image` doesn't resolve to an actual image. This is used to point to a named additional context

# build service b
```

Compose file:

```yaml
services:
  a:
     build:
       dockerfile: a.Dockerfile
       # built image will be tagged <project_name>_a
  b:
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM base_image` will be resolved as a dependency on service "a" which has to be built first
         base_image: "service:a"
```

## Build with Bake

Using
[Bake](https://docs.docker.com/build/bake/) let you pass the complete build definition for all services
and to orchestrate build execution in the most efficient way.

To enable this feature, run Compose with the `COMPOSE_BAKE=true` variable set in your environment.

```console
$ COMPOSE_BAKE=true docker compose build
[+] Building 0.0s (0/1)
 => [internal] load local bake definitions                                 0.0s
...
[+] Building 2/2 manifest list sha256:4bd2e88a262a02ddef525c381a5bdb08c83  0.0s
 ✔ service_b  Built                                                        0.7s
 ✔ service_a  Built
```

Bake can also be selected as the default builder by editing your `$HOME/.docker/config.json` config file:

```json
{
  ...
  "plugins": {
    "compose": {
      "build": "bake"
    }
  }
  ...
}
```

## Additional resources

- [Docker Compose build reference](https://docs.docker.com/reference/cli/docker/compose/build/)
- [Learn about multi-stage Dockerfiles](https://docs.docker.com/build/building/multi-stage/)

---

# Best practices for working with environment variables in Docker Compose

> Explainer on the best ways to set, use, and manage environment variables in Compose

# Best practices for working with environment variables in Docker Compose

   Table of contents

---

#### Handle sensitive information securely

Be cautious about including sensitive data in environment variables. Consider using [Secrets](https://docs.docker.com/compose/how-tos/use-secrets/) for managing sensitive information.

#### Understand environment variable precedence

Be aware of how Docker Compose handles the [precedence of environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/) from different sources (`.env` files, shell variables, Dockerfiles).

#### Use specific environment files

Consider how your application adapts to different environments. For example development, testing, production, and use different `.env` files as needed.

#### Know interpolation

Understand how [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/) works within compose files for dynamic configurations.

#### Command line overrides

Be aware that you can [override environment variables](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#cli) from the command line when starting containers. This is useful for testing or when you have temporary changes.
