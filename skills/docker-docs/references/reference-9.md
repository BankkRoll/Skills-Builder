# Docker Engine API(1.51)

# Docker Engine API(1.51)

> Reference documentation and Swagger (OpenAPI) specification for the Docker Engine API.

![logo](https://docs.docker.com/assets/images/logo-docker-main.png)

- Errors
- Versioning
- Authentication
- Containers
  - getList containers
  - postCreate a container
  - getInspect a container
  - getList processes running inside a container
  - getGet container logs
  - getGet changes on a container’s filesystem
  - getExport a container
  - getGet container stats based on resource usage
  - postResize a container TTY
  - postStart a container
  - postStop a container
  - postRestart a container
  - postKill a container
  - postUpdate a container
  - postRename a container
  - postPause a container
  - postUnpause a container
  - postAttach to a container
  - getAttach to a container via a websocket
  - postWait for a container
  - delRemove a container
  - headGet information about files in a container
  - getGet an archive of a filesystem resource in a container
  - putExtract an archive of files or folders to a directory in a container
  - postDelete stopped containers
- Images
  - getList Images
  - postBuild an image
  - postDelete builder cache
  - postCreate an image
  - getInspect an image
  - getGet the history of an image
  - postPush an image
  - postTag an image
  - delRemove an image
  - getSearch images
  - postDelete unused images
  - postCreate a new image from a container
  - getExport an image
  - getExport several images
  - postImport images
- Networks
  - getList networks
  - getInspect a network
  - delRemove a network
  - postCreate a network
  - postConnect a container to a network
  - postDisconnect a container from a network
  - postDelete unused networks
- Volumes
  - getList volumes
  - postCreate a volume
  - getInspect a volume
  - put"Update a volume. Valid only for Swarm cluster volumes"
  - delRemove a volume
  - postDelete unused volumes
- Exec
  - postCreate an exec instance
  - postStart an exec instance
  - postResize an exec instance
  - getInspect an exec instance
- Swarm
  - getInspect swarm
  - postInitialize a new swarm
  - postJoin an existing swarm
  - postLeave a swarm
  - postUpdate a swarm
  - getGet the unlock key
  - postUnlock a locked manager
- Nodes
  - getList nodes
  - getInspect a node
  - delDelete a node
  - postUpdate a node
- Services
  - getList services
  - postCreate a service
  - getInspect a service
  - delDelete a service
  - postUpdate a service
  - getGet service logs
- Tasks
  - getList tasks
  - getInspect a task
  - getGet task logs
- Secrets
  - getList secrets
  - postCreate a secret
  - getInspect a secret
  - delDelete a secret
  - postUpdate a Secret
- Configs
  - getList configs
  - postCreate a config
  - getInspect a config
  - delDelete a config
  - postUpdate a Config
- Plugins
  - getList plugins
  - getGet plugin privileges
  - postInstall a plugin
  - getInspect a plugin
  - delRemove a plugin
  - postEnable a plugin
  - postDisable a plugin
  - postUpgrade a plugin
  - postCreate a plugin
  - postPush a plugin
  - postConfigure a plugin
- System
  - postCheck auth configuration
  - getGet system information
  - getGet version
  - getPing
  - headPing
  - getMonitor events
  - getGet data usage information
- Distribution
  - getGet image information from the registry
- Session
  - postInitialize interactive session

[API docs by Redocly](https://redocly.com/redoc/)

# Docker Engine API(1.51)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.51.yaml)

The Engine API is an HTTP API served by Docker Engine. It is the API the
Docker client uses to communicate with the Engine, so everything the Docker
client can do can be done with the API.

Most of the client's commands map directly to API endpoints (e.g. `docker ps`
is `GET /containers/json`). The notable exception is running containers,
which consists of several API calls.

## Errors

The API uses standard HTTP status codes to indicate the success or failure
of the API call. The body of the response will be JSON in the following
format:

```
{
  "message": "page not found"
}
```

## Versioning

The API is usually changed in each release, so API calls are versioned to
ensure that clients don't break. To lock to a specific version of the API,
you prefix the URL with its version, for example, call `/v1.30/info` to use
the v1.30 version of the `/info` endpoint. If the API version specified in
the URL is not supported by the daemon, a HTTP `400 Bad Request` error message
is returned.

If you omit the version-prefix, the current version of the API (v1.50) is used.
For example, calling `/info` is the same as calling `/v1.51/info`. Using the
API without a version-prefix is deprecated and will be removed in a future release.

Engine releases in the near future should support this version of the API,
so your client will continue to work even if it is talking to a newer Engine.

The API uses an open schema model, which means the server may add extra properties
to responses. Likewise, the server will ignore any extra query parameters and
request body properties. When you write clients, you need to ignore additional
properties in responses to ensure they do not break when talking to newer
daemons.

## Authentication

Authentication for registries is handled client side. The client has to send
authentication details to various endpoints that need to communicate with
registries, such as `POST /images/(name)/push`. These are sent as
`X-Registry-Auth` header as a [base64url encoded](https://tools.ietf.org/html/rfc4648#section-5)
(JSON) string with the following structure:

```
{
  "username": "string",
  "password": "string",
  "serveraddress": "string"
}
```

The `serveraddress` is a domain/IP without a protocol. Throughout this
structure, double quotes are required.

If you have already got an identity token from the [/authendpoint](#operation/SystemAuth),
you can just pass this instead of credentials:

```
{
  "identitytoken": "9cbaf023786cd7..."
}
```

## Containers

Create and manage containers.

## List containers

Returns a list of containers. For details on the format, see the
[inspect endpoint](#operation/ContainerInspect).

Note that it uses a different, smaller representation of a container
than inspecting a single container. For example, the list of linked
containers is not propagated .

##### query Parameters

| all | booleanDefault:falseReturn all containers. By default, only running containers are shown. |
| --- | --- |
| limit | integerReturn this number of most recently created containers, including
non-running ones. |
| size | booleanDefault:falseReturn the size of container as fieldsSizeRwandSizeRootFs. |
| filters | stringFilters to process on the container list, encoded as JSON (amap[string][]string). For example,{"status": ["paused"]}will
only return paused containers.Available filters:ancestor=(<image-name>[:<tag>],<image id>, or<image@digest>)before=(<container id>or<container name>)expose=(<port>[/<proto>]|<startport-endport>/[<proto>])exited=<int>containers with exit code of<int>health=(starting|healthy|unhealthy|none)id=<ID>a container's IDisolation=(default|process|hyperv) (Windows daemon only)is-task=(true|false)label=keyorlabel="key=value"of a container labelname=<name>a container's namenetwork=(<network id>or<network name>)publish=(<port>[/<proto>]|<startport-endport>/[<proto>])since=(<container id>or<container name>)status=(created|restarting|running|removing|paused|exited|dead)volume=(<volume name>or<mount point destination>) |

### Responses

### Response samples

- 200
- 400
- 500

Content typeapplication/json`[{"Id": "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf","Names": ["/funny_chatelet"],"Image": "docker.io/library/ubuntu:latest","ImageID": "sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782","ImageManifestDescriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null},"Command": "/bin/bash","Created": "1739811096","Ports": [{"PrivatePort": 8080,"PublicPort": 80,"Type": "tcp"}],"SizeRw": "122880","SizeRootFs": "1653948416","Labels": {"com.example.vendor": "Acme","com.example.license": "GPL","com.example.version": "1.0"},"State": "running","Status": "Up 4 days","HostConfig": {"NetworkMode": "mynetwork","Annotations": {"io.kubernetes.docker.type": "container","io.kubernetes.sandbox.id": "3befe639bed0fd6afdd65fd1fa84506756f59360ec4adc270b0fdac9be22b4d3"}},"NetworkSettings": {"Networks": {"property1": {"IPAMConfig": {"IPv4Address": "172.20.30.33","IPv6Address": "2001:db8:abcd::3033","LinkLocalIPs": ["169.254.34.68","fe80::3468"]},"Links": ["container_1","container_2"],"MacAddress": "02:42:ac:11:00:04","Aliases": ["server_x","server_y"],"DriverOpts": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"GwPriority": [10],"NetworkID": "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a","EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b","Gateway": "172.17.0.1","IPAddress": "172.17.0.4","IPPrefixLen": 16,"IPv6Gateway": "2001:db8:2::100","GlobalIPv6Address": "2001:db8::5689","GlobalIPv6PrefixLen": 64,"DNSNames": ["foobar","server_x","server_y","my.ctr"]},"property2": {"IPAMConfig": {"IPv4Address": "172.20.30.33","IPv6Address": "2001:db8:abcd::3033","LinkLocalIPs": ["169.254.34.68","fe80::3468"]},"Links": ["container_1","container_2"],"MacAddress": "02:42:ac:11:00:04","Aliases": ["server_x","server_y"],"DriverOpts": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"GwPriority": [10],"NetworkID": "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a","EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b","Gateway": "172.17.0.1","IPAddress": "172.17.0.4","IPPrefixLen": 16,"IPv6Gateway": "2001:db8:2::100","GlobalIPv6Address": "2001:db8::5689","GlobalIPv6PrefixLen": 64,"DNSNames": ["foobar","server_x","server_y","my.ctr"]}}},"Mounts": [{"Type": "volume","Name": "myvolume","Source": "/var/lib/docker/volumes/myvolume/_data","Destination": "/usr/share/nginx/html/","Driver": "local","Mode": "z","RW": true,"Propagation": ""}]}]`

## Create a container

##### query Parameters

| name | string^/?[a-zA-Z0-9][a-zA-Z0-9_.-]+$Assign the specified name to the container. Must match/?[a-zA-Z0-9][a-zA-Z0-9_.-]+. |
| --- | --- |
| platform | stringDefault:""Platform in the formatos[/arch[/variant]]used for image lookup.When specified, the daemon checks if the requested image is present
in the local image cache with the given OS and Architecture, and
otherwise returns a404status.If the option is not set, the host's native OS and Architecture are
used to look up the image in the image cache. However, if no platform
is passed and the given image does exist in the local image cache,
but its OS or architecture does not match, the container is created
with the available image, and a warning is added to theWarningsfield in the response, for example;WARNING:The requested image's platform(linux/arm64/v8)does not
         match the detected host platform(linux/amd64)and no
         specific platform was requested |

##### Request Body schema:application/jsonapplication/octet-streamapplication/jsonrequired

Container to create

| Hostname | stringThe hostname to use for the container, as a valid RFC 1123 hostname. |
| --- | --- |
| Domainname | stringThe domain name to use for the container. |
| User | stringCommands run as this user inside the container. If omitted, commands
run as the user specified in the image the container was started from.Can be either user-name or UID, and optional group-name or GID,
separated by a colon (<user-name|UID>[<:group-name|GID>]). |
| AttachStdin | booleanDefault:falseWhether to attach tostdin. |
| AttachStdout | booleanDefault:trueWhether to attach tostdout. |
| AttachStderr | booleanDefault:trueWhether to attach tostderr. |
|  | object or nullAn object mapping ports to an empty object in the form:{"<port>/<tcp|udp|sctp>": {}} |
| Tty | booleanDefault:falseAttach standard streams to a TTY, includingstdinif it is not closed. |
| OpenStdin | booleanDefault:falseOpenstdin |
| StdinOnce | booleanDefault:falseClosestdinafter one attached client disconnects |
| Env | Array ofstringsA list of environment variables to set inside the container in the
form["VAR=value", ...]. A variable without=is removed from the
environment, rather than to have an empty value. |
| Cmd | Array ofstringsCommand to run specified as a string or an array of strings. |
|  | object(HealthConfig)A test to perform to check that the container is healthy.
Healthcheck commands should be side-effect free. |
| ArgsEscaped | boolean or nullDefault:falseCommand is already escaped (Windows only) |
| Image | stringThe name (or reference) of the image to use when creating the container,
or which was used when the container was created. |
|  | objectAn object mapping mount point paths inside the container to empty
objects. |
| WorkingDir | stringThe working directory for commands to run in. |
| Entrypoint | Array ofstringsThe entry point for the container as a string or an array of strings.If the array consists of exactly one empty string ([""]) then the
entry point is reset to system default (i.e., the entry point used by
docker when there is noENTRYPOINTinstruction in theDockerfile). |
| NetworkDisabled | boolean or nullDisable networking for the container. |
| MacAddress | string or nullMAC address of the container.Deprecated: this field is deprecated in API v1.44 and up. Use EndpointSettings.MacAddress instead. |
| OnBuild | Array ofstrings or nullONBUILDmetadata that were defined in the image'sDockerfile. |
|  | objectUser-defined key/value metadata. |
| StopSignal | string or nullSignal to stop a container as a string or unsigned integer. |
| StopTimeout | integer or nullDefault:10Timeout to stop a container in seconds. |
| Shell | Array ofstrings or nullShell for whenRUN,CMD, andENTRYPOINTuses a shell. |
|  | object(HostConfig)Container configuration that depends on the host we are running on |
|  | object(NetworkingConfig)NetworkingConfig represents the container's networking configuration for
each of its interfaces.
It is used for the networking configs specified in thedocker createanddocker network connectcommands. |

### Responses

### Request samples

- Payload

Content typeapplication/jsonapplication/octet-streamapplication/json`{"Hostname": "","Domainname": "","User": "","AttachStdin": false,"AttachStdout": true,"AttachStderr": true,"Tty": false,"OpenStdin": false,"StdinOnce": false,"Env": ["FOO=bar","BAZ=quux"],"Cmd": ["date"],"Entrypoint": "","Image": "ubuntu","Labels": {"com.example.vendor": "Acme","com.example.license": "GPL","com.example.version": "1.0"},"Volumes": {"/volumes/data": { }},"WorkingDir": "","NetworkDisabled": false,"MacAddress": "12:34:56:78:9a:bc","ExposedPorts": {"22/tcp": { }},"StopSignal": "SIGTERM","StopTimeout": 10,"HostConfig": {"Binds": ["/tmp:/tmp"],"Links": ["redis3:redis"],"Memory": 0,"MemorySwap": 0,"MemoryReservation": 0,"NanoCpus": 500000,"CpuPercent": 80,"CpuShares": 512,"CpuPeriod": 100000,"CpuRealtimePeriod": 1000000,"CpuRealtimeRuntime": 10000,"CpuQuota": 50000,"CpusetCpus": "0,1","CpusetMems": "0,1","MaximumIOps": 0,"MaximumIOBps": 0,"BlkioWeight": 300,"BlkioWeightDevice": [{ }],"BlkioDeviceReadBps": [{ }],"BlkioDeviceReadIOps": [{ }],"BlkioDeviceWriteBps": [{ }],"BlkioDeviceWriteIOps": [{ }],"DeviceRequests": [{"Driver": "nvidia","Count": -1,"DeviceIDs"": ["0","1","GPU-fef8089b-4820-abfc-e83e-94318197576e"],"Capabilities": [["gpu","nvidia","compute"]],"Options": {"property1": "string","property2": "string"}}],"MemorySwappiness": 60,"OomKillDisable": false,"OomScoreAdj": 500,"PidMode": "","PidsLimit": 0,"PortBindings": {"22/tcp": [{"HostPort": "11022"}]},"PublishAllPorts": false,"Privileged": false,"ReadonlyRootfs": false,"Dns": ["8.8.8.8"],"DnsOptions": [""],"DnsSearch": [""],"VolumesFrom": ["parent","other:ro"],"CapAdd": ["NET_ADMIN"],"CapDrop": ["MKNOD"],"GroupAdd": ["newgroup"],"RestartPolicy": {"Name": "","MaximumRetryCount": 0},"AutoRemove": true,"NetworkMode": "bridge","Devices": [ ],"Ulimits": [{ }],"LogConfig": {"Type": "json-file","Config": { }},"SecurityOpt": [ ],"StorageOpt": { },"CgroupParent": "","VolumeDriver": "","ShmSize": 67108864},"NetworkingConfig": {"EndpointsConfig": {"isolated_nw": {"IPAMConfig": {"IPv4Address": "172.20.30.33","IPv6Address": "2001:db8:abcd::3033","LinkLocalIPs": ["169.254.34.68","fe80::3468"]},"Links": ["container_1","container_2"],"Aliases": ["server_x","server_y"]},"database_nw": { }}}}`

### Response samples

- 201
- 400
- 404
- 409
- 500

Content typeapplication/json`{"Id": "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743","Warnings": [ ]}`

## Inspect a container

Return low-level information about a container.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| size | booleanDefault:falseReturn the size of container as fieldsSizeRwandSizeRootFs |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"Id": "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf","Created": "2025-02-17T17:43:39.64001363Z","Path": "/bin/sh","Args": ["-c","exit 9"],"State": {"Status": "running","Running": true,"Paused": false,"Restarting": false,"OOMKilled": false,"Dead": false,"Pid": 1234,"ExitCode": 0,"Error": "string","StartedAt": "2020-01-06T09:06:59.461876391Z","FinishedAt": "2020-01-06T09:07:59.461876391Z","Health": {"Status": "healthy","FailingStreak": 0,"Log": [{"Start": "2020-01-04T10:44:24.496525531Z","End": "2020-01-04T10:45:21.364524523Z","ExitCode": 0,"Output": "string"}]}},"Image": "sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782","ResolvConfPath": "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/resolv.conf","HostnamePath": "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/hostname","HostsPath": "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/hosts","LogPath": "/var/lib/docker/containers/5b7c7e2b992aa426584ce6c47452756066be0e503a08b4516a433a54d2f69e59/5b7c7e2b992aa426584ce6c47452756066be0e503a08b4516a433a54d2f69e59-json.log","Name": "/funny_chatelet","RestartCount": 0,"Driver": "overlayfs","Platform": "linux","ImageManifestDescriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null},"MountLabel": "","ProcessLabel": "","AppArmorProfile": "","ExecIDs": ["b35395de42bc8abd327f9dd65d913b9ba28c74d2f0734eeeae84fa1c616a0fca","3fc1232e5cd20c8de182ed81178503dc6437f4e7ef12b52cc5e8de020652f1c4"],"HostConfig": {"CpuShares": 0,"Memory": 0,"CgroupParent": "string","BlkioWeight": 1000,"BlkioWeightDevice": [{"Path": "string","Weight": 0}],"BlkioDeviceReadBps": [{"Path": "string","Rate": 0}],"BlkioDeviceWriteBps": [{"Path": "string","Rate": 0}],"BlkioDeviceReadIOps": [{"Path": "string","Rate": 0}],"BlkioDeviceWriteIOps": [{"Path": "string","Rate": 0}],"CpuPeriod": 0,"CpuQuota": 0,"CpuRealtimePeriod": 0,"CpuRealtimeRuntime": 0,"CpusetCpus": "0-3","CpusetMems": "string","Devices": [{"PathOnHost": "/dev/deviceName","PathInContainer": "/dev/deviceName","CgroupPermissions": "mrw"}],"DeviceCgroupRules": ["c 13:* rwm"],"DeviceRequests": [{"Driver": "nvidia","Count": -1,"DeviceIDs": ["0","1","GPU-fef8089b-4820-abfc-e83e-94318197576e"],"Capabilities": [["gpu","nvidia","compute"]],"Options": {"property1": "string","property2": "string"}}],"KernelMemoryTCP": 0,"MemoryReservation": 0,"MemorySwap": 0,"MemorySwappiness": 100,"NanoCpus": 0,"OomKillDisable": true,"Init": true,"PidsLimit": 0,"Ulimits": [{"Name": "string","Soft": 0,"Hard": 0}],"CpuCount": 0,"CpuPercent": 0,"IOMaximumIOps": 0,"IOMaximumBandwidth": 0,"Binds": ["string"],"ContainerIDFile": "","LogConfig": {"Type": "local","Config": {"max-file": "5","max-size": "10m"}},"NetworkMode": "string","PortBindings": {"443/tcp": [{"HostIp": "127.0.0.1","HostPort": "4443"}],"80/tcp": [{"HostIp": "0.0.0.0","HostPort": "80"},{"HostIp": "0.0.0.0","HostPort": "8080"}],"80/udp": [{"HostIp": "0.0.0.0","HostPort": "80"}],"53/udp": [{"HostIp": "0.0.0.0","HostPort": "53"}],"2377/tcp": null},"RestartPolicy": {"Name": "","MaximumRetryCount": 0},"AutoRemove": true,"VolumeDriver": "string","VolumesFrom": ["string"],"Mounts": [{"Target": "string","Source": "string","Type": "volume","ReadOnly": true,"Consistency": "string","BindOptions": {"Propagation": "private","NonRecursive": false,"CreateMountpoint": false,"ReadOnlyNonRecursive": false,"ReadOnlyForceRecursive": false},"VolumeOptions": {"NoCopy": false,"Labels": {"property1": "string","property2": "string"},"DriverConfig": {"Name": "string","Options": {"property1": "string","property2": "string"}},"Subpath": "dir-inside-volume/subdirectory"},"ImageOptions": {"Subpath": "dir-inside-image/subdirectory"},"TmpfsOptions": {"SizeBytes": 0,"Mode": 0,"Options": [["noexec"]]}}],"ConsoleSize": [80,64],"Annotations": {"property1": "string","property2": "string"},"CapAdd": ["string"],"CapDrop": ["string"],"CgroupnsMode": "private","Dns": ["string"],"DnsOptions": ["string"],"DnsSearch": ["string"],"ExtraHosts": ["string"],"GroupAdd": ["string"],"IpcMode": "string","Cgroup": "string","Links": ["string"],"OomScoreAdj": 500,"PidMode": "string","Privileged": true,"PublishAllPorts": true,"ReadonlyRootfs": true,"SecurityOpt": ["string"],"StorageOpt": {"property1": "string","property2": "string"},"Tmpfs": {"property1": "string","property2": "string"},"UTSMode": "string","UsernsMode": "string","ShmSize": 0,"Sysctls": {"net.ipv4.ip_forward": "1"},"Runtime": "string","Isolation": "default","MaskedPaths": ["/proc/asound","/proc/acpi","/proc/kcore","/proc/keys","/proc/latency_stats","/proc/timer_list","/proc/timer_stats","/proc/sched_debug","/proc/scsi","/sys/firmware","/sys/devices/virtual/powercap"],"ReadonlyPaths": ["/proc/bus","/proc/fs","/proc/irq","/proc/sys","/proc/sysrq-trigger"]},"GraphDriver": {"Name": "overlay2","Data": {"MergedDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/merged","UpperDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/diff","WorkDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/work"}},"SizeRw": "122880","SizeRootFs": "1653948416","Mounts": [{"Type": "volume","Name": "myvolume","Source": "/var/lib/docker/volumes/myvolume/_data","Destination": "/usr/share/nginx/html/","Driver": "local","Mode": "z","RW": true,"Propagation": ""}],"Config": {"Hostname": "439f4e91bd1d","Domainname": "string","User": "123:456","AttachStdin": false,"AttachStdout": true,"AttachStderr": true,"ExposedPorts": {"80/tcp": { },"443/tcp": { }},"Tty": false,"OpenStdin": false,"StdinOnce": false,"Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd": ["/bin/sh"],"Healthcheck": {"Test": ["string"],"Interval": 0,"Timeout": 0,"Retries": 0,"StartPeriod": 0,"StartInterval": 0},"ArgsEscaped": false,"Image": "example-image:1.0","Volumes": {"property1": { },"property2": { }},"WorkingDir": "/public/","Entrypoint": [ ],"NetworkDisabled": true,"MacAddress": "string","OnBuild": [ ],"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"StopSignal": "SIGTERM","StopTimeout": 10,"Shell": ["/bin/sh","-c"]},"NetworkSettings": {"Bridge": "docker0","SandboxID": "9d12daf2c33f5959c8bf90aa513e4f65b561738661003029ec84830cd503a0c3","HairpinMode": false,"LinkLocalIPv6Address": "","LinkLocalIPv6PrefixLen": "","Ports": {"443/tcp": [{"HostIp": "127.0.0.1","HostPort": "4443"}],"80/tcp": [{"HostIp": "0.0.0.0","HostPort": "80"},{"HostIp": "0.0.0.0","HostPort": "8080"}],"80/udp": [{"HostIp": "0.0.0.0","HostPort": "80"}],"53/udp": [{"HostIp": "0.0.0.0","HostPort": "53"}],"2377/tcp": null},"SandboxKey": "/var/run/docker/netns/8ab54b426c38","SecondaryIPAddresses": [{"Addr": "string","PrefixLen": 0}],"SecondaryIPv6Addresses": [{"Addr": "string","PrefixLen": 0}],"EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b","Gateway": "172.17.0.1","GlobalIPv6Address": "2001:db8::5689","GlobalIPv6PrefixLen": 64,"IPAddress": "172.17.0.4","IPPrefixLen": 16,"IPv6Gateway": "2001:db8:2::100","MacAddress": "02:42:ac:11:00:04","Networks": {"property1": {"IPAMConfig": {"IPv4Address": "172.20.30.33","IPv6Address": "2001:db8:abcd::3033","LinkLocalIPs": ["169.254.34.68","fe80::3468"]},"Links": ["container_1","container_2"],"MacAddress": "02:42:ac:11:00:04","Aliases": ["server_x","server_y"],"DriverOpts": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"GwPriority": [10],"NetworkID": "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a","EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b","Gateway": "172.17.0.1","IPAddress": "172.17.0.4","IPPrefixLen": 16,"IPv6Gateway": "2001:db8:2::100","GlobalIPv6Address": "2001:db8::5689","GlobalIPv6PrefixLen": 64,"DNSNames": ["foobar","server_x","server_y","my.ctr"]},"property2": {"IPAMConfig": {"IPv4Address": "172.20.30.33","IPv6Address": "2001:db8:abcd::3033","LinkLocalIPs": ["169.254.34.68","fe80::3468"]},"Links": ["container_1","container_2"],"MacAddress": "02:42:ac:11:00:04","Aliases": ["server_x","server_y"],"DriverOpts": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"GwPriority": [10],"NetworkID": "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a","EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b","Gateway": "172.17.0.1","IPAddress": "172.17.0.4","IPPrefixLen": 16,"IPv6Gateway": "2001:db8:2::100","GlobalIPv6Address": "2001:db8::5689","GlobalIPv6PrefixLen": 64,"DNSNames": ["foobar","server_x","server_y","my.ctr"]}}}}`

## List processes running inside a container

On Unix systems, this is done by running the `ps` command. This endpoint
is not supported on Windows.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| ps_args | stringDefault:"-ef"The arguments to pass tops. For example,aux |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"Titles": {"Titles": ["UID","PID","PPID","C","STIME","TTY","TIME","CMD"]},"Processes": {"Processes": [["root","13642","882","0","17:03","pts/0","00:00:00","/bin/bash"],["root","13735","13642","0","17:06","pts/0","00:00:00","sleep 10"]]}}`

## Get container logs

Get `stdout` and `stderr` logs from a container.

Note: This endpoint works only for containers with the `json-file` or
`journald` logging driver.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| follow | booleanDefault:falseKeep connection after returning logs. |
| --- | --- |
| stdout | booleanDefault:falseReturn logs fromstdout |
| stderr | booleanDefault:falseReturn logs fromstderr |
| since | integerDefault:0Only return logs since this time, as a UNIX timestamp |
| until | integerDefault:0Only return logs before this time, as a UNIX timestamp |
| timestamps | booleanDefault:falseAdd timestamps to every log line |
| tail | stringDefault:"all"Only return this number of log lines from the end of the logs.
Specify as an integer orallto output all log lines. |

### Responses

### Response samples

- 404

Content typeapplication/vnd.docker.raw-streamapplication/vnd.docker.multiplexed-streamapplication/jsonapplication/vnd.docker.raw-streamNo sample

## Get changes on a container’s filesystem

Returns which files in a container's filesystem have been added, deleted,
or modified. The `Kind` of modification can be one of:

- `0`: Modified ("C")
- `1`: Added ("A")
- `2`: Deleted ("D")

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`[{"Path": "/dev","Kind": 0},{"Path": "/dev/kmsg","Kind": 1},{"Path": "/test","Kind": 1}]`

## Export a container

Export the contents of a container as a tarball.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

### Responses

### Response samples

- 404

Content typeapplication/octet-streamapplication/jsonapplication/octet-streamNo sample

## Get container stats based on resource usage

This endpoint returns a live stream of a container’s resource usage
statistics.

The `precpu_stats` is the CPU statistic of the *previous* read, and is
used to calculate the CPU usage percentage. It is not an exact copy
of the `cpu_stats` field.

If either `precpu_stats.online_cpus` or `cpu_stats.online_cpus` is
nil then for compatibility with older daemons the length of the
corresponding `cpu_usage.percpu_usage` array should be used.

On a cgroup v2 host, the following fields are not set

- `blkio_stats`: all fields other than `io_service_bytes_recursive`
- `cpu_stats`: `cpu_usage.percpu_usage`
- `memory_stats`: `max_usage` and `failcnt`
  Also, `memory_stats.stats` fields are incompatible with cgroup v1.

To calculate the values shown by the `stats` command of the docker cli tool
the following formulas can be used:

- used_memory = `memory_stats.usage - memory_stats.stats.cache` (cgroups v1)
- used_memory = `memory_stats.usage - memory_stats.stats.inactive_file` (cgroups v2)
- available_memory = `memory_stats.limit`
- Memory usage % = `(used_memory / available_memory) * 100.0`
- cpu_delta = `cpu_stats.cpu_usage.total_usage - precpu_stats.cpu_usage.total_usage`
- system_cpu_delta = `cpu_stats.system_cpu_usage - precpu_stats.system_cpu_usage`
- number_cpus = `length(cpu_stats.cpu_usage.percpu_usage)` or `cpu_stats.online_cpus`
- CPU usage % = `(cpu_delta / system_cpu_delta) * number_cpus * 100.0`

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| stream | booleanDefault:trueStream the output. If false, the stats will be output once and then
it will disconnect. |
| --- | --- |
| one-shot | booleanDefault:falseOnly get a single stat instead of waiting for 2 cycles. Must be used
withstream=false. |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"name": "boring_wozniak","id": "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743","read": "2025-01-16T13:55:22.165243637Z","preread": "2025-01-16T13:55:21.160452595Z","pids_stats": {"current": 5,"limit": "18446744073709551615"},"blkio_stats": {"io_service_bytes_recursive": [{"major": 254,"minor": 0,"op": "read","value": 7593984},{"major": 254,"minor": 0,"op": "write","value": 100}],"io_serviced_recursive": null,"io_queue_recursive": null,"io_service_time_recursive": null,"io_wait_time_recursive": null,"io_merged_recursive": null,"io_time_recursive": null,"sectors_recursive": null},"num_procs": 16,"storage_stats": {"read_count_normalized": 7593984,"read_size_bytes": 7593984,"write_count_normalized": 7593984,"write_size_bytes": 7593984},"cpu_stats": {"cpu_usage": {"total_usage": 29912000,"percpu_usage": [29912000],"usage_in_kernelmode": 21994000,"usage_in_usermode": 7918000},"system_cpu_usage": 5,"online_cpus": 5,"throttling_data": {"periods": 0,"throttled_periods": 0,"throttled_time": 0}},"precpu_stats": {"cpu_usage": {"total_usage": 29912000,"percpu_usage": [29912000],"usage_in_kernelmode": 21994000,"usage_in_usermode": 7918000},"system_cpu_usage": 5,"online_cpus": 5,"throttling_data": {"periods": 0,"throttled_periods": 0,"throttled_time": 0}},"memory_stats": {"usage": 0,"max_usage": 0,"stats": {"active_anon": 1572864,"active_file": 5115904,"anon": 1572864,"anon_thp": 0,"file": 7626752,"file_dirty": 0,"file_mapped": 2723840,"file_writeback": 0,"inactive_anon": 0,"inactive_file": 2510848,"kernel_stack": 16384,"pgactivate": 0,"pgdeactivate": 0,"pgfault": 2042,"pglazyfree": 0,"pglazyfreed": 0,"pgmajfault": 45,"pgrefill": 0,"pgscan": 0,"pgsteal": 0,"shmem": 0,"slab": 1180928,"slab_reclaimable": 725576,"slab_unreclaimable": 455352,"sock": 0,"thp_collapse_alloc": 0,"thp_fault_alloc": 1,"unevictable": 0,"workingset_activate": 0,"workingset_nodereclaim": 0,"workingset_refault": 0},"failcnt": 0,"limit": 8217579520,"commitbytes": 0,"commitpeakbytes": 0,"privateworkingset": 0},"networks": {"eth0": {"rx_bytes": 5338,"rx_dropped": 0,"rx_errors": 0,"rx_packets": 36,"tx_bytes": 648,"tx_dropped": 0,"tx_errors": 0,"tx_packets": 8},"eth5": {"rx_bytes": 4641,"rx_dropped": 0,"rx_errors": 0,"rx_packets": 26,"tx_bytes": 690,"tx_dropped": 0,"tx_errors": 0,"tx_packets": 9}}}`

## Resize a container TTY

Resize the TTY for a container.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| hrequired | integerHeight of the TTY session in characters |
| --- | --- |
| wrequired | integerWidth of the TTY session in characters |

### Responses

### Response samples

- 404

Content typetext/plainapplication/jsontext/plainNo sample

## Start a container

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| detachKeys | stringOverride the key sequence for detaching a container. Format is a
single character[a-Z]orctrl-<value>where<value>is one
of:a-z,@,^,[,,or_. |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Stop a container

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| signal | stringSignal to send to the container as an integer or string (e.g.SIGINT). |
| --- | --- |
| t | integerNumber of seconds to wait before killing the container |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Restart a container

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| signal | stringSignal to send to the container as an integer or string (e.g.SIGINT). |
| --- | --- |
| t | integerNumber of seconds to wait before killing the container |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Kill a container

Send a POSIX signal to a container, defaulting to killing to the
container.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| signal | stringDefault:"SIGKILL"Signal to send to the container as an integer or string (e.g.SIGINT). |
| --- | --- |

### Responses

### Response samples

- 404
- 409
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Update a container

Change various configuration options of a container without having to
recreate it.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### Request Body schema:application/jsonrequired

| CpuShares | integerAn integer value representing this container's relative CPU weight
versus other containers. |
| --- | --- |
| Memory | integer<int64>Default:0Memory limit in bytes. |
| CgroupParent | stringPath tocgroupsunder which the container'scgroupis created. If
the path is not absolute, the path is considered to be relative to thecgroupspath of the init process. Cgroups are created if they do not
already exist. |
| BlkioWeight | integer[ 0 .. 1000 ]Block IO weight (relative weight). |
|  | Array ofobjectsBlock IO weight (relative device weight) in the form:[{"Path":"device_path","Weight":weight}] |
|  | Array ofobjects(ThrottleDevice)Limit read rate (bytes per second) from a device, in the form:[{"Path":"device_path","Rate":rate}] |
|  | Array ofobjects(ThrottleDevice)Limit write rate (bytes per second) to a device, in the form:[{"Path":"device_path","Rate":rate}] |
|  | Array ofobjects(ThrottleDevice)Limit read rate (IO per second) from a device, in the form:[{"Path":"device_path","Rate":rate}] |
|  | Array ofobjects(ThrottleDevice)Limit write rate (IO per second) to a device, in the form:[{"Path":"device_path","Rate":rate}] |
| CpuPeriod | integer<int64>The length of a CPU period in microseconds. |
| CpuQuota | integer<int64>Microseconds of CPU time that the container can get in a CPU period. |
| CpuRealtimePeriod | integer<int64>The length of a CPU real-time period in microseconds. Set to 0 to
allocate no time allocated to real-time tasks. |
| CpuRealtimeRuntime | integer<int64>The length of a CPU real-time runtime in microseconds. Set to 0 to
allocate no time allocated to real-time tasks. |
| CpusetCpus | stringCPUs in which to allow execution (e.g.,0-3,0,1). |
| CpusetMems | stringMemory nodes (MEMs) in which to allow execution (0-3, 0,1). Only
effective on NUMA systems. |
|  | Array ofobjects(DeviceMapping)A list of devices to add to the container. |
| DeviceCgroupRules | Array ofstringsa list of cgroup rules to apply to the container |
|  | Array ofobjects(DeviceRequest)A list of requests for devices to be sent to device drivers. |
| KernelMemoryTCP | integer<int64>Hard limit for kernel TCP buffer memory (in bytes). Depending on the
OCI runtime in use, this option may be ignored. It is no longer supported
by the default (runc) runtime.This field is omitted when empty.Deprecated: This field is deprecated as kernel 6.12 has deprecatedmemory.kmem.tcp.limit_in_bytesfield
for cgroups v1. This field will be removed in a future release. |
| MemoryReservation | integer<int64>Memory soft limit in bytes. |
| MemorySwap | integer<int64>Total memory limit (memory + swap). Set as-1to enable unlimited
swap. |
| MemorySwappiness | integer<int64>[ 0 .. 100 ]Tune a container's memory swappiness behavior. Accepts an integer
between 0 and 100. |
| NanoCpus | integer<int64>CPU quota in units of 10-9CPUs. |
| OomKillDisable | booleanDisable OOM Killer for the container. |
| Init | boolean or nullRun an init inside the container that forwards signals and reaps
processes. This field is omitted if empty, and the default (as
configured on the daemon) is used. |
| PidsLimit | integer or null<int64>Tune a container's PIDs limit. Set0or-1for unlimited, ornullto not change. |
|  | Array ofobjectsA list of resource limits to set in the container. For example:{"Name":"nofile","Soft":1024,"Hard":2048} |
| CpuCount | integer<int64>The number of usable CPUs (Windows only).On Windows Server containers, the processor resource controls are
mutually exclusive. The order of precedence isCPUCountfirst, thenCPUShares, andCPUPercentlast. |
| CpuPercent | integer<int64>The usable percentage of the available CPUs (Windows only).On Windows Server containers, the processor resource controls are
mutually exclusive. The order of precedence isCPUCountfirst, thenCPUShares, andCPUPercentlast. |
| IOMaximumIOps | integer<int64>Maximum IOps for the container system drive (Windows only) |
| IOMaximumBandwidth | integer<int64>Maximum IO in bytes per second for the container system drive
(Windows only). |
|  | object(RestartPolicy)The behavior to apply when the container exits. The default is not to
restart.An ever increasing delay (double the previous delay, starting at 100ms) is
added before each restart to prevent flooding the server. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"BlkioWeight": 300,"CpuShares": 512,"CpuPeriod": 100000,"CpuQuota": 50000,"CpuRealtimePeriod": 1000000,"CpuRealtimeRuntime": 10000,"CpusetCpus": "0,1","CpusetMems": "0","Memory": 314572800,"MemorySwap": 514288000,"MemoryReservation": 209715200,"RestartPolicy": {"MaximumRetryCount": 4,"Name": "on-failure"}}`

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"Warnings": ["Published ports are discarded when using host network mode"]}`

## Rename a container

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| namerequired | stringNew name for the container |
| --- | --- |

### Responses

### Response samples

- 404
- 409
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Pause a container

Use the freezer cgroup to suspend all processes in a container.

Traditionally, when suspending a process the `SIGSTOP` signal is used,
which is observable by the process being suspended. With the freezer
cgroup the process is unaware, and unable to capture, that it is being
suspended, and subsequently resumed.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Unpause a container

Resume a container which has been paused.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "No such container: c2ada9df5af8"}`

