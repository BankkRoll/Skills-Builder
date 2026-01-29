# Interface: NavigationIntents and more

# Interface: NavigationIntents

> Docker extension API reference

# Interface: NavigationIntents

   Table of contents

---

**Since**

0.2.0

## Container Methods

### viewContainers

▸ **viewContainers**(): `Promise`<`void`>

Navigate to the **Containers** tab in Docker Desktop.

```typescript
ddClient.desktopUI.navigate.viewContainers()
```

#### Returns

`Promise`<`void`>

---

### viewContainer

▸ **viewContainer**(`id`): `Promise`<`void`>

Navigate to the **Container** tab in Docker Desktop.

```typescript
await ddClient.desktopUI.navigate.viewContainer(id)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`void`>

A promise that fails if the container doesn't exist.

---

### viewContainerLogs

▸ **viewContainerLogs**(`id`): `Promise`<`void`>

Navigate to the **Container logs** tab in Docker Desktop.

```typescript
await ddClient.desktopUI.navigate.viewContainerLogs(id)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`void`>

A promise that fails if the container doesn't exist.

---

### viewContainerInspect

▸ **viewContainerInspect**(`id`): `Promise`<`void`>

Navigate to the **Inspect container** view in Docker Desktop.

```typescript
await ddClient.desktopUI.navigate.viewContainerInspect(id)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`void`>

A promise that fails if the container doesn't exist.

---

### viewContainerTerminal

▸ **viewContainerTerminal**(`id`): `Promise`<`void`>

Navigate to the container terminal window in Docker Desktop.

```typescript
await ddClient.desktopUI.navigate.viewContainerTerminal(id)
```

**Since**

0.3.4

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`void`>

A promise that fails if the container doesn't exist.

---

### viewContainerStats

▸ **viewContainerStats**(`id`): `Promise`<`void`>

Navigate to the container stats to see the CPU, memory, disk read/write and network I/O usage.

```typescript
await ddClient.desktopUI.navigate.viewContainerStats(id)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`void`>

A promise that fails if the container doesn't exist.

---

## Images Methods

### viewImages

▸ **viewImages**(): `Promise`<`void`>

Navigate to the **Images** tab in Docker Desktop.

```typescript
await ddClient.desktopUI.navigate.viewImages()
```

#### Returns

`Promise`<`void`>

---

### viewImage

▸ **viewImage**(`id`, `tag`): `Promise`<`void`>

Navigate to a specific image referenced by `id` and `tag` in Docker Desktop.
In this navigation route you can find the image layers, commands, created time and size.

```typescript
await ddClient.desktopUI.navigate.viewImage(id, tag)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full image id (including sha), e.g.sha256:34ab3ae068572f4e85c448b4035e6be5e19cc41f69606535cd4d768a63432673. |
| tag | string | The tag of the image, e.g.latest,0.0.1, etc. |

#### Returns

`Promise`<`void`>

A promise that fails if the image doesn't exist.

---

## Volume Methods

### viewVolumes

▸ **viewVolumes**(): `Promise`<`void`>

Navigate to the **Volumes** tab in Docker Desktop.

```typescript
ddClient.desktopUI.navigate.viewVolumes()
```

#### Returns

`Promise`<`void`>

---

### viewVolume

▸ **viewVolume**(`volume`): `Promise`<`void`>

Navigate to a specific volume in Docker Desktop.

```typescript
await ddClient.desktopUI.navigate.viewVolume(volume)
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| volume | string | The name of the volume, e.g.my-volume. |

#### Returns

`Promise`<`void`>

---

# Interface: OpenDialogResult

> Docker extension API reference

# Interface: OpenDialogResult

   Table of contents

---

**Since**

0.2.3

## Properties

### canceled

• `Readonly` **canceled**: `boolean`

Whether the dialog was canceled.

---

### filePaths

• `Readonly` **filePaths**: `string`[]

An array of file paths chosen by the user. If the dialog is cancelled this will be an empty array.

---

### bookmarks

• `Optional` `Readonly` **bookmarks**: `string`[]

macOS only. An array matching the `filePaths` array of `base64` encoded strings which contains security scoped bookmark data. `securityScopedBookmarks` must be enabled for this to be populated.

---

# Interface: RawExecResult

> Docker extension API reference

# Interface: RawExecResult

   Table of contents

---

**Since**

0.2.0

## Hierarchy

- **RawExecResult**
  ↳ [ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)

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

---

# Interface: RequestConfig

> Docker extension API reference

# Interface: RequestConfig

   Table of contents

---

**Since**

0.2.0

## Properties

### url

• `Readonly` **url**: `string`

---

### method

• `Readonly` **method**: `string`

---

### headers

• `Readonly` **headers**: `Record`<`string`, `string`>

---

