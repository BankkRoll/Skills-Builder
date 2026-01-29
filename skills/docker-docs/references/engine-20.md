# Docker Engine 17.09 release notes and more

# Docker Engine 17.09 release notes

# Docker Engine 17.09 release notes

   Table of contents

---

## 17.09.1-ce

2017-12-07

### Builder

- Fix config leakage on shared parent stage [moby/moby#33753](https://github.com/moby/moby/issues/33753)
- Warn on empty continuation lines only, not on comment-only lines [moby/moby#35004](https://github.com/moby/moby/pull/35004)

### Client

- Set API version on Client even when Ping fails [docker/cli#546](https://github.com/docker/cli/pull/546)

### Networking

- Overlay fix for transient IP reuse [docker/libnetwork#2016](https://github.com/docker/libnetwork/pull/2016)
- Fix reapTime logic in NetworkDB and handle DNS cleanup for attachable container [docker/libnetwork#2017](https://github.com/docker/libnetwork/pull/2017)
- Disable hostname lookup on chain exists check [docker/libnetwork#2019](https://github.com/docker/libnetwork/pull/2019)
- Fix lint issues [docker/libnetwork#2020](https://github.com/docker/libnetwork/pull/2020)
- Restore error type in FindNetwork [moby/moby#35634](https://github.com/moby/moby/pull/35634)

### Runtime

- Protect `health monitor` Go channel [moby/moby#35482](https://github.com/moby/moby/pull/35482)
- Fix leaking container/exec state [moby/moby#35484](https://github.com/moby/moby/pull/35484)
- Add /proc/scsi to masked paths (patch to work around [CVE-2017-16539](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-16539) [moby/moby/#35399](https://github.com/moby/moby/pull/35399)
- Vendor tar-split: fix to prevent memory exhaustion issue that could crash Docker daemon [moby/moby/#35424](https://github.com/moby/moby/pull/35424) Fixes [CVE-2017-14992](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14992)
- Fix P/Z HubPullSuite tests [moby/moby#34837](https://github.com/moby/moby/pull/34837)

- Windows: Add support for version filtering on pull [moby/moby#35090](https://github.com/moby/moby/pull/35090)

- Windows: Stop filtering Windows manifest lists by version [moby/moby#35117](https://github.com/moby/moby/pull/35117)
- Use rslave instead of rprivate in chroot archive [moby/moby/#35217](https://github.com/moby/moby/pull/35217)
- Remove container rootfs mountPath after unmount [moby/moby#34573](https://github.com/moby/moby/pull/34573)
- Fix honoring tmpfs size of user /dev/shm mount [moby/moby#35316](https://github.com/moby/moby/pull/35316)
- Don't abort when setting may_detach_mounts (log the error instead) [moby/moby#35172](https://github.com/moby/moby/pull/35172)
- Fix version comparison when negotiating the API version [moby/moby#35008](https://github.com/moby/moby/pull/35008)

### Swarm mode

- Increase gRPC request timeout when sending snapshots [docker/swarmkit#2404](https://github.com/docker/swarmkit/pull/2404)

- Fix node filtering when there is no log driver [docker/swarmkit#2442](https://github.com/docker/swarmkit/pull/2442)
- Add an error on attempt to change cluster name [docker/swarmkit/#2454](https://github.com/docker/swarmkit/pull/2454)
- Delete node attachments when node is removed [docker/swarmkit/#2456](https://github.com/docker/swarmkit/pull/2456)
- Provide custom gRPC dialer to override default proxy dialer [docker/swarmkit/#2457](https://github.com/docker/swarmkit/pull/2457)
- Avoids recursive readlock on swarm info [moby/moby#35388](https://github.com/moby/moby/pull/35388)

## 17.09.0-ce

2017-09-26

### Builder

- Add `--chown` flag to `ADD/COPY` commands in Dockerfile [moby/moby#34263](https://github.com/moby/moby/pull/34263)

- Fix cloning unneeded files while building from git repositories [moby/moby#33704](https://github.com/moby/moby/pull/33704)

### Client

- Allow extension fields in the v3.4 version of the compose format [docker/cli#452](https://github.com/docker/cli/pull/452)
- Make compose file allow to specify names for non-external volume [docker/cli#306](https://github.com/docker/cli/pull/306)
- Support `--compose-file -` as stdin [docker/cli#347](https://github.com/docker/cli/pull/347)
- Support `start_period` for healthcheck in Docker Compose [docker/cli#475](https://github.com/docker/cli/pull/475)

- Add support for `stop-signal` in docker stack commands [docker/cli#388](https://github.com/docker/cli/pull/388)
- Add support for update order in compose deployments [docker/cli#360](https://github.com/docker/cli/pull/360)
- Add ulimits to unsupported compose fields [docker/cli#482](https://github.com/docker/cli/pull/482)
- Add `--format` to `docker-search` [docker/cli#440](https://github.com/docker/cli/pull/440)

- Show images digests when `{{.Digest}}` is in format [docker/cli#439](https://github.com/docker/cli/pull/439)
- Print output of `docker stack rm` on `stdout` instead of `stderr` [docker/cli#491](https://github.com/docker/cli/pull/491)

- Fix `docker history --format {{json .}}` printing human-readable timestamps instead of ISO8601 when `--human=true` [docker/cli#438](https://github.com/docker/cli/pull/438)
- Fix idempotence of `docker stack deploy` when secrets or configs are used [docker/cli#509](https://github.com/docker/cli/pull/509)
- Fix presentation of random host ports [docker/cli#404](https://github.com/docker/cli/pull/404)
- Fix redundant service restarts when service created with multiple secrets [moby/moby#34746](https://github.com/moby/moby/issues/34746)

### Logging

- Fix Splunk logger not transmitting log data when tag is empty and raw-mode is used [moby/moby#34520](https://github.com/moby/moby/pull/34520)

### Networking

- Add the control plane MTU option in the daemon config [moby/moby#34103](https://github.com/moby/moby/pull/34103)
- Add service virtual IP to sandbox's loopback address [docker/libnetwork#1877](https://github.com/docker/libnetwork/pull/1877)

### Runtime

- Graphdriver: promote overlay2 over aufs [moby/moby#34430](https://github.com/moby/moby/pull/34430)
- LCOW: Additional flags for VHD boot [moby/moby#34451](https://github.com/moby/moby/pull/34451)
- LCOW: Don't block export [moby/moby#34448](https://github.com/moby/moby/pull/34448)
- LCOW: Dynamic sandbox management [moby/moby#34170](https://github.com/moby/moby/pull/34170)
- LCOW: Force Hyper-V Isolation [moby/moby#34468](https://github.com/moby/moby/pull/34468)
- LCOW: Move toolsScratchPath to /tmp [moby/moby#34396](https://github.com/moby/moby/pull/34396)
- LCOW: Remove hard-coding [moby/moby#34398](https://github.com/moby/moby/pull/34398)
- LCOW: WORKDIR correct handling [moby/moby#34405](https://github.com/moby/moby/pull/34405)
- Windows: named pipe mounts [moby/moby#33852](https://github.com/moby/moby/pull/33852)

- Fix "permission denied" errors when accessing volume with SELinux enforcing mode [moby/moby#34684](https://github.com/moby/moby/pull/34684)
- Fix layers size reported as `0` in `docker system df` [moby/moby#34826](https://github.com/moby/moby/pull/34826)
- Fix some "device or resource busy" errors when removing containers on RHEL 7.4 based kernels [moby/moby#34886](https://github.com/moby/moby/pull/34886)

### Swarm mode

- Include whether the managers in the swarm are autolocked as part of `docker info` [docker/cli#471](https://github.com/docker/cli/pull/471)

- Add 'docker service rollback' subcommand [docker/cli#205](https://github.com/docker/cli/pull/205)

- Fix managers failing to join if the gRPC snapshot is larger than 4MB [docker/swarmkit#2375](https://github.com/docker/swarmkit/pull/2375)
- Fix "permission denied" errors for configuration file in SELinux-enabled containers [moby/moby#34732](https://github.com/moby/moby/pull/34732)
- Fix services failing to deploy on ARM nodes [moby/moby#34021](https://github.com/moby/moby/pull/34021)

### Packaging

- Build scripts for ppc64el on Ubuntu [docker/docker-ce-packaging#43](https://github.com/docker/docker-ce-packaging/pull/43)

### Deprecation

- Remove deprecated `--enable-api-cors` daemon flag [moby/moby#34821](https://github.com/moby/moby/pull/34821)

---

# Docker Engine 17.10 release notes

# Docker Engine 17.10 release notes

   Table of contents

---

## 17.10.0-ce

2017-10-17

> Important
>
> `docker service scale` and `docker service rollback` use non-detached mode as default,
> use `--detach` to keep the old behaviour.

### Builder

- Reset uid/gid to 0 in uploaded build context to share build cache with other clients [docker/cli#513](https://github.com/docker/cli/pull/513)

- Add support for `ADD` urls without any sub path [moby/moby#34217](https://github.com/moby/moby/pull/34217)

### Client

- Move output of `docker stack rm` to stdout [docker/cli#491](https://github.com/docker/cli/pull/491)
- Use natural sort for secrets and configs in cli [docker/cli#307](https://github.com/docker/cli/pull/307)
- Use non-detached mode as default for `docker service` commands [docker/cli#525](https://github.com/docker/cli/pull/525)
- Set APIVersion on the client, even when Ping fails [docker/cli#546](https://github.com/docker/cli/pull/546)

- Fix loader error with different build syntax in `docker stack deploy` [docker/cli#544](https://github.com/docker/cli/pull/544)

- Change the default output format for `docker container stats` to show `CONTAINER ID` and `NAME` [docker/cli#565](https://github.com/docker/cli/pull/565)

- Add `--no-trunc` flag to `docker container stats` [docker/cli#565](https://github.com/docker/cli/pull/565)
- Add experimental `docker trust`: `view`, `revoke`, `sign` subcommands [docker/cli#472](https://github.com/docker/cli/pull/472)

- Various doc and shell completion fixes [docker/cli#610](https://github.com/docker/cli/pull/610) [docker/cli#611](https://github.com/docker/cli/pull/611) [docker/cli#618](https://github.com/docker/cli/pull/618) [docker/cli#580](https://github.com/docker/cli/pull/580) [docker/cli#598](https://github.com/docker/cli/pull/598) [docker/cli#603](https://github.com/docker/cli/pull/603)

### Networking

- Enabling ILB/ELB on windows using per-node, per-network LB endpoint [moby/moby#34674](https://github.com/moby/moby/pull/34674)
- Overlay fix for transient IP reuse [docker/libnetwork#1935](https://github.com/docker/libnetwork/pull/1935)
- Serializing bitseq alloc [docker/libnetwork#1788](https://github.com/docker/libnetwork/pull/1788)

- Disable hostname lookup on chain exists check [docker/libnetwork#1974](https://github.com/docker/libnetwork/pull/1974)

### Runtime

- LCOW: Add UVM debuggability by grabbing logs before tear-down [moby/moby#34846](https://github.com/moby/moby/pull/34846)
- LCOW: Prepare work for bind mounts [moby/moby#34258](https://github.com/moby/moby/pull/34258)
- LCOW: Support for docker cp, ADD/COPY on build [moby/moby#34252](https://github.com/moby/moby/pull/34252)
- LCOW: VHDX boot to readonly [moby/moby#34754](https://github.com/moby/moby/pull/34754)
- Volume: evaluate symlinks before relabeling mount source [moby/moby#34792](https://github.com/moby/moby/pull/34792)

- Fixing ‘docker cp’ to allow new target file name in a host symlinked directory [moby/moby#31993](https://github.com/moby/moby/pull/31993)

- Add support for Windows version filtering on pull [moby/moby#35090](https://github.com/moby/moby/pull/35090)

### Swarm mode

- Produce an error if `docker swarm init --force-new-cluster` is executed on worker nodes [moby/moby#34881](https://github.com/moby/moby/pull/34881)

- Add support for `.Node.Hostname` templating in swarm services [moby/moby#34686](https://github.com/moby/moby/pull/34686)

- Increase gRPC request timeout to 20 seconds for sending snapshots [docker/swarmkit#2391](https://github.com/docker/swarmkit/pull/2391)

- Do not filter nodes if logdriver is set to `none` [docker/swarmkit#2396](https://github.com/docker/swarmkit/pull/2396)

- Adding ipam options to ipam driver requests [docker/swarmkit#2324](https://github.com/docker/swarmkit/pull/2324)

---

# Docker Engine 17.11 release notes

# Docker Engine 17.11 release notes

   Table of contents

---

## 17.11.0-ce

2017-11-20

> Important
>
> Docker CE 17.11 is the first Docker release based on
> [containerd 1.0 beta](https://github.com/containerd/containerd/releases/tag/v1.0.0-beta.2).
> Docker CE 17.11 and later don't recognize containers started with previous
> Docker versions. If you use Live Restore, you must stop all containers before
> upgrading to Docker CE 17.11. If you don't, any containers started by Docker
> versions that predate 17.11 aren't recognized by Docker after the upgrade and
> keep running, un-managed, on the system.

### Builder

- Test & Fix build with rm/force-rm matrix [moby/moby#35139](https://github.com/moby/moby/pull/35139)

- Fix build with `--stream` with a large context [moby/moby#35404](https://github.com/moby/moby/pull/35404)

### Client

- Hide help flag from help output [docker/cli#645](https://github.com/docker/cli/pull/645)
- Support parsing of named pipes for compose volumes [docker/cli#560](https://github.com/docker/cli/pull/560)
- [Compose] Cast values to expected type after interpolating values [docker/cli#601](https://github.com/docker/cli/pull/601)

- Add output for "secrets" and "configs" on `docker stack deploy` [docker/cli#593](https://github.com/docker/cli/pull/593)

- Fix flag description for `--host-add` [docker/cli#648](https://github.com/docker/cli/pull/648)

- Do not truncate ID on docker service ps --quiet [docker/cli#579](https://github.com/docker/cli/pull/579)

### Deprecation

- Update bash completion and deprecation for synchronous service updates [docker/cli#610](https://github.com/docker/cli/pull/610)

### Logging

- copy to log driver's bufsize, fixes #34887 [moby/moby#34888](https://github.com/moby/moby/pull/34888)

- Add TCP support for GELF log driver [moby/moby#34758](https://github.com/moby/moby/pull/34758)
- Add credentials endpoint option for awslogs driver [moby/moby#35055](https://github.com/moby/moby/pull/35055)

### Networking

- Fix network name masking network ID on delete [moby/moby#34509](https://github.com/moby/moby/pull/34509)
- Fix returned error code for network creation from 500 to 409 [moby/moby#35030](https://github.com/moby/moby/pull/35030)
- Fix tasks fail with error "Unable to complete atomic operation, key modified" [docker/libnetwork#2004](https://github.com/docker/libnetwork/pull/2004)

### Runtime

- Switch to Containerd 1.0 client [moby/moby#34895](https://github.com/moby/moby/pull/34895)
- Increase container default shutdown timeout on Windows [moby/moby#35184](https://github.com/moby/moby/pull/35184)
- LCOW: API: Add `platform` to /images/create and /build [moby/moby#34642](https://github.com/moby/moby/pull/34642)
- Stop filtering Windows manifest lists by version [moby/moby#35117](https://github.com/moby/moby/pull/35117)
- Use windows console mode constants from Azure/go-ansiterm [moby/moby#35056](https://github.com/moby/moby/pull/35056)
- Windows Daemon should respect DOCKER_TMPDIR [moby/moby#35077](https://github.com/moby/moby/pull/35077)
- Windows: Fix startup logging [moby/moby#35253](https://github.com/moby/moby/pull/35253)

- Add support for Windows version filtering on pull [moby/moby#35090](https://github.com/moby/moby/pull/35090)

- Fixes LCOW after containerd 1.0 introduced regressions [moby/moby#35320](https://github.com/moby/moby/pull/35320)

- ContainerWait on remove: don't stuck on rm fail [moby/moby#34999](https://github.com/moby/moby/pull/34999)
- oci: obey CL_UNPRIVILEGED for user namespaced daemon [moby/moby#35205](https://github.com/moby/moby/pull/35205)
- Don't abort when setting may_detach_mounts [moby/moby#35172](https://github.com/moby/moby/pull/35172)

- Fix panic on get container pid when live restore containers [moby/moby#35157](https://github.com/moby/moby/pull/35157)
- Mask `/proc/scsi` path for containers to prevent removal of devices (CVE-2017-16539) [moby/moby#35399](https://github.com/moby/moby/pull/35399)

- Update to [github.com/vbatts/tar-split@v0.10.2](mailto:github.com/vbatts/tar-split@v0.10.2) (CVE-2017-14992) [moby/moby#35424](https://github.com/moby/moby/pull/35424)

### Swarm Mode

- Modifying integration test due to new ipam options in swarmkit [moby/moby#35103](https://github.com/moby/moby/pull/35103)

- Fix deadlock on getting swarm info [moby/moby#35388](https://github.com/moby/moby/pull/35388)

- Expand the scope of the `Err` field in `TaskStatus` to also cover non-terminal errors that block the task from progressing [docker/swarmkit#2287](https://github.com/docker/swarmkit/pull/2287)

### Packaging

- Build packages for Debian 10 (Buster) [docker/docker-ce-packaging#50](https://github.com/docker/docker-ce-packaging/pull/50)
- Build packages for Ubuntu 17.10 (Artful) [docker/docker-ce-packaging#55](https://github.com/docker/docker-ce-packaging/pull/55)

---

# Docker Engine 17.12 release notes

# Docker Engine 17.12 release notes

   Table of contents

---

## 17.12.1-ce

2018-02-27

### Client

- Fix `node-generic-resource` typo [moby/moby#35970](https://github.com/moby/moby/pull/35970) and [moby/moby#36125](https://github.com/moby/moby/pull/36125)

- Return errors from daemon on stack deploy configs create/update [docker/cli#757](https://github.com/docker/cli/pull/757)

### Logging

- awslogs: fix batch size calculation for large logs [moby/moby#35726](https://github.com/moby/moby/pull/35726)

- Support a proxy in splunk log driver [moby/moby#36220](https://github.com/moby/moby/pull/36220)

### Networking

- Fix ingress network when upgrading from 17.09 to 17.12 [moby/moby#36003](https://github.com/moby/moby/pull/36003)

- Add verbose info to partial overlay ID [moby/moby#35989](https://github.com/moby/moby/pull/35989)

- Fix IPv6 networking being deconfigured if live-restore is being enabled [docker/libnetwork#2043](https://github.com/docker/libnetwork/pull/2043)
- Fix watchMiss thread context [docker/libnetwork#2051](https://github.com/docker/libnetwork/pull/2051)

### Packaging

- Set TasksMax in docker.service [docker/docker-ce-packaging#78](https://github.com/docker/docker-ce-packaging/pull/78)

### Runtime

- Bump Golang to 1.9.4
- Bump containerd to 1.0.1

- Fix dockerd not being able to reconnect to containerd when it is restarted [moby/moby#36173](https://github.com/moby/moby/pull/36173)
- Fix containerd events from being processed twice [moby/moby#35891](https://github.com/moby/moby/issues/35891)
- Fix vfs graph driver failure to initialize because of failure to setup fs quota [moby/moby#35827](https://github.com/moby/moby/pull/35827)
- Fix regression of health check not using container's working directory [moby/moby#35845](https://github.com/moby/moby/pull/35845)
- Honor `DOCKER_RAMDISK` with containerd 1.0 [moby/moby#35957](https://github.com/moby/moby/pull/35957)
- Update runc to fix hang during start and exec [moby/moby#36097](https://github.com/moby/moby/pull/36097)
- Windows: Vendor of Microsoft/hcsshim @v.0.6.8 partial fix for import layer failing [moby/moby#35924](https://github.com/moby/moby/pull/35924)

- Do not make graphdriver homes private mounts [moby/moby#36047](https://github.com/moby/moby/pull/36047)
- Use rslave propagation for mounts from daemon root [moby/moby#36055](https://github.com/moby/moby/pull/36055)
- Set daemon root to use shared mount propagation [moby/moby#36096](https://github.com/moby/moby/pull/36096)
- Validate that mounted paths exist when container is started, not just during creation [moby/moby#35833](https://github.com/moby/moby/pull/35833)
- Add `REMOVE` and `ORPHANED` to TaskState [moby/moby#36146](https://github.com/moby/moby/pull/36146)

- Fix issue where network inspect does not show Created time for networks in swarm scope [moby/moby#36095](https://github.com/moby/moby/pull/36095)

- Nullify container read write layer upon release [moby/moby#36130](https://github.com/moby/moby/pull/36160) and [moby/moby#36343](https://github.com/moby/moby/pull/36242)

### Swarm

- Remove watchMiss from swarm mode [docker/libnetwork#2047](https://github.com/docker/libnetwork/pull/2047)

### Known Issues

- Health check no longer uses the container's working directory [moby/moby#35843](https://github.com/moby/moby/issues/35843)
- Errors not returned from client in stack deploy configs [moby/moby#757](https://github.com/docker/cli/pull/757)
- Docker cannot use memory limit when using systemd options [moby/moby#35123](https://github.com/moby/moby/issues/35123)

## 17.12.0-ce

2017-12-27

### Known Issues

- AWS logs batch size calculation [moby/moby#35726](https://github.com/moby/moby/pull/35726)
- Health check no longer uses the container's working directory [moby/moby#35843](https://github.com/moby/moby/issues/35843)
- Errors not returned from client in stack deploy configs [moby/moby#757](https://github.com/docker/cli/pull/757)
- Daemon aborts when project quota fails [moby/moby#35827](https://github.com/moby/moby/pull/35827)
- Docker cannot use memory limit when using systemd options [moby/moby#35123](https://github.com/moby/moby/issues/35123)

### Builder

- Fix build cache hash for broken symlink [moby/moby#34271](https://github.com/moby/moby/pull/34271)
- Fix long stream sync [moby/moby#35404](https://github.com/moby/moby/pull/35404)
- Fix dockerfile parser failing silently on long tokens [moby/moby#35429](https://github.com/moby/moby/pull/35429)

### Client

- Remove secret/config duplication in cli/compose [docker/cli#671](https://github.com/docker/cli/pull/671)
- Add `--local` flag to `docker trust sign` [docker/cli#575](https://github.com/docker/cli/pull/575)
- Add `docker trust inspect` [docker/cli#694](https://github.com/docker/cli/pull/694)

- Add `name` field to secrets and configs to allow interpolation in Compose files [docker/cli#668](https://github.com/docker/cli/pull/668)
- Add `--isolation` for setting swarm service isolation mode [docker/cli#426](https://github.com/docker/cli/pull/426)

- Remove deprecated "daemon" subcommand [docker/cli#689](https://github.com/docker/cli/pull/689)

- Fix behaviour of `rmi -f` with unexpected errors [docker/cli#654](https://github.com/docker/cli/pull/654)

- Integrated Generic resource in service create [docker/cli#429](https://github.com/docker/cli/pull/429)

- Fix external networks in stacks [docker/cli#743](https://github.com/docker/cli/pull/743)

- Remove support for referencing images by image shortid [docker/cli#753](https://github.com/docker/cli/pull/753) and [moby/moby#35790](https://github.com/moby/moby/pull/35790)
- Use commit-sha instead of tag for containerd [moby/moby#35770](https://github.com/moby/moby/pull/35770)

### Documentation

- Update API version history for 1.35 [moby/moby#35724](https://github.com/moby/moby/pull/35724)

### Logging

- Logentries driver line-only=true []byte output fix [moby/moby#35612](https://github.com/moby/moby/pull/35612)
- Logentries line-only logopt fix to maintain backwards compatibility [moby/moby#35628](https://github.com/moby/moby/pull/35628)

- Add `--until` flag for docker logs [moby/moby#32914](https://github.com/moby/moby/pull/32914)
- Add gelf log driver plugin to Windows build [moby/moby#35073](https://github.com/moby/moby/pull/35073)

- Set timeout on splunk batch send [moby/moby#35496](https://github.com/moby/moby/pull/35496)
- Update Graylog2/go-gelf [moby/moby#35765](https://github.com/moby/moby/pull/35765)

### Networking

- Move load balancer sandbox creation/deletion into libnetwork [moby/moby#35422](https://github.com/moby/moby/pull/35422)
- Only chown network files within container metadata [moby/moby#34224](https://github.com/moby/moby/pull/34224)
- Restore error type in FindNetwork [moby/moby#35634](https://github.com/moby/moby/pull/35634)

- Fix consumes MIME type for NetworkConnect [moby/moby#35542](https://github.com/moby/moby/pull/35542)

- Added support for persisting Windows network driver specific options [moby/moby#35563](https://github.com/moby/moby/pull/35563)

- Fix timeout on netlink sockets and watchmiss leak [moby/moby#35677](https://github.com/moby/moby/pull/35677)

- New daemon config for networking diagnosis [moby/moby#35677](https://github.com/moby/moby/pull/35677)

- Clean up node management logic [docker/libnetwork#2036](https://github.com/docker/libnetwork/pull/2036)
- Allocate VIPs when endpoints are restored [docker/swarmkit#2474](https://github.com/docker/swarmkit/pull/2474)

### Runtime

- Update to containerd v1.0.0 [moby/moby#35707](https://github.com/moby/moby/pull/35707)
- Have VFS graphdriver use accelerated in-kernel copy [moby/moby#35537](https://github.com/moby/moby/pull/35537)
- Introduce `workingdir` option for docker exec [moby/moby#35661](https://github.com/moby/moby/pull/35661)
- Bump Go to 1.9.2 [moby/moby#33892](https://github.com/moby/moby/pull/33892) [docker/cli#716](https://github.com/docker/cli/pull/716)
- `/dev` should not be readonly with `--readonly` flag [moby/moby#35344](https://github.com/moby/moby/pull/35344)

- Add custom build-time Graphdrivers priority list [moby/moby#35522](https://github.com/moby/moby/pull/35522)

- LCOW: CLI changes to add platform flag - pull, run, create and build [docker/cli#474](https://github.com/docker/cli/pull/474)
- Fix width/height on Windows for `docker exec` [moby/moby#35631](https://github.com/moby/moby/pull/35631)
- Detect overlay2 support on pre-4.0 kernels [moby/moby#35527](https://github.com/moby/moby/pull/35527)
- Devicemapper: remove container rootfs mountPath after umount [moby/moby#34573](https://github.com/moby/moby/pull/34573)
- Disallow overlay/overlay2 on top of NFS [moby/moby#35483](https://github.com/moby/moby/pull/35483)

- Fix potential panic during plugin set. [moby/moby#35632](https://github.com/moby/moby/pull/35632)
- Fix some issues with locking on the container [moby/moby#35501](https://github.com/moby/moby/pull/35501)
- Fixup some issues with plugin refcounting [moby/moby#35265](https://github.com/moby/moby/pull/35265)

- Add missing lock in ProcessEvent [moby/moby#35516](https://github.com/moby/moby/pull/35516)
- Add vfs quota support [moby/moby#35231](https://github.com/moby/moby/pull/35231)

- Skip empty directories on prior graphdriver detection [moby/moby#35528](https://github.com/moby/moby/pull/35528)
- Skip xfs quota tests when running in user namespace [moby/moby#35526](https://github.com/moby/moby/pull/35526)

- Added SubSecondPrecision to config option. [moby/moby#35529](https://github.com/moby/moby/pull/35529)

- Update fsnotify to fix deadlock in removing watch [moby/moby#35453](https://github.com/moby/moby/pull/35453)

- Fix "duplicate mount point" when `--tmpfs /dev/shm` is used [moby/moby#35467](https://github.com/moby/moby/pull/35467)
- Fix honoring tmpfs-size for user `/dev/shm` mount [moby/moby#35316](https://github.com/moby/moby/pull/35316)
- Fix EBUSY errors under overlayfs and v4.13+ kernels [moby/moby#34948](https://github.com/moby/moby/pull/34948)

- Container: protect health monitor channel [moby/moby#35482](https://github.com/moby/moby/pull/35482)
- Container: protect the health status with mutex [moby/moby#35517](https://github.com/moby/moby/pull/35517)
- Container: update real-time resources [moby/moby#33731](https://github.com/moby/moby/pull/33731)
- Create labels when volume exists only remotely [moby/moby#34896](https://github.com/moby/moby/pull/34896)

- Fix leaking container/exec state [moby/moby#35484](https://github.com/moby/moby/pull/35484)

- Disallow using legacy (v1) registries [moby/moby#35751](https://github.com/moby/moby/pull/35751) and [docker/cli#747](https://github.com/docker/cli/pull/747)

- Windows: Fix case insensitive filename matching against builder cache [moby/moby#35793](https://github.com/moby/moby/pull/35793)
- Fix race conditions around process handling and error checks [moby/moby#35809](https://github.com/moby/moby/pull/35809)

- Ensure containers are stopped on daemon startup [moby/moby#35805](https://github.com/moby/moby/pull/35805)
- Follow containerd namespace conventions [moby/moby#35812](https://github.com/moby/moby/pull/35812)

### Swarm Mode

- Added support for swarm service isolation mode [moby/moby#34424](https://github.com/moby/moby/pull/34424)

- Fix task clean up for tasks that are complete [docker/swarmkit#2477](https://github.com/docker/swarmkit/pull/2477)

### Packaging

- Add Packaging for Fedora 27 [docker/docker-ce-packaging#59](https://github.com/docker/docker-ce-packaging/pull/59)

- Change default versioning scheme to 0.0.0-dev unless specified for packaging [docker/docker-ce-packaging#67](https://github.com/docker/docker-ce-packaging/pull/67)
- Pass Version to engine static builds [docker/docker-ce-packaging#70](https://github.com/docker/docker-ce-packaging/pull/70)

- Added support for aarch64 on Debian (stretch/jessie) and Ubuntu Zesty or newer [docker/docker-ce-packaging#35](https://github.com/docker/docker-ce-packaging/pull/35)

---

# Docker Engine 18.01 release notes

# Docker Engine 18.01 release notes

   Table of contents

---

## 18.01.0-ce

2018-01-10

### Builder

- Fix files not being deleted if user-namespaces are enabled [moby/moby#35822](https://github.com/moby/moby/pull/35822)

- Add support for expanding environment-variables in `docker commit --change ...` [moby/moby#35582](https://github.com/moby/moby/pull/35582)

### Client

- Return errors from client in stack deploy configs [docker/cli#757](https://github.com/docker/cli/pull/757)

- Fix description of filter flag in prune commands [docker/cli#774](https://github.com/docker/cli/pull/774)

- Add "pid" to unsupported options list [docker/cli#768](https://github.com/docker/cli/pull/768)
- Add support for experimental Cli configuration [docker/cli#758](https://github.com/docker/cli/pull/758)
- Add support for generic resources to bash completion [docker/cli#749](https://github.com/docker/cli/pull/749)

- Fix error in zsh completion script for docker exec [docker/cli#751](https://github.com/docker/cli/pull/751)

- Add a debug message when client closes websocket attach connection [moby/moby#35720](https://github.com/moby/moby/pull/35720)

- Fix bash completion for `"docker swarm"` [docker/cli#772](https://github.com/docker/cli/pull/772)

### Documentation

- Correct references to `--publish` long syntax in docs [docker/cli#746](https://github.com/docker/cli/pull/746)
- Corrected descriptions for MAC_ADMIN and MAC_OVERRIDE [docker/cli#761](https://github.com/docker/cli/pull/761)
- Updated developer doc to explain external CLI [moby/moby#35681](https://github.com/moby/moby/pull/35681)

- Fix `"on-failure"` restart policy being documented as "failure" [docker/cli#754](https://github.com/docker/cli/pull/754)
- Fix anchors to "Storage driver options" [docker/cli#748](https://github.com/docker/cli/pull/748)

### Experimental

- Add kubernetes support to `docker stack` command [docker/cli#721](https://github.com/docker/cli/pull/721)

- Don't append the container id to custom directory checkpoints. [moby/moby#35694](https://github.com/moby/moby/pull/35694)

### Logging

- Fix daemon crash when using the GELF log driver over TCP when the GELF server goes down [moby/moby#35765](https://github.com/moby/moby/pull/35765)

- Fix awslogs batch size calculation for large logs [moby/moby#35726](https://github.com/moby/moby/pull/35726)

### Networking

- Windows: Fix to allow docker service to start on Windows VM [docker/libnetwork#1916](https://github.com/docker/libnetwork/pull/1916)
- Fix for docker intercepting DNS requests on ICS network [docker/libnetwork#2014](https://github.com/docker/libnetwork/pull/2014)

- Windows: Added a new network creation driver option [docker/libnetwork#2021](https://github.com/docker/libnetwork/pull/2021)

### Runtime

- Validate Mount-specs on container start to prevent missing host-path [moby/moby#35833](https://github.com/moby/moby/pull/35833)

- Fix overlay2 storage driver inside a user namespace [moby/moby#35794](https://github.com/moby/moby/pull/35794)

- Zfs: fix busy error on container stop [moby/moby#35674](https://github.com/moby/moby/pull/35674)

- Fix health checks not using the container's working directory [moby/moby#35845](https://github.com/moby/moby/pull/35845)
- Fix VFS graph driver failure to initialize because of failure to setup fs quota [moby/moby#35827](https://github.com/moby/moby/pull/35827)
- Fix containerd events being processed twice [moby/moby#35896](https://github.com/moby/moby/pull/35896)

### Swarm mode

- Fix published ports not being updated if a service has the same number of host-mode published ports with Published Port 0 [docker/swarmkit#2376](https://github.com/docker/swarmkit/pull/2376)

- Make the task termination order deterministic [docker/swarmkit#2265](https://github.com/docker/swarmkit/pull/2265)

---

# Docker Engine 18.02 release notes

# Docker Engine 18.02 release notes

   Table of contents

---

## 18.02.0-ce

2018-02-07

### Builder

- Gitutils: fix checking out submodules [moby/moby#35737](https://github.com/moby/moby/pull/35737)

### Client

- Attach: Ensure attach exit code matches container's [docker/cli#696](https://github.com/docker/cli/pull/696)

- Added support for tmpfs-mode in compose file [docker/cli#808](https://github.com/docker/cli/pull/808)
- Adds a new compose file version 3.6 [docker/cli#808](https://github.com/docker/cli/pull/808)

- Fix issue of filter in `docker ps` where `health=starting` returns nothing [moby/moby#35940](https://github.com/moby/moby/pull/35940)

- Improve presentation of published port ranges [docker/cli#581](https://github.com/docker/cli/pull/581)

- Bump Go to 1.9.3 [docker/cli#827](https://github.com/docker/cli/pull/827)

- Fix broken Kubernetes stack flags [docker/cli#831](https://github.com/docker/cli/pull/831)

- Annotate "stack" commands to be "swarm" and "kubernetes" [docker/cli#804](https://github.com/docker/cli/pull/804)

### Experimental

- Add manifest command [docker/cli#138](https://github.com/docker/cli/pull/138)

- LCOW remotefs - return error in Read() implementation [moby/moby#36051](https://github.com/moby/moby/pull/36051)

- LCOW: Coalesce daemon stores, allow dual LCOW and WCOW mode [moby/moby#34859](https://github.com/moby/moby/pull/34859)

- LCOW: Fix OpenFile parameters [moby/moby#36043](https://github.com/moby/moby/pull/36043)

- LCOW: Raise minimum requirement to Windows RS3 RTM build (16299) [moby/moby#36065](https://github.com/moby/moby/pull/36065)

### Logging

- Improve daemon config reload; log active configuration [moby/moby#36019](https://github.com/moby/moby/pull/36019)

- Fixed error detection using IsErrNotFound and IsErrNotImplemented for the ContainerLogs method [moby/moby#36000](https://github.com/moby/moby/pull/36000)

- Add journald tag as SYSLOG_IDENTIFIER [moby/moby#35570](https://github.com/moby/moby/pull/35570)

- Splunk: limit the reader size on error responses [moby/moby#35509](https://github.com/moby/moby/pull/35509)

### Networking

- Disable service on release network results in zero-downtime deployments with rolling upgrades [moby/moby#35960](https://github.com/moby/moby/pull/35960)

- Fix services failing to start if multiple networks with the same name exist in different spaces [moby/moby#30897](https://github.com/moby/moby/pull/30897)
- Fix duplicate networks being added with `docker service update --network-add` [docker/cli#780](https://github.com/docker/cli/pull/780)
- Fixing ingress network when upgrading from 17.09 to 17.12. [moby/moby#36003](https://github.com/moby/moby/pull/36003)
- Fix ndots configuration [docker/libnetwork#1995](https://github.com/docker/libnetwork/pull/1995)
- Fix IPV6 networking being deconfigured if live-restore is enabled [docker/libnetwork#2043](https://github.com/docker/libnetwork/pull/2043)

- Add support for MX type DNS queries in the embedded DNS server [docker/libnetwork#2041](https://github.com/docker/libnetwork/pull/2041)

### Packaging

- Added packaging for Fedora 26, Fedora 27, and Centos 7 on aarch64 [docker/docker-ce-packaging#71](https://github.com/docker/docker-ce-packaging/pull/71)

- Removed support for Ubuntu Zesty [docker/docker-ce-packaging#73](https://github.com/docker/docker-ce-packaging/pull/73)
- Removed support for Fedora 25 [docker/docker-ce-packaging#72](https://github.com/docker/docker-ce-packaging/pull/72)

### Runtime

- Fixes unexpected Docker Daemon shutdown based on pipe error [moby/moby#35968](https://github.com/moby/moby/pull/35968)
- Fix some occurrences of hcsshim::ImportLayer failed in Win32: The system cannot find the path specified [moby/moby#35924](https://github.com/moby/moby/pull/35924)

- Windows: increase the maximum layer size during build to 127GB [moby/moby#35925](https://github.com/moby/moby/pull/35925)

- Fix Devicemapper: Error running DeleteDevice dm_task_run failed [moby/moby#35919](https://github.com/moby/moby/pull/35919)

- Introduce « exec_die » event [moby/moby#35744](https://github.com/moby/moby/pull/35744)

- Update API to version 1.36 [moby/moby#35744](https://github.com/moby/moby/pull/35744)

- Fix `docker update` not updating cpu quota, and cpu-period of a running container [moby/moby#36030](https://github.com/moby/moby/pull/36030)

- Make container shm parent unbindable [moby/moby#35830](https://github.com/moby/moby/pull/35830)

- Make image (layer) downloads faster by using pigz [moby/moby#35697](https://github.com/moby/moby/pull/35697)
- Protect the daemon from volume plugins that are slow or deadlocked [moby/moby#35441](https://github.com/moby/moby/pull/35441)

- Fix `DOCKER_RAMDISK` environment variable not being honoured [moby/moby#35957](https://github.com/moby/moby/pull/35957)

- Bump containerd to 1.0.1 (9b55aab90508bd389d7654c4baf173a981477d55) [moby/moby#35986](https://github.com/moby/moby/pull/35986)
- Update runc to fix hang during start and exec [moby/moby#36097](https://github.com/moby/moby/pull/36097)

- Fix "--node-generic-resource" singular/plural [moby/moby#36125](https://github.com/moby/moby/pull/36125)

---

# Docker Engine 18.03 release notes

# Docker Engine 18.03 release notes

   Table of contents

---

## 18.03.1-ce

2018-04-26

### Client

- Fix error with merge compose file with networks [docker/cli#983](https://github.com/docker/cli/pull/983)

- Fix docker stack deploy re-deploying services after the service was updated with `--force` [docker/cli#963](https://github.com/docker/cli/pull/963)
- Fix docker version output alignment [docker/cli#965](https://github.com/docker/cli/pull/965)

### Runtime

- Fix AppArmor profiles not being applied to `docker exec` processes [moby/moby#36466](https://github.com/moby/moby/pull/36466)
- Don't sort plugin mount slice [moby/moby#36711](https://github.com/moby/moby/pull/36711)
- Daemon/cluster: handle partial attachment entries during configure [moby/moby#36769](https://github.com/moby/moby/pull/36769)

- Bump Golang to 1.9.5 [moby/moby#36779](https://github.com/moby/moby/pull/36779) [docker/cli#986](https://github.com/docker/cli/pull/986)

- Daemon/stats: more resilient cpu sampling [moby/moby#36519](https://github.com/moby/moby/pull/36519)

- Containerd: update to 1.0.3 release [moby/moby#36749](https://github.com/moby/moby/pull/36749)

- Fix Windows layer leak when write fails [moby/moby#36728](https://github.com/moby/moby/pull/36728)

- Don't make container mount unbindable [moby/moby#36768](https://github.com/moby/moby/pull/36768)

- Fix Daemon panics on container export after a daemon restart [moby/moby/36586](https://github.com/moby/moby/pull/36586)
- Fix digest cache being removed on autherrors [moby/moby#36509](https://github.com/moby/moby/pull/36509)
- Make sure plugin container is removed on failure [moby/moby#36715](https://github.com/moby/moby/pull/36715)
- Copy: avoid using all system memory with authz plugins [moby/moby#36595](https://github.com/moby/moby/pull/36595)
- Relax some libcontainerd client locking [moby/moby#36848](https://github.com/moby/moby/pull/36848)
- Update `hcsshim` to v0.6.10 to address [CVE-2018-8115](https://portal.msrc.microsoft.com/en-us/security-guidance/advisory/CVE-2018-8115)

### Swarm Mode

- Increase raft Election tick to 10 times Heartbeat tick [moby/moby#36672](https://github.com/moby/moby/pull/36672)

### Networking

- Gracefully remove LB endpoints from services [docker/libnetwork#2112](https://github.com/docker/libnetwork/pull/2112)
- Retry other external DNS servers on ServFail [docker/libnetwork#2121](https://github.com/docker/libnetwork/pull/2121)
- Improve scalability of bridge network isolation rules [docker/libnetwork#2117](https://github.com/docker/libnetwork/pull/2117)
- Allow for larger preset property values, do not override [docker/libnetwork#2124](https://github.com/docker/libnetwork/pull/2124)
- Prevent panics on concurrent reads/writes when calling `changeNodeState` [docker/libnetwork#2136](https://github.com/docker/libnetwork/pull/2136)

## 18.03.0-ce

2018-03-21

### Builder

- Switch to -buildmode=pie [moby/moby#34369](https://github.com/moby/moby/pull/34369)
- Allow Dockerfile to be outside of build-context [docker/cli#886](https://github.com/docker/cli/pull/886)
- Builder: fix wrong cache hits building from tars [moby/moby#36329](https://github.com/moby/moby/pull/36329)

- Fixes files leaking to other images in a multi-stage build [moby/moby#36338](https://github.com/moby/moby/pull/36338)

### Client

- Simplify the marshaling of compose types.Config [docker/cli#895](https://github.com/docker/cli/pull/895)

- Add support for multiple composefile when deploying [docker/cli#569](https://github.com/docker/cli/pull/569)

- Fix broken Kubernetes stack flags [docker/cli#831](https://github.com/docker/cli/pull/831)
- Fix stack marshaling for Kubernetes [docker/cli#890](https://github.com/docker/cli/pull/890)
- Fix and simplify bash completion for service env, mounts and labels [docker/cli#682](https://github.com/docker/cli/pull/682)
- Fix `before` and `since` filter for `docker ps` [moby/moby#35938](https://github.com/moby/moby/pull/35938)
- Fix `--label-file` weird behavior [docker/cli#838](https://github.com/docker/cli/pull/838)
- Fix compilation of defaultCredentialStore() on unsupported platforms [docker/cli#872](https://github.com/docker/cli/pull/872)

- Improve and fix bash completion for images [docker/cli#717](https://github.com/docker/cli/pull/717)

- Added check for empty source in bind mount [docker/cli#824](https://github.com/docker/cli/pull/824)

- Fix TLS from environment variables in client [moby/moby#36270](https://github.com/moby/moby/pull/36270)

- docker build now runs faster when registry-specific credential helper(s) are configured [docker/cli#840](https://github.com/docker/cli/pull/840)
- Update event filter zsh completion with `disable`, `enable`, `install` and `remove` [docker/cli#372](https://github.com/docker/cli/pull/372)
- Produce errors when empty ids are passed into inspect calls [moby/moby#36144](https://github.com/moby/moby/pull/36144)
- Marshall version for the k8s controller [docker/cli#891](https://github.com/docker/cli/pull/891)
- Set a non-zero timeout for HTTP client communication with plugin backend [docker/cli#883](https://github.com/docker/cli/pull/883)

- Add DOCKER_TLS environment variable for --tls option [docker/cli#863](https://github.com/docker/cli/pull/863)
- Add --template-driver option for secrets/configs [docker/cli#896](https://github.com/docker/cli/pull/896)
- Move `docker trust` commands out of experimental [docker/cli#934](https://github.com/docker/cli/pull/934) [docker/cli#935](https://github.com/docker/cli/pull/935) [docker/cli#944](https://github.com/docker/cli/pull/944)

### Logging

- AWS logs - don't add new lines to maximum sized events [moby/moby#36078](https://github.com/moby/moby/pull/36078)
- Move log validator logic after plugins are loaded [moby/moby#36306](https://github.com/moby/moby/pull/36306)
- Support a proxy in Splunk log driver [moby/moby#36220](https://github.com/moby/moby/pull/36220)

- Fix log tail with empty logs [moby/moby#36305](https://github.com/moby/moby/pull/36305)

### Networking

- Libnetwork revendoring [moby/moby#36137](https://github.com/moby/moby/pull/36137)

- Fix for deadlock on exit with Memberlist revendor [docker/libnetwork#2040](https://github.com/docker/libnetwork/pull/2040)

- Fix user specified ndots option [docker/libnetwork#2065](https://github.com/docker/libnetwork/pull/2065)

- Fix to use ContainerID for Windows instead of SandboxID [docker/libnetwork#2010](https://github.com/docker/libnetwork/pull/2010)

- Verify NetworkingConfig to make sure EndpointSettings is not nil [moby/moby#36077](https://github.com/moby/moby/pull/36077)

- Fix `DockerNetworkInternalMode` issue [moby/moby#36298](https://github.com/moby/moby/pull/36298)
- Fix race in attachable network attachment [moby/moby#36191](https://github.com/moby/moby/pull/36191)
- Fix timeout issue of `InspectNetwork` on AArch64 [moby/moby#36257](https://github.com/moby/moby/pull/36257)

- Verbose info is missing for partial overlay ID [moby/moby#35989](https://github.com/moby/moby/pull/35989)
- Update `FindNetwork` to address network name duplications [moby/moby#30897](https://github.com/moby/moby/pull/30897)
- Disallow attaching ingress network [docker/swarmkit#2523](https://github.com/docker/swarmkit/pull/2523)

- Prevent implicit removal of the ingress network [moby/moby#36538](https://github.com/moby/moby/pull/36538)
- Fix stale HNS endpoints on Windows [moby/moby#36603](https://github.com/moby/moby/pull/36603)
- IPAM fixes for duplicate IP addresses [docker/libnetwork#2104](https://github.com/docker/libnetwork/pull/2104) [docker/libnetwork#2105](https://github.com/docker/libnetwork/pull/2105)

### Runtime

- Enable HotAdd for Windows [moby/moby#35414](https://github.com/moby/moby/pull/35414)
- LCOW: Graphdriver fix deadlock in hotRemoveVHDs [moby/moby#36114](https://github.com/moby/moby/pull/36114)
- LCOW: Regular mount if only one layer [moby/moby#36052](https://github.com/moby/moby/pull/36052)
- Remove interim env var LCOW_API_PLATFORM_IF_OMITTED [moby/moby#36269](https://github.com/moby/moby/pull/36269)
- Revendor Microsoft/opengcs @ v0.3.6 [moby/moby#36108](https://github.com/moby/moby/pull/36108)

- Fix issue of ExitCode and PID not show up in Task.Status.ContainerStatus [moby/moby#36150](https://github.com/moby/moby/pull/36150)
- Fix issue with plugin scanner going too deep [moby/moby#36119](https://github.com/moby/moby/pull/36119)

- Do not make graphdriver homes private mounts [moby/moby#36047](https://github.com/moby/moby/pull/36047)
- Do not recursive unmount on cleanup of zfs/btrfs [moby/moby#36237](https://github.com/moby/moby/pull/36237)
- Don't restore image if layer does not exist [moby/moby#36304](https://github.com/moby/moby/pull/36304)
- Adjust minimum API version for templated configs/secrets [moby/moby#36366](https://github.com/moby/moby/pull/36366)
- Bump containerd to 1.0.2 (cfd04396dc68220d1cecbe686a6cc3aa5ce3667c) [moby/moby#36308](https://github.com/moby/moby/pull/36308)
- Bump Golang to 1.9.4 [moby/moby#36243](https://github.com/moby/moby/pull/36243)
- Ensure daemon root is unmounted on shutdown [moby/moby#36107](https://github.com/moby/moby/pull/36107)
- Update runc to 6c55f98695e902427906eed2c799e566e3d3dfb5 [moby/moby#36222](https://github.com/moby/moby/pull/36222)

- Fix container cleanup on daemon restart [moby/moby#36249](https://github.com/moby/moby/pull/36249)

- Support SCTP port mapping (bump up API to v1.37) [moby/moby#33922](https://github.com/moby/moby/pull/33922)
- Support SCTP port mapping [docker/cli#278](https://github.com/docker/cli/pull/278)

- Fix Volumes property definition in ContainerConfig [moby/moby#35946](https://github.com/moby/moby/pull/35946)

- Bump moby and dependencies [docker/cli#829](https://github.com/docker/cli/pull/829)
- C.RWLayer: check for nil before use [moby/moby#36242](https://github.com/moby/moby/pull/36242)

- Add `REMOVE` and `ORPHANED` to TaskState [moby/moby#36146](https://github.com/moby/moby/pull/36146)

- Fixed error detection using `IsErrNotFound` and `IsErrNotImplemented` for `ContainerStatPath`, `CopyFromContainer`, and `CopyToContainer` methods [moby/moby#35979](https://github.com/moby/moby/pull/35979)

- Add an integration/internal/container helper package [moby/moby#36266](https://github.com/moby/moby/pull/36266)
- Add canonical import path [moby/moby#36194](https://github.com/moby/moby/pull/36194)
- Add/use container.Exec() to integration [moby/moby#36326](https://github.com/moby/moby/pull/36326)

- Fix "--node-generic-resource" singular/plural [moby/moby#36125](https://github.com/moby/moby/pull/36125)

- Daemon.cleanupContainer: nullify container RWLayer upon release [moby/moby#36160](https://github.com/moby/moby/pull/36160)
- Daemon: passdown the `--oom-kill-disable` option to containerd [moby/moby#36201](https://github.com/moby/moby/pull/36201)
- Display a warn message when there is binding ports and net mode is host [moby/moby#35510](https://github.com/moby/moby/pull/35510)
- Refresh containerd remotes on containerd restarted [moby/moby#36173](https://github.com/moby/moby/pull/36173)
- Set daemon root to use shared propagation [moby/moby#36096](https://github.com/moby/moby/pull/36096)
- Optimizations for recursive unmount [moby/moby#34379](https://github.com/moby/moby/pull/34379)
- Perform plugin mounts in the runtime [moby/moby#35829](https://github.com/moby/moby/pull/35829)
- Graphdriver: Fix RefCounter memory leak [moby/moby#36256](https://github.com/moby/moby/pull/36256)
- Use continuity fs package for volume copy [moby/moby#36290](https://github.com/moby/moby/pull/36290)
- Use proc/exe for reexec [moby/moby#36124](https://github.com/moby/moby/pull/36124)

- Add API support for templated secrets and configs [moby/moby#33702](https://github.com/moby/moby/pull/33702) and [moby/moby#36366](https://github.com/moby/moby/pull/36366)

- Use rslave propagation for mounts from daemon root [moby/moby#36055](https://github.com/moby/moby/pull/36055)

- Add /proc/keys to masked paths [moby/moby#36368](https://github.com/moby/moby/pull/36368)

- Bump Runc to 1.0.0-rc5 [moby/moby#36449](https://github.com/moby/moby/pull/36449)

- Fixes `runc exec` on big-endian architectures [moby/moby#36449](https://github.com/moby/moby/pull/36449)

- Use chroot when mount namespaces aren't provided [moby/moby#36449](https://github.com/moby/moby/pull/36449)

- Fix systemd slice expansion so that it could be consumed by cAdvisor [moby/moby#36449](https://github.com/moby/moby/pull/36449)
- Fix devices mounted with wrong uid/gid [moby/moby#36449](https://github.com/moby/moby/pull/36449)
- Fix read-only containers with IPC private mounts `/dev/shm` read-only [moby/moby#36526](https://github.com/moby/moby/pull/36526)

### Swarm Mode

- Replace EC Private Key with PKCS#8 PEMs [docker/swarmkit#2246](https://github.com/docker/swarmkit/pull/2246)
- Fix IP overlap with empty EndpointSpec [docker/swarmkit #2505](https://github.com/docker/swarmkit/pull/2505)
- Add support for Support SCTP port mapping [docker/swarmkit#2298](https://github.com/docker/swarmkit/pull/2298)
- Do not reschedule tasks if only placement constraints change and are satisfied by the assigned node [docker/swarmkit#2496](https://github.com/docker/swarmkit/pull/2496)
- Ensure task reaper stopChan is closed no more than once [docker/swarmkit #2491](https://github.com/docker/swarmkit/pull/2491)
- Synchronization fixes [docker/swarmkit#2495](https://github.com/docker/swarmkit/pull/2495)
- Add log message to indicate message send retry if streaming unimplemented [docker/swarmkit#2483](https://github.com/docker/swarmkit/pull/2483)
- Debug logs for session, node events on dispatcher, heartbeats [docker/swarmkit#2486](https://github.com/docker/swarmkit/pull/2486)

- Add swarm types to bash completion event type filter [docker/cli#888](https://github.com/docker/cli/pull/888)

- Fix issue where network inspect does not show Created time for networks in swarm scope [moby/moby#36095](https://github.com/moby/moby/pull/36095)

---

# Docker Engine 18.04 release notes

# Docker Engine 18.04 release notes

   Table of contents

---

## 18.04.0-ce

2018-04-10

### Builder

- Fix typos in builder and client. [moby/moby#36424](https://github.com/moby/moby/pull/36424)

### Client

- Print Stack API and Kubernetes versions in version command. [docker/cli#898](https://github.com/docker/cli/pull/898)

- Fix Kubernetes duplication in version command. [docker/cli#953](https://github.com/docker/cli/pull/953)

- Use HasAvailableFlags instead of HasFlags for Options in help. [docker/cli#959](https://github.com/docker/cli/pull/959)

- Add support for mandatory variables to stack deploy. [docker/cli#893](https://github.com/docker/cli/pull/893)

- Fix docker stack services command Port output. [docker/cli#943](https://github.com/docker/cli/pull/943)

- Deprecate unencrypted storage. [docker/cli#561](https://github.com/docker/cli/pull/561)
- Don't set a default filename for ConfigFile. [docker/cli#917](https://github.com/docker/cli/pull/917)

- Fix compose network name. [docker/cli#941](https://github.com/docker/cli/pull/941)

### Logging

- Silent login: use credentials from cred store to login. [docker/cli#139](https://github.com/docker/cli/pull/139)

- Add support for compressibility of log file. [moby/moby#29932](https://github.com/moby/moby/pull/29932)

- Fix empty LogPath with non-blocking logging mode. [moby/moby#36272](https://github.com/moby/moby/pull/36272)

### Networking

- Prevent explicit removal of ingress network. [moby/moby#36538](https://github.com/moby/moby/pull/36538)

### Runtime

- Devmapper cleanup improvements. [moby/moby#36307](https://github.com/moby/moby/pull/36307)
- Devmapper.Mounted: remove. [moby/moby#36437](https://github.com/moby/moby/pull/36437)
- Devmapper/Remove(): use Rmdir, ignore errors. [moby/moby#36438](https://github.com/moby/moby/pull/36438)
- LCOW - Change platform parser directive to FROM statement flag. [moby/moby#35089](https://github.com/moby/moby/pull/35089)
- Split daemon service code to windows file. [moby/moby#36653](https://github.com/moby/moby/pull/36653)
- Windows: Block pulling uplevel images. [moby/moby#36327](https://github.com/moby/moby/pull/36327)
- Windows: Hyper-V containers are broken after 36586 was merged. [moby/moby#36610](https://github.com/moby/moby/pull/36610)
- Windows: Move kernel_windows to use golang registry functions. [moby/moby#36617](https://github.com/moby/moby/pull/36617)
- Windows: Pass back system errors on container exit. [moby/moby#35967](https://github.com/moby/moby/pull/35967)
- Windows: Remove servicing mode. [moby/moby#36267](https://github.com/moby/moby/pull/36267)
- Windows: Report Version and UBR. [moby/moby#36451](https://github.com/moby/moby/pull/36451)
- Bump Runc to 1.0.0-rc5. [moby/moby#36449](https://github.com/moby/moby/pull/36449)
- Mount failure indicates the path that failed. [moby/moby#36407](https://github.com/moby/moby/pull/36407)
- Change return for errdefs.getImplementer(). [moby/moby#36489](https://github.com/moby/moby/pull/36489)
- Client: fix hijackedconn reading from buffer. [moby/moby#36663](https://github.com/moby/moby/pull/36663)
- Content encoding negotiation added to archive request. [moby/moby#36164](https://github.com/moby/moby/pull/36164)
- Daemon/stats: more resilient cpu sampling. [moby/moby#36519](https://github.com/moby/moby/pull/36519)
- Daemon/stats: remove obnoxious types file. [moby/moby#36494](https://github.com/moby/moby/pull/36494)
- Daemon: use context error rather than inventing new one. [moby/moby#36670](https://github.com/moby/moby/pull/36670)
- Enable CRIU on non-amd64 architectures (v2). [moby/moby#36676](https://github.com/moby/moby/pull/36676)

- Fixes intermittent client hang after closing stdin to attached container [moby/moby#36517](https://github.com/moby/moby/pull/36517)
- Fix daemon panic on container export after restart [moby/moby#36586](https://github.com/moby/moby/pull/36586)
- Follow-up fixes on multi-stage moby's Dockerfile. [moby/moby#36425](https://github.com/moby/moby/pull/36425)

- Freeze busybox and latest glibc in Docker image. [moby/moby#36375](https://github.com/moby/moby/pull/36375)
- If container will run as non root user, drop permitted, effective caps early. [moby/moby#36587](https://github.com/moby/moby/pull/36587)
- Layer: remove metadata store interface. [moby/moby#36504](https://github.com/moby/moby/pull/36504)
- Minor optimizations to dockerd. [moby/moby#36577](https://github.com/moby/moby/pull/36577)
- Whitelist statx syscall. [moby/moby#36417](https://github.com/moby/moby/pull/36417)

- Add missing error return for plugin creation. [moby/moby#36646](https://github.com/moby/moby/pull/36646)

- Fix AppArmor not being applied to Exec processes. [moby/moby#36466](https://github.com/moby/moby/pull/36466)

- Daemon/logger/ring.go: log error not instance. [moby/moby#36475](https://github.com/moby/moby/pull/36475)

- Fix stats collector spinning CPU if no stats are collected. [moby/moby#36609](https://github.com/moby/moby/pull/36609)
- Fix(distribution): digest cache should not be moved if it was an auth. [moby/moby#36509](https://github.com/moby/moby/pull/36509)
- Make sure plugin container is removed on failure. [moby/moby#36715](https://github.com/moby/moby/pull/36715)

- Bump to containerd 1.0.3. [moby/moby#36749](https://github.com/moby/moby/pull/36749)
- Don't sort plugin mount slice. [moby/moby#36711](https://github.com/moby/moby/pull/36711)

### Swarm Mode

- Fixes for synchronizing the dispatcher shutdown with in-progress rpcs. [moby/moby#36371](https://github.com/moby/moby/pull/36371)
- Increase raft ElectionTick to 10xHeartbeatTick. [moby/moby#36672](https://github.com/moby/moby/pull/36672)
- Make Swarm manager Raft quorum parameters configurable in daemon config. [moby/moby#36726](https://github.com/moby/moby/pull/36726)
- Ingress network should not be attachable. [docker/swarmkit#2523](https://github.com/docker/swarmkit/pull/2523)
- [manager/state] Add fernet as an option for raft encryption. [docker/swarmkit#2535](https://github.com/docker/swarmkit/pull/2535)
- Log GRPC server errors. [docker/swarmkit#2541](https://github.com/docker/swarmkit/pull/2541)
- Log leadership changes at the manager level. [docker/swarmkit#2542](https://github.com/docker/swarmkit/pull/2542)
- Remove the containerd executor. [docker/swarmkit#2568](https://github.com/docker/swarmkit/pull/2568)
- Agent: backoff session when no remotes are available. [docker/swarmkit#2570](https://github.com/docker/swarmkit/pull/2570)
- [ca/manager] Remove root CA key encryption support entirely. [docker/swarmkit#2573](https://github.com/docker/swarmkit/pull/2573)

- Fix agent logging race. [docker/swarmkit#2578](https://github.com/docker/swarmkit/pull/2578)

- Adding logic to restore networks in order. [docker/swarmkit#2571](https://github.com/docker/swarmkit/pull/2571)

---

# Docker Engine 18.05 release notes

# Docker Engine 18.05 release notes

   Table of contents

---

## 18.05.0-ce

2018-05-09

### Builder

- Adding `netbsd` compatibility to the package `pkg/term`. [moby/moby#36887](https://github.com/moby/moby/pull/36887)
- Standardizes output path for artifacts of intermediate builds to `/build/`. [moby/moby#36858](https://github.com/moby/moby/pull/36858)

### Client

- Fix `docker stack deploy` reference flag. [docker/cli#981](https://github.com/docker/cli/pull/981)
- Fix docker stack deploy re-deploying services after the service was updated with `--force`. [docker/cli#963](https://github.com/docker/cli/pull/963)

- Add bash completion for `secret|config create --template-driver`. [docker/cli#1004](https://github.com/docker/cli/pull/1004)
- Add fish completions for docker trust subcommand. [docker/cli#984](https://github.com/docker/cli/pull/984)

- Fix --format example for docker history. [docker/cli#980](https://github.com/docker/cli/pull/980)
- Fix error with merge composefile with networks. [docker/cli#983](https://github.com/docker/cli/pull/983)

### Logging

- Standardized the properties of storage-driver log messages. [moby/moby#36492](https://github.com/moby/moby/pull/36492)
- Improve partial message support in logger. [moby/moby#35831](https://github.com/moby/moby/pull/35831)

### Networking

- Allow for larger preset property values, do not override. [docker/libnetwork#2124](https://github.com/docker/libnetwork/pull/2124)
- networkdb: User write lock in handleNodeEvent. [docker/libnetwork#2136](https://github.com/docker/libnetwork/pull/2136)

- Import libnetwork fix for rolling updates. [moby/moby#36638](https://github.com/moby/moby/pull/36638)
- Update libnetwork to improve scalability of bridge network isolation rules. [moby/moby#36774](https://github.com/moby/moby/pull/36774)

- Fix a misused network object name. [moby/moby#36745](https://github.com/moby/moby/pull/36745)

### Runtime

- LCOW: Implement `docker save`. [moby/moby#36599](https://github.com/moby/moby/pull/36599)
- Pkg: devmapper: dynamically load dm_task_deferred_remove. [moby/moby#35518](https://github.com/moby/moby/pull/35518)
- Windows: Add GetLayerPath implementation in graphdriver. [moby/moby#36738](https://github.com/moby/moby/pull/36738)

- Fix Windows layer leak when write fails. [moby/moby#36728](https://github.com/moby/moby/pull/36728)
- Fix FIFO, sockets and device files when run in user NS. [moby/moby#36756](https://github.com/moby/moby/pull/36756)
- Fix docker version output alignment. [docker/cli#965](https://github.com/docker/cli/pull/965)

- Always make sysfs read-write with privileged. [moby/moby#36808](https://github.com/moby/moby/pull/36808)
- Bump Golang to 1.10.1. [moby/moby#35739](https://github.com/moby/moby/pull/35739)
- Bump containerd client. [moby/moby#36684](https://github.com/moby/moby/pull/36684)
- Bump golang.org/x/net to go1.10 release commit. [moby/moby#36894](https://github.com/moby/moby/pull/36894)
- Context.WithTimeout: do call the cancel func. [moby/moby#36920](https://github.com/moby/moby/pull/36920)
- Copy: avoid using all system memory with authz plugins. [moby/moby#36595](https://github.com/moby/moby/pull/36595)
- Daemon/cluster: handle partial attachment entries during configure. [moby/moby#36769](https://github.com/moby/moby/pull/36769)
- Don't make container mount unbindable. [moby/moby#36768](https://github.com/moby/moby/pull/36768)
- Extra check before unmounting on shutdown. [moby/moby#36879](https://github.com/moby/moby/pull/36879)
- Move mount parsing to separate package. [moby/moby#36896](https://github.com/moby/moby/pull/36896)
- No global volume driver store. [moby/moby#36637](https://github.com/moby/moby/pull/36637)
- Pkg/mount improvements. [moby/moby#36091](https://github.com/moby/moby/pull/36091)
- Relax some libcontainerd client locking. [moby/moby#36848](https://github.com/moby/moby/pull/36848)
- Remove daemon dependency on api packages. [moby/moby#36912](https://github.com/moby/moby/pull/36912)
- Remove the retries for service update. [moby/moby#36827](https://github.com/moby/moby/pull/36827)
- Revert unencryted storage warning prompt. [docker/cli#1008](https://github.com/docker/cli/pull/1008)
- Support cancellation in `directory.Size()`. [moby/moby#36734](https://github.com/moby/moby/pull/36734)
- Switch from x/net/context -> context. [moby/moby#36904](https://github.com/moby/moby/pull/36904)
- Fixed a function to check Content-type is `application/json` or not. [moby/moby#36778](https://github.com/moby/moby/pull/36778)

- Add default pollSettings config functions. [moby/moby#36706](https://github.com/moby/moby/pull/36706)
- Add if judgment before receiving operations on daemonWaitCh. [moby/moby#36651](https://github.com/moby/moby/pull/36651)

- Fix issues with running volume tests as non-root.. [moby/moby#36935](https://github.com/moby/moby/pull/36935)

### Swarm Mode

- RoleManager will remove detected nodes from the cluster membership [docker/swarmkit#2548](https://github.com/docker/swarmkit/pull/2548)
- Scheduler/TaskReaper: handle unassigned tasks marked for shutdown [docker/swarmkit#2574](https://github.com/docker/swarmkit/pull/2574)
- Avoid predefined error log. [docker/swarmkit#2561](https://github.com/docker/swarmkit/pull/2561)
- Task reaper should delete tasks with removed slots that were not yet assigned. [docker/swarmkit#2557](https://github.com/docker/swarmkit/pull/2557)
- Agent reports FIPS status. [docker/swarmkit#2587](https://github.com/docker/swarmkit/pull/2587)

- Fix: timeMutex critical operation outside of critical section. [docker/swarmkit#2603](https://github.com/docker/swarmkit/pull/2603)

- Expose swarmkit's Raft tuning parameters in engine config. [moby/moby#36726](https://github.com/moby/moby/pull/36726)
- Make internal/test/daemon.Daemon swarm aware. [moby/moby#36826](https://github.com/moby/moby/pull/36826)