## Attach to a container

Attach to a container to read its output or send it input. You can attach
to the same container multiple times and you can reattach to containers
that have been detached.

Either the `stream` or `logs` parameter must be `true` for this endpoint
to do anything.

See the [documentation for thedocker attachcommand](https://docs.docker.com/engine/reference/commandline/attach/)
for more details.

### Hijacking

This endpoint hijacks the HTTP connection to transport `stdin`, `stdout`,
and `stderr` on the same socket.

This is the response from the daemon for an attach request:

```
HTTP/1.1 200 OK
Content-Type: application/vnd.docker.raw-stream

[STREAM]
```

After the headers and two new lines, the TCP connection can now be used
for raw, bidirectional communication between the client and server.

To hint potential proxies about connection hijacking, the Docker client
can also optionally send connection upgrade headers.

For example, the client sends this request to upgrade the connection:

```
POST /containers/16253994b7c4/attach?stream=1&stdout=1 HTTP/1.1
Upgrade: tcp
Connection: Upgrade
```

The Docker daemon will respond with a `101 UPGRADED` response, and will
similarly follow with the raw stream:

```
HTTP/1.1 101 UPGRADED
Content-Type: application/vnd.docker.raw-stream
Connection: Upgrade
Upgrade: tcp

[STREAM]
```

### Stream format

When the TTY setting is disabled in [POST /containers/create](#operation/ContainerCreate),
the HTTP Content-Type header is set to application/vnd.docker.multiplexed-stream
and the stream over the hijacked connected is multiplexed to separate out
`stdout` and `stderr`. The stream consists of a series of frames, each
containing a header and a payload.

The header contains the information which the stream writes (`stdout` or
`stderr`). It also contains the size of the associated frame encoded in
the last four bytes (`uint32`).

It is encoded on the first eight bytes like this:

```go
header := [8]byte{STREAM_TYPE, 0, 0, 0, SIZE1, SIZE2, SIZE3, SIZE4}
```

`STREAM_TYPE` can be:

- 0: `stdin` (is written on `stdout`)
- 1: `stdout`
- 2: `stderr`

`SIZE1, SIZE2, SIZE3, SIZE4` are the four bytes of the `uint32` size
encoded as big endian.

Following the header is the payload, which is the specified number of
bytes of `STREAM_TYPE`.

The simplest way to implement this protocol is the following:

1. Read 8 bytes.
2. Choose `stdout` or `stderr` depending on the first byte.
3. Extract the frame size from the last four bytes.
4. Read the extracted size and output it on the correct output.
5. Goto 1.

### Stream format when using a TTY

When the TTY setting is enabled in [POST /containers/create](#operation/ContainerCreate),
the stream is not multiplexed. The data exchanged over the hijacked
connection is simply the raw data from the process PTY and client's
`stdin`.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| detachKeys | stringOverride the key sequence for detaching a container.Format is a single
character[a-Z]orctrl-<value>where<value>is one of:a-z,@,^,[,,or_. |
| --- | --- |
| logs | booleanDefault:falseReplay previous logs from the container.This is useful for attaching to a container that has started and you
want to output everything since the container started.Ifstreamis also enabled, once all the previous output has been
returned, it will seamlessly transition into streaming current
output. |
| stream | booleanDefault:falseStream attached streams from the time the request was made onwards. |
| stdin | booleanDefault:falseAttach tostdin |
| stdout | booleanDefault:falseAttach tostdout |
| stderr | booleanDefault:falseAttach tostderr |

### Responses

### Response samples

- 404

Content typeapplication/vnd.docker.raw-streamapplication/vnd.docker.multiplexed-streamapplication/jsonapplication/vnd.docker.raw-streamNo sample

## Attach to a container via a websocket

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| detachKeys | stringOverride the key sequence for detaching a container.Format is a single
character[a-Z]orctrl-<value>where<value>is one of:a-z,@,^,[,,, or_. |
| --- | --- |
| logs | booleanDefault:falseReturn logs |
| stream | booleanDefault:falseReturn stream |
| stdin | booleanDefault:falseAttach tostdin |
| stdout | booleanDefault:falseAttach tostdout |
| stderr | booleanDefault:falseAttach tostderr |

### Responses

### Response samples

- 400
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Wait for a container

Block until a container stops, then returns the exit code.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| condition | stringDefault:"not-running"Enum:"not-running""next-exit""removed"Wait until a container state reaches the given condition.Defaults tonot-runningif omitted or empty. |
| --- | --- |

### Responses

### Response samples

- 200
- 400
- 404
- 500

Content typeapplication/json`{"StatusCode": 0,"Error": {"Message": "string"}}`

## Remove a container

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| v | booleanDefault:falseRemove anonymous volumes associated with the container. |
| --- | --- |
| force | booleanDefault:falseIf the container is running, kill it before removing it. |
| link | booleanDefault:falseRemove the specified link associated with the container. |

### Responses

### Response samples

- 400
- 404
- 409
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Get information about files in a container

A response header `X-Docker-Container-Path-Stat` is returned, containing
a base64 - encoded JSON object with some filesystem header information
about the path.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| pathrequired | stringResource in the container’s filesystem to archive. |
| --- | --- |

### Responses

### Response samples

- 400
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Get an archive of a filesystem resource in a container

Get a tar archive of a resource in the filesystem of container id.

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| pathrequired | stringResource in the container’s filesystem to archive. |
| --- | --- |

### Responses

### Response samples

- 404

Content typeapplication/x-tarapplication/jsonapplication/x-tarNo sample

## Extract an archive of files or folders to a directory in a container

Upload a tar archive to be extracted to a path in the filesystem of container id.
`path` parameter is asserted to be a directory. If it exists as a file, 400 error
will be returned with message "not a directory".

##### path Parameters

| idrequired | stringID or name of the container |
| --- | --- |

##### query Parameters

| pathrequired | stringPath to a directory in the container to extract the archive’s contents into. |
| --- | --- |
| noOverwriteDirNonDir | stringIf1,true, orTruethen it will be an error if unpacking the
given content would cause an existing directory to be replaced with
a non-directory and vice versa. |
| copyUIDGID | stringIf1,true, then it will copy UID/GID maps to the dest file or
dir |

##### Request Body schema:application/x-tarapplication/octet-streamapplication/x-tarrequired

The input stream must be a tar archive compressed with one of the
following algorithms: `identity` (no compression), `gzip`, `bzip2`,
or `xz`.

 string <binary>

### Responses

### Response samples

- 400
- 403
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "not a directory"}`

## Delete stopped containers

##### query Parameters

| filters | stringFilters to process on the prune list, encoded as JSON (amap[string][]string).Available filters:until=<timestamp>Prune containers created before this timestamp. The<timestamp>can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g.10m,1h30m) computed relative to the daemon machine’s time.label(label=<key>,label=<key>=<value>,label!=<key>, orlabel!=<key>=<value>) Prune containers with (or without, in caselabel!=...is used) the specified labels. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"ContainersDeleted": ["string"],"SpaceReclaimed": 0}`

## Images

## List Images

Returns a list of images on the server. Note that it uses a different, smaller representation of an image than inspecting a single image.

##### query Parameters

| all | booleanDefault:falseShow all images. Only images from a final layer (no children) are shown by default. |
| --- | --- |
| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the images list.Available filters:before=(<image-name>[:<tag>],<image id>or<image@digest>)dangling=truelabel=keyorlabel="key=value"of an image labelreference=(<image-name>[:<tag>])since=(<image-name>[:<tag>],<image id>or<image@digest>)until=<timestamp> |
| shared-size | booleanDefault:falseCompute and show shared size as aSharedSizefield on each image. |
| digests | booleanDefault:falseShow digest information as aRepoDigestsfield on each image. |
| manifests | booleanDefault:falseIncludeManifestsin the image summary. |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`[{"Id": "sha256:ec3f0931a6e6b6855d76b2d7b0be30e81860baccd891b2e243280bf1cd8ad710","ParentId": "","RepoTags": ["example:1.0","example:latest","example:stable","internal.registry.example.com:5000/example:1.0"],"RepoDigests": ["example@sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb","internal.registry.example.com:5000/example@sha256:b69959407d21e8a062e0416bf13405bb2b71ed7a84dde4158ebafacfa06f5578"],"Created": "1644009612","Size": 172064416,"SharedSize": 1239828,"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"Containers": 2,"Manifests": [{"ID": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f","Descriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null},"Available": true,"Size": {"Total": 8213251,"Content": 3987495},"Kind": "image","ImageData": {"Platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"Containers": ["ede54ee1fda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c7430","abadbce344c096744d8d6071a90d474d28af8f1034b5ea9fb03c3f4bfc6d005e"],"Size": {"Unpacked": 3987495}},"AttestationData": {"For": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f"}}],"Descriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null}}]`

## Build an image

Build an image from a tar archive with a `Dockerfile` in it.

The `Dockerfile` specifies how the image is built from the tar archive. It is typically in the archive's root, but can be at a different path or have a different name by specifying the `dockerfile` parameter. [See theDockerfilereference for more information](https://docs.docker.com/engine/reference/builder/).

The Docker daemon performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. After that, each instruction is run one-by-one until the ID of the new image is output.

The build is canceled if the client drops the connection by quitting or being killed.

##### query Parameters

| dockerfile | stringDefault:"Dockerfile"Path within the build context to theDockerfile. This is ignored ifremoteis specified and points to an externalDockerfile. |
| --- | --- |
| t | stringA name and optional tag to apply to the image in thename:tagformat. If you omit the tag the defaultlatestvalue is assumed. You can provide severaltparameters. |
| extrahosts | stringExtra hosts to add to /etc/hosts |
| remote | stringA Git repository URI or HTTP/HTTPS context URI. If the URI points to a single text file, the file’s contents are placed into a file calledDockerfileand the image is built from that file. If the URI points to a tarball, the file is downloaded by the daemon and the contents therein used as the context for the build. If the URI points to a tarball and thedockerfileparameter is also specified, there must be a file with the corresponding path inside the tarball. |
| q | booleanDefault:falseSuppress verbose build output. |
| nocache | booleanDefault:falseDo not use the cache when building the image. |
| cachefrom | stringJSON array of images used for build cache resolution. |
| pull | stringAttempt to pull the image even if an older image exists locally. |
| rm | booleanDefault:trueRemove intermediate containers after a successful build. |
| forcerm | booleanDefault:falseAlways remove intermediate containers, even upon failure. |
| memory | integerSet memory limit for build. |
| memswap | integerTotal memory (memory + swap). Set as-1to disable swap. |
| cpushares | integerCPU shares (relative weight). |
| cpusetcpus | stringCPUs in which to allow execution (e.g.,0-3,0,1). |
| cpuperiod | integerThe length of a CPU period in microseconds. |
| cpuquota | integerMicroseconds of CPU time that the container can get in a CPU period. |
| buildargs | stringJSON map of string pairs for build-time variables. Users pass these values at build-time. Docker uses the buildargs as the environment context for commands run via theDockerfileRUN instruction, or for variable expansion in otherDockerfileinstructions. This is not meant for passing secret values.For example, the build argFOO=barwould become{"FOO":"bar"}in JSON. This would result in the query parameterbuildargs={"FOO":"bar"}. Note that{"FOO":"bar"}should be URI component encoded.Read more about the buildargs instruction. |
| shmsize | integerSize of/dev/shmin bytes. The size must be greater than 0. If omitted the system uses 64MB. |
| squash | booleanSquash the resulting images layers into a single layer.(Experimental release only.) |
| labels | stringArbitrary key/value labels to set on the image, as a JSON map of string pairs. |
| networkmode | stringSets the networking mode for the run commands during build. Supported
standard values are:bridge,host,none, andcontainer:<name|id>.
Any other value is taken as a custom network's name or ID to which this
container should connect to. |
| platform | stringDefault:""Platform in the format os[/arch[/variant]] |
| target | stringDefault:""Target build stage |
| outputs | stringDefault:""BuildKit output configuration in the format of a stringified JSON array of objects.
Each object must have two top-level properties:TypeandAttrs.
TheTypeproperty must be set to 'moby'.
TheAttrsproperty is a map of attributes for the BuildKit output configuration.
Seehttps://docs.docker.com/build/exporters/oci-docker/for more information.Example:[{"Type":"moby","Attrs":{"type":"image","force-compression":"true","compression":"zstd"}}] |
| version | stringDefault:"1"Enum:"1""2"Version of the builder backend to use.1is the first generation classic (deprecated) builder in the Docker daemon (default)2isBuildKit |

##### header Parameters

| Content-type | stringDefault:application/x-tarValue:"application/x-tar" |
| --- | --- |
| X-Registry-Config | stringThis is a base64-encoded JSON object with auth configurations for multiple registries that a build may refer to.The key is a registry URL, and the value is an auth configuration object,as described in the authentication section. For example:{"docker.example.com":{"username":"janedoe","password":"hunter2"},"https://index.docker.io/v1/":{"username":"mobydock","password":"conta1n3rize14"}}Only the registry domain name (and port if not the default 443) are required. However, for legacy reasons, the Docker Hub registry must be specified with both ahttps://prefix and a/v1/suffix even though Docker will prefer to use the v2 registry API. |

##### Request Body schema:application/octet-stream

A tar archive compressed with one of the following algorithms: identity (no compression), gzip, bzip2, xz.

 string <binary>

### Responses

### Response samples

- 400
- 500

Content typeapplication/json`{"message": "Something went wrong."}`

## Delete builder cache

##### query Parameters

| keep-storage | integer<int64>Amount of disk space in bytes to keep for cacheDeprecated: This parameter is deprecated and has been renamed to "reserved-space".
It is kept for backward compatibility and will be removed in API v1.52. |
| --- | --- |
| reserved-space | integer<int64>Amount of disk space in bytes to keep for cache |
| max-used-space | integer<int64>Maximum amount of disk space allowed to keep for cache |
| min-free-space | integer<int64>Target amount of free disk space after pruning |
| all | booleanRemove all types of build cache |
| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the list of build cache objects.Available filters:until=<timestamp>remove cache older than<timestamp>. The<timestamp>can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g.10m,1h30m) computed relative to the daemon's local time.id=<id>parent=<id>type=<string>description=<string>inusesharedprivate |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"CachesDeleted": ["string"],"SpaceReclaimed": 0}`

## Create an image

Pull or import an image.

##### query Parameters

| fromImage | stringName of the image to pull. If the name includes a tag or digest, specific behavior applies:If onlyfromImageincludes a tag, that tag is used.If bothfromImageandtagare provided,tagtakes precedence.IffromImageincludes a digest, the image is pulled by digest, andtagis ignored.If neither a tag nor digest is specified, all tags are pulled. |
| --- | --- |
| fromSrc | stringSource to import. The value may be a URL from which the image can be retrieved or-to read the image from the request body. This parameter may only be used when importing an image. |
| repo | stringRepository name given to an image when it is imported. The repo may include a tag. This parameter may only be used when importing an image. |
| tag | stringTag or digest. If empty when pulling an image, this causes all tags for the given image to be pulled. |
| message | stringSet commit message for imported image. |
| changes | Array ofstringsApplyDockerfileinstructions to the image that is created,
for example:changes=ENV DEBUG=true.
Note thatENV DEBUG=trueshould be URI component encoded.SupportedDockerfileinstructions:CMD|ENTRYPOINT|ENV|EXPOSE|ONBUILD|USER|VOLUME|WORKDIR |
| platform | stringDefault:""Platform in the format os[/arch[/variant]].When used in combination with thefromImageoption, the daemon checks
if the given image is present in the local image cache with the given
OS and Architecture, and otherwise attempts to pull the image. If the
option is not set, the host's native OS and Architecture are used.
If the given image does not exist in the local image cache, the daemon
attempts to pull the image with the host's native OS and Architecture.
If the given image does exists in the local image cache, but its OS or
architecture does not match, a warning is produced.When used with thefromSrcoption to import an image from an archive,
this option sets the platform information for the imported image. If
the option is not set, the host's native OS and Architecture are used
for the imported image. |

##### header Parameters

| X-Registry-Auth | stringA base64url-encoded auth configuration.Refer to theauthentication sectionfor
details. |
| --- | --- |

##### Request Body schema:text/plainapplication/octet-streamtext/plain

Image content if the value `-` has been specified in fromSrc query parameter

 string

### Responses

### Response samples

- 404
- 500

Content typeapplication/json`{"message": "Something went wrong."}`

## Inspect an image

Return low-level information about an image.

##### path Parameters

| namerequired | stringImage name or id |
| --- | --- |

##### query Parameters

| manifests | booleanDefault:falseInclude Manifests in the image summary. |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"Id": "sha256:ec3f0931a6e6b6855d76b2d7b0be30e81860baccd891b2e243280bf1cd8ad710","Descriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null},"Manifests": [{"ID": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f","Descriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null},"Available": true,"Size": {"Total": 8213251,"Content": 3987495},"Kind": "image","ImageData": {"Platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"Containers": ["ede54ee1fda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c7430","abadbce344c096744d8d6071a90d474d28af8f1034b5ea9fb03c3f4bfc6d005e"],"Size": {"Unpacked": 3987495}},"AttestationData": {"For": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f"}}],"RepoTags": ["example:1.0","example:latest","example:stable","internal.registry.example.com:5000/example:1.0"],"RepoDigests": ["example@sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb","internal.registry.example.com:5000/example@sha256:b69959407d21e8a062e0416bf13405bb2b71ed7a84dde4158ebafacfa06f5578"],"Parent": "","Comment": "","Created": "2022-02-04T21:20:12.497794809Z","DockerVersion": "27.0.1","Author": "","Config": {"User": "web:web","ExposedPorts": {"80/tcp": { },"443/tcp": { }},"Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd": ["/bin/sh"],"Healthcheck": {"Test": ["string"],"Interval": 0,"Timeout": 0,"Retries": 0,"StartPeriod": 0,"StartInterval": 0},"ArgsEscaped": false,"Volumes": {"/app/data": { },"/app/config": { }},"WorkingDir": "/public/","Entrypoint": [ ],"OnBuild": [ ],"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"StopSignal": "SIGTERM","Shell": ["/bin/sh","-c"]},"Architecture": "arm","Variant": "v7","Os": "linux","OsVersion": "","Size": 1239828,"GraphDriver": {"Name": "overlay2","Data": {"MergedDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/merged","UpperDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/diff","WorkDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/work"}},"RootFS": {"Type": "layers","Layers": ["sha256:1834950e52ce4d5a88a1bbd131c537f4d0e56d10ff0dd69e66be3b7dfa9df7e6","sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef"]},"Metadata": {"LastTagTime": "2022-02-28T14:40:02.623929178Z"}}`

## Get the history of an image

Return parent layers of an image.

##### path Parameters

| namerequired | stringImage name or ID |
| --- | --- |

##### query Parameters

| platform | stringJSON-encoded OCI platform to select the platform-variant.
If omitted, it defaults to any locally available platform,
prioritizing the daemon's host platform.If the daemon provides a multi-platform image store, this selects
the platform-variant to show the history for. If the image is
a single-platform image, or if the multi-platform image does not
provide a variant matching the given platform, an error is returned.Example:{"os": "linux", "architecture": "arm", "variant": "v5"} |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`[{"Id": "3db9c44f45209632d6050b35958829c3a2aa256d81b9a7be45b362ff85c54710","Created": 1398108230,"CreatedBy": "/bin/sh -c #(nop) ADD file:eb15dbd63394e063b805a3c32ca7bf0266ef64676d5a6fab4801f2e81e2a5148 in /","Tags": ["ubuntu:lucid","ubuntu:10.04"],"Size": 182964289,"Comment": ""},{"Id": "6cfa4d1f33fb861d4d114f43b25abd0ac737509268065cdfd69d544a59c85ab8","Created": 1398108222,"CreatedBy": "/bin/sh -c #(nop) MAINTAINER Tianon Gravi <admwiggin@gmail.com> - mkimage-debootstrap.sh -i iproute,iputils-ping,ubuntu-minimal -t lucid.tar.xz lucid http://archive.ubuntu.com/ubuntu/","Tags": [ ],"Size": 0,"Comment": ""},{"Id": "511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158","Created": 1371157430,"CreatedBy": "","Tags": ["scratch12:latest","scratch:latest"],"Size": 0,"Comment": "Imported from -"}]`

## Push an image

Push an image to a registry.

If you wish to push an image on to a private registry, that image must
already have a tag which references the registry. For example,
`registry.example.com/myimage:latest`.

The push is cancelled if the HTTP connection is closed.

##### path Parameters

| namerequired | stringName of the image to push. For example,registry.example.com/myimage.
The image must be present in the local image store with the same name.The name should be provided without tag; if a tag is provided, it
is ignored. For example,registry.example.com/myimage:latestis
considered equivalent toregistry.example.com/myimage.Use thetagparameter to specify the tag to push. |
| --- | --- |

##### query Parameters

| tag | stringTag of the image to push. For example,latest. If no tag is provided,
all tags of the given image that are present in the local image store
are pushed. |
| --- | --- |
| platform | stringJSON-encoded OCI platform to select the platform-variant to push.
If not provided, all available variants will attempt to be pushed.If the daemon provides a multi-platform image store, this selects
the platform-variant to push to the registry. If the image is
a single-platform image, or if the multi-platform image does not
provide a variant matching the given platform, an error is returned.Example:{"os": "linux", "architecture": "arm", "variant": "v5"} |

##### header Parameters

| X-Registry-Authrequired | stringA base64url-encoded auth configuration.Refer to theauthentication sectionfor
details. |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Tag an image

Create a tag that refers to a source image.

This creates an additional reference (tag) to the source image. The tag
can include a different repository name and/or tag. If the repository
or tag already exists, it will be overwritten.

##### path Parameters

| namerequired | stringImage name or ID to tag. |
| --- | --- |

##### query Parameters

| repo | stringThe repository to tag in. For example,someuser/someimage. |
| --- | --- |
| tag | stringThe name of the new tag. |

### Responses

### Response samples

- 400
- 404
- 409
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Remove an image

Remove an image, along with any untagged parent images that were
referenced by that image.

Images can't be removed if they have descendant images, are being
used by a running container or are being used by a build.

##### path Parameters

| namerequired | stringImage name or ID |
| --- | --- |

##### query Parameters

| force | booleanDefault:falseRemove the image even if it is being used by stopped containers or has other tags |
| --- | --- |
| noprune | booleanDefault:falseDo not delete untagged parent images |
| platforms | Array ofstringsSelect platform-specific content to delete.
Multiple values are accepted.
Each platform is a OCI platform encoded as a JSON string. |

### Responses

### Response samples

- 200
- 404
- 409
- 500

Content typeapplication/json`[{"Untagged": "3e2f21a89f"},{"Deleted": "3e2f21a89f"},{"Deleted": "53b4f83ac9"}]`

## Search images

Search for an image on Docker Hub.

##### query Parameters

| termrequired | stringTerm to search |
| --- | --- |
| limit | integerMaximum number of results to return |
| filters | stringA JSON encoded value of the filters (amap[string][]string) to process on the images list. Available filters:is-official=(true|false)stars=<number>Matches images that has at least 'number' stars. |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`[{"description": "A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size!","is_official": true,"is_automated": false,"name": "alpine","star_count": 10093},{"description": "Busybox base image.","is_official": true,"is_automated": false,"name": "Busybox base image.","star_count": 3037},{"description": "The PostgreSQL object-relational database system provides reliability and data integrity.","is_official": true,"is_automated": false,"name": "postgres","star_count": 12408}]`

## Delete unused images

##### query Parameters

| filters | stringFilters to process on the prune list, encoded as JSON (amap[string][]string). Available filters:dangling=<boolean>When set totrue(or1), prune only
 unusedanduntagged images. When set tofalse(or0), all unused images are pruned.until=<string>Prune images created before this timestamp. The<timestamp>can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g.10m,1h30m) computed relative to the daemon machine’s time.label(label=<key>,label=<key>=<value>,label!=<key>, orlabel!=<key>=<value>) Prune images with (or without, in caselabel!=...is used) the specified labels. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"ImagesDeleted": [{"Untagged": "string","Deleted": "string"}],"SpaceReclaimed": 0}`

## Create a new image from a container

##### query Parameters

| container | stringThe ID or name of the container to commit |
| --- | --- |
| repo | stringRepository name for the created image |
| tag | stringTag name for the create image |
| comment | stringCommit message |
| author | stringAuthor of the image (e.g.,John Hannibal Smith <hannibal@a-team.com>) |
| pause | booleanDefault:trueWhether to pause the container before committing |
| changes | stringDockerfileinstructions to apply while committing |

##### Request Body schema:application/json

The container configuration

| Hostname | stringThe hostname to use for the container, as a valid RFC 1123 hostname. |
| --- | --- |
| Domainname | stringThe domain name to use for the container. |
| User | stringCommands run as this user inside the container. If omitted, commands
run as the user specified in the image the container was started from.Can be either user-name or UID, and optional group-name or GID,
separated by a colon (<user-name|UID>[<:group-name|GID>]). |
| AttachStdin | booleanDefault:falseWhether to attach tostdin. |
| AttachStdout | booleanDefault:trueWhether to attach tostdout. |
| AttachStderr | booleanDefault:trueWhether to attach tostderr. |
|  | object or nullAn object mapping ports to an empty object in the form:{"<port>/<tcp|udp|sctp>": {}} |
| Tty | booleanDefault:falseAttach standard streams to a TTY, includingstdinif it is not closed. |
| OpenStdin | booleanDefault:falseOpenstdin |
| StdinOnce | booleanDefault:falseClosestdinafter one attached client disconnects |
| Env | Array ofstringsA list of environment variables to set inside the container in the
form["VAR=value", ...]. A variable without=is removed from the
environment, rather than to have an empty value. |
| Cmd | Array ofstringsCommand to run specified as a string or an array of strings. |
|  | object(HealthConfig)A test to perform to check that the container is healthy.
Healthcheck commands should be side-effect free. |
| ArgsEscaped | boolean or nullDefault:falseCommand is already escaped (Windows only) |
| Image | stringThe name (or reference) of the image to use when creating the container,
or which was used when the container was created. |
|  | objectAn object mapping mount point paths inside the container to empty
objects. |
| WorkingDir | stringThe working directory for commands to run in. |
| Entrypoint | Array ofstringsThe entry point for the container as a string or an array of strings.If the array consists of exactly one empty string ([""]) then the
entry point is reset to system default (i.e., the entry point used by
docker when there is noENTRYPOINTinstruction in theDockerfile). |
| NetworkDisabled | boolean or nullDisable networking for the container. |
| MacAddress | string or nullMAC address of the container.Deprecated: this field is deprecated in API v1.44 and up. Use EndpointSettings.MacAddress instead. |
| OnBuild | Array ofstrings or nullONBUILDmetadata that were defined in the image'sDockerfile. |
|  | objectUser-defined key/value metadata. |
| StopSignal | string or nullSignal to stop a container as a string or unsigned integer. |
| StopTimeout | integer or nullDefault:10Timeout to stop a container in seconds. |
| Shell | Array ofstrings or nullShell for whenRUN,CMD, andENTRYPOINTuses a shell. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Hostname": "439f4e91bd1d","Domainname": "string","User": "123:456","AttachStdin": false,"AttachStdout": true,"AttachStderr": true,"ExposedPorts": {"80/tcp": { },"443/tcp": { }},"Tty": false,"OpenStdin": false,"StdinOnce": false,"Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd": ["/bin/sh"],"Healthcheck": {"Test": ["string"],"Interval": 0,"Timeout": 0,"Retries": 0,"StartPeriod": 0,"StartInterval": 0},"ArgsEscaped": false,"Image": "example-image:1.0","Volumes": {"property1": { },"property2": { }},"WorkingDir": "/public/","Entrypoint": [ ],"NetworkDisabled": true,"MacAddress": "string","OnBuild": [ ],"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"StopSignal": "SIGTERM","StopTimeout": 10,"Shell": ["/bin/sh","-c"]}`

### Response samples

- 201
- 404
- 500

Content typeapplication/json`{"Id": "string"}`

## Export an image

Get a tarball containing all images and metadata for a repository.

If `name` is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned. If `name` is an image ID, similarly only that image (and its parents) are returned, but with the exclusion of the `repositories` file in the tarball, as there were no image names referenced.

### Image tarball format

An image tarball contains [Content as defined in the OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-layout.md#content).

Additionally, includes the manifest.json file associated with a backwards compatible docker save format.

If the tarball defines a repository, the tarball should also include a `repositories` file at the root that contains a list of repository and tag names mapped to layer IDs.

```json
{
  "hello-world": {
    "latest": "565a9d68a73f6706862bfe8409a7f659776d4d60a8d096eb4a3cbce6999cc2a1"
  }
}
```

##### path Parameters

| namerequired | stringImage name or ID |
| --- | --- |

##### query Parameters

| platform | stringJSON encoded OCI platform describing a platform which will be used
to select a platform-specific image to be saved if the image is
multi-platform.
If not provided, the full multi-platform image will be saved.Example:{"os": "linux", "architecture": "arm", "variant": "v5"} |
| --- | --- |

### Responses

## Export several images

Get a tarball containing all images and metadata for several image
repositories.

For each value of the `names` parameter: if it is a specific name and
tag (e.g. `ubuntu:latest`), then only that image (and its parents) are
returned; if it is an image ID, similarly only that image (and its parents)
are returned and there would be no names referenced in the 'repositories'
file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

| names | Array ofstringsImage names to filter by |
| --- | --- |
| platform | stringJSON encoded OCI platform describing a platform which will be used
to select a platform-specific image to be saved if the image is
multi-platform.
If not provided, the full multi-platform image will be saved.Example:{"os": "linux", "architecture": "arm", "variant": "v5"} |

### Responses

## Import images

Load a set of images and tags into a repository.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

| quiet | booleanDefault:falseSuppress progress details during load. |
| --- | --- |
| platform | stringJSON encoded OCI platform describing a platform which will be used
to select a platform-specific image to be load if the image is
multi-platform.
If not provided, the full multi-platform image will be loaded.Example:{"os": "linux", "architecture": "arm", "variant": "v5"} |

##### Request Body schema:application/x-tar

Tar archive containing images

 string <binary>

### Responses

### Response samples

- 500

Content typeapplication/json`{"message": "Something went wrong."}`

## Networks

Networks are user-defined networks that containers can be attached to.
See the [networking documentation](https://docs.docker.com/network/)
for more information.

## List networks

Returns a list of networks. For details on the format, see the
[network inspect endpoint](#operation/NetworkInspect).

Note that it uses a different, smaller representation of a network than
inspecting a single network. For example, the list of containers attached
to the network is not propagated in API versions 1.28 and up.

##### query Parameters

| filters | stringJSON encoded value of the filters (amap[string][]string) to process
on the networks list.Available filters:dangling=<boolean>When set totrue(or1), returns all
 networks that are not in use by a container. When set tofalse(or0), only networks that are in use by one or more
 containers are returned.driver=<driver-name>Matches a network's driver.id=<network-id>Matches all or part of a network ID.label=<key>orlabel=<key>=<value>of a network label.name=<network-name>Matches all or part of a network name.scope=["swarm"|"global"|"local"]Filters networks by scope (swarm,global, orlocal).type=["custom"|"builtin"]Filters networks by type. Thecustomkeyword returns all user-defined networks. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`[{"Name": "bridge","Id": "f2de39df4171b0dc801e8002d1d999b77256983dfc63041c0f34030aa3977566","Created": "2016-10-19T06:21:00.416543526Z","Scope": "local","Driver": "bridge","EnableIPv4": true,"EnableIPv6": false,"Internal": false,"Attachable": false,"Ingress": false,"IPAM": {"Driver": "default","Config": [{"Subnet": "172.17.0.0/16"}]},"Options": {"com.docker.network.bridge.default_bridge": "true","com.docker.network.bridge.enable_icc": "true","com.docker.network.bridge.enable_ip_masquerade": "true","com.docker.network.bridge.host_binding_ipv4": "0.0.0.0","com.docker.network.bridge.name": "docker0","com.docker.network.driver.mtu": "1500"}},{"Name": "none","Id": "e086a3893b05ab69242d3c44e49483a3bbbd3a26b46baa8f61ab797c1088d794","Created": "0001-01-01T00:00:00Z","Scope": "local","Driver": "null","EnableIPv4": false,"EnableIPv6": false,"Internal": false,"Attachable": false,"Ingress": false,"IPAM": {"Driver": "default","Config": [ ]},"Containers": { },"Options": { }},{"Name": "host","Id": "13e871235c677f196c4e1ecebb9dc733b9b2d2ab589e30c539efeda84a24215e","Created": "0001-01-01T00:00:00Z","Scope": "local","Driver": "host","EnableIPv4": false,"EnableIPv6": false,"Internal": false,"Attachable": false,"Ingress": false,"IPAM": {"Driver": "default","Config": [ ]},"Containers": { },"Options": { }}]`

## Inspect a network

##### path Parameters

| idrequired | stringNetwork ID or name |
| --- | --- |

##### query Parameters

| verbose | booleanDefault:falseDetailed inspect output for troubleshooting |
| --- | --- |
| scope | stringFilter the network by scope (swarm, global, or local) |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"Name": "my_network","Id": "7d86d31b1478e7cca9ebed7e73aa0fdeec46c5ca29497431d3007d2d9e15ed99","Created": "2016-10-19T04:33:30.360899459Z","Scope": "local","Driver": "overlay","EnableIPv4": true,"EnableIPv6": false,"IPAM": {"Driver": "default","Config": [{"Subnet": "172.20.0.0/16","IPRange": "172.20.10.0/24","Gateway": "172.20.10.11","AuxiliaryAddresses": {"property1": "string","property2": "string"}}],"Options": {"foo": "bar"}},"Internal": false,"Attachable": false,"Ingress": false,"ConfigFrom": {"Network": "config_only_network_01"},"ConfigOnly": false,"Containers": {"19a4d5d687db25203351ed79d478946f861258f018fe384f229f2efa4b23513c": {"Name": "test","EndpointID": "628cadb8bcb92de107b2a1e516cbffe463e321f548feb37697cce00ad694f21a","MacAddress": "02:42:ac:13:00:02","IPv4Address": "172.19.0.2/16","IPv6Address": ""}},"Options": {"com.docker.network.bridge.default_bridge": "true","com.docker.network.bridge.enable_icc": "true","com.docker.network.bridge.enable_ip_masquerade": "true","com.docker.network.bridge.host_binding_ipv4": "0.0.0.0","com.docker.network.bridge.name": "docker0","com.docker.network.driver.mtu": "1500"},"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"Peers": [{"Name": "6869d7c1732b","IP": "10.133.77.91"}]}`

