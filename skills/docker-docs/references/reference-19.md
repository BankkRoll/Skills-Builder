# docker buildx create and more

# docker buildx create

# docker buildx create

| Description | Create a new builder instance |
| --- | --- |
| Usage | docker buildx create [OPTIONS] [CONTEXT|ENDPOINT] |

## Description

Create makes a new builder instance pointing to a Docker context or endpoint,
where context is the name of a context from `docker context ls` and endpoint is
the address for Docker socket (eg. `DOCKER_HOST` value).

By default, the current Docker configuration is used for determining the
context/endpoint value.

Builder instances are isolated environments where builds can be invoked. All
Docker contexts also get the default builder instance.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --append |  | Append a node to builder instead of changing it |
| --bootstrap |  | Boot builder after creation |
| --buildkitd-config |  | BuildKit daemon config file |
| --buildkitd-flags |  | BuildKit daemon flags |
| --driver |  | Driver to use (available:docker-container,kubernetes,remote) |
| --driver-opt |  | Options for the driver |
| --leave |  | Remove a node from builder instead of changing it |
| --name |  | Builder instance name |
| --node |  | Create/modify node with given name |
| --platform |  | Fixed platforms for current node |
| --use |  | Set the current builder instance |

## Examples

### Append a new node to an existing builder (--append)

The `--append` flag changes the action of the command to append a new node to an
existing builder specified by `--name`. Buildx will choose an appropriate node
for a build based on the platforms it supports.

```console
$ docker buildx create mycontext1
eager_beaver

$ docker buildx create --name eager_beaver --append mycontext2
eager_beaver
```

### Specify a configuration file for the BuildKit daemon (--buildkitd-config)

```text
--buildkitd-config FILE
```

