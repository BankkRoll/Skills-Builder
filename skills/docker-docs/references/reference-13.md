# Docker Engine API and more

# Docker Engine API

> Learn how you can use Docker Engine API and SDKs in the language of your choice.

# Docker Engine API

   Table of contents

---

Docker provides an API for interacting with the Docker daemon (called the Docker
Engine API), as well as SDKs for Go and Python. The SDKs allow you to efficiently build and
scale Docker apps and solutions. If Go or Python don't work
for you, you can use the Docker Engine API directly.

For information about Docker Engine SDKs, see [Develop with Docker Engine SDKs](https://docs.docker.com/reference/api/engine/sdk/).

The Docker Engine API is a RESTful API accessed by an HTTP client such as `wget` or
`curl`, or the HTTP library which is part of most modern programming languages.

## View the API reference

You can
[view the reference for the latest version of the API](https://docs.docker.com/reference/api/engine/version/v1.53/)
or
[choose a specific version](https://docs.docker.com/reference/api/engine/#api-version-matrix).

## Versioned API and SDK

The version of the Docker Engine API you should use depends upon the version of
your Docker daemon and Docker client.

A given version of the Docker Engine SDK supports a specific version of the
Docker Engine API, as well as all earlier versions. If breaking changes occur,
they are documented prominently.

> Note
>
> The Docker daemon and client don't necessarily need to be the same version
> at all times. However, keep the following in mind.
>
>
>
> - If the daemon is newer than the client, the client doesn't know about new
>   features or deprecated API endpoints in the daemon.
> - If the client is newer than the daemon, the client can request API
>   endpoints that the daemon doesn't know about.

A new version of the API is released when new features are added. The Docker API
is backward-compatible, so you don't need to update code that uses the API
unless you need to take advantage of new features.

To see the highest version of the API your Docker daemon and client support, use
`docker version`:

```console
$ docker version
Client: Docker Engine - Community
 Version:           29.2.0-rc.2
 API version:       1.53
 Go version:        go1.25.6
 Git commit:        d5ed037
 Built:             Mon Jan 19 12:05:12 2026
 OS/Arch:           linux/arm64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          29.2.0-rc.2
  API version:      1.53 (minimum version 1.44)
  Go version:       go1.25.6
  Git commit:       f164e50
  Built:            Mon Jan 19 12:05:12 2026
  OS/Arch:          linux/arm64
  ...
```

You can specify the API version to use in any of the following ways:

- When using the SDK, use the latest version. At a minimum, use the version
  that incorporates the API version with the features you need.
- When using `curl` directly, specify the version as the first part of the URL.
  For instance, if the endpoint is `/containers/` you can use
  `/v1.53/containers/`.
- To force the Docker CLI or the Docker Engine SDKs to use an older version
  of the API than the version reported by `docker version`, set the
  environment variable `DOCKER_API_VERSION` to the correct version. This works
  on Linux, Windows, or macOS clients.
  ```console
  $ DOCKER_API_VERSION=1.52
  ```
  While the environment variable is set, that version of the API is used, even
  if the Docker daemon supports a newer version. This environment variable
  disables API version negotiation, so you should only use it if you must
  use a specific version of the API, or for debugging purposes.
- The Docker Go SDK allows you to enable API version negotiation, automatically
  selects an API version that's supported by both the client and the Docker Engine
  that's in use.
- For the SDKs, you can also specify the API version programmatically as a
  parameter to the `client` object. See the
  [Go constructor](https://pkg.go.dev/github.com/docker/docker/client#NewClientWithOpts)
  or the
  [Python SDK documentation forclient](https://docker-py.readthedocs.io/en/stable/client.html).

### API version matrix

| Docker version | Maximum API version | Change log |
| --- | --- | --- |
| 29.0 | 1.52 | changes |
| 28.3 | 1.51 | changes |
| 28.2 | 1.50 | changes |
| 28.1 | 1.49 | changes |
| 28.0 | 1.48 | changes |
| 27.5 | 1.47 | changes |
| 27.4 | 1.47 | changes |
| 27.3 | 1.47 | changes |
| 27.2 | 1.47 | changes |
| 27.1 | 1.46 | changes |
| 27.0 | 1.46 | changes |
| 26.1 | 1.45 | changes |
| 26.0 | 1.45 | changes |
| 25.0 | 1.44 | changes |
| 24.0 | 1.43 | changes |
| 23.0 | 1.42 | changes |
| 20.10 | 1.41 | changes |
| 19.03 | 1.40 | changes |
| 18.09 | 1.39 | changes |
| 18.06 | 1.38 | changes |
| 18.05 | 1.37 | changes |
| 18.04 | 1.37 | changes |
| 18.03 | 1.37 | changes |
| 18.02 | 1.36 | changes |
| 17.12 | 1.35 | changes |
| 17.11 | 1.34 | changes |
| 17.10 | 1.33 | changes |
| 17.09 | 1.32 | changes |
| 17.07 | 1.31 | changes |
| 17.06 | 1.30 | changes |
| 17.05 | 1.29 | changes |
| 17.04 | 1.28 | changes |
| 17.03.1 | 1.27 | changes |
| 17.03 | 1.26 | changes |
| 1.13.1 | 1.26 | changes |
| 1.13 | 1.25 | changes |
| 1.12 | 1.24 | changes |

### Deprecated API versions

API versions before v1.44 are deprecated. You can find archived documentation
for deprecated versions of the API in the code repository on GitHub:

- [Documentation for API versions 1.24–1.43](https://github.com/moby/moby/tree/28.x/docs/api).
- [Documentation for API versions 1.18–1.23](https://github.com/moby/moby/tree/v25.0.0/docs/api).
- [Documentation for API versions 1.17 and before](https://github.com/moby/moby/tree/v1.9.1/docs/reference/api).

---

# Interface: BackendV0

> Docker extension API reference

# Interface: BackendV0

   Table of contents

---

## Container Methods

### execInContainer

▸ **execInContainer**(`container`, `cmd`): `Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

Executes a command inside a container.

```typescript
const output = await window.ddClient.backend.execInContainer(container, cmd);

console.log(output);
```

> Warning
>
> It will be removed in a future version.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| container | string | - |
| cmd | string | The command to be executed. |

#### Returns

`Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

---

## HTTP Methods

### get

▸ **get**(`url`): `Promise`<`unknown`>

Performs an HTTP GET request to a backend service.

```typescript
window.ddClient.backend
 .get("/some/service")
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [get](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#get) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

### post

▸ **post**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP POST request to a backend service.

```typescript
window.ddClient.backend
 .post("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [post](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#post) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |
| data | any | The body of the request. |

#### Returns

`Promise`<`unknown`>

---

### put

▸ **put**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP PUT request to a backend service.

```typescript
window.ddClient.backend
 .put("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [put](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#put) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |
| data | any | The body of the request. |

#### Returns

`Promise`<`unknown`>

---

### patch

▸ **patch**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP PATCH request to a backend service.

```typescript
window.ddClient.backend
 .patch("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [patch](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#patch) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |
| data | any | The body of the request. |

#### Returns

`Promise`<`unknown`>

---

### delete

▸ **delete**(`url`): `Promise`<`unknown`>

Performs an HTTP DELETE request to a backend service.

```typescript
window.ddClient.backend
 .delete("/some/service")
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [delete](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#delete) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

### head

▸ **head**(`url`): `Promise`<`unknown`>

Performs an HTTP HEAD request to a backend service.

```typescript
window.ddClient.backend
 .head("/some/service")
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [head](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#head) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

### request

▸ **request**(`config`): `Promise`<`unknown`>

Performs an HTTP request to a backend service.

```typescript
window.ddClient.backend
 .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [request](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#request) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| config | RequestConfigV0 | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

## VM Methods

### execInVMExtension

▸ **execInVMExtension**(`cmd`): `Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

Executes a command inside the backend container.
If your extensions ships with additional binaries that should be run inside the backend container you can use the `execInVMExtension` function.

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);

console.log(output);
```

> Warning
>
> It will be removed in a future version. Use [exec](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/#exec) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to be executed. |

#### Returns

`Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

---

### spawnInVMExtension

▸ **spawnInVMExtension**(`cmd`, `args`, `callback`): `void`

Returns a stream from the command executed in the backend container.

```typescript
window.ddClient.spawnInVMExtension(
  `cmd`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // Once the command exits we get the status code
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> Warning
>
> It will be removed in a future version.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to be executed. |
| args | string[] | The arguments of the command to execute. |
| callback | (data:any,error:any) =>void | The callback function where to listen from the command output data and errors. |

#### Returns

`void`

---

# Interface: DesktopUI

> Docker extension API reference

# Interface: DesktopUI

   Table of contents

---

**Since**

0.2.0

## Properties

### toast

• `Readonly` **toast**: [Toast](https://docs.docker.com/reference/api/extensions-sdk/Toast/)

---

### dialog

• `Readonly` **dialog**: [Dialog](https://docs.docker.com/reference/api/extensions-sdk/Dialog/)

---

### navigate

• `Readonly` **navigate**: [NavigationIntents](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/)

---

# Interface: Dialog

> Docker extension API reference

# Interface: Dialog

   Table of contents

---

Allows opening native dialog boxes.

**Since**

0.2.3

## Methods

### showOpenDialog

▸ **showOpenDialog**(`dialogProperties`): `Promise`<[OpenDialogResult](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)>

Display a native open dialog. Lets you select a file or a folder.

```typescript
ddClient.desktopUI.dialog.showOpenDialog({properties: ['openFile']});
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| dialogProperties | any | Properties to specify the open dialog behaviour, seehttps://www.electronjs.org/docs/latest/api/dialog#dialogshowopendialogbrowserwindow-options. |

#### Returns

`Promise`<[OpenDialogResult](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)>

---

# Interface: Docker

> Docker extension API reference

# Interface: Docker

   Table of contents

---

**Since**

0.2.0

## Properties

### cli

• `Readonly` **cli**: [DockerCommand](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/)

You can also directly execute the Docker binary.

```typescript
const output = await ddClient.docker.cli.exec("volume", [
  "ls",
  "--filter",
  "dangling=true"
]);
```

Output:

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

For convenience, the command result object also has methods to easily parse it depending on output format. See [ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/) instead.

---

Streams the output as a result of the execution of a Docker command.
It is useful when the output of the command is too long, or you need to get the output as a stream.

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    onOutput(data): void {
        // As we can receive both `stdout` and `stderr`, we wrap them in a JSON object
        JSON.stringify(
          {
            stdout: data.stdout,
            stderr: data.stderr,
          },
          null,
          "  "
        );
    },
    onError(error: any): void {
      console.error(error);
    },
    onClose(exitCode: number): void {
      console.log("onClose with exit code " + exitCode);
    },
  },
});
```

## Methods

### listContainers

▸ **listContainers**(`options?`): `Promise`<`unknown`>

Get the list of running containers (same as `docker ps`).

By default, this will not list stopped containers.
You can use the option `{"all": true}` to list all the running and stopped containers.

```typescript
const containers = await ddClient.docker.listContainers();
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| options? | any | (Optional). A JSON like{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }For more information about the different properties seethe Docker API endpoint documentation. |

#### Returns

`Promise`<`unknown`>

---

### listImages

▸ **listImages**(`options?`): `Promise`<`unknown`>

Get the list of local container images

```typescript
const images = await ddClient.docker.listImages();
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| options? | any | (Optional). A JSON like{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true * }For more information about the different properties seethe Docker API endpoint documentation. |

#### Returns

`Promise`<`unknown`>

---

# Interface: DockerCommand

> Docker extension API reference

# Interface: DockerCommand

   Table of contents

---

**Since**

0.2.0

## Properties

### exec

• **exec**: [Exec](https://docs.docker.com/reference/api/extensions-sdk/Exec/)

---

# Interface: DockerDesktopClient

> Docker extension API reference

# Interface: DockerDesktopClient

   Table of contents

---

An amalgam of the v0 and v1 interfaces of the Docker Desktop API client,
provided for backwards compatibility reasons. Unless you're working with
a legacy extension, use the v1 type instead.

## Properties

### backend

• `Readonly` **backend**: `undefined` | [BackendV0](https://docs.docker.com/reference/api/extensions-sdk/BackendV0/)

The `window.ddClient.backend` object can be used to communicate with the backend defined in the vm section of
the extension metadata.
The client is already connected to the backend.

> Warning
>
> It will be removed in a future version. Use [extension](https://docs.docker.com/reference/api/extensions-sdk/DockerDesktopClient/#extension) instead.

#### Inherited from

DockerDesktopClientV0.backend

---

### extension

• `Readonly` **extension**: [Extension](https://docs.docker.com/reference/api/extensions-sdk/Extension/)

The `ddClient.extension` object can be used to communicate with the backend defined in the vm section of the
extension metadata.
The client is already connected to the backend.

#### Inherited from

DockerDesktopClientV1.extension

---

### desktopUI

• `Readonly` **desktopUI**: [DesktopUI](https://docs.docker.com/reference/api/extensions-sdk/DesktopUI/)

#### Inherited from

DockerDesktopClientV1.desktopUI

---

### host

• `Readonly` **host**: [Host](https://docs.docker.com/reference/api/extensions-sdk/Host/)

#### Inherited from

DockerDesktopClientV1.host

---

### docker

• `Readonly` **docker**: [Docker](https://docs.docker.com/reference/api/extensions-sdk/Docker/)

#### Inherited from

DockerDesktopClientV1.docker

## Container Methods

### listContainers

▸ **listContainers**(`options`): `Promise`<`unknown`>

Get the list of running containers (same as `docker ps`).

By default, this will not list stopped containers.
You can use the option `{"all": true}` to list all the running and stopped containers.

```typescript
const containers = await window.ddClient.listContainers();
```

> Warning
>
> It will be removed in a future version. Use [listContainers](https://docs.docker.com/reference/api/extensions-sdk/Docker/#listcontainers) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| options | never | (Optional). A JSON like{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }For more information about the different properties seethe Docker API endpoint documentation. |

#### Returns

`Promise`<`unknown`>

#### Inherited from

DockerDesktopClientV0.listContainers

---

## Image Methods

### listImages

▸ **listImages**(`options`): `Promise`<`unknown`>

Get the list of images

```typescript
const images = await window.ddClient.listImages();
```

> Warning
>
> It will be removed in a future version. Use [listImages](https://docs.docker.com/reference/api/extensions-sdk/Docker/#listimages) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| options | never | (Optional). A JSON like{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true }For more information about the different properties seethe Docker API endpoint documentation. |

#### Returns

`Promise`<`unknown`>

#### Inherited from

DockerDesktopClientV0.listImages

---

## Navigation Methods

### navigateToContainers

▸ **navigateToContainers**(): `void`

Navigate to the container's window in Docker Desktop.

```typescript
window.ddClient.navigateToContainers();
```

> Warning
>
> It will be removed in a future version. Use [viewContainers](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/#viewcontainers) instead.

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.navigateToContainers

---

### navigateToContainer

▸ **navigateToContainer**(`id`): `Promise`<`any`>

Navigate to the container window in Docker Desktop.

```typescript
await window.ddClient.navigateToContainer(id);
```

> Warning
>
> It will be removed in a future version.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`any`>

A promise that fails if the container doesn't exist.

#### Inherited from

DockerDesktopClientV0.navigateToContainer

---

### navigateToContainerLogs

▸ **navigateToContainerLogs**(`id`): `Promise`<`any`>

Navigate to the container logs window in Docker Desktop.

```typescript
await window.ddClient.navigateToContainerLogs(id);
```

> Warning
>
> It will be removed in a future version.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`any`>

A promise that fails if the container doesn't exist.

#### Inherited from

DockerDesktopClientV0.navigateToContainerLogs

---

### navigateToContainerInspect

▸ **navigateToContainerInspect**(`id`): `Promise`<`any`>

Navigate to the container inspect window in Docker Desktop.

```typescript
await window.ddClient.navigateToContainerInspect(id);
```

> Warning
>
> It will be removed in a future version.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`any`>

A promise that fails if the container doesn't exist.

#### Inherited from

DockerDesktopClientV0.navigateToContainerInspect

---

### navigateToContainerStats

▸ **navigateToContainerStats**(`id`): `Promise`<`any`>

Navigate to the container stats to see the CPU, memory, disk read/write and network I/O usage.

```typescript
await window.ddClient.navigateToContainerStats(id);
```

> Warning
>
> It will be removed in a future version.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`any`>

A promise that fails if the container doesn't exist.

#### Inherited from

DockerDesktopClientV0.navigateToContainerStats

---

### navigateToImages

▸ **navigateToImages**(): `void`

Navigate to the images window in Docker Desktop.

```typescript
await window.ddClient.navigateToImages(id);
```

> Warning
>
> It will be removed in a future version. Use [viewImages](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/#viewimages) instead.

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.navigateToImages

---

### navigateToImage

▸ **navigateToImage**(`id`, `tag`): `Promise`<`any`>

Navigate to a specific image referenced by `id` and `tag` in Docker Desktop.
In this navigation route you can find the image layers, commands, created time and size.

```typescript
await window.ddClient.navigateToImage(id, tag);
```

> Warning
>
> It will be removed in a future version. Use [viewImage](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/#viewimage) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full image id (including sha), e.g.sha256:34ab3ae068572f4e85c448b4035e6be5e19cc41f69606535cd4d768a63432673. |
| tag | string | The tag of the image, e.g.latest,0.0.1, etc. |

#### Returns

`Promise`<`any`>

A promise that fails if the container doesn't exist.

#### Inherited from

DockerDesktopClientV0.navigateToImage

---

### navigateToVolumes

▸ **navigateToVolumes**(): `void`

Navigate to the volumes window in Docker Desktop.

```typescript
await window.ddClient.navigateToVolumes();
```

> Warning
>
> It will be removed in a future version. Use [viewVolumes](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/#viewvolumes) instead.

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.navigateToVolumes

---

### navigateToVolume

▸ **navigateToVolume**(`volume`): `void`

Navigate to a specific volume in Docker Desktop.

```typescript
window.ddClient.navigateToVolume(volume);
```

> Warning
>
> It will be removed in a future version. Use [viewVolume](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/#viewvolume) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| volume | string | The name of the volume, e.g.my-volume. |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.navigateToVolume

---

## Other Methods

### execHostCmd

▸ **execHostCmd**(`cmd`): `Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

Invoke a binary on the host. The binary is typically shipped with your extension using the host section in the extension metadata. Note that extensions run with user access rights, this API is not restricted to binaries listed in the host section of the extension metadata (some extensions might install software during user interaction, and invoke newly installed binaries even if not listed in the extension metadata)

```typescript
window.ddClient.execHostCmd(`cliShippedOnHost xxx`).then((cmdResult: any) => {
 console.log(cmdResult);
});
```

> Warning
>
> It will be removed in a future version. Use [exec](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/#exec) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to be executed. |

#### Returns

`Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

#### Inherited from

DockerDesktopClientV0.execHostCmd

---

### spawnHostCmd

▸ **spawnHostCmd**(`cmd`, `args`, `callback`): `void`

Invoke an extension binary on your host and get the output stream.

```typescript
window.ddClient.spawnHostCmd(
  `cliShippedOnHost`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // Once the command exits we get the status code
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> Warning
>
> It will be removed in a future version. Use [exec](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/#exec) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to be executed. |
| args | string[] | The arguments of the command to execute. |
| callback | (data:any,error:any) =>void | The callback function where to listen from the command output data and errors. |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.spawnHostCmd

---

### execDockerCmd

▸ **execDockerCmd**(`cmd`, `...args`): `Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

You can also directly execute the Docker binary.

```typescript
const output = await window.ddClient.execDockerCmd("info");
```

> Warning
>
> It will be removed in a future version. Use [exec](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/#exec) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to execute. |
| ...args | string[] | The arguments of the command to execute. |

#### Returns

`Promise`<[ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

The result will contain both the standard output and the standard error of the executed command:

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

For convenience, the command result object also has methods to easily parse it depending on the output format:

- `output.lines(): string[]` splits output lines.
- `output.parseJsonObject(): any` parses a well-formed JSON output.
- `output.parseJsonLines(): any[]` parses each output line as a JSON object.

If the output of the command is too long, or you need to get the output as a stream you can use the

- spawnDockerCmd function:

```typescript
window.ddClient.spawnDockerCmd("logs", ["-f", "..."], (data, error) => {
  console.log(data.stdout);
});
```

#### Inherited from

DockerDesktopClientV0.execDockerCmd

---

### spawnDockerCmd

▸ **spawnDockerCmd**(`cmd`, `args`, `callback`): `void`

> Warning
>
> It will be removed in a future version. Use [exec](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/#exec) instead.

#### Parameters

| Name | Type |
| --- | --- |
| cmd | string |
| args | string[] |
| callback | (data:any,error:any) =>void |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.spawnDockerCmd

---

### openExternal

▸ **openExternal**(`url`): `void`

Opens an external URL with the system default browser.

```typescript
window.ddClient.openExternal("https://docker.com");
```

> Warning
>
> It will be removed in a future version. Use [openExternal](https://docs.docker.com/reference/api/extensions-sdk/Host/#openexternal) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL the browser opens (must have the protocolhttporhttps). |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.openExternal

---

## Toast Methods

### toastSuccess

▸ **toastSuccess**(`msg`): `void`

Display a toast message of type success.

```typescript
window.ddClient.toastSuccess("message");
```

> **Warning`**
>
>
>
> It will be removed in a future version. Use [success](https://docs.docker.com/reference/api/extensions-sdk/Toast/#success) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| msg | string | The message to display in the toast. |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.toastSuccess

---

### toastWarning

▸ **toastWarning**(`msg`): `void`

Display a toast message of type warning.

```typescript
window.ddClient.toastWarning("message");
```

> Warning
>
> It will be removed in a future version. Use [warning](https://docs.docker.com/reference/api/extensions-sdk/Toast/#warning) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| msg | string | The message to display in the toast. |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.toastWarning

---

### toastError

▸ **toastError**(`msg`): `void`

Display a toast message of type error.

```typescript
window.ddClient.toastError("message");
```

> Warning
>
> It will be removed in a future version. Use [error](https://docs.docker.com/reference/api/extensions-sdk/Toast/#error) instead.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| msg | string | The message to display in the toast. |

#### Returns

`void`

#### Inherited from

DockerDesktopClientV0.toastError

---

# Interface: Exec

> Docker extension API reference

# Interface: Exec

   Table of contents

---

## Callable

### Exec

▸ **Exec**(`cmd`, `args`, `options?`): `Promise`<[ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)>

Executes a command.

**Since**

0.2.0

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to execute. |
| args | string[] | The arguments of the command to execute. |
| options? | ExecOptions | The list of options. |

#### Returns

`Promise`<[ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)>

A promise that will resolve once the command finishes.

### Exec

▸ **Exec**(`cmd`, `args`, `options`): [ExecProcess](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/)

Streams the result of a command if `stream` is specified in the `options` parameter.

Specify the `stream` if the output of your command is too long or if you need to stream things indefinitely (for example container logs).

**Since**

0.2.2

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| cmd | string | The command to execute. |
| args | string[] | The arguments of the command to execute. |
| options | SpawnOptions | The list of options. |

#### Returns

[ExecProcess](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/)

The spawned process.

---

# Interface: ExecOptions

> Docker extension API reference

# Interface: ExecOptions

   Table of contents

---

**Since**

0.3.0

## Hierarchy

- **ExecOptions**
  ↳ [SpawnOptions](https://docs.docker.com/reference/api/extensions-sdk/SpawnOptions/)

## Properties

### cwd

• `Optional` **cwd**: `string`

---

### env

• `Optional` **env**: `ProcessEnv`

---

# Interface: ExecProcess

> Docker extension API reference

# Interface: ExecProcess

   Table of contents

---

**Since**

0.2.3

## Methods

### close

▸ **close**(): `void`

Close the process started by exec(streamingOptions)

#### Returns

`void`

---

# Interface: ExecResult

> Docker extension API reference

# Interface: ExecResult

   Table of contents

---

**Since**

0.2.0

## Hierarchy

- [RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/)
  ↳ **ExecResult**

## Methods

### lines

▸ **lines**(): `string`[]

Split output lines.

#### Returns

`string`[]

The list of lines.

---

### parseJsonLines

▸ **parseJsonLines**(): `any`[]

Parse each output line as a JSON object.

#### Returns

`any`[]

The list of lines where each line is a JSON object.

---

### parseJsonObject

▸ **parseJsonObject**(): `any`

Parse a well-formed JSON output.

#### Returns

`any`

The JSON object.

## Properties

### cmd

• `Optional` `Readonly` **cmd**: `string`

#### Inherited from

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[cmd](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#cmd)

---

### killed

• `Optional` `Readonly` **killed**: `boolean`

#### Inherited from

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[killed](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#killed)

---

### signal

• `Optional` `Readonly` **signal**: `string`

#### Inherited from

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[signal](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#signal)

---

### code

• `Optional` `Readonly` **code**: `number`

#### Inherited from

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[code](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#code)

---

### stdout

• `Readonly` **stdout**: `string`

#### Inherited from

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[stdout](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#stdout)

---

### stderr

• `Readonly` **stderr**: `string`

#### Inherited from

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[stderr](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#stderr)

---

# Interface: ExecResultV0

> Docker extension API reference

# Interface: ExecResultV0

   Table of contents

---

## Properties

### cmd

• `Optional` `Readonly` **cmd**: `string`

---

### killed

• `Optional` `Readonly` **killed**: `boolean`

---

### signal

• `Optional` `Readonly` **signal**: `string`

---

### code

• `Optional` `Readonly` **code**: `number`

---

### stdout

• `Readonly` **stdout**: `string`

---

### stderr

• `Readonly` **stderr**: `string`

## Methods

### lines

▸ **lines**(): `string`[]

Split output lines.

#### Returns

`string`[]

The list of lines.

---

### parseJsonLines

▸ **parseJsonLines**(): `any`[]

Parse each output line as a JSON object.

#### Returns

`any`[]

The list of lines where each line is a JSON object.

---

### parseJsonObject

▸ **parseJsonObject**(): `any`

Parse a well-formed JSON output.

#### Returns

`any`

The JSON object.

---

# Interface: ExecStreamOptions

> Docker extension API reference

# Interface: ExecStreamOptions

   Table of contents

---

**Since**

0.2.2

## Properties

### onOutput

• `Optional` **onOutput**: (`data`: { `stdout`: `string` ; `stderr?`: `undefined` } | { `stdout?`: `undefined` ; `stderr`: `string` }) => `void`

#### Type declaration

▸ (`data`): `void`

Invoked when receiving output from command execution.
By default, the output is split into chunks at arbitrary boundaries.
If you prefer the output to be split into complete lines, set `splitOutputLines`
to true. The callback is then invoked once for each line.

**Since**

0.2.0

##### Parameters

| Name | Type | Description |
| --- | --- | --- |
| data | { stdout: string; stderr?: undefined } | { stdout?: undefined; stderr: string } | Output content. Can include either stdout string, or stderr string, one at a time. |

##### Returns

`void`

---

### onError

• `Optional` **onError**: (`error`: `any`) => `void`

#### Type declaration

▸ (`error`): `void`

Invoked to report error if the executed command errors.

##### Parameters

| Name | Type | Description |
| --- | --- | --- |
| error | any | The error happening in the executed command |

##### Returns

`void`

---

### onClose

• `Optional` **onClose**: (`exitCode`: `number`) => `void`

#### Type declaration

▸ (`exitCode`): `void`

Invoked when process exits.

##### Parameters

| Name | Type | Description |
| --- | --- | --- |
| exitCode | number | The process exit code |

##### Returns

`void`

---

### splitOutputLines

• `Optional` `Readonly` **splitOutputLines**: `boolean`

Specifies the behaviour invoking `onOutput(data)`. Raw output by default, splitting output at any position. If set to true, `onOutput` will be invoked once for each line.

---

# Interface: Extension

> Docker extension API reference

# Interface: Extension

   Table of contents

---

**Since**

0.2.0

## Properties

### vm

• `Optional` `Readonly` **vm**: [ExtensionVM](https://docs.docker.com/reference/api/extensions-sdk/ExtensionVM/)

---

### host

• `Optional` `Readonly` **host**: [ExtensionHost](https://docs.docker.com/reference/api/extensions-sdk/ExtensionHost/)

---

### image

• `Readonly` **image**: `string`

**Since**

0.3.3

---

# Interface: ExtensionCli

> Docker extension API reference

# Interface: ExtensionCli

   Table of contents

---

**Since**

0.2.0

## Properties

### exec

• **exec**: [Exec](https://docs.docker.com/reference/api/extensions-sdk/Exec/)

---

# Interface: ExtensionHost

> Docker extension API reference

# Interface: ExtensionHost

   Table of contents

---

**Since**

0.2.0

## Properties

### cli

• `Readonly` **cli**: [ExtensionCli](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/)

Executes a command in the host.

For example, execute the shipped binary `kubectl -h` command in the host:

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

---

Streams the output of the command executed in the backend container or in the host.

Provided the `kubectl` binary is shipped as part of your extension, you can spawn the `kubectl -h` command in the host:

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
           stream: {
             onOutput(data): void {
                 // As we can receive both `stdout` and `stderr`, we wrap them in a JSON object
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```

---

# Interface: ExtensionVM

> Docker extension API reference

# Interface: ExtensionVM

   Table of contents

---

**Since**

0.2.0

## Properties

### cli

• `Readonly` **cli**: [ExtensionCli](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/)

Executes a command in the backend container.

Example: Execute the command `ls -l` inside the backend container:

```typescript
await ddClient.extension.vm.cli.exec(
  "ls",
  ["-l"]
);
```

Streams the output of the command executed in the backend container.

When the extension defines its own `compose.yaml` file
with multiple containers, the command is executed on the first container defined.
Change the order in which containers are defined to execute commands on another
container.

Example: Spawn the command `ls -l` inside the backend container:

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
           stream: {
             onOutput(data): void {
                 // As we can receive both `stdout` and `stderr`, we wrap them in a JSON object
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```

**Param**

Command to execute.

**Param**

Arguments of the command to execute.

**Param**

The callback function where to listen from the command output data and errors.

---

### service

• `Optional` `Readonly` **service**: [HttpService](https://docs.docker.com/reference/api/extensions-sdk/HttpService/)

---

# Interface: Host

> Docker extension API reference

# Interface: Host

   Table of contents

---

**Since**

0.2.0

## Methods

### openExternal

▸ **openExternal**(`url`): `void`

Opens an external URL with the system default browser.

**Since**

0.2.0

```typescript
ddClient.host.openExternal("https://docker.com");
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL the browser will open (must have the protocolhttporhttps). |

#### Returns

`void`

## Properties

### platform

• **platform**: `string`

Returns a string identifying the operating system platform. See [https://nodejs.org/api/os.html#osplatform](https://nodejs.org/api/os.html#osplatform)

**Since**

0.2.2

---

### arch

• **arch**: `string`

Returns the operating system CPU architecture. See [https://nodejs.org/api/os.html#osarch](https://nodejs.org/api/os.html#osarch)

**Since**

0.2.2

---

### hostname

• **hostname**: `string`

Returns the host name of the operating system. See [https://nodejs.org/api/os.html#oshostname](https://nodejs.org/api/os.html#oshostname)

**Since**

0.2.2

---

# Interface: HttpService

> Docker extension API reference

# Interface: HttpService

   Table of contents

---

**Since**

0.2.0

## Methods

### get

▸ **get**(`url`): `Promise`<`unknown`>

Performs an HTTP GET request to a backend service.

```typescript
ddClient.extension.vm.service
 .get("/some/service")
 .then((value: any) => console.log(value)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

### post

▸ **post**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP POST request to a backend service.

```typescript
ddClient.extension.vm.service
 .post("/some/service", { ... })
 .then((value: any) => console.log(value));
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |
| data | any | The body of the request. |

#### Returns

`Promise`<`unknown`>

---

### put

▸ **put**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP PUT request to a backend service.

```typescript
ddClient.extension.vm.service
 .put("/some/service", { ... })
 .then((value: any) => console.log(value));
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |
| data | any | The body of the request. |

#### Returns

`Promise`<`unknown`>

---

### patch

▸ **patch**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP PATCH request to a backend service.

```typescript
ddClient.extension.vm.service
 .patch("/some/service", { ... })
 .then((value: any) => console.log(value));
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |
| data | any | The body of the request. |

#### Returns

`Promise`<`unknown`>

---

### delete

▸ **delete**(`url`): `Promise`<`unknown`>

Performs an HTTP DELETE request to a backend service.

```typescript
ddClient.extension.vm.service
 .delete("/some/service")
 .then((value: any) => console.log(value));
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

### head

▸ **head**(`url`): `Promise`<`unknown`>

Performs an HTTP HEAD request to a backend service.

```typescript
ddClient.extension.vm.service
 .head("/some/service")
 .then((value: any) => console.log(value));
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>

---

### request

▸ **request**(`config`): `Promise`<`unknown`>

Performs an HTTP request to a backend service.

```typescript
ddClient.extension.vm.service
 .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
 .then((value: any) => console.log(value));
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| config | RequestConfig | The URL of the backend service. |

#### Returns

`Promise`<`unknown`>