## Remove a network

##### path Parameters

| idrequired | stringNetwork ID or name |
| --- | --- |

### Responses

### Response samples

- 403
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Create a network

##### Request Body schema:application/jsonrequired

Network configuration

| Namerequired | stringThe network's name. |
| --- | --- |
| Driver | stringDefault:"bridge"Name of the network driver plugin to use. |
| Scope | stringThe level at which the network exists (e.g.swarmfor cluster-wide
orlocalfor machine level). |
| Internal | booleanRestrict external access to the network. |
| Attachable | booleanGlobally scoped network is manually attachable by regular
containers from workers in swarm mode. |
| Ingress | booleanIngress network is the network which provides the routing-mesh
in swarm mode. |
| ConfigOnly | booleanDefault:falseCreates a config-only network. Config-only networks are placeholder
networks for network configurations to be used by other networks.
Config-only networks cannot be used directly to run containers
or services. |
|  | object(ConfigReference)The config-only network source to provide the configuration for
this network. |
|  | object(IPAM) |
| EnableIPv4 | booleanEnable IPv4 on the network. |
| EnableIPv6 | booleanEnable IPv6 on the network. |
|  | objectNetwork specific options to be used by the drivers. |
|  | objectUser-defined key/value metadata. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Name": "my_network","Driver": "bridge","Scope": "string","Internal": true,"Attachable": true,"Ingress": false,"ConfigOnly": false,"ConfigFrom": {"Network": "config_only_network_01"},"IPAM": {"Driver": "default","Config": [{"Subnet": "172.20.0.0/16","IPRange": "172.20.10.0/24","Gateway": "172.20.10.11","AuxiliaryAddresses": {"property1": "string","property2": "string"}}],"Options": {"foo": "bar"}},"EnableIPv4": true,"EnableIPv6": true,"Options": {"com.docker.network.bridge.default_bridge": "true","com.docker.network.bridge.enable_icc": "true","com.docker.network.bridge.enable_ip_masquerade": "true","com.docker.network.bridge.host_binding_ipv4": "0.0.0.0","com.docker.network.bridge.name": "docker0","com.docker.network.driver.mtu": "1500"},"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"}}`

