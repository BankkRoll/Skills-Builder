# Extension metadata and more

# Extension metadata

> Docker extension metadata

# Extension metadata

   Table of contents

---

## The metadata.json file

The `metadata.json` file is the entry point for your extension. It contains the metadata for your extension, such as the
name, version, and description. It also contains the information needed to build and run your extension. The image for
a Docker extension must include a `metadata.json` file at the root of its filesystem.

The format of the `metadata.json` file must be:

```json
{
    "icon": "extension-icon.svg",
    "ui": ...
    "vm": ...
    "host": ...
}
```

The `ui`, `vm`, and `host` sections are optional and depend on what a given extension provides. They describe the extension content to be installed.

### UI section

The `ui` section defines a new tab that's added to the dashboard in Docker Desktop. It follows the form:

```json
"ui":{
    "dashboard-tab":
    {
        "title":"MyTitle",
        "root":"/ui",
        "src":"index.html"
    }
}
```

`root` specifies the folder where the UI code is within the extension image filesystem.
`src` specifies the entrypoint that should be loaded in the extension tab.

Other UI extension points will be available in the future.

### VM section

The `vm` section defines a backend service that runs inside the Desktop VM. It must define either an `image` or a
`compose.yaml` file that specifies what service to run in the Desktop VM.

```json
"vm": {
    "image":"${DESKTOP_PLUGIN_IMAGE}"
},
```

When you use `image`, a default compose file is generated for the extension.

> `${DESKTOP_PLUGIN_IMAGE}` is a specific keyword that allows an easy way to refer to the image packaging the extension.
> It is also possible to specify any other full image name here. However, in many cases using the same image makes
> things easier for extension development.

```json
"vm": {
    "composefile": "compose.yaml"
},
```

The Compose file, with a volume definition for example, would look like:

```yaml
services:
  myExtension:
    image: ${DESKTOP_PLUGIN_IMAGE}
    volumes:
      - /host/path:/container/path
```

### Host section

The `host` section defines executables that Docker Desktop copies on the host.

```json
"host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/myBinary"
          },
        ],
        "windows": [
          {
            "path": "/windows/myBinary.exe"
          },
        ],
        "linux": [
          {
            "path": "/linux/myBinary"
          },
        ]
      }
    ]
  }
```

`binaries` defines a list of binaries Docker Desktop copies from the extension image to the host.

`path` specifies the binary path in the image filesystem. Docker Desktop is responsible for copying these files in its own location, and the JavaScript API allows invokes these binaries.

