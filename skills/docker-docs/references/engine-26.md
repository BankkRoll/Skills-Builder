# Docker Engine 26.0 release notes and more

# Docker Engine 26.0 release notes

> Learn about the new features, bug fixes, and breaking changes for Docker Engine

# Docker Engine 26.0 release notes

   Table of contents

---

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 26.0.

For more information about:

- Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
- Changes to the Engine API, see
  [Engine API version history](https://docs.docker.com/reference/api/engine/version-history/).

## 26.0.2

*2024-04-18*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.0.2)
- [moby/moby, 26.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.0.2)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.0.2/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.0.2/docs/api/version-history.md).

### Security

This release contains a security fix for [CVE-2024-32473](https://github.com/moby/moby/security/advisories/GHSA-x84c-p2g9-rqv9), an unexpected configuration of IPv6 on IPv4-only interfaces.

### Bug fixes and enhancements

- [CVE-2024-32473](https://github.com/moby/moby/security/advisories/GHSA-x84c-p2g9-rqv9): Ensure IPv6 is disabled on interfaces only allocated an IPv4 address by the engine. [moby#GHSA-x84c-p2g9-rqv9](https://github.com/moby/moby/security/advisories/GHSA-x84c-p2g9-rqv9)

## 26.0.1

*2024-04-11*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.0.1)
- [moby/moby, 26.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.0.1)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.0.1/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.0.1/docs/api/version-history.md).

### Bug fixes and enhancements