### Response samples

- 201
- 400
- 403
- 404
- 500

Content typeapplication/json`{"Id": "b5c4fc71e8022147cd25de22b22173de4e3b170134117172eb595cb91b4e7e5d","Warning": ""}`

## Connect a container to a network

The network must be either a local-scoped network or a swarm-scoped network with the `attachable` option set. A network cannot be re-attached to a running container

##### path Parameters

| idrequired | stringNetwork ID or name |
| --- | --- |

##### Request Body schema:application/jsonrequired

| Container | stringThe ID or name of the container to connect to the network. |
| --- | --- |
|  | object(EndpointSettings)Configuration for a network endpoint. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Container": "3613f73ba0e4","EndpointConfig": {"IPAMConfig": {"IPv4Address": "172.24.56.89","IPv6Address": "2001:db8::5689"},"MacAddress": "02:42:ac:12:05:02","Priority": 100}}`

### Response samples

- 400
- 403
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Disconnect a container from a network

##### path Parameters

| idrequired | stringNetwork ID or name |
| --- | --- |

##### Request Body schema:application/jsonrequired

| Container | stringThe ID or name of the container to disconnect from the network. |
| --- | --- |
| Force | booleanForce the container to disconnect from the network. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Container": "string","Force": true}`

### Response samples

- 403
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Delete unused networks

##### query Parameters