Learn how to [invoke executables](https://docs.docker.com/extensions/extensions-sdk/guides/invoke-host-binaries/).

---

# Extension security

> Aspects of the security model of extensions

# Extension security

   Table of contents

---

## Extension capabilities

An extension can have the following optional parts:

- A user interface in HTML or JavaScript, displayed in Docker Desktop Dashboard
- A backend part that runs as a container
- Executables deployed on the host machine.

Extensions are executed with the same permissions as the Docker Desktop user. Extension capabilities include running any Docker commands (including running containers and mounting folders), running extension binaries, and accessing files on your machine that are accessible by the user running Docker Desktop.
Note that extensions are not restricted to execute binaries that they list in the [host section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) of the extension metadata: since these binaries can contain any code running as user, they can in turn execute any other commands as long as the user has rights to execute them.

The Extensions SDK provides a set of JavaScript APIs to invoke commands or invoke these binaries from the extension UI code. Extensions can also provide a backend part that starts a long-lived running container in the background.

> Important
>
> Make sure you trust the publisher or author of the extension when you install it, as the extension has the same access rights as the user running Docker Desktop.

---

# Extension architecture

> Docker extension architecture

# Extension architecture

   Table of contents

---

Extensions are applications that run inside the Docker Desktop. They're packaged as Docker images, distributed
through Docker Hub, and installed by users either through the Marketplace within the Docker Desktop Dashboard or the
Docker Extensions CLI.

Extensions can be composed of three (optional) components:

- A frontend (or User Interface): A web application displayed in a tab of the dashboard in Docker Desktop
- A backend: One or many containerized services running in the Docker Desktop VM
- Executables: Shell scripts or binaries that Docker Desktop copies on the host when installing the extension

![Overview of the three components of an extension](https://docs.docker.com/extensions/extensions-sdk/architecture/images/extensions-architecture.png)  ![Overview of the three components of an extension](https://docs.docker.com/extensions/extensions-sdk/architecture/images/extensions-architecture.png)

An extension doesn't necessarily need to have all these components, but at least one of them depending on the extension features.
To configure and run those components, Docker Desktop uses a `metadata.json` file. See the
[metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/) section for more details.

## The frontend

The frontend is basically a web application made from HTML, Javascript, and CSS. It can be built with a simple HTML
file, some vanilla Javascript or any frontend framework, such as React or Vue.js.

When Docker Desktop installs the extension, it extracts the UI folder from the extension image, as defined by the
`ui` section in the `metadata.json`. See the [ui metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#ui-section) for more details.

Every time users click on the **Extensions** tab, Docker Desktop initializes the extension's UI as if it was the first time. When they navigate away from the tab, both the UI itself and all the sub-processes started by it (if any) are terminated.

The frontend can invoke `docker` commands, communicate with the extension backend, or invoke extension executables
deployed on the host, through the [Extensions SDK](https://www.npmjs.com/package/@docker/extension-api-client).

> Tip
>
> The `docker extension init` generates a React based extension. But you can still use it as a starting point for
> your own extension and use any other frontend framework, like Vue, Angular, Svelte, etc. or event stay with
> vanilla Javascript.

Learn more about
[building a frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) for your extension.

## The backend

Alongside a frontend application, extensions can also contain one or many backend services. In most cases, the Extension does not need a backend, and features can be implemented just by invoking docker commands through the SDK. However, there are some cases when an extension requires a backend
service, for example:

- To run long-running processes that must outlive the frontend
- To store data in a local database and serve them back with a REST API
- To store the extension state, like when a button starts a long-running process, so that if you navigate away
  from the extension and come back, the frontend can pick up where it left off
- To access specific resources in the Docker Desktop VM, for example by mounting folders in the compose
  file

> Tip
>
> The `docker extension init` generates a Go backend. But you can still use it as a starting point for
> your own extension and use any other language like Node.js, Python, Java, .Net, or any other language and framework.

Usually, the backend is made of one container that runs within the Docker Desktop VM. Internally, Docker Desktop creates
a Docker Compose project, creates the container from the `image` option of the `vm` section of the `metadata.json`, and
attaches it to the Compose project. See the [ui metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#vm-section) for more details.

In some cases, a `compose.yaml` file can be used instead of an `image`. This is useful when the backend container
needs more specific options, such as mounting volumes or requesting [capabilities](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)
that can't be expressed just with a Docker image. The `compose.yaml` file can also be used to add multiple containers
needed by the extension, like a database or a message broker.
Note that, if the Compose file defines many services, the SDK can only contact the first of them.

> Note
>
> In some cases, it is useful to also interact with the Docker engine from the backend.
> See [How to use the Docker socket](https://docs.docker.com/extensions/extensions-sdk/guides/use-docker-socket-from-backend/) from the backend.

To communicate with the backend, the Extension SDK provides [functions](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/#get) to make `GET`,
`POST`, `PUT`, `HEAD`, and `DELETE` requests from the frontend. Under the hood, the communication is done through a socket
or named pipe, depending on the operating system. If the backend was listening to a port, it would be difficult to
prevent collision with other applications running on the host or in a container already. Also, some users are
running Docker Desktop in constrained environments where they can't open ports on their machines.

![Backend and frontend communication](https://docs.docker.com/extensions/extensions-sdk/architecture/images/extensions-arch-2.png)  ![Backend and frontend communication](https://docs.docker.com/extensions/extensions-sdk/architecture/images/extensions-arch-2.png)

Finally, the backend can be built with any technology, as long as it can run in a container and listen on a socket.

Learn more about
[adding a backend](https://docs.docker.com/extensions/extensions-sdk/build/backend-extension-tutorial/) to your extension.

## Executables

In addition to the frontend and the backend, extensions can also contain executables. Executables are binaries or shell scripts
that are installed on the host when the extension is installed. The frontend can invoke them with [the extension SDK](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/#invoke-an-extension-binary-on-the-host).

These executables are useful when the extension needs to interact with a third-party CLI tool, like AWS, `kubectl`, etc.
Shipping those executables with the extension ensure that the CLI tool is always available, at the right version, on
the users' machine.

When Docker Desktop installs the extension, it copies the executables on the host as defined by the `host` section in
the `metadata.json`. See the [ui metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) for more details.

![Executable and frontend communication](https://docs.docker.com/extensions/extensions-sdk/architecture/images/extensions-arch-3.png)  ![Executable and frontend communication](https://docs.docker.com/extensions/extensions-sdk/architecture/images/extensions-arch-3.png)

However, since they're executed on the users' machine, they have to be available to the platform they're running on.
For example, if you want to ship the `kubectl` executable, you need to provide a different version for Windows, Mac,
and Linux. Multi arch images will also need to include binaries built for the right arch (AMD / ARM)

See the [host metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) for more details.

Learn how to [invoke host binaries](https://docs.docker.com/extensions/extensions-sdk/guides/invoke-host-binaries/).

---

# Add a backend to your extension

> Learn how to add a backend to your extension.

# Add a backend to your extension

   Table of contents

---

Your extension can ship a backend part with which the frontend can interact with. This page provides information on why and how to add a backend.

Before you start, make sure you have installed the latest version of [Docker Desktop](https://www.docker.com/products/docker-desktop/).

> Tip
>
>
>
> Check the [Quickstart guide](https://docs.docker.com/extensions/extensions-sdk/quickstart/) and `docker extension init <my-extension>`. They provide a better base for your extension as it's more up-to-date and related to your install of Docker Desktop.

## Why add a backend?

Thanks to the Docker Extensions SDK, most of the time you should be able to do what you need from the Docker CLI
directly from [the frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/#use-the-extension-apis-client).

Nonetheless, there are some cases where you might need to add a backend to your extension. So far, extension
builders have used the backend to:

- Store data in a local database and serve them back with a REST API.
- Store the extension state, for example when a button starts a long-running process, so that if you navigate away from the extension user interface and comes back, the frontend can pick up where it left off.

For more information about extension backends, see [Architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/#the-backend).

## Add a backend to the extension

If you created your extension using the `docker extension init` command, you already have a backend setup. Otherwise, you have to first create a `vm` directory that contains the code and updates the Dockerfile to
containerize it.

Here is the extension folder structure with a backend:

```bash
.
├── Dockerfile # (1)
├── Makefile
├── metadata.json
├── ui
    └── index.html
└── vm # (2)
    ├── go.mod
    └── main.go
```

1. Contains everything required to build the backend and copy it in the extension's container filesystem.
2. The source folder that contains the backend code of the extension.

Although you can start from an empty directory or from the `vm-ui extension` [sample](https://github.com/docker/extensions-sdk/tree/main/samples),
it is highly recommended that you start from the `docker extension init` command and change it to suit your needs.

> Tip
>
> The `docker extension init` generates a Go backend. But you can still use it as a starting point for
> your own extension and use any other language like Node.js, Python, Java, .Net, or any other language and framework.

In this tutorial, the backend service simply exposes one route that returns a JSON payload that says "Hello".

```json
{ "Message": "Hello" }
```

> Important
>
> We recommend that, the frontend and the backend communicate through sockets, and named pipes on Windows, instead of
> HTTP. This prevents port collision with any other running application or container running
> on the host. Also, some Docker Desktop users are running in constrained environments where they
> can't open ports on their machines. When choosing the language and framework for your backend, make sure it
> supports sockets connection.

```go
package main

import (
	"flag"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/labstack/echo"
	"github.com/sirupsen/logrus"
)

func main() {
	var socketPath string
	flag.StringVar(&socketPath, "socket", "/run/guest/volumes-service.sock", "Unix domain socket to listen on")
	flag.Parse()

	os.RemoveAll(socketPath)

	logrus.New().Infof("Starting listening on %s\n", socketPath)
	router := echo.New()
	router.HideBanner = true

	startURL := ""

	ln, err := listen(socketPath)
	if err != nil {
		log.Fatal(err)
	}
	router.Listener = ln

	router.GET("/hello", hello)

	log.Fatal(router.Start(startURL))
}

func listen(path string) (net.Listener, error) {
	return net.Listen("unix", path)
}

func hello(ctx echo.Context) error {
	return ctx.JSON(http.StatusOK, HTTPMessageBody{Message: "hello world"})
}

type HTTPMessageBody struct {
	Message string
}
```

> Important
>
> We don't have a working example for Node yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Node)
> and let us know if you'd like a sample for Node.

> Important
>
> We don't have a working example for Python yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Python)
> and let us know if you'd like a sample for Python.

> Important
>
> We don't have a working example for Java yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Java)
> and let us know if you'd like a sample for Java.

> Important
>
> We don't have a working example for .NET. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=.Net)
> and let us know if you'd like a sample for .NET.

## Adapt the Dockerfile

> Note
>
> When using the `docker extension init`, it creates a `Dockerfile` that already contains what is needed for a Go backend.

To deploy your Go backend when installing the extension, you need first to configure the `Dockerfile`, so that it:

- Builds the backend application
- Copies the binary in the extension's container filesystem
- Starts the binary when the container starts listening on the extension socket

> Tip
>
> To ease version management, you can reuse the same image to build the frontend, build the
> backend service, and package the extension.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:17.7-alpine3.14 AS client-builder
# ... build frontend application

# Build the Go backend
FROM golang:1.17-alpine AS builder
ENV CGO_ENABLED=0
WORKDIR /backend
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=bind,source=vm/.,target=. \
    go build -trimpath -ldflags="-s -w" -o bin/service

FROM alpine:3.15
# ... add labels and copy the frontend application

COPY --from=builder /backend/bin/service /
CMD /service -socket /run/guest-services/extension-allthethings-extension.sock
```

> Important
>
> We don't have a working Dockerfile for Node yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Node)
> and let us know if you'd like a Dockerfile for Node.

> Important
>
> We don't have a working Dockerfile for Python yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Python)
> and let us know if you'd like a Dockerfile for Python.

> Important
>
> We don't have a working Dockerfile for Java yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Java)
> and let us know if you'd like a Dockerfile for Java.

> Important
>
> We don't have a working Dockerfile for .Net. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=.Net)
> and let us know if you'd like a Dockerfile for .Net.

## Configure the metadata file

To start the backend service of your extension inside the VM of Docker Desktop, you have to configure the image name
in the `vm` section of the `metadata.json` file.

```json
{
  "vm": {
    "image": "${DESKTOP_PLUGIN_IMAGE}"
  },
  "icon": "docker.svg",
  "ui": {
    ...
  }
}
```

For more information on the `vm` section of the `metadata.json`, see [Metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/).

> Warning
>
> Do not replace the `${DESKTOP_PLUGIN_IMAGE}` placeholder in the `metadata.json` file. The placeholder is replaced automatically with the correct image name when the extension is installed.

## Invoke the extension backend from your frontend

Using the [advanced frontend extension example](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/), we can invoke our extension backend.

Use the Docker Desktop Client object and then invoke the `/hello` route from the backend service with `ddClient. extension.vm.service.get` that returns the body of the response.

Replace the `ui/src/App.tsx` file with the following code:

```tsx
// ui/src/App.tsx
import React, { useEffect } from 'react';
import { createDockerDesktopClient } from "@docker/extension-api-client";

//obtain docker desktop extension client
const ddClient = createDockerDesktopClient();

export function App() {
  const ddClient = createDockerDesktopClient();
  const [hello, setHello] = useState<string>();

  useEffect(() => {
    const getHello = async () => {
      const result = await ddClient.extension.vm?.service?.get('/hello');
      setHello(JSON.stringify(result));
    }
    getHello()
  }, []);

  return (
    <Typography>{hello}</Typography>
  );
}
```

> Important
>
> We don't have an example for Vue yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> and let us know if you'd like a sample with Vue.

> Important
>
> We don't have an example for Angular yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> and let us know if you'd like a sample with Angular.

> Important
>
> We don't have an example for Svelte yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> and let us know if you'd like a sample with Svelte.

## Re-build the extension and update it

Since you have modified the configuration of the extension and added a stage in the Dockerfile, you must re-build the extension.

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

Once built, you need to update it, or install it if you haven't already done so.

```bash
docker extension update awesome-inc/my-extension:latest
```

Now you can see the backend service running in the **Containers** view of the Docker Desktop Dashboard and watch the logs when you need to debug it.

> Tip
>
> You may need to turn on the **Show system containers** option in **Settings** to see the backend container running.
> See [Show extension containers](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/#show-the-extension-containers) for more information.

Open the Docker Desktop Dashboard and select the **Containers** tab. You should see the response from the backend service
call displayed.

## What's next?

- Learn how to [share and publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).
- Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).

---

# Create an advanced frontend extension

> Advanced frontend extension tutorial

# Create an advanced frontend extension

   Table of contents

---

To start creating your extension, you first need a directory with files which range from the extension’s source code to the required extension-specific files. This page provides information on how to set up an extension with a more advanced frontend.

Before you start, make sure you have installed the latest version of
[Docker Desktop](https://docs.docker.com/desktop/release-notes/).

## Extension folder structure

The quickest way to create a new extension is to run `docker extension init my-extension` as in the
[Quickstart](https://docs.docker.com/extensions/extensions-sdk/quickstart/). This creates a new directory `my-extension` that contains a fully functional extension.

> Tip
>
> The `docker extension init` generates a React based extension. But you can still use it as a starting point for
> your own extension and use any other frontend framework, like Vue, Angular, Svelte, etc. or even stay with
> vanilla Javascript.

Although you can start from an empty directory or from the `react-extension` [sample folder](https://github.com/docker/extensions-sdk/tree/main/samples),
it's highly recommended that you start from the `docker extension init` command and change it to suit your needs.

```bash
.
├── Dockerfile # (1)
├── ui # (2)
│   ├── public # (3)
│   │   └── index.html
│   ├── src # (4)
│   │   ├── App.tsx
│   │   ├── index.tsx
│   ├── package.json
│   └── package-lock.lock
│   ├── tsconfig.json
├── docker.svg # (5)
└── metadata.json # (6)
```

1. Contains everything required to build the extension and run it in Docker Desktop.
2. High-level folder containing your front-end app source code.
3. Assets that aren’t compiled or dynamically generated are stored here. These can be static assets like logos or the robots.txt file.
4. The src, or source folder contains all the React components, external CSS files, and dynamic assets that are brought into the component files.
5. The icon that is displayed in the left-menu of the Docker Desktop Dashboard.
6. A file that provides information about the extension such as the name, description, and version.

## Adapting the Dockerfile

> Note
>
> When using the `docker extension init`, it creates a `Dockerfile` that already contains what is needed for a React
> extension.

Once the extension is created, you need to configure the `Dockerfile` to build the extension and configure the labels
that are used to populate the extension's card in the Marketplace. Here is an example of a `Dockerfile` for a React
extension:

```Dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM node:18.9-alpine3.15 AS client-builder
WORKDIR /ui
# cache packages in layer
COPY ui/package.json /ui/package.json
COPY ui/package-lock.json /ui/package-lock.json
RUN --mount=type=cache,target=/usr/src/app/.npm \
    npm set cache /usr/src/app/.npm && \
    npm ci
# install
COPY ui /ui
RUN npm run build

FROM alpine
LABEL org.opencontainers.image.title="My extension" \
    org.opencontainers.image.description="Your Desktop Extension Description" \
    org.opencontainers.image.vendor="Awesome Inc." \
    com.docker.desktop.extension.api.version="0.3.3" \
    com.docker.desktop.extension.icon="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" \
    com.docker.extension.screenshots="" \
    com.docker.extension.detailed-description="" \
    com.docker.extension.publisher-url="" \
    com.docker.extension.additional-urls="" \
    com.docker.extension.changelog=""

COPY metadata.json .
COPY docker.svg .
COPY --from=client-builder /ui/build ui
```

> Note
>
>
>
> In the example Dockerfile, you can see that the image label `com.docker.desktop.extension.icon` is set to an icon URL. The Extensions Marketplace displays this icon without installing the extension. The Dockerfile also includes `COPY docker.svg .` to copy an icon file inside the image. This second icon file is used to display the extension UI in the Dashboard, once the extension is installed.

> Important
>
> We don't have a working Dockerfile for Vue yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> and let us know if you'd like a Dockerfile for Vue.

> Important
>
> We don't have a working Dockerfile for Angular yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> and let us know if you'd like a Dockerfile for Angular.

> Important
>
> We don't have a working Dockerfile for Svelte yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> and let us know if you'd like a Dockerfile for Svelte.

## Configure the metadata file

In order to add a tab in Docker Desktop for your extension, you have to configure it in the `metadata.json`
file the root of your extension directory.

```json
{
  "icon": "docker.svg",
  "ui": {
    "dashboard-tab": {
      "title": "UI Extension",
      "root": "/ui",
      "src": "index.html"
    }
  }
}
```

The `title` property is the name of the extension that is displayed in the left-menu of the Docker Desktop Dashboard.
The `root` property is the path to the frontend application in the extension's container filesystem used by the
system to deploy it on the host.
The `src` property is the path to the HTML entry point of the frontend application within the `root` folder.

For more information on the `ui` section of the `metadata.json`, see [Metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#ui-section).

## Build the extension and install it

Now that you have configured the extension, you need to build the extension image that Docker Desktop will use to
install it.

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

This built an image tagged `awesome-inc/my-extension:latest`, you can run `docker inspect awesome-inc/my-extension:latest` to see more details about it.

Finally, you can install the extension and see it appearing in the Docker Desktop Dashboard.

```bash
docker extension install awesome-inc/my-extension:latest
```

## Use the Extension APIs client

To use the Extension APIs and perform actions with Docker Desktop, the extension must first import the
`@docker/extension-api-client` library. To install it, run the command below:

```bash
npm install @docker/extension-api-client
```

Then call the `createDockerDesktopClient` function to create a client object to call the extension APIs.

```js
import { createDockerDesktopClient } from '@docker/extension-api-client';

const ddClient = createDockerDesktopClient();
```

When using Typescript, you can also install `@docker/extension-api-client-types` as a dev dependency. This will
provide you with type definitions for the extension APIs and auto-completion in your IDE.

```bash
npm install @docker/extension-api-client-types --save-dev
```

![Auto completion in an IDE](https://docs.docker.com/extensions/extensions-sdk/build/images/types-autocomplete.png)  ![Auto completion in an IDE](https://docs.docker.com/extensions/extensions-sdk/build/images/types-autocomplete.png)

For example, you can use the `docker.cli.exec` function to get the list of all the containers via the `docker ps --all`
command and display the result in a table.

Replace the `ui/src/App.tsx` file with the following code:

```tsx
// ui/src/App.tsx
import React, { useEffect } from 'react';
import {
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from "@mui/material";
import { createDockerDesktopClient } from "@docker/extension-api-client";

//obtain docker desktop extension client
const ddClient = createDockerDesktopClient();

export function App() {
  const [containers, setContainers] = React.useState<any[]>([]);

  useEffect(() => {
    // List all containers
    ddClient.docker.cli.exec('ps', ['--all', '--format', '"{{json .}}"']).then((result) => {
      // result.parseJsonLines() parses the output of the command into an array of objects
      setContainers(result.parseJsonLines());
    });
  }, []);

  return (
    <Stack>
      <Typography data-testid="heading" variant="h3" role="title">
        Container list
      </Typography>
      <Typography
      data-testid="subheading"
      variant="body1"
      color="text.secondary"
      sx={{ mt: 2 }}
    >
      Simple list of containers using Docker Extensions SDK.
      </Typography>
      <TableContainer sx={{mt:2}}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Container id</TableCell>
              <TableCell>Image</TableCell>
              <TableCell>Command</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {containers.map((container) => (
              <TableRow
                key={container.ID}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell>{container.ID}</TableCell>
                <TableCell>{container.Image}</TableCell>
                <TableCell>{container.Command}</TableCell>
                <TableCell>{container.CreatedAt}</TableCell>
                <TableCell>{container.Status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
}
```

![Screenshot of the container list.](https://docs.docker.com/extensions/extensions-sdk/build/images/react-extension.png)  ![Screenshot of the container list.](https://docs.docker.com/extensions/extensions-sdk/build/images/react-extension.png)

> Important
>
> We don't have an example for Vue yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> and let us know if you'd like a sample with Vue.

> Important
>
> We don't have an example for Angular yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> and let us know if you'd like a sample with Angular.

> Important
>
> We don't have an example for Svelte yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> and let us know if you'd like a sample with Svelte.

## Policies enforced for the front-end code

Extension UI code is rendered in a separate electron session and doesn't have a node.js environment initialized, nor direct access to the electron APIs.

This is to limit the possible unexpected side effects to the overall Docker Dashboard.

The extension UI code can't perform privileged tasks, such as making changes to the system, or spawning sub-processes, except by using the SDK APIs provided with the extension framework.
The Extension UI code can also perform interactions with Docker Desktop, such as navigating to various places in the Dashboard, only through the extension SDK APIs.

Extensions UI parts are isolated from each other and extension UI code is running in its own session for each extension. Extensions can't access other extensions’ session data.

`localStorage` is one of the mechanisms of a browser’s web storage. It allows users to save data as key-value pairs in the browser for later use. `localStorage` doesn't clear data when the browser (the extension pane) closes. This makes it ideal for persisting data when navigating out of the extension to other parts of Docker Desktop.

If your extension uses `localStorage` to store data, other extensions running in Docker Desktop can't access the local storage of your extension. The extension’s local storage is persisted even after Docker Desktop is stopped or restarted. When an extension is upgraded, its local storage is persisted, whereas when it is uninstalled, its local storage is completely removed.

## Re-build the extension and update it

Since you have modified the code of the extension, you must build again the extension.

```console
$ docker build --tag=awesome-inc/my-extension:latest .
```

Once built, you need to update it.

```console
$ docker extension update awesome-inc/my-extension:latest
```

Now you can see the backend service running in the containers tab of the Docker Desktop Dashboard and watch the logs
when you need to debug it.

> Tip
>
> You can turn on [hot reloading](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/#hot-reloading-whilst-developing-the-ui) to avoid the need to
> rebuild the extension every time you make a change.

## What's next?

- Add a [backend](https://docs.docker.com/extensions/extensions-sdk/build/backend-extension-tutorial/) to your extension.
- Learn how to [test and debug](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/) your extension.
- Learn how to [setup CI for your extension](https://docs.docker.com/extensions/extensions-sdk/dev/continuous-integration/).
- Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).
- For more information and guidelines on building the UI, see the [Design and UI styling section](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/).
- If you want to set up user authentication for the extension, see [Authentication](https://docs.docker.com/extensions/extensions-sdk/guides/oauth2-flow/).

---

# Create a simple extension

> Minimal frontend extension tutorial

# Create a simple extension

   Table of contents

---

To start creating your extension, you first need a directory with files which range from the extension’s source code to the required extension-specific files. This page provides information on how to set up a minimal frontend extension based on plain HTML.

Before you start, make sure you have installed the latest version of
[Docker Desktop](https://docs.docker.com/desktop/release-notes/).

> Tip
>
>
>
> If you want to start a codebase for your new extension, our [Quickstart guide](https://docs.docker.com/extensions/extensions-sdk/quickstart/) and `docker extension init <my-extension>` provides a better base for your extension.

## Extension folder structure

In the `minimal-frontend` [sample folder](https://github.com/docker/extensions-sdk/tree/main/samples), you can find a ready-to-go example that represents a UI Extension built on HTML. We will go through this code example in this tutorial.

Although you can start from an empty directory, it is highly recommended that you start from the template below and change it accordingly to suit your needs.

```bash
.
├── Dockerfile # (1)
├── metadata.json # (2)
└── ui # (3)
    └── index.html
```

1. Contains everything required to build the extension and run it in Docker Desktop.
2. A file that provides information about the extension such as the name, description, and version.
3. The source folder that contains all your HTML, CSS and JS files. There can also be other static assets such as logos
  and icons. For more information and guidelines on building the UI, see the [Design and UI styling section](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/).

## Create a Dockerfile

At a minimum, your Dockerfile needs:

- [Labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/) which provide extra information about the extension, icon and screenshots.
- The source code which in this case is an `index.html` that sits within the `ui` folder.
- The `metadata.json` file.

```Dockerfile
# syntax=docker/dockerfile:1
FROM scratch

LABEL org.opencontainers.image.title="Minimal frontend" \
    org.opencontainers.image.description="A sample extension to show how easy it's to get started with Desktop Extensions." \
    org.opencontainers.image.vendor="Awesome Inc." \
    com.docker.desktop.extension.api.version="0.3.3" \
    com.docker.desktop.extension.icon="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png"

COPY ui ./ui
COPY metadata.json .
```

## Configure the metadata file

A `metadata.json` file is required at the root of the image filesystem.

```json
{
  "ui": {
    "dashboard-tab": {
      "title": "Minimal frontend",
      "root": "/ui",
      "src": "index.html"
    }
  }
}
```

For more information on the `metadata.json`, see [Metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/).

## Build the extension and install it

Now that you have configured the extension, you need to build the extension image that Docker Desktop will use to
install it.

```console
$ docker build --tag=awesome-inc/my-extension:latest .
```

This built an image tagged `awesome-inc/my-extension:latest`, you can run `docker inspect awesome-inc/my-extension:latest` to see more details about it.

Finally, you can install the extension and see it appearing in the Docker Desktop Dashboard.

```console
$ docker extension install awesome-inc/my-extension:latest
```

## Preview the extension

To preview the extension in Docker Desktop, close and open the Docker Desktop Dashboard once the installation is complete.

The left-hand menu displays a new tab with the name of your extension.

![Minimal frontend extension](https://docs.docker.com/extensions/extensions-sdk/build/images/ui-minimal-extension.png)  ![Minimal frontend extension](https://docs.docker.com/extensions/extensions-sdk/build/images/ui-minimal-extension.png)

## What's next?

- Build a more [advanced frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) extension.
- Learn how to [test and debug](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/) your extension.
- Learn how to [setup CI for your extension](https://docs.docker.com/extensions/extensions-sdk/dev/continuous-integration/).
- Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).

---

# Design guidelines for Docker extensions

> Docker extension design

# Design guidelines for Docker extensions

   Table of contents

---

At Docker, we aim to build tools that integrate into a user's existing workflows rather than requiring them to adopt new ones. We strongly recommend that you follow these guidelines when creating extensions. We review and approve your Marketplace publication based on these requirements.

Here is a simple checklist to go through when creating your extension:

- Is it easy to get started?
- Is it easy to use?
- Is it easy to get help when needed?

## Create a consistent experience with Docker Desktop

Use the [Docker Material UI Theme](https://www.npmjs.com/package/@docker/docker-mui-theme) and the [Docker Extensions Styleguide](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771) to ensure that your extension feels like it is part of Docker Desktop to create a seamless experience for users.

- Ensure the extension has both a light and dark theme. Using the components and styles as per the Docker style guide ensures that your extension meets the [level AA accessibility standard.](https://www.w3.org/WAI/WCAG2AA-Conformance).
  ![Light and dark mode](https://docs.docker.com/extensions/extensions-sdk/design/images/light_dark_mode.webp)  ![Light and dark mode](https://docs.docker.com/extensions/extensions-sdk/design/images/light_dark_mode.webp)
- Ensure that your extension icon is visible both in light and dark mode.
  ![Icon colors in light and dark mode](https://docs.docker.com/extensions/extensions-sdk/design/images/icon_colors.webp)  ![Icon colors in light and dark mode](https://docs.docker.com/extensions/extensions-sdk/design/images/icon_colors.webp)
- Ensure that the navigational behavior is consistent with the rest of Docker Desktop. Add a header to set the context for the extension.
  ![Header that sets the context](https://docs.docker.com/extensions/extensions-sdk/design/images/header.webp)  ![Header that sets the context](https://docs.docker.com/extensions/extensions-sdk/design/images/header.webp)
- Avoid embedding terminal windows. The advantage we have with Docker Desktop over the CLI is that we have the opportunity to provide rich information to users. Make use of this interface as much as possible.
  ![Terminal window used incorrectly](https://docs.docker.com/extensions/extensions-sdk/design/images/terminal_window_dont.webp)  ![Terminal window used incorrectly](https://docs.docker.com/extensions/extensions-sdk/design/images/terminal_window_dont.webp)![Terminal window used correctly](https://docs.docker.com/extensions/extensions-sdk/design/images/terminal_window_do.webp)  ![Terminal window used correctly](https://docs.docker.com/extensions/extensions-sdk/design/images/terminal_window_do.webp)

## Build features natively

- In order not to disrupt the flow of users, avoid scenarios where the user has to navigate outside Docker Desktop, to the CLI or a webpage for example, in order to carry out certain functionalities. Instead, build features that are native to Docker Desktop.
  ![Incorrect way to switch context](https://docs.docker.com/extensions/extensions-sdk/design/images/switch_context_dont.webp)  ![Incorrect way to switch context](https://docs.docker.com/extensions/extensions-sdk/design/images/switch_context_dont.webp)![Correct way to switch context](https://docs.docker.com/extensions/extensions-sdk/design/images/switch_context_do.webp)  ![Correct way to switch context](https://docs.docker.com/extensions/extensions-sdk/design/images/switch_context_do.webp)

## Break down complicated user flows

- If a flow is too complicated or the concept is abstract, break down the flow into multiple steps with one simple call-to-action in each step. This helps when onboarding novice users to your extension
  ![A complicated flow](https://docs.docker.com/extensions/extensions-sdk/design/images/complicated_flows.webp)  ![A complicated flow](https://docs.docker.com/extensions/extensions-sdk/design/images/complicated_flows.webp)
- Where there are multiple call-to-actions, ensure you use the primary (filled button style) and secondary buttons (outline button style) to convey the importance of each action.
  ![Call to action](https://docs.docker.com/extensions/extensions-sdk/design/images/cta.webp)  ![Call to action](https://docs.docker.com/extensions/extensions-sdk/design/images/cta.webp)

## Onboarding new users

When creating your extension, ensure that first time users of the extension and your product can understand its value-add and adopt it easily. Ensure you include contextual help within the extension.

- Ensure that all necessary information is added to the extensions Marketplace as well as the extensions detail page. This should include:
  - Screenshots of the extension. Note that the recommended size for screenshots is 2400x1600 pixels.
  - A detailed description that covers what the purpose of the extension is, who would find it useful and how it works.
  - Link to necessary resources such as documentation.
- If your extension has particularly complex functionality, add a demo or video to the start page. This helps onboard a first time user quickly.
  ![start page](https://docs.docker.com/extensions/extensions-sdk/design/images/start_page.webp)  ![start page](https://docs.docker.com/extensions/extensions-sdk/design/images/start_page.webp)

## What's next?

- Explore our [design principles](https://docs.docker.com/extensions/extensions-sdk/design/design-principles/).
- Take a look at our [UI styling guidelines](https://docs.docker.com/extensions/extensions-sdk/design/).
- Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

---

# Docker design principles

> Docker extension design

# Docker design principles

   Table of contents

---

## Provide actionable guidance

We anticipate needs and provide simple explanations with clear actions so people are never lost and always know what to do next. Recommendations lead users to functionality that enhances the experience and extends their knowledge.

## Create value through confidence

People from all levels of experience should feel they know how to use our product. Experiences are familiar, unified, and easy to use so all users feel like experts.

## Infuse productivity with delight

We seek out moments of purposeful delight that elevate rather than distract, making work easier and more gratifying. Simple tasks are automated and users are left with more time for innovation.

## Build trust through transparency

We always provide clarity on what is happening and why. No amount of detail is withheld; the right information is shown at the right time and is always accessible.

## Scale with intention

Our products focus on inclusive growth and are continuously useful and adapt to match changing individual needs. We support all levels of expertise by meeting users where they are with conscious personalization.

## What's next?

- Take a look at our [UI styling guidelines](https://docs.docker.com/extensions/extensions-sdk/design/).
- Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).
