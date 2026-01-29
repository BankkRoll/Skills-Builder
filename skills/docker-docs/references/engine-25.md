# Docker Engine 24.0 release notes and more

# Docker Engine 24.0 release notes

> Learn about the new features, bug fixes, and breaking changes for Docker Engine

# Docker Engine 24.0 release notes

   Table of contents

---

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 24.0.

For more information about:

- Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
- Changes to the Engine API, see
  [Engine API version history](https://docs.docker.com/reference/api/engine/version-history/).

## 24.0.9

*2024-01-31*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.9 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.9)
- [moby/moby, 24.0.9 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.9)

## Security

This release contains security fixes for the following CVEs
affecting Docker Engine and its components.

| CVE | Component | Fix version | Severity |
| --- | --- | --- | --- |
| CVE-2024-21626 | runc | 1.1.12 | High, CVSS 8.6 |
| CVE-2024-24557 | Docker Engine | 24.0.9 | Medium, CVSS 6.9 |

> Important
>
> Note that this release of Docker Engine doesn't include fixes for
> the following known vulnerabilities in BuildKit:
>
>
>
> - [CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)
> - [CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652)
> - [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)
> - [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650)
>
>
>
> To address these vulnerabilities,
> upgrade to [Docker Engine v25.0.2](https://docs.docker.com/engine/release-notes/25.0/#2502).

For more information about the security issues addressed in this release,
and the unaddressed vulnerabilities in BuildKit,
refer to the
[blog post](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/).

For details about each vulnerability, see the relevant security advisory:

- [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
- [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

### Packaging updates

- Upgrade runc to [v1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12). [moby/moby#47269](https://github.com/moby/moby/pull/47269)
- Upgrade containerd to [v1.7.13](https://github.com/containerd/containerd/releases/tag/v1.7.13) (static binaries only). [moby/moby#47280](https://github.com/moby/moby/pull/47280)

## 24.0.8

*2024-01-25*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.8 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.8)
- [moby/moby, 24.0.8 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.8)

### Bug fixes and enhancements

- Live restore: Containers with auto remove (`docker run --rm`) are no longer forcibly removed on engine restart. [moby/moby#46857](https://github.com/moby/moby/pull/46869)

### Packaging updates

- Upgrade Go to `go1.20.13`. [moby/moby#47054](https://github.com/moby/moby/pull/47054), [docker/cli#4826](https://github.com/docker/cli/pull/4826), [docker/docker-ce-packaging#975](https://github.com/docker/docker-ce-packaging/pull/975)
- Upgrade containerd (static binaries only) to [v1.7.12](https://github.com/containerd/containerd/releases/tag/v1.7.12) [moby/moby#47096](https://github.com/moby/moby/pull/47096)
- Upgrade runc to v1.1.11. [moby/moby#47010](https://github.com/moby/moby/pull/47010)

## 24.0.7

*2023-10-27*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.7 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.7)
- [moby/moby, 24.0.7 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.7)

### Bug fixes and enhancements

- Write overlay2 layer metadata atomically. [moby/moby#46703](https://github.com/moby/moby/pull/46703)
- Fix "Rootful-in-Rootless" Docker-in-Docker on systemd version 250 and later. [moby/moby#46626](https://github.com/moby/moby/pull/46626)
- Fix `dockerd-rootless-setuptools.sh` when username contains a backslash. [moby/moby#46407](https://github.com/moby/moby/pull/46407)
- Fix a bug that would prevent network sandboxes to be fully deleted when stopping containers with no network attachments and when `dockerd --bridge=none` is used. [moby/moby#46702](https://github.com/moby/moby/pull/46702)
- Fix a bug where cancelling an API request could interrupt container restart. [moby/moby#46697](https://github.com/moby/moby/pull/46697)
- Fix an issue where containers would fail to start when providing `--ip-range` with a range larger than the subnet. [docker/for-mac#6870](https://github.com/docker/for-mac/issues/6870)
- Fix data corruption with zstd output. [moby/moby#46709](https://github.com/moby/moby/pull/46709)
- Fix the conditions under which the container's MAC address is applied. [moby/moby#46478](https://github.com/moby/moby/pull/46478)
- Improve the performance of the stats collector. [moby/moby#46448](https://github.com/moby/moby/pull/46448)
- Fix an issue with source policy rules ending up in the wrong order. [moby/moby#46441](https://github.com/moby/moby/pull/46441)

### Packaging updates

- Add support for Fedora 39 and Ubuntu 23.10. [docker/docker-ce-packaging#940](https://github.com/docker/docker-ce-packaging/pull/940), [docker/docker-ce-packaging#955](https://github.com/docker/docker-ce-packaging/pull/955)
- Fix `docker.socket` not getting disabled when uninstalling the `docker-ce` RPM package. [docker/docker-ce-packaging#852](https://github.com/docker/docker-ce-packaging/pull/852)
- Upgrade Go to `go1.20.10`. [docker/docker-ce-packaging#951](https://github.com/docker/docker-ce-packaging/pull/951)
- Upgrade containerd to `v1.7.6` (static binaries only). [moby/moby#46103](https://github.com/moby/moby/pull/46103)
- Upgrade the `containerd.io` package to [v1.6.24](https://github.com/containerd/containerd/releases/tag/v1.6.24).

### Security

- Deny containers access to `/sys/devices/virtual/powercap` by default. This change hardens against
  [CVE-2020-8694](https://scout.docker.com/v/CVE-2020-8694),
  [CVE-2020-8695](https://scout.docker.com/v/CVE-2020-8695), and
  [CVE-2020-12912](https://scout.docker.com/v/CVE-2020-12912),
  and an attack known as [the PLATYPUS attack](https://platypusattack.com/).
  For more details, see
  [advisory](https://github.com/moby/moby/security/advisories/GHSA-jq35-85cj-fj4p),
  [commit](https://github.com/moby/moby/commit/c9ccbfad11a60e703e91b6cca4f48927828c7e35).

## 24.0.6

*2023-09-05*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.6 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.6)
- [moby/moby, 24.0.6 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.6)

### Bug fixes and enhancements

- containerd storage backend: Fix `docker ps` failing when a container image is no longer present in the content store. [moby/moby#46095](https://github.com/moby/moby/pull/46095)
- containerd storage backend: Fix `docker ps -s -a` and `docker container prune` failing when a container image config is no longer present in the content store. [moby/moby#46097](https://github.com/moby/moby/pull/46097)
- containerd storage backend: Fix `docker inspect` failing when a container image config is no longer (or was never) present in the content store. [moby/moby#46244](https://github.com/moby/moby/pull/46244)
- containerd storage backend: Fix diff and export with the `overlayfs` snapshotter by using reference-counted rootfs mounts. [moby/moby#46266](https://github.com/moby/moby/pull/46266)
- containerd storage backend: Fix a misleading error message when the image platforms available locally do not match the desired platform. [moby/moby#46300](https://github.com/moby/moby/pull/46300)
- containerd storage backend: Fix the `FROM scratch` Dockerfile instruction with the classic builder. [moby/moby#46302](https://github.com/moby/moby/pull/46302)
- containerd storage backend: Fix `mismatched image rootfs and manifest layers` errors with the classic builder. [moby/moby#46310](https://github.com/moby/moby/pull/46310)
- Warn when pulling Docker Image Format v1, and Docker Image manifest version 2, schema 1 images from all registries. [moby/moby#46290](https://github.com/moby/moby/pull/46290)
- Fix live-restore of volumes with custom volume options. [moby/moby#46366](https://github.com/moby/moby/pull/46366)
- Fix incorrectly dropping capabilities bits when running a container as a non-root user (note: this change was already effectively present due to a regression). [moby/moby#46221](https://github.com/moby/moby/pull/46221)
- Fix network isolation iptables rules preventing IPv6 Neighbor Solicitation packets from being exchanged between containers. [moby/moby#46214](https://github.com/moby/moby/pull/46214)
- Fix `dockerd.exe --register-service` not working when the binary is in the current directory on Windows. [moby/moby#46215](https://github.com/moby/moby/pull/46215)
- Add a hint suggesting the use of a PAT to `docker login` against Docker Hub. [docker/cli#4500](https://github.com/docker/cli/pull/4500)
- Improve shell startup time for users of Bash completion for the CLI. [docker/cli#4517](https://github.com/docker/cli/pull/4517)
- Improve the speed of some commands by skipping `GET /_ping` when possible. [docker/cli#4508](https://github.com/docker/cli/pull/4508)
- Fix credential scopes when using a PAT to `docker manifest inspect` an image on Docker Hub. [docker/cli#4512](https://github.com/docker/cli/pull/4512)
- Fix `docker events` not supporting `--format=json`. [docker/cli#4544](https://github.com/docker/cli/pull/4544)

### Packaging updates

- Upgrade Go to `go1.20.7`. [moby/moby#46140](https://github.com/moby/moby/pull/46140), [docker/cli#4476](https://github.com/docker/cli/pull/4476), [docker/docker-ce-packaging#932](https://github.com/docker/docker-ce-packaging/pull/932)
- Upgrade containerd to `v1.7.3` (static binaries only). [moby/moby#46103](https://github.com/moby/moby/pull/46103)
- Upgrade Compose to `v2.21.0`. [docker/docker-ce-packaging#936](https://github.com/docker/docker-ce-packaging/pull/936)

## 24.0.5

*2023-07-24*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.5 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.5)
- [moby/moby, 24.0.5 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.5)

### Bug fixes and enhancements

- The Go client now avoids using UNIX socket paths in the HTTP `Host:` header, in order to be compatible with changes introduced in `go1.20.6`. [moby/moby#45962](https://github.com/moby/moby/pull/45962), [moby/moby#45990](https://github.com/moby/moby/pull/45990)
- containerd storage backend: Fix `Variant` not being included in `docker image inspect` and `GET /images/{name}/json`. [moby/moby#46025](https://github.com/moby/moby/pull/46025)
- containerd storage backend: Prevent potential garbage collection of content during image export. [moby/moby#46021](https://github.com/moby/moby/pull/46021)
- containerd storage backend: Prevent duplicate digest entries in `RepoDigests`. [moby/moby#46014](https://github.com/moby/moby/pull/46014)
- containerd storage backend: Fix operations taking place against the incorrect tag when working with an image referenced by tag and digest. [moby/moby#46013](https://github.com/moby/moby/pull/46013)
- containerd storage backend: Fix a panic caused by `EXPOSE` when building containers with the legacy builder. [moby/moby#45921](https://github.com/moby/moby/pull/45921)
- Fix a regression causing unintuitive errors to be returned when attempting to create an `overlay` network on a non-Swarm node. [moby/moby#45974](https://github.com/moby/moby/pull/45974)
- Properly report errors parsing volume specifications from the command line. [docker/cli#4423](https://github.com/docker/cli/pull/4423)
- Fix a panic caused when `auths: null` is found in the CLI config file. [docker/cli#4450](https://github.com/docker/cli/pull/4450)

### Packaging updates

- Use init scripts as provided by in moby/moby `contrib/init`. [docker/docker-ce-packaging#914](https://github.com/docker/docker-ce-packaging/pull/914), [docker/docker-ce-packaging#926](https://github.com/docker/docker-ce-packaging/pull/926)
- Drop Upstart from `contrib/init`. [moby/moby#46044](https://github.com/moby/moby/pull/46044)
- Upgrade Go to `go1.20.6`. [docker/cli#4428](https://github.com/docker/cli/pull/4428), [moby/moby#45970](https://github.com/moby/moby/pull/45970), [docker/docker-ce-packaging#921](https://github.com/docker/docker-ce-packaging/pull/921)
- Upgrade Compose to `v2.20.2`. [docker/docker-ce-packaging#924](https://github.com/docker/docker-ce-packaging/pull/924)
- Upgrade buildx to `v0.11.2`. [docker/docker-ce-packaging#922](https://github.com/docker/docker-ce-packaging/pull/922)

## 24.0.4

*2023-07-07*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.4)
- [moby/moby, 24.0.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.4)

### Bug fixes and enhancements

- Fix a regression introduced during 24.0.3 that causes a panic during live-restore of containers with bind mounts. [moby/moby#45903](https://github.com/moby/moby/pull/45903)

## 24.0.3

*2023-07-06*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.3)
- [moby/moby, 24.0.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.3)

### Bug fixes and enhancements

- containerd image store: Fix an issue where multi-platform images that did not include a manifest for the default platform could not be interacted with. [moby/moby#45849](https://github.com/moby/moby/pull/45849)
- containerd image store: Fix specious attempts to cache `FROM scratch` in container builds. [moby/moby#45822](https://github.com/moby/moby/pull/45822)
- containerd image store: Fix `docker cp` with snapshotters that cannot mount the same content multiple times. [moby/moby#45780](https://github.com/moby/moby/pull/45780), [moby/moby#45786](https://github.com/moby/moby/pull/45786)
- containerd image store: Fix builds with `type=image` not being correctly unpacked/stored. [moby/moby#45692](https://github.com/moby/moby/pull/45692)
- containerd image store: Fix incorrectly attempting to unpack pseudo-images (including attestations) in `docker load`. [moby/moby#45688](https://github.com/moby/moby/pull/45688)
- containerd image store: Correctly set the user agent, and include additional information like the snapshotter when interacting with registries. [moby/moby#45671](https://github.com/moby/moby/pull/45671), [moby/moby#45684](https://github.com/moby/moby/pull/45684)
- containerd image store: Fix a failure to unpack already-pulled content after switching between snapshotters. [moby/moby#45678](https://github.com/moby/moby/pull/45678)
- containerd image store: Fix images that have been re-tagged or with all tags removed being pruned while still in use. [moby/moby#45857](https://github.com/moby/moby/pull/45857)
- Fix a Swarm CSI issue where the Topology field was not propagated into NodeCSIInfo. [moby/moby#45810](https://github.com/moby/moby/pull/45810)
- Fix failures to add new Swarm managers caused by a very large raft log. [moby/moby#45703](https://github.com/moby/moby/pull/45703), [moby/swarmkit#3122](https://github.com/moby/swarmkit/pull/3122), [moby/swarmkit#3128](https://github.com/moby/swarmkit/pull/3128)
- `name_to_handle_at(2)` is now always allowed in the default seccomp profile. [moby/moby#45833](https://github.com/moby/moby/pull/45833)
- Fix an issue that prevented encrypted Swarm overlay networks from working on ports other than the default (4789). [moby/moby#45637](https://github.com/moby/moby/pull/45637)
- Fix a failure to restore mount reference-counts during live-restore. [moby/moby#45824](https://github.com/moby/moby/pull/45824)
- Fix various networking-related failures during live-restore. [moby/moby#45658](https://github.com/moby/moby/pull/45658), [moby/moby#45659](https://github.com/moby/moby/pull/45659)
- Fix running containers restoring with a zero (successful) exit status when the daemon is unexpectedly terminated. [moby/moby#45801](https://github.com/moby/moby/pull/45801)
- Fix a potential panic while executing healthcheck probes. [moby/moby#45798](https://github.com/moby/moby/pull/45798)
- Fix a panic caused by a race condition in container exec start. [moby/moby#45794](https://github.com/moby/moby/pull/45794)
- Fix an exception caused by attaching a terminal to an exec with a non-existent command. [moby/moby#45643](https://github.com/moby/moby/pull/45643)
- Fix `host-gateway` with BuildKit by passing the IP as a label (also requires [docker/buildx#1894](https://github.com/docker/buildx/pull/1894)). [moby/moby#45790](https://github.com/moby/moby/pull/45790)
- Fix an issue where `POST /containers/{id}/stop` would forcefully terminate the container when the request was canceled, instead of waiting until the specified timeout for a 'graceful' stop. [moby/moby#45774](https://github.com/moby/moby/pull/45774)
- Fix an issue where `docker cp -a` from the root (`/`) directory would fail. [moby/moby#45748](https://github.com/moby/moby/pull/45748)
- Improve compatibility with non-runc container runtimes by more correctly setting resource constraint parameters in the OCI config. [moby/moby#45746](https://github.com/moby/moby/pull/45746)
- Fix an issue caused by overlapping subuid/subgid ranges in certain configurations (e.g. LDAP) in rootless mode. [moby/moby#45747](https://github.com/moby/moby/pull/45747), [rootless-containers/rootlesskit#369](https://github.com/rootless-containers/rootlesskit/pull/369)
- Greatly reduce CPU and memory usage while populating the Debug section of `GET /info`. [moby/moby#45856](https://github.com/moby/moby/pull/45856)
- Fix an issue where debug information was not correctly printed during `docker info` when only the client is in debug mode. [docker/cli#4393](https://github.com/docker/cli/pull/4393)
- Fix issues related to hung connections when connecting to hosts over a SSH connection. [docker/cli#4395](https://github.com/docker/cli/pull/4395)

### Packaging updates

- Upgrade Go to `go1.20.5`. [moby/moby#45745](https://github.com/moby/moby/pull/45745), [docker/cli#4351](https://github.com/docker/cli/pull/4351), [docker/docker-ce-packaging#904](https://github.com/docker/docker-ce-packaging/pull/904)
- Upgrade Compose to `v2.19.1`. [docker/docker-ce-packaging#916](https://github.com/docker/docker-ce-packaging/pull/916)
- Upgrade buildx to `v0.11.1`. [docker/docker-ce-packaging#918](https://github.com/docker/docker-ce-packaging/pull/918)

## 24.0.2

*2023-05-26*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.2)
- [moby/moby, 24.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.2)

### Bug fixes and enhancements

- Fix a panic during build when referencing locally tagged images. [moby/buildkit#3899](https://github.com/moby/buildkit/pull/3899), [moby/moby#45582](https://github.com/moby/moby/pull/45582)
- Fix builds potentially failing with `exit code: 4294967295` when performing many concurrent build stages. [moby/moby#45620](https://github.com/moby/moby/pull/45620)
- Fix DNS resolution on Windows ignoring `etc/hosts` (`%WINDIR%\System32\Drivers\etc\hosts`), including resolution of `localhost`. [moby/moby#45562](https://github.com/moby/moby/pull/45562)
- Apply a workaround for a containerd bug that causes concurrent `docker exec` commands to take significantly longer than expected. [moby/moby#45625](https://github.com/moby/moby/pull/45625)
- containerd image store: Fix an issue where the image `Created` field would contain an incorrect value. [moby/moby#45623](https://github.com/moby/moby/pull/45623)
- containerd image store: Adjust the output of image pull progress so that the output has the same format regardless of whether the containerd image store is enabled. [moby/moby#45602](https://github.com/moby/moby/pull/45602)
- containerd image store: Switching between the default and containerd image store now requires a daemon restart. [moby/moby#45616](https://github.com/moby/moby/pull/45616)

### Packaging updates

- Upgrade Buildx to `v0.10.5`. [docker/docker-ce-packaging#900](https://github.com/docker/docker-ce-packaging/pull/900)

## 24.0.1

*2023-05-19*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.1)
- [moby/moby, 24.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.1)

### Removed

- Remove CLI completions for storage drivers removed in the 24.0 major release. [docker/cli#4302](https://github.com/docker/cli/pull/4302)

### Bug fixes and enhancements

- Fix an issue where DNS query NXDOMAIN replies from external servers were forwarded to the client as SERVFAIL. [moby/moby#45573](https://github.com/moby/moby/pull/45573)
- Fix an issue where `docker pull --platform` would report `No such image` regarding another tag pointing to the same image. [moby/moby#45562](https://github.com/moby/moby/pull/45562)
- Fix an issue where insecure registry configuration would be forgotten during config reload. [moby/moby#45571](https://github.com/moby/moby/pull/45571)
- containerd image store: Fix an issue where images which have no layers would not be listed in `docker images -a` [moby/moby#45588](https://github.com/moby/moby/pull/45588)
- API: Fix an issue where `GET /images/{id}/json` would return `null` instead of empty `RepoTags` and `RepoDigests`. [moby/moby#45564](https://github.com/moby/moby/pull/45564)
- API: Fix an issue where `POST /commit` did not accept an empty request body. [moby/moby#45568](https://github.com/moby/moby/pull/45568)

### Packaging updates

- Upgrade Compose to `v2.18.1`. [docker/docker-ce-packaging#896](https://github.com/docker/docker-ce-packaging/pull/896)

## 24.0.0

*2023-05-16*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 24.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.0)
- [moby/moby, 24.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.0)

### New

- Introduce experimental support for containerd as the content store (replacing the existing storage drivers). [moby/moby#43735](https://github.com/moby/moby/pull/43735), [other moby/moby pull requests](https://github.com/moby/moby/pulls?q=is%3Apr+is%3Amerged+milestone%3A24.0.0+-label%3Aprocess%2Fcherry-picked+label%3Acontainerd-integration+)
- The `--host` CLI flag now supports a path component in a `ssh://` host address, allowing use of an alternate socket path without configuration on the remote host. [docker/cli#4073](https://github.com/docker/cli/pull/4073)
- The `docker info` CLI command now reports a version and platform field. [docker/cli#4180](https://github.com/docker/cli/pull/4180)
- Introduce the daemon flag `--default-network-opt` to configure options for newly created networks. [moby/moby#43197](https://github.com/moby/moby/pull/43197)
- Restrict access to `AF_VSOCK` in the `socket(2)` family of syscalls in the default seccomp profile. [moby/moby#44562](https://github.com/moby/moby/pull/44562)
- Introduce support for setting OCI runtime annotations on containers. [docker/cli#4156](https://github.com/docker/cli/pull/4156), [moby/moby#45025](https://github.com/moby/moby/pull/45025)
- Alternative runtimes can now be configured in `daemon.json`, enabling runtime names to be aliased and options to be passed. [moby/moby#45032](https://github.com/moby/moby/pull/45032)
- The `docker-init` binary will now be discovered in FHS-compliant libexec directories, in addition to the `PATH`. [moby/moby#45198](https://github.com/moby/moby/pull/45198)
- API: Surface the daemon-level `--no-new-privileges` in `GET /info`. [moby/moby#45320](https://github.com/moby/moby/pull/45320)

### Removed

- `docker info` no longer reports `IndexServiceAddress`. [docker/cli#4204](https://github.com/docker/cli/pull/4204)
- libnetwork: Remove fallback code for obsolete kernel versions. [moby/moby#44684](https://github.com/moby/moby/pull/44684), [moby/moby#44802](https://github.com/moby/moby/pull/44802)
- libnetwork: Remove unused code related to classic Swarm. [moby/moby#44965](https://github.com/moby/moby/pull/44965)
- libnetwork: Remove usage of the `xt_u32` kernel module from encrypted Swarm overlay networks. [moby/moby#45281](https://github.com/moby/moby/pull/45281)
- Remove support for BuildKit's deprecated `buildinfo` in favor of standard provenance attestations. [moby/moby#45097](https://github.com/moby/moby/pull/45097)
- Remove the deprecated AUFS and legacy `overlay` storage drivers. [moby/moby#45342](https://github.com/moby/moby/pull/45342), [moby/moby#45359](https://github.com/moby/moby/pull/45359)
- Remove the deprecated `overlay2.override_kernel_check` storage driver option. [moby/moby#45368](https://github.com/moby/moby/pull/45368)
- Remove workarounds for obsolete versions of `apparmor_parser` from the AppArmor profiles. [moby/moby#45500](https://github.com/moby/moby/pull/45500)
- API: `GET /images/json` no longer represents empty RepoTags and RepoDigests as`<none>:<none>`/`<none>@<none>`. Empty arrays are returned instead on API >= 1.43. [moby/moby#45068](https://github.com/moby/moby/pull/45068)

### Deprecated

- Deprecate the `--oom-score-adjust` daemon option. [moby/moby#45315](https://github.com/moby/moby/pull/45315)
- API: Deprecate the `VirtualSize` field in `GET /images/json` and `GET /images/{id}/json`. [moby/moby#45346](https://github.com/moby/moby/pull/45346)

### Bug fixes and enhancements

- The `docker stack` command no longer validates the `build` section of Compose files. [docker/cli#4214](https://github.com/docker/cli/pull/4214)
- Fix lingering healthcheck processes after the timeout is reached. [moby/moby#43739](https://github.com/moby/moby/pull/43739)
- Reduce the overhead of container startup when using the `overlay2` storage driver. [moby/moby#44285](https://github.com/moby/moby/pull/44285)
- API: Handle multiple `before=` and `since=` filters in `GET /images`. [moby/moby#44503](https://github.com/moby/moby/pull/44503)
- Fix numerous bugs in the embedded DNS resolver implementation used by user-defined networks. [moby/moby#44664](https://github.com/moby/moby/pull/44664)
- Add `execDuration` field to the map of event attributes. [moby/moby#45494](https://github.com/moby/moby/pull/45494)
- Swarm-level networks can now be created with the Windows `internal`, `l2bridge`, and `nat` drivers. [moby/swarmkit#3121](https://github.com/moby/swarmkit/pull/3121), [moby/moby#45291](https://github.com/moby/moby/pull/45291)

### Packaging updates

- Update Go to `1.20.4`. [docker/cli#4253](https://github.com/docker/cli/pull/4253), [moby/moby#45456](https://github.com/moby/moby/pull/45456), [docker/docker-ce-packaging#888](https://github.com/docker/docker-ce-packaging/pull/888)
- Update `containerd` to [v1.7.1](https://github.com/containerd/containerd/releases/tag/v1.7.1). [moby/moby#45537](https://github.com/moby/moby/pull/45537)
- Update `buildkit` to [v0.11.6](https://github.com/moby/buildkit/releases/v0.11.6). [moby/moby#45367](https://github.com/moby/moby/pull/45367)

---

# Docker Engine 25.0 release notes

> Learn about the new features, bug fixes, and breaking changes for Docker Engine

# Docker Engine 25.0 release notes

   Table of contents

---

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 25.0.

For more information about:

- Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
- Changes to the Engine API, see
  [Engine API version history](https://docs.docker.com/reference/api/engine/version-history/).

## 25.0.5

*2024-03-19*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 25.0.5 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.5)
- [moby/moby, 25.0.5 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.5)

### Security

This release contains a security fix for [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx), a potential data exfiltration from 'internal' networks via authoritative DNS servers.

### Bug fixes and enhancements

- [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx): Do not forward requests to external DNS servers for a container that is only connected to an 'internal' network. Previously, requests were forwarded if the host's DNS server was running on a loopback address, like systemd's 127.0.0.53. [moby/moby#47589](https://github.com/moby/moby/pull/47589)
- plugin: fix mounting /etc/hosts when running in UserNS. [moby/moby#47588](https://github.com/moby/moby/pull/47588)
- rootless: fix `open /etc/docker/plugins: permission denied`. [moby/moby#47587](https://github.com/moby/moby/pull/47587)
- Fix multiple parallel `docker build` runs leaking disk space. [moby/moby#47527](https://github.com/moby/moby/pull/47527)

## 25.0.4

*2024-03-07*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 25.0.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.4)
- [moby/moby, 25.0.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.4)

### Bug fixes and enhancements

- Restore DNS names for containers in the default "nat" network on Windows. [moby/moby#47490](https://github.com/moby/moby/pull/47490)
- Fix `docker start` failing when used with `--checkpoint` [moby/moby#47466](https://github.com/moby/moby/pull/47466)
- Don't enforce new validation rules for existing swarm networks [moby/moby#47482](https://github.com/moby/moby/pull/47482)
- Restore IP connectivity between the host and containers on an internal bridge network. [moby/moby#47481](https://github.com/moby/moby/pull/47481)
- Fix a regression introduced in v25.0 that prevented the classic builder from adding tar archive with `xattrs` created on a non-Linux OS [moby/moby#47483](https://github.com/moby/moby/pull/47483)
- containerd image store: Fix image pull not emitting `Pulling fs layer status` [moby/moby#47484](https://github.com/moby/moby/pull/47484)
- API: To preserve backwards compatibility, make read-only mounts non-recursive by default when using older clients (API versions < v1.44). [moby/moby#47393](https://github.com/moby/moby/pull/47393)
- API: `GET /images/{id}/json` omits the `Created` field (previously it was `0001-01-01T00:00:00Z`) if the `Created` field was missing from the image config. [moby/moby#47451](https://github.com/moby/moby/pull/47451)
- API: Populate a missing `Created` field in `GET /images/{id}/json` with `0001-01-01T00:00:00Z` for API versions <= 1.43. [moby/moby#47387](https://github.com/moby/moby/pull/47387)
- API: Fix a regression that caused API socket connection failures to report an API version negotiation failure instead. [moby/moby#47470](https://github.com/moby/moby/pull/47470)
- API: Preserve supplied endpoint configuration in a container-create API request, when a container-wide MAC address is specified, but `NetworkMode` name or id is not the same as the name or id used in `NetworkSettings.Networks`. [moby/moby#47510](https://github.com/moby/moby/pull/47510)

### Packaging updates

- Upgrade Go runtime to 1.21.8. [moby/moby#47503](https://github.com/moby/moby/pull/47503)
- Upgrade RootlessKit to v2.0.2. [moby/moby#47508](https://github.com/moby/moby/pull/47508)
- Upgrade Compose to v2.24.7. [docker/docker-ce-packaging#998](https://github.com/moby/moby/pull/998)
- Upgrade Buildx to v0.13.0. [docker/docker-ce-packaging#997](https://github.com/moby/moby/pull/997)

## 25.0.3

*2024-02-06*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 25.0.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.3)
- [moby/moby, 25.0.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.3)

### Bug fixes and enhancements

- containerd image store: Fix a bug where `docker image history` would fail if a manifest wasn't found in the content store. [moby/moby#47348](https://github.com/moby/moby/pull/47348)
- Ensure that a generated MAC address is not restored when a container is restarted, but a configured MAC address is preserved. [moby/moby#47304](https://github.com/moby/moby/pull/47304)
  > Note
  >
  > - Containers created with Docker Engine version 25.0.0 may have duplicate MAC addresses.
  >   They must be re-created.
  > - Containers with user-defined MAC addresses created with Docker Engine versions 25.0.0 or 25.0.1
  >   receive new MAC addresses when started using Docker Engine version 25.0.2.
  >   They must also be re-created.
- Fix `docker save <image>@<digest>` producing an OCI archive with index without manifests. [moby/moby#47294](https://github.com/moby/moby/pull/47294)
- Fix a bug preventing bridge networks from being created with an MTU higher than 1500 on RHEL and CentOS 7. [moby/moby#47308](https://github.com/moby/moby/issues/47308), [moby/moby#47311](https://github.com/moby/moby/pull/47311)
- Fix a bug where containers are unable to communicate over an `internal` network. [moby/moby#47303](https://github.com/moby/moby/pull/47303)
- Fix a bug where the value of the `ipv6` daemon option was ignored. [moby/moby#47310](https://github.com/moby/moby/pull/47310)
- Fix a bug where trying to install a pulling using a digest revision would cause a panic. [moby/moby#47323](https://github.com/moby/moby/pull/47323)
- Fix a potential race condition in the managed containerd supervisor. [moby/moby#47313](https://github.com/moby/moby/pull/47313)
- Fix an issue with the `journald` log driver preventing container logs from being followed correctly with systemd version 255. [moby/moby#47243](https://github.com/moby/moby/pull/47243)
- seccomp: Update the builtin seccomp profile to include syscalls added in kernel v5.17 - v6.7 to align the profile with the profile used by containerd. [moby/moby#47341](https://github.com/moby/moby/pull/47341)
- Windows: Fix cache not being used when building images based on Windows versions older than the host's version. [moby/moby#47307](https://github.com/moby/moby/pull/47307), [moby/moby#47337](https://github.com/moby/moby/pull/47337)

### Packaging updates

- Removed support for Ubuntu Lunar (23.04). [docker/ce-packaging#986](https://github.com/docker/docker-ce-packaging/pull/986)

## 25.0.2

*2024-01-31*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 25.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.2)
- [moby/moby, 25.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.2)

### Security

This release contains security fixes for the following CVEs
affecting Docker Engine and its components.

| CVE | Component | Fix version | Severity |
| --- | --- | --- | --- |
| CVE-2024-21626 | runc | 1.1.12 | High, CVSS 8.6 |
| CVE-2024-23651 | BuildKit | 1.12.5 | High, CVSS 8.7 |
| CVE-2024-23652 | BuildKit | 1.12.5 | High, CVSS 8.7 |
| CVE-2024-23653 | BuildKit | 1.12.5 | High, CVSS 7.7 |
| CVE-2024-23650 | BuildKit | 1.12.5 | Medium, CVSS 5.5 |
| CVE-2024-24557 | Docker Engine | 25.0.2 | Medium, CVSS 6.9 |

The potential impacts of the above vulnerabilities include:

- Unauthorized access to the host filesystem
- Compromising the integrity of the build cache
- In the case of CVE-2024-21626, a scenario that could lead to full container escape

For more information about the security issues addressed in this release,
refer to the [blog post](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/).
For details about each vulnerability, see the relevant security advisory:

- [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
- [CVE-2024-23651](https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv)
- [CVE-2024-23652](https://github.com/moby/buildkit/security/advisories/GHSA-4v98-7qmw-rqr8)
- [CVE-2024-23653](https://github.com/moby/buildkit/security/advisories/GHSA-wr6v-9f75-vh2g)
- [CVE-2024-23650](https://github.com/moby/buildkit/security/advisories/GHSA-9p26-698r-w4hx)
- [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

### Packaging updates

- Upgrade containerd to [v1.6.28](https://github.com/containerd/containerd/releases/tag/v1.6.28).
- Upgrade containerd to v1.7.13 (static binaries only). [moby/moby#47280](https://github.com/moby/moby/pull/47280)
- Upgrade runc to v1.1.12. [moby/moby#47269](https://github.com/moby/moby/pull/47269)
- Upgrade Compose to v2.24.5. [docker/docker-ce-packaging#985](https://github.com/docker/docker-ce-packaging/pull/985)
- Upgrade BuildKit to v0.12.5. [moby/moby#47273](https://github.com/moby/moby/pull/47273)

## 25.0.1

*2024-01-23*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 25.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.1)
- [moby/moby, 25.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.1)

### Bug fixes and enhancements

- API: Fix incorrect HTTP status code for containers with an invalid network configuration created before upgrading to Docker Engine v25.0. [moby/moby#47159](https://github.com/moby/moby/pull/47159)
- Ensure that a MAC address based on a container's IP address is re-generated when the container is stopped and restarted, in case the generated IP/MAC addresses have been reused. [moby/moby#47171](https://github.com/moby/moby/pull/47171)
- Fix `host-gateway-ip` not working during build when not set through configuration. [moby/moby#47192](https://github.com/moby/moby/pull/47192)
- Fix a bug that prevented a container from being renamed twice. [moby/moby#47196](https://github.com/moby/moby/pull/47196)
- Fix an issue causing containers to have their short ID added to their network alias when inspecting them. [moby/moby#47182](https://github.com/moby/moby/pull/47182)
- Fix an issue in detecting whether a remote build context is a Git repository. [moby/moby#47136](https://github.com/moby/moby/pull/47136)
- Fix an issue with layers order in OCI manifests. [moby/moby#47150](https://github.com/moby/moby/issues/47150)
- Fix volume mount error when passing an `addr` or `ip` mount option. [moby/moby#47185](https://github.com/moby/moby/pull/47185)
- Improve error message related to extended attributes that can't be set due to improperly namespaced attribute names. [moby/moby#47178](https://github.com/moby/moby/pull/47178)
- Swarm: Fixed `start_interval` not being passed to the container config. [moby/moby#47163](https://github.com/moby/moby/pull/47163)

### Packaging updates

- Upgrade Compose to `2.24.2`. [docker/docker-ce-packaging#981](https://github.com/docker/docker-ce-packaging/pull/981)

## 25.0.0

*2024-01-19*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

- [docker/cli, 25.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.0)
- [moby/moby, 25.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.0)

> Note
>
> In earlier versions of Docker Engine, recursive mounts (submounts) would
> always be mounted as writable, even when specifying a read-only mount. This
> behavior has changed in v25.0.0, for hosts running on kernel version 5.12 or
> later. Now, read-only bind mounts are **recursively read-only** by default.
>
>
>
> To get the same behavior as earlier releases, you can specify the
> `bind-recursive` option for the `--mount` flag.
>
>
>
> ```console
> $ docker run --mount type=bind,src=SRC,dst=DST,readonly,bind-recursive=writable IMAGE
> ```
>
>
>
> This option isn't supported with the `-v` or `--volume` flag.
> For more information, see
> [Recursive mounts](https://docs.docker.com/engine/storage/bind-mounts/#recursive-mounts).

### New

- The daemon now uses systemd's default `LimitNOFILE`. In earlier versions of
  Docker Engine, this limit was set to `infinity`. This would cause issues with
  recent versions of systemd, where the hard limit was increased, causing
  programs that adjusted their behaviors based on ulimits to consume a high
  amount of memory. [moby/moby#45534](https://github.com/moby/moby/pull/45534)
  The new setting makes containers behave the same way as programs running on
  the host, but may cause programs that make incorrect assumptions based on the
  soft limit to misbehave. To get the previous behavior, you can set
  `LimitNOFILE=1048576`.
  This change currently only affects build containers created with `docker build` when using BuildKit with the `docker` driver. Starting with Docker
  Engine v29.0 (containerd v2.1.5), this limit applies to all containers, not
  only build containers.
  If you're experiencing issues with the higher ulimit in systemd v240 or later,
  consider adding a system `drop-in` or `override` file to configure the ulimit
  settings for your setup. The [Flatcar Container Linux documentation](https://www.flatcar.org/docs/latest/setup/systemd/drop-in-units/)
  has a great article covering this topic in detail.
- Add OpenTelemetry tracing. [moby/moby#45652](https://github.com/moby/moby/pull/45652), [moby/moby#45579](https://github.com/moby/moby/pull/45579)
- Add support for CDI devices under Linux. [moby/moby#45134](https://github.com/moby/moby/pull/45134), [docker/cli#4510](https://github.com/docker/cli/pull/4510), [moby/moby#46004](https://github.com/moby/moby/pull/46004)
- Add an additional interval to be used by healthchecks during the container start period. [moby/moby#40894](https://github.com/moby/moby/pull/40894), [docker/cli#4405](https://github.com/docker/cli/pull/4405), [moby/moby#45965](https://github.com/moby/moby/pull/45965)
- Add a `--log-format` flag to `dockerd` to control the logging format: text (default) or JSON. [moby/moby#45737](https://github.com/moby/moby/pull/45737)
- Add support for recursive read-only mounts. [moby/moby#45278](https://github.com/moby/moby/pull/45278), [moby/moby#46037](https://github.com/moby/moby/pull/46037)
- Add support for filtering images based on timestamp with `docker image ls --filter=until=<timestamp>`. [moby/moby#46577](https://github.com/moby/moby/pull/46577)

### Bug fixes and enhancements

- API: Fix error message for invalid policies at `ValidateRestartPolicy`. [moby/moby#46352](https://github.com/moby/moby/pull/46352)
- API: Update `/info` endpoint to use singleflight. [moby/moby#45847](https://github.com/moby/moby/pull/45847)
- Add an error message for when specifying a Dockerfile filename with `-f`, and also using `stdin`. [docker/cli#4346](https://github.com/docker/cli/pull/4346)
- Add support for `mac-address` and `link-local-ip` fields in `--network` long format. [docker/cli#4419](https://github.com/docker/cli/pull/4419)
- Add support for specifying multiple `--network` flags with `docker container create` and `docker run`. [moby/moby#45906](https://github.com/moby/moby/pull/45906)
- Automatically enable IPv6 on a network when an IPv6 subnet is specified. [moby/moby#46455](https://github.com/moby/moby/pull/46455)
- Add support for overlay networks over IPv6 transport. [moby/moby#46790](https://github.com/moby/moby/pull/46790)
- Configuration reloading is now more robust: if there's an error during the configuration reload process, no configuration changes are applied. [moby/moby#43980](https://github.com/moby/moby/pull/43980)
- Live restore: Containers with auto remove (`docker run --rm`) are no longer forcibly removed on engine restart. [moby/moby#46857](https://github.com/moby/moby/pull/46857)
- Live restore: containers that are live-restored will now be given another health-check start period when the daemon restarts. [moby/moby#47051](https://github.com/moby/moby/pull/47051)
- Container health status is flushed to disk less frequently, reducing wear on flash storage. [moby/moby#47044](https://github.com/moby/moby/pull/47044)
- Ensure network names are unique. [moby/moby#46251](https://github.com/moby/moby/pull/46251)
- Ensure that overlay2 layer metadata is correct. [moby/moby#46471](https://github.com/moby/moby/pull/46471)
- Fix `Downloading` progress message on image pull. [moby/moby#46515](https://github.com/moby/moby/pull/46515)
- Fix `NetworkConnect` and `ContainerCreate` with improved data validation, and return all validation errors at once. [moby/moby#46183](https://github.com/moby/moby/pull/46183)
- Fix `com.docker.network.host_ipv4` option when IPv6 and ip6tables are enabled. [moby/moby#46446](https://github.com/moby/moby/pull/46446)
- Fix daemon's `cleanupContainer` if containerd is stopped. [moby/moby#46213](https://github.com/moby/moby/pull/46213)
- Fix returning incorrect HTTP status codes for libnetwork errors. [moby/moby#46146](https://github.com/moby/moby/pull/46146)
- Fix various issues with images/json API filters and image list. [moby/moby#46034](https://github.com/moby/moby/pull/46034)
- CIFS volumes now resolves FQDN correctly. [moby/moby#46863](https://github.com/moby/moby/pull/46863)
- Improve validation of the `userland-proxy-path` daemon configuration option. Validation now happens during daemon startup, instead of producing an error when starting a container with port-mapping. [moby/moby#47000](https://github.com/moby/moby/pull/47000)
- Set the MAC address of container's interface when network mode is a short network ID. [moby/moby#46406](https://github.com/moby/moby/pull/46406)
- Sort unconsumed build arguments before display in build output. [moby/moby#45917](https://github.com/moby/moby/pull/45917)
- The `docker image save` tarball output is now OCI compliant. [moby/moby#44598](https://github.com/moby/moby/pull/44598)
- The daemon no longer appends `ACCEPT` rules to the end of the `INPUT` iptables chain for encrypted overlay networks. Depending on firewall configuration, a rule may be needed to permit incoming encrypted overlay network traffic. [moby/moby#45280](https://github.com/moby/moby/pull/45280)
- Unpacking layers with extended attributes onto an incompatible filesystem will now fail instead of silently discarding extended attributes. [moby/moby#45464](https://github.com/moby/moby/pull/45464)
- Update daemon MTU option to BridgeConfig and display warning on Windows. [moby/moby#45887](https://github.com/moby/moby/pull/45887)
- Validate IPAM config when creating a network. Automatically fix networks created prior to this release where `--ip-range` is larger than `--subnet`. [moby/moby#45759](https://github.com/moby/moby/pull/45759)
- Containers connected only to internal networks will now have no default route set, making the `connect` syscall fail-fast. [moby/moby#46603](https://github.com/moby/moby/pull/46603)
- containerd image store: Add image events for `push`, `pull`, and `save`. [moby/moby#46405](https://github.com/moby/moby/pull/46405)
- containerd image store: Add support for pulling legacy schema1 images. [moby/moby#46513](https://github.com/moby/moby/pull/46513)
- containerd image store: Add support for pushing all tags. [moby/moby#46485](https://github.com/moby/moby/pull/46485)
- containerd image store: Add support for registry token. [moby/moby#46475](https://github.com/moby/moby/pull/46475)
- containerd image store: Add support for showing the number of containers that use an image. [moby/moby#46511](https://github.com/moby/moby/pull/46511)
- containerd image store: Fix a bug related to the `ONBUILD`, `MAINTAINER`, and `HEALTHCHECK` Dockerfile instructions. [moby/moby#46313](https://github.com/moby/moby/pull/46313)
- containerd image store: Fix `Pulling from` progress message. [moby/moby#46494](https://github.com/moby/moby/pull/46494)
- containerd image store: Add support for referencing images via the truncated ID with `sha256:` prefix. [moby/moby#46435](https://github.com/moby/moby/pull/46435)
- containerd image store: Fix `docker images` showing intermediate layers by default. [moby/moby#46423](https://github.com/moby/moby/pull/46423)
- containerd image store: Fix checking if the specified platform exists when getting an image. [moby/moby#46495](https://github.com/moby/moby/pull/46495)
- containerd image store: Fix errors when multiple `ADD` or `COPY` instructions were used with the classic builder. [moby/moby#46383](https://github.com/moby/moby/pull/46383)
- containerd image store: Fix stack overflow errors when importing an image. [moby/moby#46418](https://github.com/moby/moby/pull/46418)
- containerd image store: Improve `docker pull` progress output. [moby/moby#46412](https://github.com/moby/moby/pull/46412)
- containerd image store: Print the tag, digest, and size after pushing an image. [moby/moby#46384](https://github.com/moby/moby/pull/46384)
- containerd image store: Remove panic from `UpdateConfig`. [moby/moby#46433](https://github.com/moby/moby/pull/46433)
- containerd image store: Return an error when an image tag resembles a digest. [moby/moby#46492](https://github.com/moby/moby/pull/46492)
- containerd image store: `docker image ls` now shows the correct image creation time and date. [moby/moby#46719](https://github.com/moby/moby/pull/46719)
- containerd image store: Fix an issue handling user namespace settings. [moby/moby#46375](https://github.com/moby/moby/pull/46375)
- containerd image store: Add support for pulling all tags (`docker pull -a`). [moby/moby#46618](https://github.com/moby/moby/pull/46618)
- containerd image store: Use the domain name in the image reference as the default registry authentication domain. [moby/moby#46779](https://github.com/moby/moby/pull/46779)

### Packaging updates

- Upgrade API to v1.44. [moby/moby#45468](https://github.com/moby/moby/pull/45468)
- Upgrade Compose to `2.24.1`. [docker/docker-ce-packaging#980](https://github.com/docker/docker-ce-packaging/pull/980)
- Upgrade containerd to v1.7.12 (static binaries only). [moby/moby#47070](https://github.com/moby/moby/pull/47070)
- Upgrade Go runtime to [1.21.6](https://go.dev/doc/devel/release#go1.21.minor). [moby/moby#47053](https://github.com/moby/moby/pull/47053)
- Upgrade runc to v1.1.11. [moby/moby#47007](https://github.com/moby/moby/pull/47007)
- Upgrade BuildKit to v0.12.4. [moby/moby#46882](https://github.com/moby/moby/pull/46882)
- Upgrade Buildx to v0.12.1. [docker/docker-ce-packaging#979](https://github.com/docker/docker-ce-packaging/pull/979)

### Removed

- API: Remove VirtualSize field for the `GET /images/json` and `GET /images/{id}/json` endpoints. [moby/moby#45469](https://github.com/moby/moby/pull/45469)
- Remove deprecated `devicemapper` storage driver. [moby/moby#43637](https://github.com/moby/moby/pull/43637)
- Remove deprecated orchestrator options. [docker/cli#4366](https://github.com/docker/cli/pull/4366)
- Remove support for Debian Upstart init system. [moby/moby#45548](https://github.com/moby/moby/pull/45548), [moby/moby#45551](https://github.com/moby/moby/pull/45551)
- Remove the `--oom-score-adjust` daemon option. [moby/moby#45484](https://github.com/moby/moby/pull/45484)
- Remove warning for deprecated `~/.dockercfg` file. [docker/cli#4281](https://github.com/docker/cli/pull/4281)
- Remove `logentries` logging driver. [moby/moby#46925](https://github.com/moby/moby/pull/46925)

### Deprecated

- Deprecate API versions older than 1.24. [Deprecation notice](https://docs.docker.com/engine/deprecated/#deprecate-legacy-api-versions)
- Deprecate `IsAutomated` field and `is-automated` filter for `docker search`. [Deprecation notice](https://docs.docker.com/engine/deprecated/#isautomated-field-and-is-automated-filter-on-docker-search)
- API: Deprecate `Container` and `ContainerConfig` properties for `/images/{id}/json` (`docker image inspect`). [moby/moby#46939](https://github.com/moby/moby/pull/46939)

### Known limitations

#### Extended attributes for tar files

In this release, the code that handles `tar` archives was changed to be more
strict and to produce an error when failing to write extended attributes
(`xattr`). The `tar` implementation for macOS generates additional extended
attributes by default when creating tar files. These attribute prefixes aren't
valid Linux `xattr` namespace prefixes, which causes an error when Docker
attempts to process these files. For example, if you try to use a tar file with
an `ADD` Dockerfile instruction, you might see an error message similar to the
following:

```text
failed to solve: lsetxattr /sftp_key.ppk: operation not supported
```

Error messages related to extended attribute validation were improved to
include more context in [v25.0.1](#2501), but the limitation in Docker being
unable to process the files remains. Tar files created with the macOS `tar`
using default arguments will produce an error when the tar file is used with
Docker.

As a workaround, if you need to use tar files with Docker generated on macOS,
you can either:

- Use the `--no-xattr` flag for the macOS `tar` command to strip **all** the
  extended attributes. If you want to preserve extended attributes, this isn't
  a recommended option.
- Install and use `gnu-tar` to create the tarballs on macOS instead of the
  default `tar` implementation. To install `gnu-tar` using Homebrew:
  ```console
  $ brew install gnu-tar
  ```
  After installing, add the `gnu-tar` binary to your `PATH`, for example by
  updating your `.zshrc` file:
  ```console
  $ echo 'PATH="/opt/homebrew/opt/gnu-tar/libexec/gnubin:$PATH"' >> ~/.zshrc
  $ source ~/.zshrc
  ```