| filters | stringFilters to process on the prune list, encoded as JSON (amap[string][]string).Available filters:until=<timestamp>Prune networks created before this timestamp. The<timestamp>can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g.10m,1h30m) computed relative to the daemon machine’s time.label(label=<key>,label=<key>=<value>,label!=<key>, orlabel!=<key>=<value>) Prune networks with (or without, in caselabel!=...is used) the specified labels. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"NetworksDeleted": ["string"]}`

## Volumes

Create and manage persistent storage that can be attached to containers.

## List volumes

##### query Parameters

| filters | string<json>JSON encoded value of the filters (amap[string][]string) to
process on the volumes list. Available filters:dangling=<boolean>When set totrue(or1), returns all
 volumes that are not in use by a container. When set tofalse(or0), only volumes that are in use by one or more
 containers are returned.driver=<volume-driver-name>Matches volumes based on their driver.label=<key>orlabel=<key>:<value>Matches volumes based on
 the presence of alabelalone or alabeland a value.name=<volume-name>Matches all or part of a volume name. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"Volumes": [{"Name": "tardis","Driver": "custom","Mountpoint": "/var/lib/docker/volumes/tardis","CreatedAt": "2016-06-07T20:31:11.853781916Z","Status": {"hello": "world"},"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"Scope": "local","ClusterVolume": {"ID": "string","Version": {"Index": 373531},"CreatedAt": "string","UpdatedAt": "string","Spec": {"Group": "string","AccessMode": {"Scope": "single","Sharing": "none","MountVolume": { },"Secrets": [{"Key": "string","Secret": "string"}],"AccessibilityRequirements": {"Requisite": [{"property1": "string","property2": "string"}],"Preferred": [{"property1": "string","property2": "string"}]},"CapacityRange": {"RequiredBytes": 0,"LimitBytes": 0},"Availability": "active"}},"Info": {"CapacityBytes": 0,"VolumeContext": {"property1": "string","property2": "string"},"VolumeID": "string","AccessibleTopology": [{"property1": "string","property2": "string"}]},"PublishStatus": [{"NodeID": "string","State": "pending-publish","PublishContext": {"property1": "string","property2": "string"}}]},"Options": {"device": "tmpfs","o": "size=100m,uid=1000","type": "tmpfs"},"UsageData": {"Size": -1,"RefCount": -1}}],"Warnings": [ ]}`

## Create a volume

##### Request Body schema:application/jsonrequired

Volume configuration

| Name | stringThe new volume's name. If not specified, Docker generates a name. |
| --- | --- |
| Driver | stringDefault:"local"Name of the volume driver to use. |
|  | objectA mapping of driver options and values. These options are
passed directly to the driver and are driver specific. |
|  | objectUser-defined key/value metadata. |
|  | object(ClusterVolumeSpec)Cluster-specific options used to create the volume. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Name": "tardis","Driver": "custom","DriverOpts": {"device": "tmpfs","o": "size=100m,uid=1000","type": "tmpfs"},"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"ClusterVolumeSpec": {"Group": "string","AccessMode": {"Scope": "single","Sharing": "none","MountVolume": { },"Secrets": [{"Key": "string","Secret": "string"}],"AccessibilityRequirements": {"Requisite": [{"property1": "string","property2": "string"}],"Preferred": [{"property1": "string","property2": "string"}]},"CapacityRange": {"RequiredBytes": 0,"LimitBytes": 0},"Availability": "active"}}}`

### Response samples

- 201
- 500

Content typeapplication/json`{"Name": "tardis","Driver": "custom","Mountpoint": "/var/lib/docker/volumes/tardis","CreatedAt": "2016-06-07T20:31:11.853781916Z","Status": {"hello": "world"},"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"Scope": "local","ClusterVolume": {"ID": "string","Version": {"Index": 373531},"CreatedAt": "string","UpdatedAt": "string","Spec": {"Group": "string","AccessMode": {"Scope": "single","Sharing": "none","MountVolume": { },"Secrets": [{"Key": "string","Secret": "string"}],"AccessibilityRequirements": {"Requisite": [{"property1": "string","property2": "string"}],"Preferred": [{"property1": "string","property2": "string"}]},"CapacityRange": {"RequiredBytes": 0,"LimitBytes": 0},"Availability": "active"}},"Info": {"CapacityBytes": 0,"VolumeContext": {"property1": "string","property2": "string"},"VolumeID": "string","AccessibleTopology": [{"property1": "string","property2": "string"}]},"PublishStatus": [{"NodeID": "string","State": "pending-publish","PublishContext": {"property1": "string","property2": "string"}}]},"Options": {"device": "tmpfs","o": "size=100m,uid=1000","type": "tmpfs"},"UsageData": {"Size": -1,"RefCount": -1}}`

## Inspect a volume

##### path Parameters

| namerequired | stringVolume name or ID |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"Name": "tardis","Driver": "custom","Mountpoint": "/var/lib/docker/volumes/tardis","CreatedAt": "2016-06-07T20:31:11.853781916Z","Status": {"hello": "world"},"Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"Scope": "local","ClusterVolume": {"ID": "string","Version": {"Index": 373531},"CreatedAt": "string","UpdatedAt": "string","Spec": {"Group": "string","AccessMode": {"Scope": "single","Sharing": "none","MountVolume": { },"Secrets": [{"Key": "string","Secret": "string"}],"AccessibilityRequirements": {"Requisite": [{"property1": "string","property2": "string"}],"Preferred": [{"property1": "string","property2": "string"}]},"CapacityRange": {"RequiredBytes": 0,"LimitBytes": 0},"Availability": "active"}},"Info": {"CapacityBytes": 0,"VolumeContext": {"property1": "string","property2": "string"},"VolumeID": "string","AccessibleTopology": [{"property1": "string","property2": "string"}]},"PublishStatus": [{"NodeID": "string","State": "pending-publish","PublishContext": {"property1": "string","property2": "string"}}]},"Options": {"device": "tmpfs","o": "size=100m,uid=1000","type": "tmpfs"},"UsageData": {"Size": -1,"RefCount": -1}}`

## "Update a volume. Valid only for Swarm cluster volumes"

##### path Parameters

| namerequired | stringThe name or ID of the volume |
| --- | --- |

##### query Parameters

| versionrequired | integer<int64>The version number of the volume being updated. This is required to
avoid conflicting writes. Found in the volume'sClusterVolumefield. |
| --- | --- |

##### Request Body schema:application/json

The spec of the volume to update. Currently, only Availability may
change. All other fields must remain unchanged.

|  | object(ClusterVolumeSpec)Cluster-specific options used to create the volume. |
| --- | --- |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Spec": {"Group": "string","AccessMode": {"Scope": "single","Sharing": "none","MountVolume": { },"Secrets": [{"Key": "string","Secret": "string"}],"AccessibilityRequirements": {"Requisite": [{"property1": "string","property2": "string"}],"Preferred": [{"property1": "string","property2": "string"}]},"CapacityRange": {"RequiredBytes": 0,"LimitBytes": 0},"Availability": "active"}}}`

### Response samples

- 400
- 404
- 500
- 503

Content typeapplication/json`{"message": "Something went wrong."}`

## Remove a volume

Instruct the driver to remove the volume.

##### path Parameters

| namerequired | stringVolume name or ID |
| --- | --- |

##### query Parameters

| force | booleanDefault:falseForce the removal of the volume |
| --- | --- |

### Responses

### Response samples

- 404
- 409
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Delete unused volumes

##### query Parameters

| filters | stringFilters to process on the prune list, encoded as JSON (amap[string][]string).Available filters:label(label=<key>,label=<key>=<value>,label!=<key>, orlabel!=<key>=<value>) Prune volumes with (or without, in caselabel!=...is used) the specified labels.all(all=true) - Consider all (local) volumes for pruning and not just anonymous volumes. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"VolumesDeleted": ["string"],"SpaceReclaimed": 0}`

## Exec

Run new commands inside running containers. Refer to the
[command-line reference](https://docs.docker.com/engine/reference/commandline/exec/)
for more information.

To exec a command in a container, you first need to create an exec instance,
then start it. These two API endpoints are wrapped up in a single command-line
command, `docker exec`.

## Create an exec instance

Run a command inside a running container.

##### path Parameters

| idrequired | stringID or name of container |
| --- | --- |

##### Request Body schema:application/jsonrequired

Exec configuration

| AttachStdin | booleanAttach tostdinof the exec command. |
| --- | --- |
| AttachStdout | booleanAttach tostdoutof the exec command. |
| AttachStderr | booleanAttach tostderrof the exec command. |
| ConsoleSize | Array ofintegers or null= 2 items[ items>= 0]Initial console size, as an[height, width]array. |
| DetachKeys | stringOverride the key sequence for detaching a container. Format is
a single character[a-Z]orctrl-<value>where<value>is one of:a-z,@,^,[,,or_. |
| Tty | booleanAllocate a pseudo-TTY. |
| Env | Array ofstringsA list of environment variables in the form["VAR=value", ...]. |
| Cmd | Array ofstringsCommand to run, as a string or array of strings. |
| Privileged | booleanDefault:falseRuns the exec process with extended privileges. |
| User | stringThe user, and optionally, group to run the exec process inside
the container. Format is one of:user,user:group,uid,
oruid:gid. |
| WorkingDir | stringThe working directory for the exec process inside the container. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"AttachStdin": false,"AttachStdout": true,"AttachStderr": true,"DetachKeys": "ctrl-p,ctrl-q","Tty": false,"Cmd": ["date"],"Env": ["FOO=bar","BAZ=quux"]}`

### Response samples

- 201
- 404
- 409
- 500

Content typeapplication/json`{"Id": "string"}`

## Start an exec instance

Starts a previously set up exec instance. If detach is true, this endpoint
returns immediately after starting the command. Otherwise, it sets up an
interactive session with the command.

##### path Parameters

| idrequired | stringExec instance ID |
| --- | --- |

##### Request Body schema:application/json

| Detach | booleanDetach from the command. |
| --- | --- |
| Tty | booleanAllocate a pseudo-TTY. |
| ConsoleSize | Array ofintegers or null= 2 items[ items>= 0]Initial console size, as an[height, width]array. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Detach": false,"Tty": true,"ConsoleSize": [80,64]}`

## Resize an exec instance

Resize the TTY session used by an exec instance. This endpoint only works
if `tty` was specified as part of creating and starting the exec instance.

##### path Parameters

| idrequired | stringExec instance ID |
| --- | --- |

##### query Parameters

| hrequired | integerHeight of the TTY session in characters |
| --- | --- |
| wrequired | integerWidth of the TTY session in characters |

### Responses

### Response samples

- 400
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Inspect an exec instance

Return low-level information about an exec instance.

##### path Parameters

| idrequired | stringExec instance ID |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/json`{"CanRemove": false,"ContainerID": "b53ee82b53a40c7dca428523e34f741f3abc51d9f297a14ff874bf761b995126","DetachKeys": "","ExitCode": 2,"ID": "f33bbfb39f5b142420f4759b2348913bd4a8d1a6d7fd56499cb41a1bb91d7b3b","OpenStderr": true,"OpenStdin": true,"OpenStdout": true,"ProcessConfig": {"arguments": ["-c","exit 2"],"entrypoint": "sh","privileged": false,"tty": true,"user": "1000"},"Running": false,"Pid": 42000}`

## Swarm

Engines can be clustered together in a swarm. Refer to the
[swarm mode documentation](https://docs.docker.com/engine/swarm/)
for more information.

## Inspect swarm

### Responses

### Response samples

- 200
- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"ID": "abajmipo7b4xz5ip2nrla6b11","Version": {"Index": 373531},"CreatedAt": "2016-08-18T10:44:24.496525531Z","UpdatedAt": "2017-08-09T07:09:37.632105588Z","Spec": {"Name": "default","Labels": {"com.example.corp.type": "production","com.example.corp.department": "engineering"},"Orchestration": {"TaskHistoryRetentionLimit": 10},"Raft": {"SnapshotInterval": 10000,"KeepOldSnapshots": 0,"LogEntriesForSlowFollowers": 500,"ElectionTick": 3,"HeartbeatTick": 1},"Dispatcher": {"HeartbeatPeriod": 5000000000},"CAConfig": {"NodeCertExpiry": 7776000000000000,"ExternalCAs": [{"Protocol": "cfssl","URL": "string","Options": {"property1": "string","property2": "string"},"CACert": "string"}],"SigningCACert": "string","SigningCAKey": "string","ForceRotate": 0},"EncryptionConfig": {"AutoLockManagers": false},"TaskDefaults": {"LogDriver": {"Name": "json-file","Options": {"max-file": "10","max-size": "100m"}}}},"TLSInfo": {"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n","CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh","CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="},"RootRotationInProgress": false,"DataPathPort": 4789,"DefaultAddrPool": [["10.10.0.0/16","20.20.0.0/16"]],"SubnetSize": 24,"JoinTokens": {"Worker": "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx","Manager": "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2"}}`

## Initialize a new swarm

##### Request Body schema:application/jsontext/plainapplication/jsonrequired

| ListenAddr | stringListen address used for inter-manager communication, as well
as determining the networking interface used for the VXLAN
Tunnel Endpoint (VTEP). This can either be an address/port
combination in the form192.168.1.1:4567, or an interface
followed by a port number, likeeth0:4567. If the port number
is omitted, the default swarm listening port is used. |
| --- | --- |
| AdvertiseAddr | stringExternally reachable address advertised to other nodes. This
can either be an address/port combination in the form192.168.1.1:4567, or an interface followed by a port number,
likeeth0:4567. If the port number is omitted, the port
number from the listen address is used. IfAdvertiseAddris
not specified, it will be automatically detected when possible. |
| DataPathAddr | stringAddress or interface to use for data path traffic (format:<ip|interface>), for example,192.168.1.1, or an interface,
likeeth0. IfDataPathAddris unspecified, the same address
asAdvertiseAddris used.TheDataPathAddrspecifies the address that global scope
network drivers will publish towards other  nodes in order to
reach the containers running on this node. Using this parameter
it is possible to separate the container data traffic from the
management traffic of the cluster. |
| DataPathPort | integer<uint32>DataPathPort specifies the data path port number for data traffic.
Acceptable port range is 1024 to 49151.
if no port is set or is set to 0, default port 4789 will be used. |
| DefaultAddrPool | Array ofstringsDefault Address Pool specifies default subnet pools for global
scope networks. |
| ForceNewCluster | booleanForce creation of a new swarm. |
| SubnetSize | integer<uint32>SubnetSize specifies the subnet size of the networks created
from the default subnet pool. |
|  | object(SwarmSpec)User modifiable swarm configuration. |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`{"ListenAddr": "0.0.0.0:2377","AdvertiseAddr": "192.168.1.1:2377","DataPathPort": 4789,"DefaultAddrPool": ["10.10.0.0/8","20.20.0.0/8"],"SubnetSize": 24,"ForceNewCluster": false,"Spec": {"Orchestration": { },"Raft": { },"Dispatcher": { },"CAConfig": { },"EncryptionConfig": {"AutoLockManagers": false}}}`

### Response samples

- 200
- 400
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`"7v2t30z9blmxuhnyo6s4cpenp"`

## Join an existing swarm

##### Request Body schema:application/jsontext/plainapplication/jsonrequired

| ListenAddr | stringListen address used for inter-manager communication if the node
gets promoted to manager, as well as determining the networking
interface used for the VXLAN Tunnel Endpoint (VTEP). |
| --- | --- |
| AdvertiseAddr | stringExternally reachable address advertised to other nodes. This
can either be an address/port combination in the form192.168.1.1:4567, or an interface followed by a port number,
likeeth0:4567. If the port number is omitted, the port
number from the listen address is used. IfAdvertiseAddris
not specified, it will be automatically detected when possible. |
| DataPathAddr | stringAddress or interface to use for data path traffic (format:<ip|interface>), for example,192.168.1.1, or an interface,
likeeth0. IfDataPathAddris unspecified, the same address
asAdvertiseAddris used.TheDataPathAddrspecifies the address that global scope
network drivers will publish towards other nodes in order to
reach the containers running on this node. Using this parameter
it is possible to separate the container data traffic from the
management traffic of the cluster. |
| RemoteAddrs | Array ofstringsAddresses of manager nodes already participating in the swarm. |
| JoinToken | stringSecret token for joining this swarm. |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`{"ListenAddr": "0.0.0.0:2377","AdvertiseAddr": "192.168.1.1:2377","DataPathAddr": "192.168.1.1","RemoteAddrs": ["node1:2377"],"JoinToken": "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2"}`

### Response samples

- 400
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Leave a swarm

##### query Parameters

| force | booleanDefault:falseForce leave swarm, even if this is the last manager or that it will
break the cluster. |
| --- | --- |

### Responses

### Response samples

- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Update a swarm

##### query Parameters

| versionrequired | integer<int64>The version number of the swarm object being updated. This is
required to avoid conflicting writes. |
| --- | --- |
| rotateWorkerToken | booleanDefault:falseRotate the worker join token. |
| rotateManagerToken | booleanDefault:falseRotate the manager join token. |
| rotateManagerUnlockKey | booleanDefault:falseRotate the manager unlock key. |

##### Request Body schema:application/jsontext/plainapplication/jsonrequired

| Name | stringName of the swarm. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
|  | object or nullOrchestration configuration. |
|  | objectRaft configuration. |
|  | object or nullDispatcher configuration. |
|  | object or nullCA configuration. |
|  | objectParameters related to encryption-at-rest. |
|  | objectDefaults for creating tasks in this cluster. |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`{"Name": "default","Labels": {"com.example.corp.type": "production","com.example.corp.department": "engineering"},"Orchestration": {"TaskHistoryRetentionLimit": 10},"Raft": {"SnapshotInterval": 10000,"KeepOldSnapshots": 0,"LogEntriesForSlowFollowers": 500,"ElectionTick": 3,"HeartbeatTick": 1},"Dispatcher": {"HeartbeatPeriod": 5000000000},"CAConfig": {"NodeCertExpiry": 7776000000000000,"ExternalCAs": [{"Protocol": "cfssl","URL": "string","Options": {"property1": "string","property2": "string"},"CACert": "string"}],"SigningCACert": "string","SigningCAKey": "string","ForceRotate": 0},"EncryptionConfig": {"AutoLockManagers": false},"TaskDefaults": {"LogDriver": {"Name": "json-file","Options": {"max-file": "10","max-size": "100m"}}}}`

### Response samples

- 400
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Get the unlock key

### Responses

### Response samples

- 200
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"UnlockKey": "SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8"}`

## Unlock a locked manager

##### Request Body schema:application/jsonrequired

