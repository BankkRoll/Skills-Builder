# Docker Engine 18.06 release notes and more

# Docker Engine 18.06 release notes

# Docker Engine 18.06 release notes

   Table of contents

---

## 18.06.3-ce

2019-02-19

### Security fixes for Docker Engine

- Change how the `runc` critical vulnerability patch is applied to include the fix in RPM packages. [docker/engine#156](https://github.com/docker/engine/pull/156)

## 18.06.2

2019-02-11

### Security fixes for Docker Engine

- Update `runc` to address a critical vulnerability that allows specially-crafted containers to gain administrative privileges on the host. [CVE-2019-5736](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-5736)
- Ubuntu 14.04 customers using a 3.13 kernel will need to upgrade to a supported Ubuntu 4.x kernel

## 18.06.1-ce

2018-08-21

### Builder

- Fix no error if build args are missing during docker build. [docker/engine#25](https://github.com/docker/engine/pull/25)

- Set BuildKit's ExportedProduct variable to show useful errors. [docker/engine#21](https://github.com/docker/engine/pull/21)

### Client

- Various shell completion script updates: [docker/cli#1229](https://github.com/docker/cli/pull/1229),
  [docker/cli#1268](https://github.com/docker/cli/pull/1268), and [docker/cli#1272](https://github.com/docker/cli/pull/1272)

- Fix `DOCKER_CONFIG` warning message and fallback search. [docker/cli#1241](https://github.com/docker/cli/pull/1241)
- Fix help message flags on `docker stack` commands and sub-commands. [docker/cli#1267](https://github.com/docker/cli/pull/1267)

### Runtime

- Disable CRI plugin listening on port 10010 by default. [docker/engine#29](https://github.com/docker/engine/pull/29)
- Update containerd to v1.1.2. [docker/engine#33](https://github.com/docker/engine/pull/33)

- Windows: Do not invoke HCS shutdown if terminate called. [docker/engine#31](https://github.com/docker/engine/pull/31)

- Windows: Select polling-based watcher for Windows log watcher. [docker/engine#34](https://github.com/docker/engine/pull/34)

### Swarm Mode

- Fix the condition used for skipping over running tasks. [docker/swarmkit#2677](https://github.com/docker/swarmkit/pull/2677)
- Fix task sorting. [docker/swarmkit#2712](https://github.com/docker/swarmkit/pull/2712)

## 18.06.0-ce

2018-07-18

### Important notes about this release

- Docker 18.06 CE will be the last release with a 4-month maintenance lifecycle. The planned Docker 18.09 CE release will be supported for 7 months with Docker 19.03 CE being the next release in line. More details about the release process can be found
  [here](https://docs.docker.com/get-started/get-docker/).

### Builder

- Builder: fix layer leak on multi-stage wildcard copy. [moby/moby#37178](https://github.com/moby/moby/pull/37178)
- Fix parsing of invalid environment variable substitution . [moby/moby#37134](https://github.com/moby/moby/pull/37134)
- Builder: use the arch info from base image. [moby/moby#36816](https://github.com/moby/moby/pull/36816) [moby/moby#37197](https://github.com/moby/moby/pull/37197)

- New experimental builder backend based on [BuildKit](https://github.com/moby/buildkit). To enable, run daemon in experimental mode and set `DOCKER_BUILDKIT=1` environment variable on the docker CLI. [moby/moby#37151](https://github.com/moby/moby/pull/37151) [docker/cli#1111](https://github.com/docker/cli/pull/1111)

- Fix handling uppercase targets names in multi-stage builds. [moby/moby#36960](https://github.com/moby/moby/pull/36960)

### Client

- Bump spf13/cobra to v0.0.3, pflag to v1.0.1. [moby/moby#37106](https://github.com/moby/moby/pull/37106)
- Add support for the new Stack API for Kubernetes v1beta2. [docker/cli#899](https://github.com/docker/cli/pull/899)
- K8s: more robust stack error detection on deploy. [docker/cli#948](https://github.com/docker/cli/pull/948)
- Support for rollback config in compose 3.7. [docker/cli#409](https://github.com/docker/cli/pull/409)
- Update Cobra and pflag, and use built-in --version feature. [docker/cli#1069](https://github.com/docker/cli/pull/1069)
- Fix `docker stack deploy --prune` with empty name removing all services. [docker/cli#1088](https://github.com/docker/cli/pull/1088)
- [Kubernetes] stack services filters. [docker/cli#1023](https://github.com/docker/cli/pull/1023)

- Only show orchestrator flag in root, stack and version commands in help. [docker/cli#1106](https://github.com/docker/cli/pull/1106)
- Add an `Extras` field on the compose config types. [docker/cli#1126](https://github.com/docker/cli/pull/1126)
- Add options to the compose loader. [docker/cli#1128](https://github.com/docker/cli/pull/1128)

- Fix always listing nodes in docker stack ps command on Kubernetes. [docker/cli#1093](https://github.com/docker/cli/pull/1093)
- Fix output being shown twice on stack rm error message. [docker/cli#1093](https://github.com/docker/cli/pull/1093)

- Extend client API with custom HTTP requests. [moby/moby#37071](https://github.com/moby/moby/pull/37071)
- Changed error message for unreadable files to clarify possibility of a .Dockerignore entry. [docker/cli#1053](https://github.com/docker/cli/pull/1053)
- Restrict kubernetes.allNamespaces value to 'enabled' or 'disabled' in configuration file. [docker/cli#1087](https://github.com/docker/cli/pull/1087)
- Check errors when initializing the docker client in the help command. [docker/cli#1119](https://github.com/docker/cli/pull/1119)
- Better namespace experience with Kubernetes. Fix using namespace defined in ~/.kube/config for stack commands. Add a NAMESPACE column for docker stack ls command. Add a --all-namespaces flag for docker stack ls command. [docker/cli#991](https://github.com/docker/cli/pull/991)
- Export Push and Save. [docker/cli#1123](https://github.com/docker/cli/pull/1123)
- Export pull as a public function. [docker/cli#1026](https://github.com/docker/cli/pull/1026)
- Remove Kubernetes commands from experimental. [docker/cli#1068](https://github.com/docker/cli/pull/1068)
- Adding configs/secrets to service inspect pretty. [docker/cli#1006](https://github.com/docker/cli/pull/1006)

- Fix service filtering by name on Kubernetes. [docker/cli#1101](https://github.com/docker/cli/pull/1101)
- Fix component information alignment in `docker version`. [docker/cli#1065](https://github.com/docker/cli/pull/1065)
- Fix cpu/memory limits and reservations being reset on service update. [docker/cli#1079](https://github.com/docker/cli/pull/1079)

- Manifest list: request specific permissions. [docker/cli#1024](https://github.com/docker/cli/pull/1024)
- Setting --orchestrator=all also sets --all-namespaces unless specific --namespace are set. [docker/cli#1059](https://github.com/docker/cli/pull/1059)

- Fix panics when --compress and --stream are used together. [docker/cli#1105](https://github.com/docker/cli/pull/1105)

- Switch from x/net/context to context. [docker/cli#1038](https://github.com/docker/cli/pull/1038)

- Add --init option to `docker service create`. [docker/cli#479](https://github.com/docker/cli/pull/479)
- Fixed bug displaying garbage output for build command when --stream and --quiet flags combined. [docker/cli#1090](https://github.com/docker/cli/pull/1090)
- Add `init` support in 3.7 schema. [docker/cli#1129](https://github.com/docker/cli/pull/1129)

- Fix docker trust signer removal. [docker/cli#1112](https://github.com/docker/cli/pull/1112)
- Fix error message from docker inspect. [docker/cli#1071](https://github.com/docker/cli/pull/1071)

- Allow `x-*` extension on 3rd level objects. [docker/cli#1097](https://github.com/docker/cli/pull/1097)
- An invalid orchestrator now generates an error instead of being silently ignored. [docker/cli#1055](https://github.com/docker/cli/pull/1055)
- Added ORCHESTRATOR column to docker stack ls command. [docker/cli#973](https://github.com/docker/cli/pull/973)
- Warn when using host-ip for published ports for services. [docker/cli#1017](https://github.com/docker/cli/pull/1017)

- Added the option to enable experimental cli features through the `DOCKER_CLI_EXPERIMENTAL` environment variable. [docker/cli#1138](https://github.com/docker/cli/pull/1138)
- Add exec_die to the list of known container events. [docker/cli#1028](https://github.com/docker/cli/pull/1028)

- [K8s] Do env-variable expansion on the uninterpreted Config files. [docker/cli#974](https://github.com/docker/cli/pull/974)

- Print warnings on stderr for each unsupported features while parsing a compose file for deployment on Kubernetes. [docker/cli#903](https://github.com/docker/cli/pull/903)
- Added description about pids count. [docker/cli#1045](https://github.com/docker/cli/pull/1045)

- Warn user of filter when pruning. [docker/cli#1043](https://github.com/docker/cli/pull/1043)
- Fix `--rollback-*` options overwriting `--update-*` options. [docker/cli#1052](https://github.com/docker/cli/pull/1052)

- Update Attach, Build, Commit, Cp, Create subcommand fish completions. [docker/cli#1005](https://github.com/docker/cli/pull/1005)

- Add bash completion for `dockerd --default-address-pool`. [docker/cli#1173](https://github.com/docker/cli/pull/1173)
- Add bash completion for `exec_die` event. [docker/cli#1173](https://github.com/docker/cli/pull/1173)

- Update docker-credential-helper so `pass` is not called on every docker command. [docker/cli#1184](https://github.com/docker/cli/pull/1184)
- Fix for rotating swarm external CA. [docker/cli#1199](https://github.com/docker/cli/pull/1199)
- Improve version output alignment. [docker/cli#1207](https://github.com/docker/cli/pull/1207)

- Add bash completion for `service create|update --init`. [docker/cli#1210](https://github.com/docker/cli/pull/1210)

### Deprecation

- Document reserved namespaces deprecation. [docker/cli#1040](https://github.com/docker/cli/pull/1040)

### Logging

- Allow awslogs to use non-blocking mode. [moby/moby#36522](https://github.com/moby/moby/pull/36522)
- Improve logging of long log lines on fluentd log driver.. [moby/moby#36159](https://github.com/moby/moby/pull/36159)
- Re-order CHANGELOG.md to pass `make validate` test. [moby/moby#37047](https://github.com/moby/moby/pull/37047)
- Update Events, Exec, Export, History, Images, Import, Inspect, Load, and Login subcommand fish completions. [docker/cli#1061](https://github.com/docker/cli/pull/1061)
- Update documentation for RingLogger's ring buffer. [moby/moby#37084](https://github.com/moby/moby/pull/37084)

- Add metrics for log failures/partials. [moby/moby#37034](https://github.com/moby/moby/pull/37034)

- Fix logging plugin crash unrecoverable. [moby/moby#37028](https://github.com/moby/moby/pull/37028)
- Fix logging test type. [moby/moby#37070](https://github.com/moby/moby/pull/37070)
- Fix race conditions in logs API. [moby/moby#37062](https://github.com/moby/moby/pull/37062)
- Fix some issues in logfile reader and rotation. [moby/moby#37063](https://github.com/moby/moby/pull/37063)

### Networking

- Allow user to specify default address pools for docker networks. [moby/moby#36396](https://github.com/moby/moby/pull/36396) [docker/cli#818](https://github.com/docker/cli/pull/818)
- Adding logs for ipam state [docker/libnetwork#2417](https://github.com/docker/libnetwork/pull/2147)
- Fix race conditions in the overlay network driver [docker/libnetwork#2143](https://github.com/docker/libnetwork/pull/2143)
- Add wait time into xtables lock warning [docker/libnetwork#2142](https://github.com/docker/libnetwork/pull/2142)
- filter xtables lock warnings when firewalld is active [docker/libnetwork#2135](https://github.com/docker/libnetwork/pull/2135)
- Switch from x/net/context to context [docker/libnetwork#2140](https://github.com/docker/libnetwork/pull/2140)
- Adding a recovery mechanism for a split gossip cluster [docker/libnetwork#2134](https://github.com/docker/libnetwork/pull/2134)
- Running docker inspect on network attachment tasks now returns a full task object. [moby/moby#35246](https://github.com/moby/moby/pull/35246)
- Some container/network cleanups. [moby/moby#37033](https://github.com/moby/moby/pull/37033)

- Fix network inspect for overlay network. [moby/moby#37045](https://github.com/moby/moby/pull/37045)

- Improve Scalability of the Linux load balancing. [docker/engine#16](https://github.com/docker/engine/pull/16)
- Change log level from error to warning. [docker/engine#19](https://github.com/docker/engine/pull/19)

### Runtime

- Aufs: log why aufs is not supported. [moby/moby#36995](https://github.com/moby/moby/pull/36995)
- Hide experimental checkpoint features on Windows. [docker/cli#1094](https://github.com/docker/cli/pull/1094)
- Lcow: Allow the client to customize capabilities and device cgroup rules for LCOW containers. [moby/moby#37294](https://github.com/moby/moby/pull/37294)
- Changed path given for executable output in windows to actual location of executable output. [moby/moby#37295](https://github.com/moby/moby/pull/37295)

- Add windows recycle bin test and update hcsshim to v0.6.11. [moby/moby#36994](https://github.com/moby/moby/pull/36994)

- Allow to add any args when doing a make run. [moby/moby#37190](https://github.com/moby/moby/pull/37190)
- Optimize ContainerTop() aka docker top. [moby/moby#37131](https://github.com/moby/moby/pull/37131)

- Fix compilation on 32bit machines. [moby/moby#37292](https://github.com/moby/moby/pull/37292)

- Update API version to v1 38. [moby/moby#37141](https://github.com/moby/moby/pull/37141)

- Fix `docker service update --host-add` does not update existing host entry. [docker/cli#1054](https://github.com/docker/cli/pull/1054)
- Fix swagger file type for ExecIds. [moby/moby#36962](https://github.com/moby/moby/pull/36962)
- Fix swagger volume type generation. [moby/moby#37060](https://github.com/moby/moby/pull/37060)
- Fix wrong assertion in volume/service package. [moby/moby#37211](https://github.com/moby/moby/pull/37211)
- Fix daemon panic on restart when a plugin is running. [moby/moby#37234](https://github.com/moby/moby/pull/37234)

- Construct and add 'LABEL' command from 'label' option to last stage. [moby/moby#37011](https://github.com/moby/moby/pull/37011)

- Fix race condition between exec start and resize.. [moby/moby#37172](https://github.com/moby/moby/pull/37172)

- Alternative failure mitigation of `TestExecInteractiveStdinClose`. [moby/moby#37143](https://github.com/moby/moby/pull/37143)
- RawAccess allows a set of paths to be not set as masked or readonly. [moby/moby#36644](https://github.com/moby/moby/pull/36644)
- Be explicit about github.com prefix being a legacy feature. [moby/moby#37174](https://github.com/moby/moby/pull/37174)
- Bump Golang to 1.10.3. [docker/cli#1122](https://github.com/docker/cli/pull/1122)
- Close ReadClosers to prevent xz zombies. [moby/moby#34218](https://github.com/moby/moby/pull/34218)
- Daemon.ContainerStop(): fix for a negative timeout. [moby/moby#36874](https://github.com/moby/moby/pull/36874)
- Daemon.setMounts(): copy slice in place. [moby/moby#36991](https://github.com/moby/moby/pull/36991)
- Describe IP field of swagger Port definition. [moby/moby#36971](https://github.com/moby/moby/pull/36971)
- Extract volume interaction to a volumes service. [moby/moby#36688](https://github.com/moby/moby/pull/36688)
- Fixed markdown formatting in docker image v1, v1.1, and v1.2 spec. [moby/moby#37051](https://github.com/moby/moby/pull/37051)
- Improve GetTimestamp parsing. [moby/moby#35402](https://github.com/moby/moby/pull/35402)
- Jsonmessage: pass message to aux callback. [moby/moby#37064](https://github.com/moby/moby/pull/37064)
- Overlay2: remove unused cdMountFrom() helper function. [moby/moby#37041](https://github.com/moby/moby/pull/37041)

- Overlay: Fix overlay storage-driver silently ignoring unknown storage-driver options. [moby/moby#37040](https://github.com/moby/moby/pull/37040)

- Remove some unused contrib items. [moby/moby#36977](https://github.com/moby/moby/pull/36977)
- Restartmanager: do not apply restart policy on created containers. [moby/moby#36924](https://github.com/moby/moby/pull/36924)
- Set item-type for ExecIDs. [moby/moby#37121](https://github.com/moby/moby/pull/37121)
- Use go-systemd const instead of magic string in Linux version of dockerd. [moby/moby#37136](https://github.com/moby/moby/pull/37136)
- Use stdlib TLS dialer. [moby/moby#36687](https://github.com/moby/moby/pull/36687)
- Warn when an engine label using a reserved namespace (com.docker.*, io.docker.*, or org.dockerproject.*) is configured, as per
  [Docker object labels](https://docs.docker.com/engine/manage-resources/labels/). [moby/moby#36921](https://github.com/moby/moby/pull/36921)

- Fix missing plugin name in message. [moby/moby#37052](https://github.com/moby/moby/pull/37052)
- Fix link anchors in CONTRIBUTING.md. [moby/moby#37276](https://github.com/moby/moby/pull/37276)
- Fix link to Docker Toolbox. [moby/moby#37240](https://github.com/moby/moby/pull/37240)
- Fix mis-used skip condition. [moby/moby#37179](https://github.com/moby/moby/pull/37179)
- Fix bind mounts not working in some cases. [moby/moby#37031](https://github.com/moby/moby/pull/37031)
- Fix fd leak on attach. [moby/moby#37184](https://github.com/moby/moby/pull/37184)
- Fix fluentd partial detection. [moby/moby#37029](https://github.com/moby/moby/pull/37029)
- Fix incorrect link in version-history.md. [moby/moby#37049](https://github.com/moby/moby/pull/37049)

- Allow vim to be case insensitive for D in dockerfile. [moby/moby#37235](https://github.com/moby/moby/pull/37235)

- Add `t.Name()` to tests so that service names are unique. [moby/moby#37166](https://github.com/moby/moby/pull/37166)
- Add additional message when backendfs is extfs without d_type support. [moby/moby#37022](https://github.com/moby/moby/pull/37022)
- Add api version checking for tests from new feature. [moby/moby#37169](https://github.com/moby/moby/pull/37169)
- Add image metrics for push and pull. [moby/moby#37233](https://github.com/moby/moby/pull/37233)
- Add support for `init` on services. [moby/moby#37183](https://github.com/moby/moby/pull/37183)
- Add verification of escapeKeys array length in pkg/term/proxy.go. [moby/moby#36918](https://github.com/moby/moby/pull/36918)

- When link id is empty for overlay2, do not remove this link.. [moby/moby#36161](https://github.com/moby/moby/pull/36161)

- Fix build on OpenBSD by defining Self(). [moby/moby#37301](https://github.com/moby/moby/pull/37301)
- Windows: Fix named pipe support for hyper-v isolated containers. [docker/engine#2](https://github.com/docker/engine/pull/2) [docker/cli#1165](https://github.com/docker/cli/pull/1165)
- Fix manifest lists to always use correct size. [docker/cli#1183](https://github.com/docker/cli/pull/1183)

- Register OCI media types. [docker/engine#4](https://github.com/docker/engine/pull/4)
- Update containerd to v1.1.1 [docker/engine#17](https://github.com/docker/engine/pull/17)
- LCOW: Prefer Windows over Linux in a manifest list. [docker/engine#3](https://github.com/docker/engine/pull/3)
- Add updated `MaskPaths` that are used in code paths directly using containerd to address [CVE-2018-10892](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-10892). [docker/engine#15](https://github.com/docker/engine/pull/15)
- Add `/proc/acpi` to masked paths to address [CVE-2018-10892](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-10892). [docker/engine#14](https://github.com/docker/engine/pull/14)

- Fix bindmount autocreate race. [docker/engine#11](https://github.com/docker/engine/pull/11)

### Swarm Mode

- List stacks for both Swarm and Kubernetes with --orchestrator=all in docker stack ls. Allow several occurrences of --namespace for Kubernetes with docker stack ls. [docker/cli#1031](https://github.com/docker/cli/pull/1031)
- Bump SwarmKit to remove deprecated grpc metadata wrappers. [moby/moby#36905](https://github.com/moby/moby/pull/36905)
- Issue an error for --orchestrator=all when working on mismatched Swarm and Kubernetes hosts. [docker/cli#1035](https://github.com/docker/cli/pull/1035)

- Fix broken swarm commands with Kubernetes defined as orchestrator. "--orchestrator" flag is no longer global but local to stack commands and subcommands [docker/cli#1137](https://github.com/docker/cli/pull/1137) [docker/cli#1139](https://github.com/docker/cli/pull/1139)

- Bump swarmkit to include task reaper fixes and more metrics. [docker/engine#13](https://github.com/docker/engine/pull/13)

- Avoid a leak when a service with unassigned tasks is deleted. [docker/engine#27](https://github.com/docker/engine/pull/27)
- Fix racy batching on the dispatcher. [docker/engine#27](https://github.com/docker/engine/pull/27)

---

# Docker Engine 18.09 release notes

# Docker Engine 18.09 release notes

   Table of contents

---

> **Note:**
>
>
>
> With this release, the daemon, client and container runtime are now all shipped
> in separate packages. When updating, you need to update all packages at the same
> time to get the latest patch releases for each. For example, on Ubuntu:
>
>
>
> ```console
> $ sudo apt-get install docker-ce docker-ce-cli containerd.io
> ```
>
>
>
> See the [installation instructions](https://docs.docker.com/engine/install/) for the corresponding
> Linux distribution for details.

## 18.09.9

2019-09-03

### Client

- Fix Windows absolute path detection on non-Windows. [docker/cli#1990](https://github.com/docker/cli/pull/1990)
- Fix Docker refusing to load key from delegation.key on Windows. [docker/cli#1968](https://github.com/docker/cli/pull/1968)
- Completion scripts updates for bash and zsh.

### Logging

- Fix for reading journald logs. [moby/moby#37819](https://github.com/moby/moby/pull/37819) [moby/moby#38859](https://github.com/moby/moby/pull/38859)

### Networking

- Prevent panic on network attached to a container with disabled networking. [moby/moby#39589](https://github.com/moby/moby/pull/39589)
- Fix service port for an application becomes unavailable randomly. [docker/libnetwork#2069](https://github.com/docker/libnetwork/pull/2069)
- Fix cleaning up `--config-only` networks `--config-from` networkshave ungracefully exited. [docker/libnetwork#2373](https://github.com/docker/libnetwork/pull/2373)

### Runtime

- Update to Go 1.11.13.
- Fix a potential engine panic when using XFS disk quota for containers. [moby/moby#39644](https://github.com/moby/moby/pull/39644)

### Swarm

- Fix "grpc: received message larger than max" errors. [moby/moby#39306](https://github.com/moby/moby/pull/39306)
- Fix an issue where nodes several tasks could not be removed. [docker/swarmkit#2867](https://github.com/docker/swarmkit/pull/2867)

## 18.09.8

2019-07-17

### Runtime

- Masked the secrets updated to the log files when running Docker Engine in debug mode. [CVE-2019-13509](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-13509): If a Docker engine is running in debug mode, and `docker stack deploy` is used to redeploy a stack which includes non-external secrets, the logs will contain the secret.

### Client

- Fixed rollback config type interpolation for `parallelism` and `max_failure_ratio` fields.

### Known Issue

- There are important changes to the upgrade process that, if not correctly followed, can have an impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or later.

## 18.09.7

2019-06-27

### Builder

- Fixed a panic error when building dockerfiles that contain only comments. [moby/moby#38487](https://github.com/moby/moby/pull/38487)
- Added a workaround for GCR authentication issue. [moby/moby#38246](https://github.com/moby/moby/pull/38246)
- Builder-next: Fixed a bug in the GCR token cache implementation workaround. [moby/moby#39183](https://github.com/moby/moby/pull/39183)

### Networking

- Fixed an error where `--network-rm` would fail to remove a network. [moby/moby#39174](https://github.com/moby/moby/pull/39174)

### Runtime

- Added performance optimizations in aufs and layer store that helps in massively parallel container creation and removal. [moby/moby#39107](https://github.com/moby/moby/pull/39107), [moby/moby#39135](https://github.com/moby/moby/pull/39135)
- Updated containerd to version 1.2.6. [moby/moby#39016](https://github.com/moby/moby/pull/39016)
- Fixed [CVE-2018-15664](https://nvd.nist.gov/vuln/detail/CVE-2018-15664) symlink-exchange attack with directory traversal. [moby/moby#39357](https://github.com/moby/moby/pull/39357)
- Windows: fixed support for `docker service create --limit-cpu`. [moby/moby#39190](https://github.com/moby/moby/pull/39190)
- daemon: fixed a mirrors validation issue. [moby/moby#38991](https://github.com/moby/moby/pull/38991)
- Docker no longer supports sorting UID and GID ranges in ID maps. [moby/moby#39288](https://github.com/moby/moby/pull/39288)

### Logging

- Added a fix that now allows large log lines for logger plugins. [moby/moby#39038](https://github.com/moby/moby/pull/39038)

### Known Issue

- There are important changes to the upgrade process that, if not correctly followed, can have an impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or later.

## 18.09.6

2019-05-06

### Builder

- Fixed `COPY` and `ADD` with multiple `<src>` to not invalidate cache if `DOCKER_BUILDKIT=1`.[moby/moby#38964](https://github.com/moby/moby/issues/38964)

### Networking

- Cleaned up the cluster provider when the agent is closed. [docker/libnetwork#2354](https://github.com/docker/libnetwork/pull/2354)
- Windows: Now selects a random host port if the user does not specify a host port. [docker/libnetwork#2369](https://github.com/docker/libnetwork/pull/2369)

### Known Issues

- There are important changes to the upgrade process that, if not correctly followed, can have an impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or later.

## 18.09.5

2019-04-11

### Builder

- Fixed `DOCKER_BUILDKIT=1 docker build --squash ..` [docker/engine#176](https://github.com/docker/engine/pull/176)

### Client

- Fixed tty initial size error. [docker/cli#1775](https://github.com/docker/cli/pull/1775)
- Fixed dial-stdio goroutine leakage. [docker/cli#1795](https://github.com/docker/cli/pull/1795)
- Fixed the stack informer's selector used to track deployment. [docker/cli#1794](https://github.com/docker/cli/pull/1794)

### Networking

- Fixed `network=host` using wrong `resolv.conf` with `systemd-resolved`. [docker/engine#180](https://github.com/docker/engine/pull/180)
- Fixed Windows ARP entries getting corrupted randomly under load. [docker/engine#192](https://github.com/docker/engine/pull/192)

### Runtime

- Now showing stopped containers with restart policy as `Restarting`. [docker/engine#181](https://github.com/docker/engine/pull/181)
- Now using original process spec for execs. [docker/engine#178](https://github.com/docker/engine/pull/178)

### Swarm Mode

- Fixed leaking task resources when nodes are deleted. [docker/engine#185](https://github.com/docker/engine/pull/185)

### Known Issues

- There are important changes to the upgrade process that, if not correctly followed, can have an impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or later.

## 18.09.4

2019-03-28

### Builder

- Fixed [CVE-2019-13139](https://nvd.nist.gov/vuln/detail/CVE-2019-13139) by adding validation for `git ref` to avoid misinterpretation as a flag. [moby/moby#38944](https://github.com/moby/moby/pull/38944)

### Runtime

- Fixed `docker cp` error for filenames greater than 100 characters. [moby/moby#38634](https://github.com/moby/moby/pull/38634)
- Fixed `layer/layer_store` to ensure `NewInputTarStream` resources are released. [moby/moby#38413](https://github.com/moby/moby/pull/38413)
- Increased GRPC limit for `GetConfigs`. [moby/moby#38800](https://github.com/moby/moby/pull/38800)
- Updated `containerd` 1.2.5. [docker/engine#173](https://github.com/docker/engine/pull/173)

### Swarm Mode

- Fixed nil pointer exception when joining node to swarm. [moby/moby#38618](https://github.com/moby/moby/issues/38618)
- Fixed issue for swarm nodes not being able to join as masters if http proxy is set. [moby/moby#36951]

### Known Issues

- There are important changes to the upgrade process that, if not correctly followed, can have impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or later.

## 18.09.3

2019-02-28

### Networking fixes

- Windows: now avoids regeneration of network IDs to prevent broken references to networks. [docker/engine#149](https://github.com/docker/engine/pull/149)
- Windows: Fixed an issue to address `- restart always` flag on standalone containers not working when specifying a network. (docker/escalation#1037)
- Fixed an issue to address the IPAM state from networkdb if the manager is not attached to the overlay network. (docker/escalation#1049)

### Runtime fixes and updates

- Updated to Go version 1.10.8.
- Modified names in the container name generator. [docker/engine#159](https://github.com/docker/engine/pull/159)
- When copying an existing folder, xattr set errors when the target filesystem doesn't support xattr are now ignored. [docker/engine#135](https://github.com/docker/engine/pull/135)
- Graphdriver: fixed "device" mode not being detected if "character-device" bit is set. [docker/engine#160](https://github.com/docker/engine/pull/160)
- Fixed nil pointer dereference on failure to connect to containerd. [docker/engine#162](https://github.com/docker/engine/pull/162)
- Deleted stale containerd object on start failure. [docker/engine#154](https://github.com/docker/engine/pull/154)

### Known Issues

- There are important changes to the upgrade process that, if not correctly followed, can have impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or greater.

## 18.09.2

2019-02-11

### Security fixes

- Update `runc` to address a critical vulnerability that allows specially-crafted containers to gain administrative privileges on the host. [CVE-2019-5736](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-5736)
- Ubuntu 14.04 customers using a 3.13 kernel will need to upgrade to a supported Ubuntu 4.x kernel

For additional information, [refer to the Docker blog post](https://blog.docker.com/2019/02/docker-security-update-cve-2018-5736-and-container-security-best-practices/).

### Known Issues

- There are important changes to the upgrade process that, if not correctly followed, can have impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or greater.

## 18.09.1

2019-01-09

#### Important notes about this release

In Docker versions prior to 18.09, containerd was managed by the Docker engine daemon. In Docker Engine 18.09, containerd is managed by systemd. Since containerd is managed by systemd, any custom configuration to the `docker.service` systemd configuration which changes mount settings (for example, `MountFlags=slave`) breaks interactions between the Docker Engine daemon and containerd, and you will not be able to start containers.

Run the following command to get the current value of the `MountFlags` property for the `docker.service`:

```console
$ sudo systemctl show --property=MountFlags docker.service
MountFlags=
```

Update your configuration if this command prints a non-empty value for `MountFlags`, and restart the docker service.

### Security fixes

- Upgraded Go language to 1.10.6 to resolve [CVE-2018-16873](https://nvd.nist.gov/vuln/detail/CVE-2018-16873), [CVE-2018-16874](https://nvd.nist.gov/vuln/detail/CVE-2018-16874), and [CVE-2018-16875](https://nvd.nist.gov/vuln/detail/CVE-2018-16875).
- Fixed authz plugin for 0-length content and path validation.
- Added `/proc/asound` to masked paths [docker/engine#126](https://github.com/docker/engine/pull/126)

### Improvements

- Updated to BuildKit 0.3.3 [docker/engine#122](https://github.com/docker/engine/pull/122)
- Updated to containerd 1.2.2 [docker/engine#144](https://github.com/docker/engine/pull/144)
- Provided additional warnings for use of deprecated legacy overlay and devicemapper storage drivers [docker/engine#85](https://github.com/docker/engine/pull/85)
- prune: perform image pruning before build cache pruning [docker/cli#1532](https://github.com/docker/cli/pull/1532)
- Added bash completion for experimental CLI commands (manifest) [docker/cli#1542](https://github.com/docker/cli/pull/1542)
- Windows: allow process isolation on Windows 10 [docker/engine#81](https://github.com/docker/engine/pull/81)

### Fixes

- Disable kmem accounting in runc on RHEL/CentOS (docker/escalation#614, docker/escalation#692) [docker/engine#121](https://github.com/docker/engine/pull/121)
- Fixed inefficient networking configuration [docker/engine#123](https://github.com/docker/engine/pull/123)
- Fixed docker system prune doesn't accept until filter [docker/engine#122](https://github.com/docker/engine/pull/122)
- Avoid unset credentials in `containerd` [docker/engine#122](https://github.com/docker/engine/pull/122)
- Fixed iptables compatibility on Debian [docker/engine#107](https://github.com/docker/engine/pull/107)
- Fixed setting default schema to tcp for docker host [docker/cli#1454](https://github.com/docker/cli/pull/1454)
- Fixed bash completion for `service update --force` [docker/cli#1526](https://github.com/docker/cli/pull/1526)
- Windows: DetachVhd attempt in cleanup [docker/engine#113](https://github.com/docker/engine/pull/113)
- API: properly handle invalid JSON to return a 400 status [docker/engine#110](https://github.com/docker/engine/pull/110)
- API: ignore default address-pools on API < 1.39 [docker/engine#118](https://github.com/docker/engine/pull/118)
- API: add missing default address pool fields to swagger [docker/engine#119](https://github.com/docker/engine/pull/119)
- awslogs: account for UTF-8 normalization in limits [docker/engine#112](https://github.com/docker/engine/pull/112)
- Prohibit reading more than 1MB in HTTP error responses [docker/engine#114](https://github.com/docker/engine/pull/114)
- apparmor: allow receiving of signals from `docker kill` [docker/engine#116](https://github.com/docker/engine/pull/116)
- overlay2: use index=off if possible (fix EBUSY on mount) [docker/engine#84](https://github.com/docker/engine/pull/84)

### Packaging

- Add docker.socket requirement for docker.service. [docker/docker-ce-packaging#276](https://github.com/docker/docker-ce-packaging/pull/276)
- Add socket activation for RHEL-based distributions. [docker/docker-ce-packaging#274](https://github.com/docker/docker-ce-packaging/pull/274)
- Add libseccomp requirement for RPM packages. [docker/docker-ce-packaging#266](https://github.com/docker/docker-ce-packaging/pull/266)

### Known Issues

- When upgrading from 18.09.0 to 18.09.1, `containerd` is not upgraded to the correct version on Ubuntu.
- There are important changes to the upgrade process that, if not correctly followed, can have impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or greater.

## 18.09.0

2018-11-08

### Important notes about this release

In Docker versions prior to 18.09, containerd was managed by the Docker engine daemon. In Docker Engine 18.09, containerd is managed by systemd. Since containerd is managed by systemd, any custom configuration to the `docker.service` systemd
configuration which changes mount settings (for example, `MountFlags=slave`) breaks interactions between the Docker Engine daemon and containerd, and you will not be able to start containers.

Run the following command to get the current value of the `MountFlags` property for the `docker.service`:

```console
$ sudo systemctl show --property=MountFlags docker.service
MountFlags=
```

Update your configuration if this command prints a non-empty value for `MountFlags`, and restart the docker service.

### New features

- Updated API version to 1.39 [moby/moby#37640](https://github.com/moby/moby/pull/37640)
- Added support for remote connections using SSH [docker/cli#1014](https://github.com/docker/cli/pull/1014)
- Builder: added prune options to the API [moby/moby#37651](https://github.com/moby/moby/pull/37651)
- Added "Warnings" to `/info` endpoint, and move detection to the daemon [moby/moby#37502](https://github.com/moby/moby/pull/37502)
- Allows BuildKit builds to run without experimental mode enabled. Buildkit can now be configured with an option in daemon.json [moby/moby#37593](https://github.com/moby/moby/pull/37593) [moby/moby#37686](https://github.com/moby/moby/pull/37686) [moby/moby#37692](https://github.com/moby/moby/pull/37692) [docker/cli#1303](https://github.com/docker/cli/pull/1303) [docker/cli#1275](https://github.com/docker/cli/pull/1275)
- Added support for build-time secrets using a `--secret` flag when using BuildKit [docker/cli#1288](https://github.com/docker/cli/pull/1288)
- Added SSH agent socket forwarder (`docker build --ssh $SSHMOUNTID=$SSH_AUTH_SOCK`) when using BuildKit [docker/cli#1438](https://github.com/docker/cli/pull/1438) / [docker/cli#1419](https://github.com/docker/cli/pull/1419)
- Added `--chown` flag support for `ADD` and `COPY` commands on Windows [moby/moby#35521](https://github.com/moby/moby/pull/35521)
- Added `builder prune` subcommand to prune BuildKit build cache [docker/cli#1295](https://github.com/docker/cli/pull/1295) [docker/cli#1334](https://github.com/docker/cli/pull/1334)
- BuildKit: Adds configurable garbage collection policy for the BuildKit build cache [docker/engine#59](https://github.com/docker/engine/pull/59) / [moby/moby#37846](https://github.com/moby/moby/pull/37846)
- BuildKit: Adds support for `docker build --pull ...` when using BuildKit [moby/moby#37613](https://github.com/moby/moby/pull/37613)
- BuildKit: Adds support or "registry-mirrors" and "insecure-registries" when using BuildKit [docker/engine#59](https://github.com/docker/engine/pull/59) / [moby/moby#37852](https://github.com/moby/moby/pull/37852)
- BuildKit: Enables net modes and bridge. [moby/moby#37620](https://github.com/moby/moby/pull/37620)
- Added `docker engine` subcommand to manage the lifecycle of a Docker Engine running as a privileged container on top of containerd, and to allow upgrades to Docker Engine Enterprise [docker/cli#1260](https://github.com/docker/cli/pull/1260)
- Exposed product license in `docker info` output [docker/cli#1313](https://github.com/docker/cli/pull/1313)
- Showed warnings produced by daemon in `docker info` output [docker/cli#1225](https://github.com/docker/cli/pull/1225)
- Added "local" log driver [moby/moby#37092](https://github.com/moby/moby/pull/37092)
- Amazon CloudWatch: adds `awslogs-endpoint` logging option [moby/moby#37374](https://github.com/moby/moby/pull/37374)
- Added support for global default address pools [moby/moby#37558](https://github.com/moby/moby/pull/37558) [docker/cli#1233](https://github.com/docker/cli/pull/1233)
- Configured containerd log-level to be the same as dockerd [moby/moby#37419](https://github.com/moby/moby/pull/37419)
- Added configuration option for cri-containerd [moby/moby#37519](https://github.com/moby/moby/pull/37519)
- Updates containerd client to v1.2.0-rc.1 [moby/moby#37664](https://github.com/moby/moby/pull/37664), [docker/engine#75](https://github.com/docker/engine/pull/75) / [moby/moby#37710](https://github.com/moby/moby/pull/37710)
- Added support for global default address pools [moby/moby#37558](https://github.com/moby/moby/pull/37558) [docker/cli#1233](https://github.com/docker/cli/pull/1233)
- Moved the `POST /session` endpoint out of experimental. [moby/moby#40028](https://github.com/moby/moby/pull/40028)

### Improvements

- Does not return "`<unknown>`" in /info response [moby/moby#37472](https://github.com/moby/moby/pull/37472)
- BuildKit: Changes `--console=[auto,false,true]` to `--progress=[auto,plain,tty]` [docker/cli#1276](https://github.com/docker/cli/pull/1276)
- BuildKit: Sets BuildKit's ExportedProduct variable to show useful errors in the future. [moby/moby#37439](https://github.com/moby/moby/pull/37439)
- Hides `--data-path-addr` flags when connected to a daemon that doesn't support this option [docker/docker/cli#1240](https://github.com/docker/cli/pull/1240)
- Only shows buildkit-specific flags if BuildKit is enabled [docker/cli#1438](https://github.com/docker/cli/pull/1438) / [docker/cli#1427](https://github.com/docker/cli/pull/1427)
- Improves version output alignment [docker/cli#1204](https://github.com/docker/cli/pull/1204)
- Sorts plugin names and networks in a natural order [docker/cli#1166](https://github.com/docker/cli/pull/1166), [docker/cli#1266](https://github.com/docker/cli/pull/1266)
- Updates bash and zsh [completion scripts](https://github.com/docker/cli/issues?q=label%3Aarea%2Fcompletion+milestone%3A18.09.0+is%3Aclosed)
- Passes log-level to containerd. [moby/moby#37419](https://github.com/moby/moby/pull/37419)
- Uses direct server return (DSR) in east-west overlay load balancing [docker/engine#93](https://github.com/docker/engine/pull/93) / [docker/libnetwork#2270](https://github.com/docker/libnetwork/pull/2270)
- Builder: temporarily disables bridge networking when using buildkit. [moby/moby#37691](https://github.com/moby/moby/pull/37691)
- Blocks task starting until node attachments are ready [moby/moby#37604](https://github.com/moby/moby/pull/37604)
- Propagates the provided external CA certificate to the external CA object in swarm. [docker/cli#1178](https://github.com/docker/cli/pull/1178)
- Removes Ubuntu 14.04 "Trusty Tahr" as a supported platform [docker-ce-packaging#255](https://github.com/docker/docker-ce-packaging/pull/255) / [docker-ce-packaging#254](https://github.com/docker/docker-ce-packaging/pull/254)
- Removes Debian 8 "Jessie" as a supported platform [docker-ce-packaging#255](https://github.com/docker/docker-ce-packaging/pull/255) / [docker-ce-packaging#254](https://github.com/docker/docker-ce-packaging/pull/254)
- Removes 'docker-' prefix for containerd and runc binaries [docker/engine#61](https://github.com/docker/engine/pull/61) / [moby/moby#37907](https://github.com/moby/moby/pull/37907), [docker-ce-packaging#241](https://github.com/docker/docker-ce-packaging/pull/241)
- Splits "engine", "cli", and "containerd" to separate packages, and run containerd as a separate systemd service [docker-ce-packaging#131](https://github.com/docker/docker-ce-packaging/pull/131), [docker-ce-packaging#158](https://github.com/docker/docker-ce-packaging/pull/158)
- Builds binaries with Go 1.10.4 [docker-ce-packaging#181](https://github.com/docker/docker-ce-packaging/pull/181)
- Removes `-ce` suffix from version string [docker-ce-packaging#206](https://github.com/docker/docker-ce-packaging/pull/206)

### Fixes

- BuildKit: Do not cancel buildkit status request. [moby/moby#37597](https://github.com/moby/moby/pull/37597)
- Fixes no error is shown if build args are missing during docker build [moby/moby#37396](https://github.com/moby/moby/pull/37396)
- Fixes error "unexpected EOF" when adding an 8GB file [moby/moby#37771](https://github.com/moby/moby/pull/37771)
- LCOW: Ensures platform is populated on `COPY`/`ADD`. [moby/moby#37563](https://github.com/moby/moby/pull/37563)
- Fixes mapping a range of host ports to a single container port [docker/cli#1102](https://github.com/docker/cli/pull/1102)
- Fixes `trust inspect` typo: "`AdminstrativeKeys`" [docker/cli#1300](https://github.com/docker/cli/pull/1300)
- Fixes environment file parsing for imports of absent variables and those with no name. [docker/cli#1019](https://github.com/docker/cli/pull/1019)
- Fixes a potential "out of memory exception" when running `docker image prune` with a large list of dangling images [docker/cli#1432](https://github.com/docker/cli/pull/1432) / [docker/cli#1423](https://github.com/docker/cli/pull/1423)
- Fixes pipe handling in ConEmu and ConsoleZ on Windows [moby/moby#37600](https://github.com/moby/moby/pull/37600)
- Fixes long startup on windows, with non-hns governed Hyper-V networks [docker/engine#67](https://github.com/docker/engine/pull/67) / [moby/moby#37774](https://github.com/moby/moby/pull/37774)
- Fixes daemon won't start when "runtimes" option is defined both in config file and cli [docker/engine#57](https://github.com/docker/engine/pull/57) / [moby/moby#37871](https://github.com/moby/moby/pull/37871)
- Loosens permissions on `/etc/docker` directory to prevent "permission denied" errors when using `docker manifest inspect` [docker/engine#56](https://github.com/docker/engine/pull/56) / [moby/moby#37847](https://github.com/moby/moby/pull/37847)
- Fixes denial of service with large numbers in `cpuset-cpus` and `cpuset-mems` [docker/engine#70](https://github.com/docker/engine/pull/70) / [moby/moby#37967](https://github.com/moby/moby/pull/37967)
- LCOW: Add `--platform` to `docker import` [docker/cli#1375](https://github.com/docker/cli/pull/1375) / [docker/cli#1371](https://github.com/docker/cli/pull/1371)
- LCOW: Add LinuxMetadata support by default on Windows [moby/moby#37514](https://github.com/moby/moby/pull/37514)
- LCOW: Mount to short container paths to avoid command-line length limit [moby/moby#37659](https://github.com/moby/moby/pull/37659)
- LCOW: Fix builder using wrong cache layer [moby/moby#37356](https://github.com/moby/moby/pull/37356)
- Fixes json-log file descriptors leaking when using `--follow` [docker/engine#48](https://github.com/docker/engine/pull/48) [moby/moby#37576](https://github.com/moby/moby/pull/37576) [moby/moby#37734](https://github.com/moby/moby/pull/37734)
- Fixes a possible deadlock on closing the watcher on kqueue [moby/moby#37392](https://github.com/moby/moby/pull/37392)
- Uses poller based watcher to work around the file caching issue in Windows [moby/moby#37412](https://github.com/moby/moby/pull/37412)
- Handles systemd-resolved case by providing appropriate resolv.conf to networking layer [moby/moby#37485](https://github.com/moby/moby/pull/37485)
- Removes support for TLS < 1.2 [moby/moby#37660](https://github.com/moby/moby/pull/37660)
- Seccomp: Whitelist syscalls linked to `CAP_SYS_NICE` in default seccomp profile [moby/moby#37242](https://github.com/moby/moby/pull/37242)
- Seccomp: move the syslog syscall to be gated by `CAP_SYS_ADMIN` or `CAP_SYSLOG` [docker/engine#64](https://github.com/docker/engine/pull/64) / [moby/moby#37929](https://github.com/moby/moby/pull/37929)
- SELinux: Fix relabeling of local volumes specified via Mounts API on selinux-enabled systems [moby/moby#37739](https://github.com/moby/moby/pull/37739)
- Adds warning if REST API is accessible through an insecure connection [moby/moby#37684](https://github.com/moby/moby/pull/37684)
- Masks proxy credentials from URL when displayed in system info [docker/engine#72](https://github.com/docker/engine/pull/72) / [moby/moby#37934](https://github.com/moby/moby/pull/37934)
- Fixes mount propagation for btrfs [docker/engine#86](https://github.com/docker/engine/pull/86) / [moby/moby#38026](https://github.com/moby/moby/pull/38026)
- Fixes nil pointer dereference in node allocation [docker/engine#94](https://github.com/docker/engine/pull/94) / [docker/swarmkit#2764](https://github.com/docker/swarmkit/pull/2764)

### Known Issues

- There are important changes to the upgrade process that, if not correctly followed, can have impact on the availability of applications running on the Swarm during upgrades. These constraints impact any upgrades coming from any version before 18.09 to version 18.09 or greater.
- With [https://github.com/boot2docker/boot2docker/releases/download/v18.09.0/boot2docker.iso](https://github.com/boot2docker/boot2docker/releases/download/v18.09.0/boot2docker.iso), connection is being refused from a node on the virtual machine. Any publishing of swarm ports in virtualbox-created docker-machine VM's will not respond. This is occurring on macOS and Windows 10, using docker-machine version 0.15 and 0.16.
  The following `docker run` command works, allowing access from host browser:
  `docker run -d -p 4000:80 nginx`
  However, the following `docker service` command fails, resulting in curl/chrome unable to connect (connection refused):
  `docker service create -p 5000:80 nginx`
  This issue is not apparent when provisioning 18.09.0 cloud VM's using docker-machine.
  Workarounds:
  - Use cloud VM's that don't rely on boot2docker.
  - `docker run` is unaffected.
  - For Swarm, set VIRTUALBOX_BOOT2DOCKER_URL=https://github.com/boot2docker/boot2docker/releases/download/v18.06.1-ce/boot2docker.iso.
  This issue is resolved in 18.09.1.

### Deprecation Notices

- Docker has deprecated support for Device Mapper as a storage driver. It will continue to be
  supported at this time, but support will be removed in a future release.
  The
  [Overlay2 storage driver](https://docs.docker.com/engine/storage/drivers/overlayfs-driver/) is now the default for Docker Engine implementations.

For more information on the list of deprecated flags and APIs, have a look at the
[deprecation information](https://docs.docker.com/engine/deprecated/) where you can find the target removal dates.

### End of Life Notification

In this release, Docker has also removed support for TLS < 1.2 [moby/moby#37660](https://github.com/moby/moby/pull/37660),
Ubuntu 14.04 "Trusty Tahr" [docker-ce-packaging#255](https://github.com/docker/docker-ce-packaging/pull/255) / [docker-ce-packaging#254](https://github.com/docker/docker-ce-packaging/pull/254), and Debian 8 "Jessie" [docker-ce-packaging#255](https://github.com/docker/docker-ce-packaging/pull/255) / [docker-ce-packaging#254](https://github.com/docker/docker-ce-packaging/pull/254).