### data

• `Readonly` **data**: `any`

---

# Interface: RequestConfigV0

> Docker extension API reference

# Interface: RequestConfigV0

   Table of contents

---

## Properties

### url

• `Readonly` **url**: `string`

---

### method

• `Readonly` **method**: `string`

---

### headers

• `Readonly` **headers**: `Record`<`string`, `string`>

---

### data

• `Readonly` **data**: `any`

---

# Interface: ServiceError

> Docker extension API reference

# Interface: ServiceError

   Table of contents

---

Error thrown when an HTTP response is received with a status code that falls
out to the range of 2xx.

**Since**

0.2.0

## Properties

### name

• **name**: `string`

---

### message

• **message**: `string`

---

### statusCode

• **statusCode**: `number`

---

# Interface: SpawnOptions

> Docker extension API reference

# Interface: SpawnOptions

   Table of contents

---

**Since**

0.3.0

## Hierarchy

- [ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/)
  ↳ **SpawnOptions**

## Properties

### cwd

• `Optional` **cwd**: `string`

#### Inherited from

[ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/).[cwd](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/#cwd)

---

### env

• `Optional` **env**: `ProcessEnv`

#### Inherited from

[ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/).[env](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/#env)

---

### stream

• **stream**: [ExecStreamOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecStreamOptions/)

---

# Interface: Toast

> Docker extension API reference

# Interface: Toast

   Table of contents

---

Toasts provide a brief notification to the user.
They appear temporarily and shouldn't interrupt the user experience.
They also don't require user input to disappear.

**Since**

0.2.0

## Methods

### success

▸ **success**(`msg`): `void`

Display a toast message of type success.

```typescript
ddClient.desktopUI.toast.success("message");
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| msg | string | The message to display in the toast. |

#### Returns

`void`

---

### warning

▸ **warning**(`msg`): `void`

Display a toast message of type warning.

```typescript
ddClient.desktopUI.toast.warning("message");
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| msg | string | The message to display in the warning. |

#### Returns

`void`

---

### error

▸ **error**(`msg`): `void`

Display a toast message of type error.

```typescript
ddClient.desktopUI.toast.error("message");
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| msg | string | The message to display in the toast. |

#### Returns

`void`

---

# Extensions API Reference

> Docker extension API reference

# Extensions API Reference

   Table of contents

---

## Dashboard interfaces

- [Host](https://docs.docker.com/reference/api/extensions-sdk/Host/)
- [NavigationIntents](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/)
- [Toast](https://docs.docker.com/reference/api/extensions-sdk/Toast/)

## Other interfaces

- [ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)
- [RequestConfigV0](https://docs.docker.com/reference/api/extensions-sdk/RequestConfigV0/)
- [BackendV0](https://docs.docker.com/reference/api/extensions-sdk/BackendV0/)
- [OpenDialogResult](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)
- [Dialog](https://docs.docker.com/reference/api/extensions-sdk/Dialog/)
- [Docker](https://docs.docker.com/reference/api/extensions-sdk/Docker/)
- [DockerCommand](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/)
- [ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/)
- [SpawnOptions](https://docs.docker.com/reference/api/extensions-sdk/SpawnOptions/)
- [Exec](https://docs.docker.com/reference/api/extensions-sdk/Exec/)
- [ExecProcess](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/)
- [ExecStreamOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecStreamOptions/)
- [ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)
- [RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/)
- [Extension](https://docs.docker.com/reference/api/extensions-sdk/Extension/)
- [DesktopUI](https://docs.docker.com/reference/api/extensions-sdk/DesktopUI/)
- [ExtensionVM](https://docs.docker.com/reference/api/extensions-sdk/ExtensionVM/)
- [ExtensionHost](https://docs.docker.com/reference/api/extensions-sdk/ExtensionHost/)
- [ExtensionCli](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/)
- [HttpService](https://docs.docker.com/reference/api/extensions-sdk/HttpService/)
- [RequestConfig](https://docs.docker.com/reference/api/extensions-sdk/RequestConfig/)
- [ServiceError](https://docs.docker.com/reference/api/extensions-sdk/ServiceError/)
- [DockerDesktopClient](https://docs.docker.com/reference/api/extensions-sdk/DockerDesktopClient/)

---

# Docker Hub API changelog

> Docker Hub API changelog

# Docker Hub API changelog

   Table of contents

---

Here you can learn about the latest changes, new features, bug fixes, and known
issues for Docker Service APIs.

---

## 2025-11-21

### Updates

- Add missing `expires_at` fields on
  [PAT management](https://docs.docker.com/reference/api/hub/latest/#tag/access-tokens) endpoints.

## 2025-09-25

### Updates

- Fix
  [Assign repository group](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/CreateRepositoryGroup) endpoints request/response

---

## 2025-09-19

### New

- Add
  [Create repository](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/CreateRepository) endpoints for a given `namespace`.
- Add
  [Get repository](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/GetRepository) endpoints for a given `namespace`.
- Add
  [Check repository](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/CheckRepository) endpoints for a given `namespace`.

### Deprecations

- [Deprecate POST /v2/repositories](https://docs.docker.com/reference/api/hub/deprecated/#deprecate-legacy-createrepository)
- [Deprecate POST /v2/repositories/{namespace}](https://docs.docker.com/reference/api/hub/deprecated/#deprecate-legacy-createrepository)
- [Deprecate GET /v2/repositories/{namespace}/{repository}](https://docs.docker.com/reference/api/hub/deprecated/#deprecate-legacy-getrepository)
- [Deprecate HEAD /v2/repositories/{namespace}/{repository}](https://docs.docker.com/reference/api/hub/deprecated/#deprecate-legacy-getrepository)

---

## 2025-07-29

### New

- Add
  [Update repository immutable tags settings](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/UpdateRepositoryImmutableTags) endpoints for a given `namespace` and `repository`.
- Add
  [Verify repository immutable tags](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/VerifyRepositoryImmutableTags) endpoints for a given `namespace` and `repository`.

---

## 2025-06-27

### New

- Add
  [List repositories](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/listNamespaceRepositories) endpoints for a given `namespace`.

### Deprecations

- [Deprecate /v2/repositories/{namespace}](https://docs.docker.com/reference/api/hub/deprecated/#deprecate-legacy-listnamespacerepositories)

---

## 2025-03-25

### New

- Add
  [APIs](https://docs.docker.com/reference/api/hub/latest/#tag/org-access-tokens) for organization access token (OATs) management.

---

## 2025-03-18

### New

- Add access to
  [audit logs](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs) for org
  access tokens.

---

# Deprecated Docker Hub API endpoints

> Deprecated Docker Hub API endpoints

# Deprecated Docker Hub API endpoints

   Table of contents

---

This page provides an overview of endpoints that are deprecated in Docker Hub API.

## Endpoint deprecation policy

As changes are made to Docker there may be times when existing endpoints need to be removed or replaced with newer endpoints. Before an existing endpoint is removed it is labeled as "deprecated" within the documentation. After some time it may be removed.

## Deprecated endpoints

The following table provides an overview of the current status of deprecated endpoints:

**Deprecated**: the endpoint is marked "deprecated" and should no longer be used.

The endpoint may be removed, disabled, or change behavior in a future release.

**Removed**: the endpoint was removed, disabled, or hidden.

---

| Status | Feature | Date |
| --- | --- | --- |
| Deprecated | Deprecate undocumented create/get repository | 2025-09-19 |
| Deprecated | Deprecate /v2/repositories/{namespace} | 2025-06-27 |
|  | Create deprecation log table | 2025-06-27 |
| Removed | Docker Hub API v1 deprecation | 2022-08-23 |

---

### Deprecate legacy CreateRepository and GetRepository

Deprecate undocumented endpoints :

- `POST /v2/repositories` and `POST /v2/repositories/{namespace}` replaced by
  [Create repository](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/CreateRepository).
- `GET /v2/repositories/{namespace}/{repository}` replaced by
  [Get repository](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/GetRepository).
- `HEAD /v2/repositories/{namespace}/{repository}` replaced by
  [Check repository](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/CheckRepository).

---

### Deprecate legacy ListNamespaceRepositories

Deprecate undocumented endpoint `GET /v2/repositories/{namespace}` replaced by
[List repositories](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/listNamespaceRepositories).

---

### Create deprecation log table

Reformat page

---

### Docker Hub API v1 deprecation

Docker Hub API v1 has been deprecated. Use Docker Hub API v2 instead.

The following API routes within the v1 path will no longer work and will return a 410 status code:

- `/v1/repositories/{name}/images`
- `/v1/repositories/{name}/tags`
- `/v1/repositories/{name}/tags/{tag_name}`
- `/v1/repositories/{namespace}/{name}/images`
- `/v1/repositories/{namespace}/{name}/tags`
- `/v1/repositories/{namespace}/{name}/tags/{tag_name}`

If you want to continue using the Docker Hub API in your current applications, update your clients to use v2 endpoints.

| OLD | NEW |
| --- | --- |
| /v1/repositories/{name}/tags | /v2/namespaces/{namespace}/repositories/{repository}/tags |
| /v1/repositories/{namespace}/{name}/tags | /v2/namespaces/{namespace}/repositories/{repository}/tags |
| /v1/repositories/{namespace}/{name}/tags | /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag} |
| /v1/repositories/{namespace}/{name}/tags/{tag_name} | /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag} |

---