| UnlockKey | stringThe swarm's unlock key. |
| --- | --- |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"UnlockKey": "SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8"}`

### Response samples

- 500
- 503

Content typeapplication/json`{"message": "Something went wrong."}`

## Nodes

Nodes are instances of the Engine participating in a swarm. Swarm mode
must be enabled for these endpoints to work.

## List nodes

##### query Parameters

| filters | stringFilters to process on the nodes list, encoded as JSON (amap[string][]string).Available filters:id=<node id>label=<engine label>membership=(accepted|pending)`name=<node name>node.label=<node label>role=(manager|worker)` |
| --- | --- |

### Responses

### Response samples

- 200
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`[{"ID": "24ifsmvkjbyhk","Version": {"Index": 373531},"CreatedAt": "2016-08-18T10:44:24.496525531Z","UpdatedAt": "2017-08-09T07:09:37.632105588Z","Spec": {"Availability": "active","Name": "node-name","Role": "manager","Labels": {"foo": "bar"}},"Description": {"Hostname": "bf3067039e47","Platform": {"Architecture": "x86_64","OS": "linux"},"Resources": {"NanoCPUs": 4000000000,"MemoryBytes": 8272408576,"GenericResources": [{"DiscreteResourceSpec": {"Kind": "SSD","Value": 3}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID1"}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID2"}}]},"Engine": {"EngineVersion": "17.06.0","Labels": {"foo": "bar"},"Plugins": [{"Type": "Log","Name": "awslogs"},{"Type": "Log","Name": "fluentd"},{"Type": "Log","Name": "gcplogs"},{"Type": "Log","Name": "gelf"},{"Type": "Log","Name": "journald"},{"Type": "Log","Name": "json-file"},{"Type": "Log","Name": "splunk"},{"Type": "Log","Name": "syslog"},{"Type": "Network","Name": "bridge"},{"Type": "Network","Name": "host"},{"Type": "Network","Name": "ipvlan"},{"Type": "Network","Name": "macvlan"},{"Type": "Network","Name": "null"},{"Type": "Network","Name": "overlay"},{"Type": "Volume","Name": "local"},{"Type": "Volume","Name": "localhost:5000/vieux/sshfs:latest"},{"Type": "Volume","Name": "vieux/sshfs:latest"}]},"TLSInfo": {"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n","CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh","CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="}},"Status": {"State": "ready","Message": "","Addr": "172.17.0.2"},"ManagerStatus": {"Leader": true,"Reachability": "reachable","Addr": "10.0.0.46:2377"}}]`

## Inspect a node

##### path Parameters

| idrequired | stringThe ID or name of the node |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"ID": "24ifsmvkjbyhk","Version": {"Index": 373531},"CreatedAt": "2016-08-18T10:44:24.496525531Z","UpdatedAt": "2017-08-09T07:09:37.632105588Z","Spec": {"Availability": "active","Name": "node-name","Role": "manager","Labels": {"foo": "bar"}},"Description": {"Hostname": "bf3067039e47","Platform": {"Architecture": "x86_64","OS": "linux"},"Resources": {"NanoCPUs": 4000000000,"MemoryBytes": 8272408576,"GenericResources": [{"DiscreteResourceSpec": {"Kind": "SSD","Value": 3}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID1"}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID2"}}]},"Engine": {"EngineVersion": "17.06.0","Labels": {"foo": "bar"},"Plugins": [{"Type": "Log","Name": "awslogs"},{"Type": "Log","Name": "fluentd"},{"Type": "Log","Name": "gcplogs"},{"Type": "Log","Name": "gelf"},{"Type": "Log","Name": "journald"},{"Type": "Log","Name": "json-file"},{"Type": "Log","Name": "splunk"},{"Type": "Log","Name": "syslog"},{"Type": "Network","Name": "bridge"},{"Type": "Network","Name": "host"},{"Type": "Network","Name": "ipvlan"},{"Type": "Network","Name": "macvlan"},{"Type": "Network","Name": "null"},{"Type": "Network","Name": "overlay"},{"Type": "Volume","Name": "local"},{"Type": "Volume","Name": "localhost:5000/vieux/sshfs:latest"},{"Type": "Volume","Name": "vieux/sshfs:latest"}]},"TLSInfo": {"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n","CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh","CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="}},"Status": {"State": "ready","Message": "","Addr": "172.17.0.2"},"ManagerStatus": {"Leader": true,"Reachability": "reachable","Addr": "10.0.0.46:2377"}}`

## Delete a node

##### path Parameters

| idrequired | stringThe ID or name of the node |
| --- | --- |

##### query Parameters

| force | booleanDefault:falseForce remove a node from the swarm |
| --- | --- |

### Responses

### Response samples

- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Update a node

##### path Parameters

| idrequired | stringThe ID of the node |
| --- | --- |

##### query Parameters

| versionrequired | integer<int64>The version number of the node object being updated. This is required
to avoid conflicting writes. |
| --- | --- |

##### Request Body schema:application/jsontext/plainapplication/json

| Name | stringName for the node. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
| Role | stringEnum:"worker""manager"Role of the node. |
| Availability | stringEnum:"active""pause""drain"Availability of the node. |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`{"Availability": "active","Name": "node-name","Role": "manager","Labels": {"foo": "bar"}}`

### Response samples

- 400
- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Services

Services are the definitions of tasks to run on a swarm. Swarm mode must
be enabled for these endpoints to work.

## List services

##### query Parameters

| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the services list.Available filters:id=<service id>label=<service label>mode=["replicated"|"global"]name=<service name> |
| --- | --- |
| status | booleanInclude service status, with count of running and desired tasks. |

### Responses

### Response samples

- 200
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`[{"ID": "9mnpnzenvg8p8tdbtq4wvbkcz","Version": {"Index": 19},"CreatedAt": "2016-06-07T21:05:51.880065305Z","UpdatedAt": "2016-06-07T21:07:29.962229872Z","Spec": {"Name": "hopeful_cori","TaskTemplate": {"ContainerSpec": {"Image": "redis"},"Resources": {"Limits": { },"Reservations": { }},"RestartPolicy": {"Condition": "any","MaxAttempts": 0},"Placement": { },"ForceUpdate": 0},"Mode": {"Replicated": {"Replicas": 1}},"UpdateConfig": {"Parallelism": 1,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15},"RollbackConfig": {"Parallelism": 1,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15},"EndpointSpec": {"Mode": "vip","Ports": [{"Protocol": "tcp","TargetPort": 6379,"PublishedPort": 30001}]}},"Endpoint": {"Spec": {"Mode": "vip","Ports": [{"Protocol": "tcp","TargetPort": 6379,"PublishedPort": 30001}]},"Ports": [{"Protocol": "tcp","TargetPort": 6379,"PublishedPort": 30001}],"VirtualIPs": [{"NetworkID": "4qvuz4ko70xaltuqbt8956gd1","Addr": "10.255.0.2/16"},{"NetworkID": "4qvuz4ko70xaltuqbt8956gd1","Addr": "10.255.0.3/16"}]}}]`

## Create a service

##### header Parameters

| X-Registry-Auth | stringA base64url-encoded auth configuration for pulling from private
registries.Refer to theauthentication sectionfor
details. |
| --- | --- |

##### Request Body schema:application/jsonrequired

| Name | stringName of the service. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
|  | object(TaskSpec)User modifiable task configuration. |
|  | objectScheduling mode for the service. |
|  | objectSpecification for the update strategy of the service. |
|  | objectSpecification for the rollback strategy of the service. |
|  | Array ofobjects(NetworkAttachmentConfig)Specifies which networks the service should attach to.Deprecated: This field is deprecated since v1.44. The Networks field in TaskSpec should be used instead. |
|  | object(EndpointSpec)Properties that can be configured to access and load balance a service. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Name": "web","Labels": {"property1": "string","property2": "string","foo": "bar"},"TaskTemplate": {"PluginSpec": {"Name": "string","Remote": "string","Disabled": true,"PluginPrivilege": [{"Name": "network","Description": "string","Value": ["host"]}]},"ContainerSpec": {"Image": "nginx:alpine","Labels": {"property1": "string","property2": "string"},"Command": ["string"],"Args": ["string"],"Hostname": "string","Env": ["string"],"Dir": "string","User": "33","Groups": ["string"],"Privileges": {"CredentialSpec": {"Config": "0bt9dmxjvjiqermk6xrop3ekq","File": "spec.json","Registry": "string"},"SELinuxContext": {"Disable": true,"User": "string","Role": "string","Type": "string","Level": "string"},"Seccomp": {"Mode": "default","Profile": "string"},"AppArmor": {"Mode": "default"},"NoNewPrivileges": true},"TTY": true,"OpenStdin": true,"ReadOnly": true,"Mounts": [{"Target": "/usr/share/nginx/html","Source": "web-data","Type": "volume","ReadOnly": true,"Consistency": "string","BindOptions": {"Propagation": "private","NonRecursive": false,"CreateMountpoint": false,"ReadOnlyNonRecursive": false,"ReadOnlyForceRecursive": false},"VolumeOptions": {"NoCopy": false,"Labels": {"property1": "string","property2": "string","com.example.something": "something-value"},"DriverConfig": {"Name": "string","Options": {"property1": "string","property2": "string"}},"Subpath": "dir-inside-volume/subdirectory"},"ImageOptions": {"Subpath": "dir-inside-image/subdirectory"},"TmpfsOptions": {"SizeBytes": 0,"Mode": 0,"Options": [["noexec"]]}}],"StopSignal": "string","StopGracePeriod": 0,"HealthCheck": {"Test": ["string"],"Interval": 0,"Timeout": 0,"Retries": 0,"StartPeriod": 0,"StartInterval": 0},"Hosts": ["10.10.10.10 host1","ABCD:EF01:2345:6789:ABCD:EF01:2345:6789 host2"],"DNSConfig": {"Nameservers": ["8.8.8.8"],"Search": ["example.org"],"Options": ["timeout:3"]},"Secrets": [{"File": {"Name": "www.example.org.key","UID": "33","GID": "33","Mode": 384},"SecretID": "fpjqlhnwb19zds35k8wn80lq9","SecretName": "example_org_domain_key"}],"OomScoreAdj": 0,"Configs": [{"File": {"Name": "string","UID": "string","GID": "string","Mode": 0},"Runtime": { },"ConfigID": "string","ConfigName": "string"}],"Isolation": "default","Init": true,"Sysctls": {"property1": "string","property2": "string"},"CapabilityAdd": ["CAP_NET_RAW","CAP_SYS_ADMIN","CAP_SYS_CHROOT","CAP_SYSLOG"],"CapabilityDrop": ["CAP_NET_RAW"],"Ulimits": [{"Name": "string","Soft": 0,"Hard": 0}]},"NetworkAttachmentSpec": {"ContainerID": "string"},"Resources": {"Limits": {"NanoCPUs": 4000000000,"MemoryBytes": 104857600,"Pids": 100},"Reservations": {"NanoCPUs": 4000000000,"MemoryBytes": 8272408576,"GenericResources": [{"DiscreteResourceSpec": {"Kind": "SSD","Value": 3}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID1"}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID2"}}]}},"RestartPolicy": {"Condition": "on-failure","Delay": 10000000000,"MaxAttempts": 10,"Window": 0},"Placement": {"Constraints": ["node.hostname!=node3.corp.example.com","node.role!=manager","node.labels.type==production","node.platform.os==linux","node.platform.arch==x86_64"],"Preferences": [{"Spread": {"SpreadDescriptor": "node.labels.datacenter"}},{"Spread": {"SpreadDescriptor": "node.labels.rack"}}],"MaxReplicas": 0,"Platforms": [{"Architecture": "x86_64","OS": "linux"}]},"ForceUpdate": 0,"Runtime": "string","Networks": [{"Target": "string","Aliases": ["string"],"DriverOpts": {"property1": "string","property2": "string"}}],"LogDriver": {"Name": "json-file","Options": {"property1": "string","property2": "string","max-file": "3","max-size": "10M"}}},"Mode": {"Replicated": {"Replicas": 4},"Global": { },"ReplicatedJob": {"MaxConcurrent": 1,"TotalCompletions": 0},"GlobalJob": { }},"UpdateConfig": {"Parallelism": 2,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15,"Order": "stop-first"},"RollbackConfig": {"Parallelism": 1,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15,"Order": "stop-first"},"Networks": [{"Target": "string","Aliases": ["string"],"DriverOpts": {"property1": "string","property2": "string"}}],"EndpointSpec": {"Mode": "vip","Ports": [{"Name": "string","Protocol": "tcp","TargetPort": 80,"PublishedPort": 8080,"PublishMode": "ingress"}]}}`

### Response samples

- 201
- 400
- 403
- 409
- 500
- 503

Content typeapplication/json`{"ID": "ak7w3gjqoa3kuz8xcpnyy0pvl","Warnings": ["unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"]}`

## Inspect a service

##### path Parameters

| idrequired | stringID or name of service. |
| --- | --- |

##### query Parameters

| insertDefaults | booleanDefault:falseFill empty fields with default values. |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"ID": "9mnpnzenvg8p8tdbtq4wvbkcz","Version": {"Index": 19},"CreatedAt": "2016-06-07T21:05:51.880065305Z","UpdatedAt": "2016-06-07T21:07:29.962229872Z","Spec": {"Name": "hopeful_cori","TaskTemplate": {"ContainerSpec": {"Image": "redis"},"Resources": {"Limits": { },"Reservations": { }},"RestartPolicy": {"Condition": "any","MaxAttempts": 0},"Placement": { },"ForceUpdate": 0},"Mode": {"Replicated": {"Replicas": 1}},"UpdateConfig": {"Parallelism": 1,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15},"RollbackConfig": {"Parallelism": 1,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15},"EndpointSpec": {"Mode": "vip","Ports": [{"Protocol": "tcp","TargetPort": 6379,"PublishedPort": 30001}]}},"Endpoint": {"Spec": {"Mode": "vip","Ports": [{"Protocol": "tcp","TargetPort": 6379,"PublishedPort": 30001}]},"Ports": [{"Protocol": "tcp","TargetPort": 6379,"PublishedPort": 30001}],"VirtualIPs": [{"NetworkID": "4qvuz4ko70xaltuqbt8956gd1","Addr": "10.255.0.2/16"},{"NetworkID": "4qvuz4ko70xaltuqbt8956gd1","Addr": "10.255.0.3/16"}]}}`

## Delete a service

##### path Parameters

| idrequired | stringID or name of service. |
| --- | --- |

### Responses

### Response samples

- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Update a service

##### path Parameters

| idrequired | stringID or name of service. |
| --- | --- |

##### query Parameters

| versionrequired | integerThe version number of the service object being updated. This is
required to avoid conflicting writes.
This version number should be the value as currently set on the
servicebeforethe update. You can find the current version by
callingGET /services/{id} |
| --- | --- |
| registryAuthFrom | stringDefault:"spec"Enum:"spec""previous-spec"If theX-Registry-Authheader is not specified, this parameter
indicates where to find registry authorization credentials. |
| rollback | stringSet to this parameter topreviousto cause a server-side rollback
to the previous service spec. The supplied spec will be ignored in
this case. |

##### header Parameters

| X-Registry-Auth | stringA base64url-encoded auth configuration for pulling from private
registries.Refer to theauthentication sectionfor
details. |
| --- | --- |

##### Request Body schema:application/jsonrequired

| Name | stringName of the service. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
|  | object(TaskSpec)User modifiable task configuration. |
|  | objectScheduling mode for the service. |
|  | objectSpecification for the update strategy of the service. |
|  | objectSpecification for the rollback strategy of the service. |
|  | Array ofobjects(NetworkAttachmentConfig)Specifies which networks the service should attach to.Deprecated: This field is deprecated since v1.44. The Networks field in TaskSpec should be used instead. |
|  | object(EndpointSpec)Properties that can be configured to access and load balance a service. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Name": "top","Labels": {"property1": "string","property2": "string"},"TaskTemplate": {"PluginSpec": {"Name": "string","Remote": "string","Disabled": true,"PluginPrivilege": [{"Name": "network","Description": "string","Value": ["host"]}]},"ContainerSpec": {"Image": "busybox","Labels": {"property1": "string","property2": "string"},"Command": ["string"],"Args": ["top"],"Hostname": "string","Env": ["string"],"Dir": "string","User": "string","Groups": ["string"],"Privileges": {"CredentialSpec": {"Config": "0bt9dmxjvjiqermk6xrop3ekq","File": "spec.json","Registry": "string"},"SELinuxContext": {"Disable": true,"User": "string","Role": "string","Type": "string","Level": "string"},"Seccomp": {"Mode": "default","Profile": "string"},"AppArmor": {"Mode": "default"},"NoNewPrivileges": true},"TTY": true,"OpenStdin": true,"ReadOnly": true,"Mounts": [{"Target": "string","Source": "string","Type": "volume","ReadOnly": true,"Consistency": "string","BindOptions": {"Propagation": "private","NonRecursive": false,"CreateMountpoint": false,"ReadOnlyNonRecursive": false,"ReadOnlyForceRecursive": false},"VolumeOptions": {"NoCopy": false,"Labels": {"property1": "string","property2": "string"},"DriverConfig": {"Name": "string","Options": {"property1": "string","property2": "string"}},"Subpath": "dir-inside-volume/subdirectory"},"ImageOptions": {"Subpath": "dir-inside-image/subdirectory"},"TmpfsOptions": {"SizeBytes": 0,"Mode": 0,"Options": [["noexec"]]}}],"StopSignal": "string","StopGracePeriod": 0,"HealthCheck": {"Test": ["string"],"Interval": 0,"Timeout": 0,"Retries": 0,"StartPeriod": 0,"StartInterval": 0},"Hosts": ["string"],"DNSConfig": {"Nameservers": ["string"],"Search": ["string"],"Options": ["string"]},"Secrets": [{"File": {"Name": "string","UID": "string","GID": "string","Mode": 0},"SecretID": "string","SecretName": "string"}],"OomScoreAdj": 0,"Configs": [{"File": {"Name": "string","UID": "string","GID": "string","Mode": 0},"Runtime": { },"ConfigID": "string","ConfigName": "string"}],"Isolation": "default","Init": true,"Sysctls": {"property1": "string","property2": "string"},"CapabilityAdd": ["CAP_NET_RAW","CAP_SYS_ADMIN","CAP_SYS_CHROOT","CAP_SYSLOG"],"CapabilityDrop": ["CAP_NET_RAW"],"Ulimits": [{"Name": "string","Soft": 0,"Hard": 0}]},"NetworkAttachmentSpec": {"ContainerID": "string"},"Resources": {"Limits": {"NanoCPUs": 4000000000,"MemoryBytes": 8272408576,"Pids": 100},"Reservations": {"NanoCPUs": 4000000000,"MemoryBytes": 8272408576,"GenericResources": [{"DiscreteResourceSpec": {"Kind": "SSD","Value": 3}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID1"}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID2"}}]}},"RestartPolicy": {"Condition": "any","Delay": 0,"MaxAttempts": 0,"Window": 0},"Placement": {"Constraints": ["node.hostname!=node3.corp.example.com","node.role!=manager","node.labels.type==production","node.platform.os==linux","node.platform.arch==x86_64"],"Preferences": [{"Spread": {"SpreadDescriptor": "node.labels.datacenter"}},{"Spread": {"SpreadDescriptor": "node.labels.rack"}}],"MaxReplicas": 0,"Platforms": [{"Architecture": "x86_64","OS": "linux"}]},"ForceUpdate": 0,"Runtime": "string","Networks": [{"Target": "string","Aliases": ["string"],"DriverOpts": {"property1": "string","property2": "string"}}],"LogDriver": {"Name": "string","Options": {"property1": "string","property2": "string"}}},"Mode": {"Replicated": {"Replicas": 1},"Global": { },"ReplicatedJob": {"MaxConcurrent": 1,"TotalCompletions": 0},"GlobalJob": { }},"UpdateConfig": {"Parallelism": 2,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15,"Order": "stop-first"},"RollbackConfig": {"Parallelism": 1,"Delay": 1000000000,"FailureAction": "pause","Monitor": 15000000000,"MaxFailureRatio": 0.15,"Order": "stop-first"},"Networks": [{"Target": "string","Aliases": ["string"],"DriverOpts": {"property1": "string","property2": "string"}}],"EndpointSpec": {"Mode": "vip","Ports": [{"Name": "string","Protocol": "tcp","TargetPort": 0,"PublishedPort": 0,"PublishMode": "ingress"}]}}`

### Response samples

- 200
- 400
- 404
- 500
- 503

Content typeapplication/json`{"Warnings": ["unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"]}`

## Get service logs