- Fix a regression that meant network interface specific `--sysctl` options prevented container startup. [moby/moby#47646](https://github.com/moby/moby/pull/47646)
- Remove erroneous `platform` from image `config` OCI descriptor in `docker save` output. [moby/moby#47694](https://github.com/moby/moby/pull/47694)
- containerd image store: OCI archives produced by `docker save` will now have a non-empty `mediaType` field in `index.json` [moby/moby#47701](https://github.com/moby/moby/pull/47701)
- Fix a regression that prevented the internal resolver from forwarding requests from IPvlan L3 networks to external resolvers. [moby/moby#47705](https://github.com/moby/moby/pull/47705)
- Prevent the use of external resolvers in IPvlan and Macvlan networks created with no parent interface specified. [moby/moby#47705](https://github.com/moby/moby/pull/47705)

### Packaging updates

- Update Go runtime to 1.21.9 [moby/moby#47671](https://github.com/moby/moby/pull/47671), [docker/cli#4987](https://github.com/docker/cli/pull/4987)
- Update Compose to [v1.26.1](https://github.com/docker/compose/releases/tag/v2.26.1), [docker/docker-ce-packaging#1009](https://github.com/docker/docker-ce-packaging/pull/1009)
- Update containerd to [v1.7.15](https://github.com/containerd/containerd/releases/tag/v1.7.15) (static binaries only) [moby/moby#47692](https://github.com/moby/moby/pull/47692)

## 26.0.0

*2024-03-20*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.0.0)
- [moby/moby, 26.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.0.0)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.0.0/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.0.0/docs/api/version-history.md).

### Security

This release contains a security fix for [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx), a potential data exfiltration from 'internal' networks via authoritative DNS servers.

### New

- Add `Subpath` field to the `VolumeOptions` making it possible to mount a subpath of a volume. [moby/moby#45687](https://github.com/moby/moby/pull/45687)
- Add `volume-subpath` support to the mount flag (`--mount type=volume,...,volume-subpath=<subpath>`). [docker/cli#4331](https://github.com/docker/cli/pull/4331)
- Accept `=` separators and `[ipv6]` in compose files for `docker stack deploy`. [docker/cli#4860](https://github.com/docker/cli/pull/4860)
- rootless: Add support for enabling host loopback by setting the `DOCKERD_ROOTLESS_ROOTLESSKIT_DISABLE_HOST_LOOPBACK` environment variable to `false` (defaults to `true`). This lets containers connect to the host by using IP address `10.0.2.2`. [moby/moby#47352](https://github.com/moby/moby/pull/47352)
- containerd image store: `docker image ls` no longer creates duplicates entries for multi-platform images. [moby/moby#45967](https://github.com/moby/moby/pull/45967)
- containerd image store: Send Prometheus metrics. [moby/moby#47555](https://github.com/moby/moby/pull/47555)

### Bug fixes and enhancements

- [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx): Do not forward requests to external DNS servers for a container that is only connected to an 'internal' network. Previously, requests were forwarded if the host's DNS server was running on a loopback address, like systemd's 127.0.0.53. [moby/moby#47589](https://github.com/moby/moby/pull/47589)
- Ensure that a generated MAC address is not restored when a container is restarted, but a configured MAC address is preserved. [moby/moby#47233](https://github.com/moby/moby/pull/47233)
  > Warning
  >
  > Containers created using Docker Engine 25.0.0 may have duplicate MAC addresses, they must be re-created.
  > Containers created using version 25.0.0 or 25.0.1 with user-defined MAC addresses will get generated MAC addresses when they are started using 25.0.2. They must also be re-created.
- Always attempt to enable IPv6 on a container's loopback interface, and only include IPv6 in `/etc/hosts` if successful. [moby/moby#47062](https://github.com/moby/moby/pull/47062)
  > Note
  >
  > By default, IPv6 will remain enabled on a container's loopback interface when the container is not connected to an IPv6-enabled network.
  > For example, containers that are only connected to an IPv4-only network now have the `::1` address on their loopback interface.
  >
  >
  >
  > To disable IPv6 in a container,
  > use option `--sysctl net.ipv6.conf.all.disable_ipv6=1` in the `create` or `run` command,
  > or the equivalent `sysctls` option in the service configuration section of a Compose file.
  >
  >
  >
  > If IPv6 is not available in a container because it has been explicitly disabled for the container,
  > or the host's networking stack does not have IPv6 enabled (or for any other reason)
  > the container's `/etc/hosts` file will not include IPv6 entries.
- Fix `ADD` Dockerfile instruction failing with `lsetxattr <file>: operation not supported` when unpacking archive with xattrs onto a filesystem that doesn't support them. [moby/moby#47175](https://github.com/moby/moby/pull/47175)
- Fix `docker container start` failing when used with `--checkpoint`. [moby/moby#47456](https://github.com/moby/moby/pull/47456)
- Restore IP connectivity between the host and containers on an internal bridge network. [moby/moby#47356](https://github.com/moby/moby/pull/47356)
- Do not enforce new validation rules for existing swarm networks. [moby/moby#47361](https://github.com/moby/moby/pull/47361)
- Restore DNS names for containers in the default "nat" network on Windows. [moby/moby#47375](https://github.com/moby/moby/pull/47375)
- Print hint when invoking `docker image ls` with ambiguous argument. [docker/cli#4849](https://github.com/docker/cli/pull/4849)
- Cleanup `@docker_cli_[UUID]` files on OpenBSD. [docker/cli#4862](https://github.com/docker/cli/pull/4862)
- Add explicit [deprecation notice](https://github.com/docker/cli/blob/v26.0.0/docs/deprecated.md#unauthenticated-tcp-connections) message when using remote TCP connections without TLS. [docker/cli#4928](https://github.com/docker/cli/pull/4928), [moby/moby#47556](https://github.com/moby/moby/pull/47556)
- Use IPv6 nameservers from the host's `resolv.conf` as upstream resolvers for Docker Engine's internal DNS, rather than listing them in the container's `resolv.conf`. [moby/moby#47512](https://github.com/moby/moby/pull/47512)
- containerd image store: Isolate images with different containerd namespaces when `--userns-remap` option is used. [moby/moby#46786](https://github.com/moby/moby/pull/46786)
- containerd image store: Fix image pull not emitting `Pulling fs layer` status. [moby/moby#47432](https://github.com/moby/moby/pull/47432)

### API

- To preserve backwards compatibility, read-only mounts are not recursive by default when using older clients (API version < v1.44). [moby/moby#47391](https://github.com/moby/moby/pull/47391)
- `GET /images/{id}/json` omits the `Created` field (previously it was `0001-01-01T00:00:00Z`) if the `Created` field is missing from the image config. [moby/moby#47451](https://github.com/moby/moby/pull/47451)
- Populate a missing `Created` field in `GET /images/{id}/json` with `0001-01-01T00:00:00Z` for API version <= 1.43. [moby/moby#47387](https://github.com/moby/moby/pull/47387)
- The `is_automated` field in the `POST /images/search` endpoint results is always `false` now. Consequently, searching for `is-automated=true` will yield no results, while `is-automated=false` will be a no-op. [moby/moby#47465](https://github.com/moby/moby/pull/47465)
- Remove `Container` and `ContainerConfig` fields from the `GET /images/{name}/json` response. [moby/moby#47430](https://github.com/moby/moby/pull/47430)

### Packaging updates

- Update BuildKit to [v0.13.1](https://github.com/moby/buildkit/releases/tag/v0.13.1). [moby/moby#47582](https://github.com/moby/moby/pull/47582)
- Update Buildx to [v0.13.1](https://github.com/docker/buildx/releases/tag/v0.13.1). [docker/docker-ce-packaging#1000](https://github.com/docker/docker-ce-packaging/pull/1000)
- Update Compose to [v2.25.0](https://github.com/docker/compose/releases/tag/v2.25.0). [docker/docker-ce-packaging#1002](https://github.com/docker/docker-ce-packaging/pull/1002)
- Update Go runtime to [1.21.8](https://go.dev/doc/devel/release#go1.21.8). [moby/moby#47502](https://github.com/moby/moby/pull/47502)
- Update RootlessKit to [v2.0.2](https://github.com/rootless-containers/rootlesskit/releases/tag/v2.0.2). [moby/moby#47508](https://github.com/moby/moby/pull/47504)
- Update containerd to v1.7.13 (static binaries only) [moby/moby#47278](https://github.com/moby/moby/pull/47278)
- Update runc binary to v1.1.12 [moby/moby#47268](https://github.com/moby/moby/pull/47268)
- Update OTel to v0.46.1 / v1.21.0 [moby/moby#47245](https://github.com/moby/moby/pull/47245)

### Removed

- Remove `Container` and `ContainerConfig` fields from the `GET /images/{name}/json` response. [moby/moby#47430](https://github.com/moby/moby/pull/47430)
- Deprecate the ability to accept remote TCP connections without TLS. [Deprecation notice](https://github.com/docker/cli/tree/v26.0.0/deprecation.md#unauthenticated-tcp-connections) [docker/cli#4928](https://github.com/docker/cli/pull/4928) [moby/moby#47556](https://github.com/moby/moby/pull/47556).
- Remove deprecated API versions (API < v1.24) [moby/moby#47155](https://github.com/moby/moby/pull/47155)
- Disable pulling of deprecated image formats by default. These image formats are deprecated, and support will be removed in a future version. [moby/moby#47459](https://github.com/moby/moby/pull/47459)
- image: remove deprecated IDFromDigest [moby/moby#47198](https://github.com/moby/moby/pull/47198)
- Remove the deprecated `github.com/docker/docker/pkg/loopback` package. [moby/moby#47128](https://github.com/moby/moby/pull/47128)
- pkg/system: remove deprecated `ErrNotSupportedOperatingSystem`, `IsOSSupported` [moby/moby#47129](https://github.com/moby/moby/pull/47129)
- pkg/homedir: remove deprecated Key() and GetShortcutString() [moby/moby#47130](https://github.com/moby/moby/pull/47130)
- pkg/containerfs: remove deprecated ResolveScopedPath [moby/moby#47131](https://github.com/moby/moby/pull/47131)
- The daemon flag `--oom-score-adjust` was deprecated in v24.0 and is now removed. [moby/moby#46113](https://github.com/moby/moby/pull/46113)
- Remove deprecated aliases from the api/types package. These types were deprecated in v25.0.0, which provided temporary aliases. [moby/moby#47148](https://github.com/moby/moby/pull/47148)
  These aliases are now removed: `types.Info`, `types.Commit`, `types.PluginsInfo`, `types.NetworkAddressPool`, `types.Runtime`, `types.SecurityOpt`, `types.KeyValue`, `types.DecodeSecurityOptions`, `types.CheckpointCreateOptions`, `types.CheckpointListOptions`, `types.CheckpointDeleteOptions`, `types.Checkpoint`, `types.ImageDeleteResponseItem`, `types.ImageSummary`, `types.ImageMetadata`, `types.ServiceUpdateResponse`, `types.ServiceCreateResponse`, `types.ResizeOptions`, `types.ContainerAttachOptions`, `types.ContainerCommitOptions`, `types.ContainerRemoveOptions`, `types.ContainerStartOptions`, `types.ContainerListOptions`, `types.ContainerLogsOptions`
- cli/command/container: remove deprecated `NewStartOptions()` [docker/cli#4811](https://github.com/docker/cli/pull/4811)
- cli/command: remove deprecated `DockerCliOption`, `InitializeOpt` [docker/cli#4810](https://github.com/docker/cli/pull/4810)

---

# Docker Engine 26.1 release notes

> Learn about the new features, bug fixes, and breaking changes for Docker Engine

# Docker Engine 26.1 release notes

   Table of contents

---

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 26.1.

For more information about:

- Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
- Changes to the Engine API, see
  [Engine API version history](https://docs.docker.com/reference/api/engine/version-history/).

## 26.1.4

*2024-06-05*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.1.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.4)
- [moby/moby, 26.1.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.4)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.4/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.4/docs/api/version-history.md).

### Security

This release updates the Go runtime to 1.21.11 which contains security fixes for:

- [CVE-2024-24789](https://github.com/golang/go/issues/66869)
- [CVE-2024-24790](https://github.com/golang/go/issues/67680)
- A symlink time of check to time of use race condition during directory removal reported by [Addison Crump](https://github.com/addisoncrump).

### Bug fixes and enhancements

- Fixed an issue where promoting a node immediately after another node was demoted could cause the promotion to fail. [moby/moby#47870](https://github.com/moby/moby/pull/47870)
- Prevent the daemon log from being spammed with `superfluous response.WriteHeader call ...` messages. [moby/moby#47843](https://github.com/moby/moby/pull/47843)
- Don't show empty hints when plugins return an empty hook message. [docker/cli#5083](https://github.com/docker/cli/pull/5083)
- Fix a compatibility issue with Visual Studio Container Tools. [docker/cli#5095](https://github.com/docker/cli/pull/5095)

### Packaging updates

- Update containerd (static binaries only) to [v1.7.17](https://github.com/containerd/containerd/releases/tag/v1.7.17). [moby/moby#47841](https://github.com/moby/moby/pull/47841)
- [CVE-2024-24789](https://github.com/golang/go/issues/66869), [CVE-2024-24790](https://github.com/golang/go/issues/67680): Update Go runtime to 1.21.11. [moby/moby#47904](https://github.com/moby/moby/pull/47904)
- Update Compose to [v2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1). [docker/docker-ce-packages#1022](https://github.com/docker/docker-ce-packaging/pull/1022)
- Update Buildx to [v0.14.1](https://github.com/docker/buildx/releases/tag/v0.14.1). [docker/docker-ce-packages#1021](https://github.com/docker/docker-ce-packaging/pull/1021)

## 26.1.3

*2024-05-16*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.1.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.3)
- [moby/moby, 26.1.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.3)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.3/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.3/docs/api/version-history.md).

### Bug fixes and enhancements

- Fix a regression that prevented the use of DNS servers within a `--internal` network. [moby/moby#47832](https://github.com/moby/moby/pull/47832)
- When the internal DNS server's own address is supplied as an external server address, ignore it to avoid unproductive recursion. [moby/moby#47833](https://github.com/moby/moby/pull/47833)

### Packaging updates

- Allow runc to kill containers when confined to the runc profile in AppArmor version 4.0.0 and later. [moby/moby#47829](https://github.com/moby/moby/pull/47829)

## 26.1.2

*2024-05-08*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.1.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.2)
- [moby/moby, 26.1.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.2)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.2/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.2/docs/api/version-history.md).

### Bug fixes and enhancements

- Fix an issue where the CLI process would sometimes hang when a container failed to start. [docker/cli#5062](https://github.com/docker/cli/pull/5062)

### Packaging updates

- Update Go runtime to 1.21.10. [moby/moby#47806](https://github.com/moby/moby/pull/47806)

## 26.1.1

*2024-04-30*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.1.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.1)
- [moby/moby, 26.1.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.1)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.1/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.1/docs/api/version-history.md).

### Bug fixes and enhancements

- Fix `docker run -d` printing an `context canceled` spurious error when OpenTelemetry is configured. [docker/cli#5044](https://github.com/docker/cli/pull/5044)
- Experimental environment variable `DOCKER_BRIDGE_PRESERVE_KERNEL_LL=1` will prevent the daemon from removing the kernel-assigned link local address on a Linux bridge. [moby/moby#47775](https://github.com/moby/moby/pull/47775)
- Resolve an issue preventing container creation on hosts with a read-only `/proc/sys/net` filesystem. If IPv6 cannot be disabled on an interface due to this, either disable IPv6 by default on the host or ensure `/proc/sys/net` is read-write. To bypass the error, set the environment variable `DOCKER_ALLOW_IPV6_ON_IPV4_INTERFACE=1` before starting the Docker daemon. [moby/moby#47769](https://github.com/moby/moby/pull/47769)

> Note
>
> The `DOCKER_ALLOW_IPV6_ON_IPV4_INTERFACE` is added as a temporary fix and will be phased out in a future major release, when the IPv6 enablement process has been improved.

### Packaging updates

- Update BuildKit to [v0.13.2](https://github.com/moby/buildkit/releases/tag/v0.13.2). [moby/moby#47762](https://github.com/moby/moby/pull/47762)
- Update Compose to [v2.27.0](https://github.com/docker/compose/releases/tag/v2.27.0). [docker/docker-ce-packages#1017](https://github.com/docker/docker-ce-packaging/pull/1017)

## 26.1.0

*2024-04-22*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 26.1.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.0)
- [moby/moby, 26.1.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.0)
- Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.0/docs/deprecated.md).
- Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.0/docs/api/version-history.md).

### New

- Added configurable OpenTelemetry utilities and basic instrumentation to commands.
  For more information, see [OpenTelemetry for the Docker CLI](https://docs.docker.com/config/otel). [docker/cli#4889](https://github.com/docker/cli/pull/4889)

### Bug fixes and enhancements

- Native Windows containers are configured with an internal DNS server for container name resolution, and external DNS servers for other lookups.
  Not all resolvers, including `nslookup`, fall back to the external resolvers when they get a `SERVFAIL` answer from the internal server.
  So, the internal DNS server can now be configured to forward requests to the external resolvers, by setting a `feature` option in the `daemon.json` file:
  ```json
  {
    "features": {
      "windows-dns-proxy": true
    }
  }
  ```
  [moby/moby#47584](https://github.com/moby/moby/pull/47584)
  > Note
  >
  > - This will be the new default behavior in Docker Engine 27.0.
  > - The `windows-dns-proxy` feature flag will be removed in a future release.
- Swarm: Fix `Subpath` not being passed to the container config. [moby/moby#47711](https://github.com/moby/moby/pull/47711)
- Classic builder: Fix cache miss on `WORKDIR <directory>/` build step (directory with a trailing slash). [moby/moby#47723](https://github.com/moby/moby/pull/47723)
- containerd image store: Fix `docker images` failing when any image in the store has unexpected target. [moby/moby#47738](https://github.com/moby/moby/pull/47738)