Specifies the configuration file for the BuildKit daemon to use. The
configuration can be overridden by [--buildkitd-flags](#buildkitd-flags).
See an [example BuildKit daemon configuration file](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md).

If you don't specify a configuration file, Buildx looks for one by default in:

- `$BUILDX_CONFIG/buildkitd.default.toml`
- `$DOCKER_CONFIG/buildx/buildkitd.default.toml`
- `~/.docker/buildx/buildkitd.default.toml`

Note that if you create a `docker-container` builder and have specified
certificates for registries in the `buildkitd.toml` configuration, the files
will be copied into the container under `/etc/buildkit/certs` and configuration
will be updated to reflect that.

### Specify options for the BuildKit daemon (--buildkitd-flags)

```text
--buildkitd-flags FLAGS
```

Adds flags when starting the BuildKit daemon. They take precedence over the
configuration file specified by [--buildkitd-config](#buildkitd-config). See
`buildkitd --help` for the available flags.

```text
--buildkitd-flags '--debug --debugaddr 0.0.0.0:6666'
```

#### BuildKit daemon network mode

You can specify the network mode for the BuildKit daemon with either the
configuration file specified by [--buildkitd-config](#buildkitd-config) using the
`worker.oci.networkMode` option or `--oci-worker-net` flag here. The default
value is `auto` and can be one of `bridge`, `cni`, `host`:

```text
--buildkitd-flags '--oci-worker-net bridge'
```

> Note
>
> Network mode "bridge" is supported since BuildKit v0.13 and will become the
> default in next v0.14.

### Set the builder driver to use (--driver)

```text
--driver DRIVER
```

Sets the builder driver to be used. A driver is a configuration of a BuildKit
backend. Buildx supports the following drivers:

- `docker` (default)
- `docker-container`
- `kubernetes`
- `remote`

For more information about build drivers, see
[here](https://docs.docker.com/build/builders/drivers/).

#### dockerdriver

Uses the builder that is built into the Docker daemon. With this driver,
the
[--load](https://docs.docker.com/reference/cli/docker/buildx/build/#load) flag is implied by default on
`buildx build`. However, building multi-platform images or exporting cache is
not currently supported.

#### docker-containerdriver

Uses a BuildKit container that will be spawned via Docker. With this driver,
both building multi-platform images and exporting cache are supported.

Unlike `docker` driver, built images will not automatically appear in
`docker images` and
[build --load](https://docs.docker.com/reference/cli/docker/buildx/build/#load) needs to be used
to achieve that.

#### kubernetesdriver

Uses Kubernetes pods. With this driver, you can spin up pods with defined
BuildKit container image to build your images.

Unlike `docker` driver, built images will not automatically appear in
`docker images` and
[build --load](https://docs.docker.com/reference/cli/docker/buildx/build/#load) needs to be used
to achieve that.

#### remotedriver

Uses a remote instance of BuildKit daemon over an arbitrary connection. With
this driver, you manually create and manage instances of buildkit yourself, and
configure buildx to point at it.

Unlike `docker` driver, built images will not automatically appear in
`docker images` and
[build --load](https://docs.docker.com/reference/cli/docker/buildx/build/#load) needs to be used
to achieve that.

### Set additional driver-specific options (--driver-opt)

```text
--driver-opt OPTIONS
```

Passes additional driver-specific options.
For information about available driver options, refer to the detailed
documentation for the specific driver:

- [dockerdriver](https://docs.docker.com/build/builders/drivers/docker/)
- [docker-containerdriver](https://docs.docker.com/build/builders/drivers/docker-container/)
- [kubernetesdriver](https://docs.docker.com/build/builders/drivers/kubernetes/)
- [remotedriver](https://docs.docker.com/build/builders/drivers/remote/)

### Remove a node from a builder (--leave)

The `--leave` flag changes the action of the command to remove a node from a
builder. The builder needs to be specified with `--name` and node that is removed
is set with `--node`.

```console
$ docker buildx create --name mybuilder --node mybuilder0 --leave
```

### Specify the name of the builder (--name)

```text
--name NAME
```

The `--name` flag specifies the name of the builder to be created or modified.
If none is specified, one will be automatically generated.

### Specify the name of the node (--node)

```text
--node NODE
```

The `--node` flag specifies the name of the node to be created or modified. If
you don't specify a name, the node name defaults to the name of the builder it
belongs to, with an index number suffix.

### Set the platforms supported by the node (--platform)

```text
--platform PLATFORMS
```

The `--platform` flag sets the platforms supported by the node. It expects a
comma-separated list of platforms of the form OS/architecture/variant. The node
will also automatically detect the platforms it supports, but manual values take
priority over the detected ones and can be used when multiple nodes support
building for the same platform.

```console
$ docker buildx create --platform linux/amd64
$ docker buildx create --platform linux/arm64,linux/arm/v7
```

### Automatically switch to the newly created builder (--use)

The `--use` flag automatically switches the current builder to the newly created
one. Equivalent to running `docker buildx use $(docker buildx create ...)`.

---

# docker buildx dap attach

# docker buildx dap attach

| Description | Attach to a container created by the dap evaluate request |
| --- | --- |
| Usage | docker buildx dap attach PATH |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Attach to a container created by the dap evaluate request

---

# docker buildx dap build

# docker buildx dap build

| Description | Start a build |
| --- | --- |
| Usage | docker buildx dap build [OPTIONS] PATH | URL | - |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Start a debug session using the [debug adapter protocol](https://microsoft.github.io/debug-adapter-protocol/overview) to communicate with the debugger UI.

Arguments are the same as the `build`

> Note
>
> `buildx dap build` command may receive backwards incompatible features in the future
> if needed. We are looking for feedback on improving the command and extending
> the functionality further.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --add-host |  | Add a custom host-to-IP mapping (format:host:ip) |
| --allow |  | Allow extra privileged entitlement (e.g.,network.host,security.insecure,device) |
| --annotation |  | Add annotation to the image |
| --attest |  | Attestation parameters (format:type=sbom,generator=image) |
| --build-arg |  | Set build-time variables |
| --build-context |  | Additional build contexts (e.g., name=path) |
| --cache-from |  | External cache sources (e.g.,user/app:cache,type=local,src=path/to/dir) |
| --cache-to |  | Cache export destinations (e.g.,user/app:cache,type=local,dest=path/to/dir) |
| --call | build | Set method for evaluating build (check,outline,targets) |
| --cgroup-parent |  | Set the parent cgroup for theRUNinstructions during build |
| --check |  | Shorthand for--call=check |
| -f, --file |  | Name of the Dockerfile (default:PATH/Dockerfile) |
| --iidfile |  | Write the image ID to a file |
| --label |  | Set metadata for an image |
| --load |  | Shorthand for--output=type=docker |
| --metadata-file |  | Write build result metadata to a file |
| --network |  | Set the networking mode for theRUNinstructions during build |
| --no-cache |  | Do not use cache when building the image |
| --no-cache-filter |  | Do not cache specified stages |
| -o, --output |  | Output destination (format:type=local,dest=path) |
| --platform |  | Set target platform for build |
| --policy |  | Policy configuration (format:filename=path[,filename=path][,reset=true|false][,disabled=true|false][,strict=true|false][,log-level=level]) |
| --progress | auto | Set type of progress output (auto,none,plain,quiet,rawjson,tty). Use plain to show container output |
| --provenance |  | Shorthand for--attest=type=provenance |
| --pull |  | Always attempt to pull all referenced images |
| --push |  | Shorthand for--output=type=registry,unpack=false |
| -q, --quiet |  | Suppress the build output and print image ID on success |
| --sbom |  | Shorthand for--attest=type=sbom |
| --secret |  | Secret to expose to the build (format:id=mysecret[,src=/local/secret]) |
| --shm-size |  | Shared memory size for build containers |
| --ssh |  | SSH agent socket or keys to expose to the build (format:default|<id>[=<socket>|<key>[,<key>]]) |
| -t, --tag |  | Image identifier (format:[registry/]repository[:tag]) |
| --target |  | Set the target build stage to build |
| --ulimit |  | Ulimit options |

## Examples

### Launch request arguments

The following [launch request arguments](https://microsoft.github.io/debug-adapter-protocol/specification#Requests_Launch) are supported. These are sent as a JSON body as part of the launch request.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| dockerfile | string | Dockerfile | Name of the Dockerfile |
| contextPath | string | . | Set the context path for the build (normally the first positional argument) |
| target | string |  | Set the target build stage to build |
| stopOnEntry | boolean | false | Stop on the first instruction |

### Additional Arguments

Command line arguments may be passed to the debug adapter the same way they would be passed to the normal build command and they will set the value.
Launch request arguments that are set will override command line arguments if they are present.

A debug extension should include an `args` and `builder` entry in the launch configuration. These will modify the arguments passed to the binary for the tool invocation.
`builder` will add `--builder <arg>` directly after the executable and `args` will append to the end of the tool invocation.
For example, a launch configuration in Visual Studio Code with the following:

```json
{
    "args": ["--build-arg", "FOO=AAA"]
    "builder": ["mybuilder"]
}
```

This should cause the debug adapter to be invoked as `docker buildx --builder mybuilder dap build --build-arg FOO=AAA`.

---

# docker buildx dap

# docker buildx dap

| Description | Start debug adapter protocol compatible debugger |
| --- | --- |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Start debug adapter protocol compatible debugger

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx dap attach | Attach to a container created by the dap evaluate request |
| docker buildx dap build | Start a build |

---

# docker buildx debug build

# docker buildx debug build

| Description | Start a build |
| --- | --- |
| Usage | docker buildx debug build [OPTIONS] PATH | URL | - |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker builddocker builder builddocker image builddocker buildx b |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Start a build

## Options

| Option | Default | Description |
| --- | --- | --- |
| --add-host |  | Add a custom host-to-IP mapping (format:host:ip) |
| --allow |  | Allow extra privileged entitlement (e.g.,network.host,security.insecure,device) |
| --annotation |  | Add annotation to the image |
| --attest |  | Attestation parameters (format:type=sbom,generator=image) |
| --build-arg |  | Set build-time variables |
| --build-context |  | Additional build contexts (e.g., name=path) |
| --cache-from |  | External cache sources (e.g.,user/app:cache,type=local,src=path/to/dir) |
| --cache-to |  | Cache export destinations (e.g.,user/app:cache,type=local,dest=path/to/dir) |
| --call | build | Set method for evaluating build (check,outline,targets) |
| --cgroup-parent |  | Set the parent cgroup for theRUNinstructions during build |
| --check |  | Shorthand for--call=check |
| -f, --file |  | Name of the Dockerfile (default:PATH/Dockerfile) |
| --iidfile |  | Write the image ID to a file |
| --label |  | Set metadata for an image |
| --load |  | Shorthand for--output=type=docker |
| --metadata-file |  | Write build result metadata to a file |
| --network |  | Set the networking mode for theRUNinstructions during build |
| --no-cache |  | Do not use cache when building the image |
| --no-cache-filter |  | Do not cache specified stages |
| -o, --output |  | Output destination (format:type=local,dest=path) |
| --platform |  | Set target platform for build |
| --policy |  | Policy configuration (format:filename=path[,filename=path][,reset=true|false][,disabled=true|false][,strict=true|false][,log-level=level]) |
| --progress | auto | Set type of progress output (auto,none,plain,quiet,rawjson,tty). Use plain to show container output |
| --provenance |  | Shorthand for--attest=type=provenance |
| --pull |  | Always attempt to pull all referenced images |
| --push |  | Shorthand for--output=type=registry,unpack=false |
| -q, --quiet |  | Suppress the build output and print image ID on success |
| --sbom |  | Shorthand for--attest=type=sbom |
| --secret |  | Secret to expose to the build (format:id=mysecret[,src=/local/secret]) |
| --shm-size |  | Shared memory size for build containers |
| --ssh |  | SSH agent socket or keys to expose to the build (format:default|<id>[=<socket>|<key>[,<key>]]) |
| -t, --tag |  | Image identifier (format:[registry/]repository[:tag]) |
| --target |  | Set the target build stage to build |
| --ulimit |  | Ulimit options |

---

# docker buildx debug

# docker buildx debug

| Description | Start debugger |
| --- | --- |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Start debugger

## Options

| Option | Default | Description |
| --- | --- | --- |
| --invoke |  | experimental (CLI)Launch a monitor with executing specified command |
| --on | error | experimental (CLI)When to launch the monitor ([always, error]) |

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx debug build | Start a build |

---

# docker buildx du

# docker buildx du

| Description | Disk usage |
| --- | --- |
| Usage | docker buildx du |

## Description

Disk usage

## Options

| Option | Default | Description |
| --- | --- | --- |
| --filter |  | Provide filter values |
| --format |  | Format the output |
| --verbose |  | Shorthand for--format=pretty |

## Examples

### Show disk usage

The `docker buildx du` command shows the disk usage for the currently selected
builder.

```console
$ docker buildx du
ID                                RECLAIMABLE    SIZE          LAST ACCESSED
12wgll9os87pazzft8lt0yztp*        true           1.704GB       13 days ago
iupsv3it5ubh92aweb7c1wojc*        true           1.297GB       36 minutes ago
ek4ve8h4obyv5kld6vicmtqyn         true           811.7MB       13 days ago
isovrfnmkelzhtdx942w9vjcb*        true           811.7MB       13 days ago
0jty7mjrndi1yo7xkv1baralh         true           810.5MB       13 days ago
jyzkefmsysqiaakgwmjgxjpcz*        true           810.5MB       13 days ago
z8w1y95jn93gvj92jtaj6uhwk         true           318MB         2 weeks ago
rz2zgfcwlfxsxd7d41w2sz2tt         true           8.224kB*      43 hours ago
n5bkzpewmk2eiu6hn9tzx18jd         true           8.224kB*      43 hours ago
ao94g6vtbzdl6k5zgdmrmnwpt         true           8.224kB*      43 hours ago
2pyjep7njm0wh39vcingxb97i         true           8.224kB*      43 hours ago
Shared:        115.5MB
Private:       10.25GB
Reclaimable:   10.36GB
Total:         10.36GB
```

If `RECLAIMABLE` is false, the `docker buildx du prune` command won't delete
the record, even if you use `--all`. That's because the record is actively in
use by some component of the builder.

The asterisks (*) in the default output format indicate the following:

- An asterisk next to an ID (`zu7m6evdpebh5h8kfkpw9dlf2*`) indicates that the record
  is mutable. The size of the record may change, or another build can take ownership of
  it and change or commit to it. If you run the `du` command again, this item may
  not be there anymore, or the size might be different.
- An asterisk next to a size (`8.288kB*`) indicates that the record is shared.
  Storage of the record is shared with some other resource, typically an image.
  If you prune such a record then you will lose build cache but only metadata
  will be deleted as the image still needs to actual storage layers.

### Provide filter values (--filter)

Same as
[buildx prune --filter](https://docs.docker.com/reference/cli/docker/buildx/prune/#filter).

### Format the output (--format)

The formatting options (`--format`) pretty-prints usage information output
using a Go template.

Valid placeholders for the Go template are:

- `.ID`
- `.Parents`
- `.CreatedAt`
- `.Mutable`
- `.Reclaimable`
- `.Shared`
- `.Size`
- `.Description`
- `.UsageCount`
- `.LastUsedAt`
- `.Type`

When using the `--format` option, the `du` command will either output the data
exactly as the template declares or, when using the `table` directive, includes
column headers as well.

The `pretty` format is useful for inspecting the disk usage records in more
detail. It shows the mutable and shared states more clearly, as well as
additional information about the corresponding layer:

```console
$ docker buildx du --format=pretty
...
ID:           6wqu0v6hjdwvhh8yjozrepaof
Parents:
 - bqx15bcewecz4wcg14b7iodvp
Created at:   2025-06-12 15:44:02.715795569 +0000 UTC
Mutable:      false
Reclaimable:  true
Shared:       true
Size:         1.653GB
Description:  [build-base 4/4] COPY . .
Usage count:  1
Last used:    2 months ago
Type:         regular

Shared:         35.57GB
Private:        97.94GB
Reclaimable:    131.5GB
Total:          133.5GB
```

The following example uses a template without headers and outputs the
`ID` and `Size` entries separated by a colon (`:`):

```console
$ docker buildx du --format "{{.ID}}: {{.Size}}"
6wqu0v6hjdwvhh8yjozrepaof: 1.653GB
4m8061kctvjyh9qleus8rgpgx: 1.723GB
fcm9mlz2641u8r5eicjqdhy1l: 1.841GB
z2qu1swvo3afzd9mhihi3l5k0: 1.873GB
nmi6asc00aa3ja6xnt6o7wbrr: 2.027GB
0qlam41jxqsq6i27yqllgxed3: 2.495GB
3w9qhzzskq5jc262snfu90bfz: 2.617GB
```

The following example uses a `table` template and outputs the `ID` and
`Description`:

```console
$ docker buildx du --format "table {{.ID}}    {{.Description}}"
ID                           DESCRIPTION
03bbhchaib8cygqs68um6hfnl    [binaries-linux 2/5] LINK COPY --link --from=binfmt-filter /out/ /
2h8un0tyg57oj64xvbas6mzea    [cni-plugins-export 2/4] LINK COPY --link --from=cni-plugins /opt/cni/bin/loopback /buildkit-cni-loopback
evckox33t07ob9dmollhn4h4j    [cni-plugins-export 3/4] LINK COPY --link --from=cni-plugins /opt/cni/bin/host-local /buildkit-cni-host-local
jlxzwcw6xaomxj8irerow9bhb    [binaries-linux 4/5] LINK COPY --link --from=buildctl /usr/bin/buildctl /
ov2oetgebkhpsw39rv1sbh5w1    [buildkit-linux 1/1] LINK COPY --link --from=binaries / /usr/bin/
ruoczhyq25n5v9ld7n231zalx    [binaries-linux 3/5] LINK COPY --link --from=cni-plugins-export-squashed / /
ax7cov6kizxi9ufvcwsef4occ*   local source for context
```

JSON output is also supported and will print as newline delimited JSON:

```console
$ docker buildx du --format=json
{"CreatedAt":"2025-07-29T12:36:01Z","Description":"pulled from docker.io/library/rust:1.85.1-bookworm@sha256:e51d0265072d2d9d5d320f6a44dde6b9ef13653b035098febd68cce8fa7c0bc4","ID":"ic1gfidvev5nciupzz53alel4","LastUsedAt":"2025-07-29T12:36:01Z","Mutable":false,"Parents":["hmpdhm4sjrfpmae4xm2y3m0ra"],"Reclaimable":true,"Shared":false,"Size":"829889526","Type":"regular","UsageCount":1}
{"CreatedAt":"2025-08-05T09:24:09Z","Description":"pulled from docker.io/library/node:22@sha256:3218f0d1b9e4b63def322e9ae362d581fbeac1ef21b51fc502ef91386667ce92","ID":"jsw7fx09l5zsda3bri1z4mwk5","LastUsedAt":"2025-08-05T09:24:09Z","Mutable":false,"Parents":["098jsj5ebbv1w47ikqigeuurs"],"Reclaimable":true,"Shared":true,"Size":"829898832","Type":"regular","UsageCount":1}
```

You can use `jq` to pretty-print the JSON output:

```console
$ docker buildx du --format=json | jq .
{
  "CreatedAt": "2025-07-29T12:36:01Z",
  "Description": "pulled from docker.io/library/rust:1.85.1-bookworm@sha256:e51d0265072d2d9d5d320f6a44dde6b9ef13653b035098febd68cce8fa7c0bc4",
  "ID": "ic1gfidvev5nciupzz53alel4",
  "LastUsedAt": "2025-07-29T12:36:01Z",
  "Mutable": false,
  "Parents": [
    "hmpdhm4sjrfpmae4xm2y3m0ra"
  ],
  "Reclaimable": true,
  "Shared": false,
  "Size": "829889526",
  "Type": "regular",
  "UsageCount": 1
}
{
  "CreatedAt": "2025-08-05T09:24:09Z",
  "Description": "pulled from docker.io/library/node:22@sha256:3218f0d1b9e4b63def322e9ae362d581fbeac1ef21b51fc502ef91386667ce92",
  "ID": "jsw7fx09l5zsda3bri1z4mwk5",
  "LastUsedAt": "2025-08-05T09:24:09Z",
  "Mutable": false,
  "Parents": [
    "098jsj5ebbv1w47ikqigeuurs"
  ],
  "Reclaimable": true,
  "Shared": true,
  "Size": "829898832",
  "Type": "regular",
  "UsageCount": 1
}
```

### Use verbose output (--verbose)

Shorthand for [--format=pretty](#format):

```console
$ docker buildx du --verbose
...
ID:           6wqu0v6hjdwvhh8yjozrepaof
Parents:
 - bqx15bcewecz4wcg14b7iodvp
Created at:   2025-06-12 15:44:02.715795569 +0000 UTC
Mutable:      false
Reclaimable:  true
Shared:       true
Size:         1.653GB
Description:  [build-base 4/4] COPY . .
Usage count:  1
Last used:    2 months ago
Type:         regular

Shared:         35.57GB
Private:        97.94GB
Reclaimable:    131.5GB
Total:          133.5GB
```

### Override the configured builder instance (--builder)

Use the `--builder` flag to inspect the disk usage of a particular builder.

```console
$ docker buildx du --builder mybuilder
ID                                RECLAIMABLE    SIZE          LAST ACCESSED
g41agepgdczekxg2mtw0dujsv*        true           1.312GB       47 hours ago
e6ycrsa0bn9akigqgzu0sc6kr         true           318MB         47 hours ago
our9zg4ndly65ze1ccczdksiz         true           204.9MB       45 hours ago
b7xv3xpxnwupc81tc9ya3mgq6*        true           120.6MB       47 hours ago
zihgye15ss6vum3wmck9egdoy*        true           79.81MB       2 days ago
aaydharssv1ug98yhuwclkfrh*        true           79.81MB       2 days ago
ta1r4vmnjug5dhub76as4kkol*        true           74.51MB       47 hours ago
murma9f83j9h8miifbq68udjf*        true           74.51MB       47 hours ago
47f961866a49g5y8myz80ixw1*        true           74.51MB       47 hours ago
tzh99xtzlaf6txllh3cobag8t         true           74.49MB       47 hours ago
ld6laoeuo1kwapysu6afwqybl*        true           59.89MB       47 hours ago
yitxizi5kaplpyomqpos2cryp*        true           59.83MB       47 hours ago
iy8aa4b7qjn0qmy9wiga9cj8w         true           33.65MB       47 hours ago
mci7okeijyp8aqqk16j80dy09         true           19.86MB       47 hours ago
lqvj091he652slxdla4wom3pz         true           14.08MB       47 hours ago
fkt31oiv793nd26h42llsjcw7*        true           11.87MB       2 days ago
uj802yxtvkcjysnjb4kgwvn2v         true           11.68MB       45 hours ago
Reclaimable:    2.627GB
Total:          2.627GB
```

---

# docker buildx history export

# docker buildx history export

| Description | Export build records into Docker Desktop bundle |
| --- | --- |
| Usage | docker buildx history export [OPTIONS] [REF...] |

## Description

Export one or more build records to `.dockerbuild` archive files. These archives
contain metadata, logs, and build outputs, and can be imported into Docker
Desktop or shared across environments.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all |  | Export all build records for the builder |
| --finalize |  | Ensure build records are finalized before exporting |
| -o, --output |  | Output file path |

## Examples

### Export all build records to a file (--all)

Use the `--all` flag and redirect the output:

```console
docker buildx history export --all > all-builds.dockerbuild
```

Or use the `--output` flag:

```console
docker buildx history export --all -o all-builds.dockerbuild
```

### Use a specific builder instance (--builder)

```console
docker buildx history export --builder builder0 ^1 -o builder0-build.dockerbuild
```

### Enable debug logging (--debug)

```console
docker buildx history export --debug qu2gsuo8ejqrwdfii23xkkckt -o debug-build.dockerbuild
```

### Ensure build records are finalized before exporting (--finalize)

Clients can report their own traces concurrently, and not all traces may be
saved yet by the time of the export. Use the `--finalize` flag to ensure all
traces are finalized before exporting.

```console
docker buildx history export --finalize qu2gsuo8ejqrwdfii23xkkckt -o finalized-build.dockerbuild
```

### Export a single build to a custom file (--output)

```console
docker buildx history export qu2gsuo8ejqrwdfii23xkkckt --output mybuild.dockerbuild
```

You can find build IDs by running:

```console
docker buildx history ls
```

To export two builds to separate files:

```console
# Using build IDs
docker buildx history export qu2gsuo8ejqrwdfii23xkkckt qsiifiuf1ad9pa9qvppc0z1l3 -o multi.dockerbuild

# Or using relative offsets
docker buildx history export ^1 ^2 -o multi.dockerbuild
```

Or use shell redirection:

```console
docker buildx history export ^1 > mybuild.dockerbuild
docker buildx history export ^2 > backend-build.dockerbuild
```

---

# docker buildx history import

# docker buildx history import

| Description | Import build records into Docker Desktop |
| --- | --- |
| Usage | docker buildx history import [OPTIONS] - |

## Description

Import a build record from a `.dockerbuild` archive into Docker Desktop. This
lets you view, inspect, and analyze builds created in other environments or CI
pipelines.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --file |  | Import from a file path |

## Examples

### Import a.dockerbuildarchive from standard input

```console
docker buildx history import < mybuild.dockerbuild
```

### Import a build archive from a file (--file)

```console
docker buildx history import --file ./artifacts/backend-build.dockerbuild
```

### Open a build manually

By default, the `import` command automatically opens the imported build in Docker
Desktop. You don't need to run `open` unless you're opening a specific build
or re-opening it later.

If you've imported multiple builds, you can open one manually:

```console
docker buildx history open ci-build
```

---

# docker buildx history inspect attachment

# docker buildx history inspect attachment

| Description | Inspect a build record attachment |
| --- | --- |
| Usage | docker buildx history inspect attachment [OPTIONS] [REF [DIGEST]] |

## Description

Inspect a specific attachment from a build record, such as a provenance file or
SBOM. Attachments are optional artifacts stored with the build and may be
platform-specific.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --platform |  | Platform of attachment |
| --type |  | Type of attachment |

## Examples

### Inspect an attachment by platform (--platform)

```console
$ docker buildx history inspect attachment --platform linux/amd64
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:814e63f06465bc78123775714e4df1ebdda37e6403e0b4f481df74947c047163",
    "size": 600
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:36537f3920ae948ce3e12b4ae34c21190280e6e7d58eeabde0dff3fdfb43b6b0",
      "size": 21664137
    }
  ]
}
```

### Inspect an attachment by type (--type)

Supported types include:

- `index`
- `manifest`
- `image`
- `provenance`
- `sbom`

#### Index

```console
$ docker buildx history inspect attachment --type index
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:a194e24f47dc6d0e65992c09577b9bc4e7bd0cd5cc4f81e7738918f868aa397b",
      "size": 481,
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:49e40223d6a96ea0667a12737fd3dde004cf217eb48cb28c9191288cd44c6ace",
      "size": 839,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:a194e24f47dc6d0e65992c09577b9bc4e7bd0cd5cc4f81e7738918f868aa397b",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
        "architecture": "unknown",
        "os": "unknown"
      }
    }
  ]
}
```

#### Manifest

```console
$ docker buildx history inspect attachment --type manifest
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:814e63f06465bc78123775714e4df1ebdda37e6403e0b4f481df74947c047163",
    "size": 600
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:36537f3920ae948ce3e12b4ae34c21190280e6e7d58eeabde0dff3fdfb43b6b0",
      "size": 21664137
    }
  ]
}
```

#### Provenance

```console
$ docker buildx history inspect attachment --type provenance
{
  "builder": {
    "id": ""
  },
  "buildType": "https://mobyproject.org/buildkit@v1",
  "materials": [
    {
      "uri": "pkg:docker/docker/dockerfile@1",
      "digest": {
        "sha256": "9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc"
      }
    },
    {
      "uri": "pkg:docker/golang@1.19.4-alpine?platform=linux%2Farm64",
      "digest": {
        "sha256": "a9b24b67dc83b3383d22a14941c2b2b2ca6a103d805cac6820fd1355943beaf1"
      }
    }
  ],
  "invocation": {
    "configSource": {
      "entryPoint": "Dockerfile"
    },
    "parameters": {
      "frontend": "gateway.v0",
      "args": {
        "cmdline": "docker/dockerfile:1",
        "source": "docker/dockerfile:1",
        "target": "binaries"
      },
      "locals": [
        {
          "name": "context"
        },
        {
          "name": "dockerfile"
        }
      ]
    },
    "environment": {
      "platform": "linux/arm64"
    }
  },
  "metadata": {
    "buildInvocationID": "c4a87v0sxhliuewig10gnsb6v",
    "buildStartedOn": "2022-12-16T08:26:28.651359794Z",
    "buildFinishedOn": "2022-12-16T08:26:29.625483253Z",
    "reproducible": false,
    "completeness": {
      "parameters": true,
      "environment": true,
      "materials": false
    },
    "https://mobyproject.org/buildkit@v1#metadata": {
      "vcs": {
        "revision": "a9ba846486420e07d30db1107411ac3697ecab68",
        "source": "git@github.com:<org>/<repo>.git"
      }
    }
  }
}
```

### Inspect an attachment by digest

You can inspect an attachment directly using its digset, which you can get from
the `inspect` output:

```console
# Using a build ID
docker buildx history inspect attachment qu2gsuo8ejqrwdfii23xkkckt sha256:abcdef123456...

# Or using a relative offset
docker buildx history inspect attachment ^0 sha256:abcdef123456...
```

Use `--type sbom` or `--type provenance` to filter attachments by type. To
inspect a specific attachment by digest, omit the `--type` flag.

---

# docker buildx history inspect

# docker buildx history inspect

| Description | Inspect a build record |
| --- | --- |
| Usage | docker buildx history inspect [OPTIONS] [REF] |

## Description

Inspect a build record to view metadata such as duration, status, build inputs,
platforms, outputs, and attached artifacts. You can also use flags to extract
provenance, SBOMs, or other detailed information.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | pretty | Format the output |

## Examples

### Inspect the most recent build

```console
$ docker buildx history inspect
Name:           buildx (binaries)
Context:        .
Dockerfile:     Dockerfile
VCS Repository: https://github.com/crazy-max/buildx.git
VCS Revision:   f15eaa1ee324ffbbab29605600d27a84cab86361
Target:         binaries
Platforms:      linux/amd64
Keep Git Dir:   true

Started:        2025-02-07 11:56:24
Duration:       1m  1s
Build Steps:    16/16 (25% cached)

Image Resolve Mode:     local

Materials:
URI                                                             DIGEST
pkg:docker/docker/dockerfile@1                                  sha256:93bfd3b68c109427185cd78b4779fc82b484b0b7618e36d0f104d4d801e66d25
pkg:docker/golang@1.23-alpine3.21?platform=linux%2Famd64        sha256:2c49857f2295e89b23b28386e57e018a86620a8fede5003900f2d138ba9c4037
pkg:docker/tonistiigi/xx@1.6.1?platform=linux%2Famd64           sha256:923441d7c25f1e2eb5789f82d987693c47b8ed987c4ab3b075d6ed2b5d6779a3

Attachments:
DIGEST                                                                  PLATFORM        TYPE
sha256:217329d2af959d4f02e3a96dcbe62bf100cab1feb8006a047ddfe51a5397f7e3                 https://slsa.dev/provenance/v0.2
```

### Inspect a specific build

```console
# Using a build ID
docker buildx history inspect qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history inspect ^1
```

### Format the output (--format)

The formatting options (`--format`) pretty-prints the output to `pretty` (default),
`json` or using a Go template.

#### Pretty output

```console
$ docker buildx history inspect
Name:           buildx (binaries)
Context:        .
Dockerfile:     Dockerfile
VCS Repository: https://github.com/crazy-max/buildx.git
VCS Revision:   f15eaa1ee324ffbbab29605600d27a84cab86361
Target:         binaries
Platforms:      linux/amd64
Keep Git Dir:   true

Started:        2025-02-07 11:56:24
Duration:       1m  1s
Build Steps:    16/16 (25% cached)

Image Resolve Mode:     local

Materials:
URI                                                             DIGEST
pkg:docker/docker/dockerfile@1                                  sha256:93bfd3b68c109427185cd78b4779fc82b484b0b7618e36d0f104d4d801e66d25
pkg:docker/golang@1.23-alpine3.21?platform=linux%2Famd64        sha256:2c49857f2295e89b23b28386e57e018a86620a8fede5003900f2d138ba9c4037
pkg:docker/tonistiigi/xx@1.6.1?platform=linux%2Famd64           sha256:923441d7c25f1e2eb5789f82d987693c47b8ed987c4ab3b075d6ed2b5d6779a3

Attachments:
DIGEST                                                                  PLATFORM        TYPE
sha256:217329d2af959d4f02e3a96dcbe62bf100cab1feb8006a047ddfe51a5397f7e3                 https://slsa.dev/provenance/v0.2

Print build logs: docker buildx history logs g9808bwrjrlkbhdamxklx660b
```

#### JSON output

```console
$ docker buildx history inspect --format json
{
  "Name": "buildx (binaries)",
  "Ref": "5w7vkqfi0rf59hw4hnmn627r9",
  "Context": ".",
  "Dockerfile": "Dockerfile",
  "VCSRepository": "https://github.com/crazy-max/buildx.git",
  "VCSRevision": "f15eaa1ee324ffbbab29605600d27a84cab86361",
  "Target": "binaries",
  "Platform": [
    "linux/amd64"
  ],
  "KeepGitDir": true,
  "StartedAt": "2025-02-07T12:01:05.75807272+01:00",
  "CompletedAt": "2025-02-07T12:02:07.991778875+01:00",
  "Duration": 62233706155,
  "Status": "completed",
  "NumCompletedSteps": 16,
  "NumTotalSteps": 16,
  "NumCachedSteps": 4,
  "Config": {
    "ImageResolveMode": "local"
  },
  "Materials": [
    {
      "URI": "pkg:docker/docker/dockerfile@1",
      "Digests": [
        "sha256:93bfd3b68c109427185cd78b4779fc82b484b0b7618e36d0f104d4d801e66d25"
      ]
    },
    {
      "URI": "pkg:docker/golang@1.23-alpine3.21?platform=linux%2Famd64",
      "Digests": [
        "sha256:2c49857f2295e89b23b28386e57e018a86620a8fede5003900f2d138ba9c4037"
      ]
    },
    {
      "URI": "pkg:docker/tonistiigi/xx@1.6.1?platform=linux%2Famd64",
      "Digests": [
        "sha256:923441d7c25f1e2eb5789f82d987693c47b8ed987c4ab3b075d6ed2b5d6779a3"
      ]
    }
  ],
  "Attachments": [
    {
      "Digest": "sha256:450fdd2e6b868fecd69e9891c2c404ba461aa38a47663b4805edeb8d2baf80b1",
      "Type": "https://slsa.dev/provenance/v0.2"
    }
  ]
}
```

#### Go template output

```console
$ docker buildx history inspect --format "{{.Name}}: {{.VCSRepository}} ({{.VCSRevision}})"
buildx (binaries): https://github.com/crazy-max/buildx.git (f15eaa1ee324ffbbab29605600d27a84cab86361)
```

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx history inspect attachment | Inspect a build record attachment |

---

# docker buildx history logs

# docker buildx history logs

| Description | Print the logs of a build record |
| --- | --- |
| Usage | docker buildx history logs [OPTIONS] [REF] |

## Description

Print the logs for a completed build. The output appears in the same format as
`--progress=plain`, showing the full logs for each step.

By default, this shows logs for the most recent build on the current builder.

You can also specify an earlier build using an offset. For example:

- `^1` shows logs for the build before the most recent
- `^2` shows logs for the build two steps back

## Options

| Option | Default | Description |
| --- | --- | --- |
| --progress | plain | Set type of progress output (plain, rawjson, tty) |

## Examples

### Print logs for the most recent build

```console
$ docker buildx history logs
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 31B done
#1 DONE 0.0s
#2 [internal] load .dockerignore
#2 transferring context: 2B done
#2 DONE 0.0s
...
```

By default, this shows logs for the most recent build on the current builder.

### Print logs for a specific build

To print logs for a specific build, use a build ID or offset:

```console
# Using a build ID
docker buildx history logs qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history logs ^1
```

### Set type of progress output (--progress)

```console
$ docker buildx history logs ^1 --progress rawjson
{"id":"buildx_step_1","status":"START","timestamp":"2024-05-01T12:34:56.789Z","detail":"[internal] load build definition from Dockerfile"}
{"id":"buildx_step_1","status":"COMPLETE","timestamp":"2024-05-01T12:34:57.001Z","duration":212000000}
...
```

---

# docker buildx history ls

# docker buildx history ls

| Description | List build records |
| --- | --- |
| Usage | docker buildx history ls [OPTIONS] |

## Description

List completed builds recorded by the active builder. Each entry includes the
build ID, name, status, timestamp, and duration.

By default, only records for the current builder are shown. You can filter
results using flags.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --filter |  | Provide filter values (e.g.,status=error) |
| --format | table | Format the output |
| --local |  | List records for current repository only |
| --no-trunc |  | Don't truncate output |

## Examples

### List all build records for the current builder

```console
$ docker buildx history ls
BUILD ID                    NAME           STATUS     CREATED AT        DURATION
qu2gsuo8ejqrwdfii23xkkckt   .dev/2850      Completed  3 days ago        1.4s
qsiifiuf1ad9pa9qvppc0z1l3   .dev/2850      Completed  3 days ago        1.3s
g9808bwrjrlkbhdamxklx660b   .dev/3120      Completed  5 days ago        2.1s
```

### List failed builds (--filter)

```console
docker buildx history ls --filter status=error
```

You can filter the list using the `--filter` flag. Supported filters include:

| Filter | Supported comparisons | Example |
| --- | --- | --- |
| ref,repository,status | Support=and!=comparisons | --filter status!=success |
| startedAt,completedAt,duration | Support<and>comparisons with time values | --filter duration>30s |

You can combine multiple filters by repeating the `--filter` flag:

```console
docker buildx history ls --filter status=error --filter duration>30s
```

### List builds from the current project (--local)

```console
docker buildx history ls --local
```

### Display full output without truncation (--no-trunc)

```console
docker buildx history ls --no-trunc
```

### Format output (--format)

#### JSON output

```console
$ docker buildx history ls --format json
[
  {
    "ID": "qu2gsuo8ejqrwdfii23xkkckt",
    "Name": ".dev/2850",
    "Status": "Completed",
    "CreatedAt": "2025-04-15T12:33:00Z",
    "Duration": "1.4s"
  },
  {
    "ID": "qsiifiuf1ad9pa9qvppc0z1l3",
    "Name": ".dev/2850",
    "Status": "Completed",
    "CreatedAt": "2025-04-15T12:29:00Z",
    "Duration": "1.3s"
  }
]
```

#### Go template output

```console
$ docker buildx history ls --format '{{.Name}} - {{.Duration}}'
.dev/2850 - 1.4s
.dev/2850 - 1.3s
.dev/3120 - 2.1s
```

---

# docker buildx history open

# docker buildx history open

| Description | Open a build record in Docker Desktop |
| --- | --- |
| Usage | docker buildx history open [OPTIONS] [REF] |

## Description

Open a build record in Docker Desktop for visual inspection. This requires
Docker Desktop to be installed and running on the host machine.

## Examples

### Open the most recent build in Docker Desktop

```console
docker buildx history open
```

By default, this opens the most recent build on the current builder.

### Open a specific build

```console
# Using a build ID
docker buildx history open qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history open ^1
```

---

# docker buildx history rm

# docker buildx history rm

| Description | Remove build records |
| --- | --- |
| Usage | docker buildx history rm [OPTIONS] [REF...] |

## Description

Remove one or more build records from the current builder’s history. You can
remove specific builds by ID or offset, or delete all records at once using
the `--all` flag.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all |  | Remove all build records |

## Examples

### Remove a specific build

```console
# Using a build ID
docker buildx history rm qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history rm ^1
```

### Remove multiple builds

```console
# Using build IDs
docker buildx history rm qu2gsuo8ejqrwdfii23xkkckt qsiifiuf1ad9pa9qvppc0z1l3

# Or using relative offsets
docker buildx history rm ^1 ^2
```

### Remove all build records from the current builder (--all)

```console
docker buildx history rm --all
```

---

# docker buildx history trace

# docker buildx history trace

| Description | Show the OpenTelemetry trace of a build record |
| --- | --- |
| Usage | docker buildx history trace [OPTIONS] [REF] |

## Description

View the OpenTelemetry trace for a completed build. This command loads the
trace into a Jaeger UI viewer and opens it in your browser.

This helps analyze build performance, step timing, and internal execution flows.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --addr | 127.0.0.1:0 | Address to bind the UI server |
| --compare |  | Compare with another build record |

## Examples

### Open the OpenTelemetry trace for the most recent build

This command starts a temporary Jaeger UI server and opens your default browser
to view the trace.

```console
docker buildx history trace
```

### Open the trace for a specific build

```console
# Using a build ID
docker buildx history trace qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history trace ^1
```

### Run the Jaeger UI on a specific port (--addr)

```console
# Using a build ID
docker buildx history trace qu2gsuo8ejqrwdfii23xkkckt --addr 127.0.0.1:16686

# Or using a relative offset
docker buildx history trace ^1 --addr 127.0.0.1:16686
```

### Compare two build traces (--compare)

Compare two specific builds by name:

```console
# Using build IDs
docker buildx history trace --compare=qu2gsuo8ejqrwdfii23xkkckt qsiifiuf1ad9pa9qvppc0z1l3

# Or using a single relative offset
docker buildx history trace --compare=^1
```

When you use a single reference with `--compare`, it compares that build
against the most recent one.

---

# docker buildx history

# docker buildx history

| Description | Commands to work on build records |
| --- | --- |
| Usage | docker buildx history |

## Description

Commands to work on build records

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx history export | Export build records into Docker Desktop bundle |
| docker buildx history import | Import build records into Docker Desktop |
| docker buildx history inspect | Inspect a build record |
| docker buildx history logs | Print the logs of a build record |
| docker buildx history ls | List build records |
| docker buildx history open | Open a build record in Docker Desktop |
| docker buildx history rm | Remove build records |
| docker buildx history trace | Show the OpenTelemetry trace of a build record |