Get `stdout` and `stderr` logs from a service. See also
[/containers/{id}/logs](#operation/ContainerLogs).

**Note**: This endpoint works only for services with the `local`,
`json-file` or `journald` logging drivers.

##### path Parameters

| idrequired | stringID or name of the service |
| --- | --- |

##### query Parameters

| details | booleanDefault:falseShow service context and extra details provided to logs. |
| --- | --- |
| follow | booleanDefault:falseKeep connection after returning logs. |
| stdout | booleanDefault:falseReturn logs fromstdout |
| stderr | booleanDefault:falseReturn logs fromstderr |
| since | integerDefault:0Only return logs since this time, as a UNIX timestamp |
| timestamps | booleanDefault:falseAdd timestamps to every log line |
| tail | stringDefault:"all"Only return this number of log lines from the end of the logs.
Specify as an integer orallto output all log lines. |

### Responses

### Response samples

- 404

Content typeapplication/vnd.docker.raw-streamapplication/vnd.docker.multiplexed-streamapplication/jsonapplication/vnd.docker.raw-streamNo sample

## Tasks

A task is a container running on a swarm. It is the atomic scheduling unit
of swarm. Swarm mode must be enabled for these endpoints to work.

## List tasks

##### query Parameters

| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the tasks list.Available filters:desired-state=(running | shutdown | accepted)id=<task id>label=keyorlabel="key=value"name=<task name>node=<node id or name>service=<service name> |
| --- | --- |

### Responses

### Response samples

- 200
- 500
- 503

Content typeapplication/json`[{"ID": "0kzzo1i0y4jz6027t0k7aezc7","Version": {"Index": 71},"CreatedAt": "2016-06-07T21:07:31.171892745Z","UpdatedAt": "2016-06-07T21:07:31.376370513Z","Spec": {"ContainerSpec": {"Image": "redis"},"Resources": {"Limits": { },"Reservations": { }},"RestartPolicy": {"Condition": "any","MaxAttempts": 0},"Placement": { }},"ServiceID": "9mnpnzenvg8p8tdbtq4wvbkcz","Slot": 1,"NodeID": "60gvrl6tm78dmak4yl7srz94v","Status": {"Timestamp": "2016-06-07T21:07:31.290032978Z","State": "running","Message": "started","ContainerStatus": {"ContainerID": "e5d62702a1b48d01c3e02ca1e0212a250801fa8d67caca0b6f35919ebc12f035","PID": 677}},"DesiredState": "running","NetworksAttachments": [{"Network": {"ID": "4qvuz4ko70xaltuqbt8956gd1","Version": {"Index": 18},"CreatedAt": "2016-06-07T20:31:11.912919752Z","UpdatedAt": "2016-06-07T21:07:29.955277358Z","Spec": {"Name": "ingress","Labels": {"com.docker.swarm.internal": "true"},"DriverConfiguration": { },"IPAMOptions": {"Driver": { },"Configs": [{"Subnet": "10.255.0.0/16","Gateway": "10.255.0.1"}]}},"DriverState": {"Name": "overlay","Options": {"com.docker.network.driver.overlay.vxlanid_list": "256"}},"IPAMOptions": {"Driver": {"Name": "default"},"Configs": [{"Subnet": "10.255.0.0/16","Gateway": "10.255.0.1"}]}},"Addresses": ["10.255.0.10/16"]}]},{"ID": "1yljwbmlr8er2waf8orvqpwms","Version": {"Index": 30},"CreatedAt": "2016-06-07T21:07:30.019104782Z","UpdatedAt": "2016-06-07T21:07:30.231958098Z","Name": "hopeful_cori","Spec": {"ContainerSpec": {"Image": "redis"},"Resources": {"Limits": { },"Reservations": { }},"RestartPolicy": {"Condition": "any","MaxAttempts": 0},"Placement": { }},"ServiceID": "9mnpnzenvg8p8tdbtq4wvbkcz","Slot": 1,"NodeID": "60gvrl6tm78dmak4yl7srz94v","Status": {"Timestamp": "2016-06-07T21:07:30.202183143Z","State": "shutdown","Message": "shutdown","ContainerStatus": {"ContainerID": "1cf8d63d18e79668b0004a4be4c6ee58cddfad2dae29506d8781581d0688a213"}},"DesiredState": "shutdown","NetworksAttachments": [{"Network": {"ID": "4qvuz4ko70xaltuqbt8956gd1","Version": {"Index": 18},"CreatedAt": "2016-06-07T20:31:11.912919752Z","UpdatedAt": "2016-06-07T21:07:29.955277358Z","Spec": {"Name": "ingress","Labels": {"com.docker.swarm.internal": "true"},"DriverConfiguration": { },"IPAMOptions": {"Driver": { },"Configs": [{"Subnet": "10.255.0.0/16","Gateway": "10.255.0.1"}]}},"DriverState": {"Name": "overlay","Options": {"com.docker.network.driver.overlay.vxlanid_list": "256"}},"IPAMOptions": {"Driver": {"Name": "default"},"Configs": [{"Subnet": "10.255.0.0/16","Gateway": "10.255.0.1"}]}},"Addresses": ["10.255.0.5/16"]}]}]`

## Inspect a task

##### path Parameters

| idrequired | stringID of the task |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500
- 503

Content typeapplication/json`{"ID": "0kzzo1i0y4jz6027t0k7aezc7","Version": {"Index": 71},"CreatedAt": "2016-06-07T21:07:31.171892745Z","UpdatedAt": "2016-06-07T21:07:31.376370513Z","Spec": {"ContainerSpec": {"Image": "redis"},"Resources": {"Limits": { },"Reservations": { }},"RestartPolicy": {"Condition": "any","MaxAttempts": 0},"Placement": { }},"ServiceID": "9mnpnzenvg8p8tdbtq4wvbkcz","Slot": 1,"NodeID": "60gvrl6tm78dmak4yl7srz94v","Status": {"Timestamp": "2016-06-07T21:07:31.290032978Z","State": "running","Message": "started","ContainerStatus": {"ContainerID": "e5d62702a1b48d01c3e02ca1e0212a250801fa8d67caca0b6f35919ebc12f035","PID": 677}},"DesiredState": "running","NetworksAttachments": [{"Network": {"ID": "4qvuz4ko70xaltuqbt8956gd1","Version": {"Index": 18},"CreatedAt": "2016-06-07T20:31:11.912919752Z","UpdatedAt": "2016-06-07T21:07:29.955277358Z","Spec": {"Name": "ingress","Labels": {"com.docker.swarm.internal": "true"},"DriverConfiguration": { },"IPAMOptions": {"Driver": { },"Configs": [{"Subnet": "10.255.0.0/16","Gateway": "10.255.0.1"}]}},"DriverState": {"Name": "overlay","Options": {"com.docker.network.driver.overlay.vxlanid_list": "256"}},"IPAMOptions": {"Driver": {"Name": "default"},"Configs": [{"Subnet": "10.255.0.0/16","Gateway": "10.255.0.1"}]}},"Addresses": ["10.255.0.10/16"]}],"AssignedGenericResources": [{"DiscreteResourceSpec": {"Kind": "SSD","Value": 3}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID1"}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID2"}}]}`

## Get task logs

Get `stdout` and `stderr` logs from a task.
See also [/containers/{id}/logs](#operation/ContainerLogs).

**Note**: This endpoint works only for services with the `local`,
`json-file` or `journald` logging drivers.

##### path Parameters

| idrequired | stringID of the task |
| --- | --- |

##### query Parameters

| details | booleanDefault:falseShow task context and extra details provided to logs. |
| --- | --- |
| follow | booleanDefault:falseKeep connection after returning logs. |
| stdout | booleanDefault:falseReturn logs fromstdout |
| stderr | booleanDefault:falseReturn logs fromstderr |
| since | integerDefault:0Only return logs since this time, as a UNIX timestamp |
| timestamps | booleanDefault:falseAdd timestamps to every log line |
| tail | stringDefault:"all"Only return this number of log lines from the end of the logs.
Specify as an integer orallto output all log lines. |

### Responses

### Response samples

- 404

Content typeapplication/vnd.docker.raw-streamapplication/vnd.docker.multiplexed-streamapplication/jsonapplication/vnd.docker.raw-streamNo sample

## Secrets

Secrets are sensitive data that can be used by services. Swarm mode must
be enabled for these endpoints to work.

## List secrets

##### query Parameters

| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the secrets list.Available filters:id=<secret id>label=<key> or label=<key>=valuename=<secret name>names=<secret name> |
| --- | --- |

### Responses

### Response samples

- 200
- 500
- 503

Content typeapplication/json`[{"ID": "blt1owaxmitz71s9v5zh81zun","Version": {"Index": 85},"CreatedAt": "2017-07-20T13:55:28.678958722Z","UpdatedAt": "2017-07-20T13:55:28.678958722Z","Spec": {"Name": "mysql-passwd","Labels": {"some.label": "some.value"},"Driver": {"Name": "secret-bucket","Options": {"OptionA": "value for driver option A","OptionB": "value for driver option B"}}}},{"ID": "ktnbjxoalbkvbvedmg1urrz8h","Version": {"Index": 11},"CreatedAt": "2016-11-05T01:20:17.327670065Z","UpdatedAt": "2016-11-05T01:20:17.327670065Z","Spec": {"Name": "app-dev.crt","Labels": {"foo": "bar"}}}]`

## Create a secret

##### Request Body schema:application/json

| Name | stringUser-defined name of the secret. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
| Data | stringData is the data to store as a secret, formatted as a standard base64-encoded
(RFC 4648) string.
It must be empty if the Driver field is set, in which case the data is
loaded from an external secret store. The maximum allowed size is 500KB,
as defined inMaxSecretSize.This field is only used tocreatea secret, and is not returned by
other endpoints. |
|  | object(Driver)Driver represents a driver (network, logging, secrets). |
|  | object(Driver)Driver represents a driver (network, logging, secrets). |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Name": "app-key.crt","Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value","foo": "bar"},"Data": "VEhJUyBJUyBOT1QgQSBSRUFMIENFUlRJRklDQVRFCg==","Driver": {"Name": "secret-bucket","Options": {"OptionA": "value for driver option A","OptionB": "value for driver option B"}},"Templating": {"Name": "some-driver","Options": {"OptionA": "value for driver-specific option A","OptionB": "value for driver-specific option B"}}}`

### Response samples

- 201
- 409
- 500
- 503

Content typeapplication/json`{"Id": "string"}`

## Inspect a secret

##### path Parameters

| idrequired | stringID of the secret |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500
- 503

Content typeapplication/json`{"ID": "ktnbjxoalbkvbvedmg1urrz8h","Version": {"Index": 11},"CreatedAt": "2016-11-05T01:20:17.327670065Z","UpdatedAt": "2016-11-05T01:20:17.327670065Z","Spec": {"Name": "app-dev.crt","Labels": {"foo": "bar"},"Driver": {"Name": "secret-bucket","Options": {"OptionA": "value for driver option A","OptionB": "value for driver option B"}}}}`

## Delete a secret

##### path Parameters

| idrequired | stringID of the secret |
| --- | --- |

### Responses

### Response samples

- 404
- 500
- 503

Content typeapplication/json`{"message": "Something went wrong."}`

## Update a Secret

##### path Parameters

| idrequired | stringThe ID or name of the secret |
| --- | --- |

##### query Parameters

| versionrequired | integer<int64>The version number of the secret object being updated. This is
required to avoid conflicting writes. |
| --- | --- |

##### Request Body schema:application/jsontext/plainapplication/json

The spec of the secret to update. Currently, only the Labels field
can be updated. All other fields must remain unchanged from the
[SecretInspect endpoint](#operation/SecretInspect) response values.

| Name | stringUser-defined name of the secret. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
| Data | stringData is the data to store as a secret, formatted as a standard base64-encoded
(RFC 4648) string.
It must be empty if the Driver field is set, in which case the data is
loaded from an external secret store. The maximum allowed size is 500KB,
as defined inMaxSecretSize.This field is only used tocreatea secret, and is not returned by
other endpoints. |
|  | object(Driver)Driver represents a driver (network, logging, secrets). |
|  | object(Driver)Driver represents a driver (network, logging, secrets). |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`{"Name": "string","Labels": {"com.example.some-label": "some-value","com.example.some-other-label": "some-other-value"},"Data": "","Driver": {"Name": "some-driver","Options": {"OptionA": "value for driver-specific option A","OptionB": "value for driver-specific option B"}},"Templating": {"Name": "some-driver","Options": {"OptionA": "value for driver-specific option A","OptionB": "value for driver-specific option B"}}}`

### Response samples

- 400
- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Configs

Configs are application configurations that can be used by services. Swarm
mode must be enabled for these endpoints to work.

## List configs

##### query Parameters

| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the configs list.Available filters:id=<config id>label=<key> or label=<key>=valuename=<config name>names=<config name> |
| --- | --- |

### Responses

### Response samples

- 200
- 500
- 503

Content typeapplication/json`[{"ID": "ktnbjxoalbkvbvedmg1urrz8h","Version": {"Index": 11},"CreatedAt": "2016-11-05T01:20:17.327670065Z","UpdatedAt": "2016-11-05T01:20:17.327670065Z","Spec": {"Name": "server.conf"}}]`

## Create a config

##### Request Body schema:application/json

| Name | stringUser-defined name of the config. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
| Data | stringData is the data to store as a config, formatted as a standard base64-encoded
(RFC 4648) string.
The maximum allowed size is 1000KB, as defined inMaxConfigSize. |
|  | object(Driver)Driver represents a driver (network, logging, secrets). |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"Name": "server.conf","Labels": {"property1": "string","property2": "string","foo": "bar"},"Data": "VEhJUyBJUyBOT1QgQSBSRUFMIENFUlRJRklDQVRFCg==","Templating": {"Name": "some-driver","Options": {"OptionA": "value for driver-specific option A","OptionB": "value for driver-specific option B"}}}`

### Response samples

- 201
- 409
- 500
- 503

Content typeapplication/json`{"Id": "string"}`

## Inspect a config

##### path Parameters

| idrequired | stringID of the config |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500
- 503

Content typeapplication/json`{"ID": "ktnbjxoalbkvbvedmg1urrz8h","Version": {"Index": 11},"CreatedAt": "2016-11-05T01:20:17.327670065Z","UpdatedAt": "2016-11-05T01:20:17.327670065Z","Spec": {"Name": "app-dev.crt"}}`

## Delete a config

##### path Parameters

| idrequired | stringID of the config |
| --- | --- |

### Responses

### Response samples

- 404
- 500
- 503

Content typeapplication/json`{"message": "Something went wrong."}`

## Update a Config

##### path Parameters

| idrequired | stringThe ID or name of the config |
| --- | --- |

##### query Parameters

| versionrequired | integer<int64>The version number of the config object being updated. This is
required to avoid conflicting writes. |
| --- | --- |

##### Request Body schema:application/jsontext/plainapplication/json

The spec of the config to update. Currently, only the Labels field
can be updated. All other fields must remain unchanged from the
[ConfigInspect endpoint](#operation/ConfigInspect) response values.

| Name | stringUser-defined name of the config. |
| --- | --- |
|  | objectUser-defined key/value metadata. |
| Data | stringData is the data to store as a config, formatted as a standard base64-encoded
(RFC 4648) string.
The maximum allowed size is 1000KB, as defined inMaxConfigSize. |
|  | object(Driver)Driver represents a driver (network, logging, secrets). |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`{"Name": "string","Labels": {"property1": "string","property2": "string"},"Data": "string","Templating": {"Name": "some-driver","Options": {"OptionA": "value for driver-specific option A","OptionB": "value for driver-specific option B"}}}`

### Response samples

- 400
- 404
- 500
- 503

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Plugins

## List plugins

Returns information about installed plugins.

##### query Parameters

| filters | stringA JSON encoded value of the filters (amap[string][]string) to
process on the plugin list.Available filters:capability=<capability name>enable=<true>|<false> |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`[{"Id": "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078","Name": "tiborvass/sample-volume-plugin","Enabled": true,"Settings": {"Mounts": [{"Name": "some-mount","Description": "This is a mount that's used by the plugin.","Settable": ["string"],"Source": "/var/lib/docker/plugins/","Destination": "/mnt/state","Type": "bind","Options": ["rbind","rw"]}],"Env": ["DEBUG=0"],"Args": ["string"],"Devices": [{"Name": "string","Description": "string","Settable": ["string"],"Path": "/dev/fuse"}]},"PluginReference": "localhost:5000/tiborvass/sample-volume-plugin:latest","Config": {"DockerVersion": "string","Description": "A sample volume plugin for Docker","Documentation": "https://docs.docker.com/engine/extend/plugins/","Interface": {"Types": ["docker.volumedriver/1.0"],"Socket": "plugins.sock","ProtocolScheme": "some.protocol/v1.0"},"Entrypoint": ["/usr/bin/sample-volume-plugin","/data"],"WorkDir": "/bin/","User": {"UID": 1000,"GID": 1000},"Network": {"Type": "host"},"Linux": {"Capabilities": ["CAP_SYS_ADMIN","CAP_SYSLOG"],"AllowAllDevices": false,"Devices": [{"Name": "string","Description": "string","Settable": ["string"],"Path": "/dev/fuse"}]},"PropagatedMount": "/mnt/volumes","IpcHost": false,"PidHost": false,"Mounts": [{"Name": "some-mount","Description": "This is a mount that's used by the plugin.","Settable": ["string"],"Source": "/var/lib/docker/plugins/","Destination": "/mnt/state","Type": "bind","Options": ["rbind","rw"]}],"Env": [{"Name": "DEBUG","Description": "If set, prints debug messages","Settable": null,"Value": "0"}],"Args": {"Name": "args","Description": "command line arguments","Settable": ["string"],"Value": ["string"]},"rootfs": {"type": "layers","diff_ids": ["sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887","sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"]}}}]`

## Get plugin privileges

##### query Parameters

| remoterequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/jsontext/plainapplication/json`[{"Name": "network","Description": "","Value": ["host"]},{"Name": "mount","Description": "","Value": ["/data"]},{"Name": "device","Description": "","Value": ["/dev/cpu_dma_latency"]}]`

## Install a plugin

Pulls and installs a plugin. After the plugin is installed, it can be
enabled using the [POST /plugins/{name}/enableendpoint](#operation/PostPluginsEnable).

##### query Parameters

| remoterequired | stringRemote reference for plugin to install.The:latesttag is optional, and is used as the default if omitted. |
| --- | --- |
| name | stringLocal name for the pulled plugin.The:latesttag is optional, and is used as the default if omitted. |

##### header Parameters

| X-Registry-Auth | stringA base64url-encoded auth configuration to use when pulling a plugin
from a registry.Refer to theauthentication sectionfor
details. |
| --- | --- |

##### Request Body schema:application/jsontext/plainapplication/json

 Array

| Name | string |
| --- | --- |
| Description | string |
| Value | Array ofstrings |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`[{"Name": "network","Description": "","Value": ["host"]},{"Name": "mount","Description": "","Value": ["/data"]},{"Name": "device","Description": "","Value": ["/dev/cpu_dma_latency"]}]`

### Response samples

- 500

Content typeapplication/json`{"message": "Something went wrong."}`

## Inspect a plugin

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"Id": "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078","Name": "tiborvass/sample-volume-plugin","Enabled": true,"Settings": {"Mounts": [{"Name": "some-mount","Description": "This is a mount that's used by the plugin.","Settable": ["string"],"Source": "/var/lib/docker/plugins/","Destination": "/mnt/state","Type": "bind","Options": ["rbind","rw"]}],"Env": ["DEBUG=0"],"Args": ["string"],"Devices": [{"Name": "string","Description": "string","Settable": ["string"],"Path": "/dev/fuse"}]},"PluginReference": "localhost:5000/tiborvass/sample-volume-plugin:latest","Config": {"DockerVersion": "string","Description": "A sample volume plugin for Docker","Documentation": "https://docs.docker.com/engine/extend/plugins/","Interface": {"Types": ["docker.volumedriver/1.0"],"Socket": "plugins.sock","ProtocolScheme": "some.protocol/v1.0"},"Entrypoint": ["/usr/bin/sample-volume-plugin","/data"],"WorkDir": "/bin/","User": {"UID": 1000,"GID": 1000},"Network": {"Type": "host"},"Linux": {"Capabilities": ["CAP_SYS_ADMIN","CAP_SYSLOG"],"AllowAllDevices": false,"Devices": [{"Name": "string","Description": "string","Settable": ["string"],"Path": "/dev/fuse"}]},"PropagatedMount": "/mnt/volumes","IpcHost": false,"PidHost": false,"Mounts": [{"Name": "some-mount","Description": "This is a mount that's used by the plugin.","Settable": ["string"],"Source": "/var/lib/docker/plugins/","Destination": "/mnt/state","Type": "bind","Options": ["rbind","rw"]}],"Env": [{"Name": "DEBUG","Description": "If set, prints debug messages","Settable": null,"Value": "0"}],"Args": {"Name": "args","Description": "command line arguments","Settable": ["string"],"Value": ["string"]},"rootfs": {"type": "layers","diff_ids": ["sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887","sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"]}}}`

## Remove a plugin

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

##### query Parameters

| force | booleanDefault:falseDisable the plugin before removing. This may result in issues if the
plugin is in use by a container. |
| --- | --- |

### Responses

### Response samples

- 200
- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"Id": "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078","Name": "tiborvass/sample-volume-plugin","Enabled": true,"Settings": {"Mounts": [{"Name": "some-mount","Description": "This is a mount that's used by the plugin.","Settable": ["string"],"Source": "/var/lib/docker/plugins/","Destination": "/mnt/state","Type": "bind","Options": ["rbind","rw"]}],"Env": ["DEBUG=0"],"Args": ["string"],"Devices": [{"Name": "string","Description": "string","Settable": ["string"],"Path": "/dev/fuse"}]},"PluginReference": "localhost:5000/tiborvass/sample-volume-plugin:latest","Config": {"DockerVersion": "string","Description": "A sample volume plugin for Docker","Documentation": "https://docs.docker.com/engine/extend/plugins/","Interface": {"Types": ["docker.volumedriver/1.0"],"Socket": "plugins.sock","ProtocolScheme": "some.protocol/v1.0"},"Entrypoint": ["/usr/bin/sample-volume-plugin","/data"],"WorkDir": "/bin/","User": {"UID": 1000,"GID": 1000},"Network": {"Type": "host"},"Linux": {"Capabilities": ["CAP_SYS_ADMIN","CAP_SYSLOG"],"AllowAllDevices": false,"Devices": [{"Name": "string","Description": "string","Settable": ["string"],"Path": "/dev/fuse"}]},"PropagatedMount": "/mnt/volumes","IpcHost": false,"PidHost": false,"Mounts": [{"Name": "some-mount","Description": "This is a mount that's used by the plugin.","Settable": ["string"],"Source": "/var/lib/docker/plugins/","Destination": "/mnt/state","Type": "bind","Options": ["rbind","rw"]}],"Env": [{"Name": "DEBUG","Description": "If set, prints debug messages","Settable": null,"Value": "0"}],"Args": {"Name": "args","Description": "command line arguments","Settable": ["string"],"Value": ["string"]},"rootfs": {"type": "layers","diff_ids": ["sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887","sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"]}}}`

## Enable a plugin

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

##### query Parameters

| timeout | integerDefault:0Set the HTTP client timeout (in seconds) |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Disable a plugin

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

##### query Parameters

| force | booleanForce disable a plugin even if still in use. |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Upgrade a plugin

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

##### query Parameters

| remoterequired | stringRemote reference to upgrade to.The:latesttag is optional, and is used as the default if omitted. |
| --- | --- |

##### header Parameters

| X-Registry-Auth | stringA base64url-encoded auth configuration to use when pulling a plugin
from a registry.Refer to theauthentication sectionfor
details. |
| --- | --- |

##### Request Body schema:application/jsontext/plainapplication/json

 Array

| Name | string |
| --- | --- |
| Description | string |
| Value | Array ofstrings |

### Responses

### Request samples

- Payload

Content typeapplication/jsontext/plainapplication/json`[{"Name": "network","Description": "","Value": ["host"]},{"Name": "mount","Description": "","Value": ["/data"]},{"Name": "device","Description": "","Value": ["/dev/cpu_dma_latency"]}]`

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Create a plugin

##### query Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

##### Request Body schema:application/x-tar

Path to tar containing plugin rootfs and manifest

 string <binary>

### Responses

### Response samples

- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Push a plugin

Push a plugin to the registry.

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

### Responses

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## Configure a plugin

##### path Parameters

| namerequired | stringThe name of the plugin. The:latesttag is optional, and is the
default if omitted. |
| --- | --- |

##### Request Body schema:application/json

 Array string

### Responses

### Request samples

- Payload

Content typeapplication/json`["DEBUG=1"]`

### Response samples

- 404
- 500

Content typeapplication/jsontext/plainapplication/json`{"message": "Something went wrong."}`

## System

## Check auth configuration

Validate credentials for a registry and, if available, get an identity
token for accessing the registry without password.

##### Request Body schema:application/json

Authentication to check

| username | string |
| --- | --- |
| password | string |
| email | stringEmail is an optional value associated with the username.Deprecated: This field is deprecated since docker 1.11 (API v1.23) and will be removed in a future release. |
| serveraddress | string |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"username": "hannibal","password": "xxxx","serveraddress": "https://index.docker.io/v1/"}`

### Response samples

- 200
- 401
- 500

Content typeapplication/json`{"Status": "Login Succeeded","IdentityToken": "9cbaf023786cd7..."}`

## Get system information

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"ID": "7TRN:IPZB:QYBB:VPBQ:UMPP:KARE:6ZNR:XE6T:7EWV:PKF4:ZOJD:TPYS","Containers": 14,"ContainersRunning": 3,"ContainersPaused": 1,"ContainersStopped": 10,"Images": 508,"Driver": "overlay2","DriverStatus": [["Backing Filesystem","extfs"],["Supports d_type","true"],["Native Overlay Diff","true"]],"DockerRootDir": "/var/lib/docker","Plugins": {"Volume": ["local"],"Network": ["bridge","host","ipvlan","macvlan","null","overlay"],"Authorization": ["img-authz-plugin","hbm"],"Log": ["awslogs","fluentd","gcplogs","gelf","journald","json-file","splunk","syslog"]},"MemoryLimit": true,"SwapLimit": true,"KernelMemoryTCP": true,"CpuCfsPeriod": true,"CpuCfsQuota": true,"CPUShares": true,"CPUSet": true,"PidsLimit": true,"OomKillDisable": true,"IPv4Forwarding": true,"Debug": true,"NFd": 64,"NGoroutines": 174,"SystemTime": "2017-08-08T20:28:29.06202363Z","LoggingDriver": "string","CgroupDriver": "cgroupfs","CgroupVersion": "1","NEventsListener": 30,"KernelVersion": "6.8.0-31-generic","OperatingSystem": "Ubuntu 24.04 LTS","OSVersion": "24.04","OSType": "linux","Architecture": "x86_64","NCPU": 4,"MemTotal": 2095882240,"IndexServerAddress": "https://index.docker.io/v1/","RegistryConfig": {"InsecureRegistryCIDRs": ["::1/128","127.0.0.0/8"],"IndexConfigs": {"127.0.0.1:5000": {"Name": "127.0.0.1:5000","Mirrors": [ ],"Secure": false,"Official": false},"[2001:db8:a0b:12f0::1]:80": {"Name": "[2001:db8:a0b:12f0::1]:80","Mirrors": [ ],"Secure": false,"Official": false},"docker.io": {"Name": "docker.io","Mirrors": ["https://hub-mirror.corp.example.com:5000/"],"Secure": true,"Official": true},"registry.internal.corp.example.com:3000": {"Name": "registry.internal.corp.example.com:3000","Mirrors": [ ],"Secure": false,"Official": false}},"Mirrors": ["https://hub-mirror.corp.example.com:5000/","https://[2001:db8:a0b:12f0::1]/"]},"GenericResources": [{"DiscreteResourceSpec": {"Kind": "SSD","Value": 3}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID1"}},{"NamedResourceSpec": {"Kind": "GPU","Value": "UUID2"}}],"HttpProxy": "http://xxxxx:xxxxx@proxy.corp.example.com:8080","HttpsProxy": "https://xxxxx:xxxxx@proxy.corp.example.com:4443","NoProxy": "*.local, 169.254/16","Name": "node5.corp.example.com","Labels": ["storage=ssd","production"],"ExperimentalBuild": true,"ServerVersion": "27.0.1","Runtimes": {"runc": {"path": "runc"},"runc-master": {"path": "/go/bin/runc"},"custom": {"path": "/usr/local/bin/my-oci-runtime","runtimeArgs": ["--debug","--systemd-cgroup=false"]}},"DefaultRuntime": "runc","Swarm": {"NodeID": "k67qz4598weg5unwwffg6z1m1","NodeAddr": "10.0.0.46","LocalNodeState": "active","ControlAvailable": true,"Error": "","RemoteManagers": [{"NodeID": "71izy0goik036k48jg985xnds","Addr": "10.0.0.158:2377"},{"NodeID": "79y6h1o4gv8n120drcprv5nmc","Addr": "10.0.0.159:2377"},{"NodeID": "k67qz4598weg5unwwffg6z1m1","Addr": "10.0.0.46:2377"}],"Nodes": 4,"Managers": 3,"Cluster": {"ID": "abajmipo7b4xz5ip2nrla6b11","Version": {"Index": 373531},"CreatedAt": "2016-08-18T10:44:24.496525531Z","UpdatedAt": "2017-08-09T07:09:37.632105588Z","Spec": {"Name": "default","Labels": {"com.example.corp.type": "production","com.example.corp.department": "engineering"},"Orchestration": {"TaskHistoryRetentionLimit": 10},"Raft": {"SnapshotInterval": 10000,"KeepOldSnapshots": 0,"LogEntriesForSlowFollowers": 500,"ElectionTick": 3,"HeartbeatTick": 1},"Dispatcher": {"HeartbeatPeriod": 5000000000},"CAConfig": {"NodeCertExpiry": 7776000000000000,"ExternalCAs": [{"Protocol": "cfssl","URL": "string","Options": {"property1": "string","property2": "string"},"CACert": "string"}],"SigningCACert": "string","SigningCAKey": "string","ForceRotate": 0},"EncryptionConfig": {"AutoLockManagers": false},"TaskDefaults": {"LogDriver": {"Name": "json-file","Options": {"max-file": "10","max-size": "100m"}}}},"TLSInfo": {"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n","CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh","CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="},"RootRotationInProgress": false,"DataPathPort": 4789,"DefaultAddrPool": [["10.10.0.0/16","20.20.0.0/16"]],"SubnetSize": 24}},"LiveRestoreEnabled": false,"Isolation": "default","InitBinary": "docker-init","ContainerdCommit": {"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a"},"RuncCommit": {"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a"},"InitCommit": {"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a"},"SecurityOptions": ["name=apparmor","name=seccomp,profile=default","name=selinux","name=userns","name=rootless"],"ProductLicense": "Community Engine","DefaultAddressPools": [{"Base": "10.10.0.0/16","Size": "24"}],"FirewallBackend": {"Driver": "nftables","Info": [["ReloadedAt","2025-01-01T00:00:00Z"]]},"DiscoveredDevices": [{"Source": "cdi","ID": "vendor.com/gpu=0"}],"Warnings": ["WARNING: No memory limit support"],"CDISpecDirs": ["/etc/cdi","/var/run/cdi"],"Containerd": {"Address": "/run/containerd/containerd.sock","Namespaces": {"Containers": "moby","Plugins": "plugins.moby"}}}`

## Get version

Returns the version of Docker that is running and various information about the system that Docker is running on.

### Responses

### Response samples

- 200
- 500

Content typeapplication/json`{"Platform": {"Name": "string"},"Components": [{"Name": "Engine","Version": "27.0.1","Details": { }}],"Version": "27.0.1","ApiVersion": "1.47","MinAPIVersion": "1.24","GitCommit": "48a66213fe","GoVersion": "go1.22.7","Os": "linux","Arch": "amd64","KernelVersion": "6.8.0-31-generic","Experimental": true,"BuildTime": "2020-06-22T15:49:27.000000000+00:00"}`

## Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

## Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

## Monitor events

Stream real-time events from the server.

Various objects within Docker report events when something happens to them.

Containers report these events: `attach`, `commit`, `copy`, `create`, `destroy`, `detach`, `die`, `exec_create`, `exec_detach`, `exec_start`, `exec_die`, `export`, `health_status`, `kill`, `oom`, `pause`, `rename`, `resize`, `restart`, `start`, `stop`, `top`, `unpause`, `update`, and `prune`

Images report these events: `create`, `delete`, `import`, `load`, `pull`, `push`, `save`, `tag`, `untag`, and `prune`

Volumes report these events: `create`, `mount`, `unmount`, `destroy`, and `prune`

Networks report these events: `create`, `connect`, `disconnect`, `destroy`, `update`, `remove`, and `prune`

The Docker daemon reports these events: `reload`

Services report these events: `create`, `update`, and `remove`

Nodes report these events: `create`, `update`, and `remove`

Secrets report these events: `create`, `update`, and `remove`

Configs report these events: `create`, `update`, and `remove`

The Builder reports `prune` events

##### query Parameters

| since | stringShow events created since this timestamp then stream new events. |
| --- | --- |
| until | stringShow events created until this timestamp then stop streaming. |
| filters | stringA JSON encoded value of filters (amap[string][]string) to process on the event list. Available filters:config=<string>config name or IDcontainer=<string>container name or IDdaemon=<string>daemon name or IDevent=<string>event typeimage=<string>image name or IDlabel=<string>image or container labelnetwork=<string>network name or IDnode=<string>node IDplugin=plugin name or IDscope=local or swarmsecret=<string>secret name or IDservice=<string>service name or IDtype=<string>object to filter by, one ofcontainer,image,volume,network,daemon,plugin,node,service,secretorconfigvolume=<string>volume name |

### Responses

### Response samples

- 200
- 400
- 500

Content typeapplication/json`{"Type": "container","Action": "create","Actor": {"ID": "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743","Attributes": {"com.example.some-label": "some-label-value","image": "alpine:latest","name": "my-container"}},"scope": "local","time": 1629574695,"timeNano": 1629574695515050000}`

## Get data usage information

##### query Parameters

| type | Array ofstringsItems Enum:"container""image""volume""build-cache"Object types, for which to compute and return data. |
| --- | --- |

### Responses

### Response samples

- 200
- 500

Content typeapplication/jsontext/plainapplication/json`{"LayersSize": 1092588,"Images": [{"Id": "sha256:2b8fd9751c4c0f5dd266fcae00707e67a2545ef34f9a29354585f93dac906749","ParentId": "","RepoTags": ["busybox:latest"],"RepoDigests": ["busybox@sha256:a59906e33509d14c036c8678d687bd4eec81ed7c4b8ce907b888c607f6a1e0e6"],"Created": 1466724217,"Size": 1092588,"SharedSize": 0,"Labels": { },"Containers": 1}],"Containers": [{"Id": "e575172ed11dc01bfce087fb27bee502db149e1a0fad7c296ad300bbff178148","Names": ["/top"],"Image": "busybox","ImageID": "sha256:2b8fd9751c4c0f5dd266fcae00707e67a2545ef34f9a29354585f93dac906749","Command": "top","Created": 1472592424,"Ports": [ ],"SizeRootFs": 1092588,"Labels": { },"State": "exited","Status": "Exited (0) 56 minutes ago","HostConfig": {"NetworkMode": "default"},"NetworkSettings": {"Networks": {"bridge": {"IPAMConfig": null,"Links": null,"Aliases": null,"NetworkID": "d687bc59335f0e5c9ee8193e5612e8aee000c8c62ea170cfb99c098f95899d92","EndpointID": "8ed5115aeaad9abb174f68dcf135b49f11daf597678315231a32ca28441dec6a","Gateway": "172.18.0.1","IPAddress": "172.18.0.2","IPPrefixLen": 16,"IPv6Gateway": "","GlobalIPv6Address": "","GlobalIPv6PrefixLen": 0,"MacAddress": "02:42:ac:12:00:02"}}},"Mounts": [ ]}],"Volumes": [{"Name": "my-volume","Driver": "local","Mountpoint": "/var/lib/docker/volumes/my-volume/_data","Labels": null,"Scope": "local","Options": null,"UsageData": {"Size": 10920104,"RefCount": 2}}],"BuildCache": [{"ID": "hw53o5aio51xtltp5xjp8v7fx","Parents": [ ],"Type": "regular","Description": "pulled from docker.io/library/debian@sha256:234cb88d3020898631af0ccbbcca9a66ae7306ecd30c9720690858c1b007d2a0","InUse": false,"Shared": true,"Size": 0,"CreatedAt": "2021-06-28T13:31:01.474619385Z","LastUsedAt": "2021-07-07T22:02:32.738075951Z","UsageCount": 26},{"ID": "ndlpt0hhvkqcdfkputsk4cq9c","Parents": ["ndlpt0hhvkqcdfkputsk4cq9c"],"Type": "regular","Description": "mount / from exec /bin/sh -c echo 'Binary::apt::APT::Keep-Downloaded-Packages \"true\";' > /etc/apt/apt.conf.d/keep-cache","InUse": false,"Shared": true,"Size": 51,"CreatedAt": "2021-06-28T13:31:03.002625487Z","LastUsedAt": "2021-07-07T22:02:32.773909517Z","UsageCount": 26}]}`

## Distribution

## Get image information from the registry

Return image digest and platform information by contacting the registry.

##### path Parameters

| namerequired | stringImage name or id |
| --- | --- |

### Responses

### Response samples

- 200
- 401
- 500

Content typeapplication/json`{"Descriptor": {"mediaType": "application/vnd.oci.image.manifest.v1+json","digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96","size": 424,"urls": ["http://example.com"],"annotations": {"com.docker.official-images.bashbrew.arch": "amd64","org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8","org.opencontainers.image.base.name": "scratch","org.opencontainers.image.created": "2025-01-27T00:00:00Z","org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79","org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base","org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu","org.opencontainers.image.version": "24.04"},"data": null,"platform": {"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"},"artifactType": null},"Platforms": [{"architecture": "arm","os": "windows","os.version": "10.0.19041.1165","os.features": ["win32k"],"variant": "v7"}]}`

## Session

## Initialize interactive session

Start a new interactive session with a server. Session allows server to
call back to the client for advanced capabilities.

### Hijacking

This endpoint hijacks the HTTP connection to HTTP2 transport that allows
the client to expose gPRC services on that connection.

For example, the client sends this request to upgrade the connection:

```
POST /session HTTP/1.1
Upgrade: h2c
Connection: Upgrade
```

The Docker daemon responds with a `101 UPGRADED` response follow with
the raw stream:

```
HTTP/1.1 101 UPGRADED
Connection: Upgrade
Upgrade: h2c
```

### Responses
