# docker trust key generate and more

# docker trust key generate

# docker trust key generate

| Description | Generate and load a signing key-pair |
| --- | --- |
| Usage | docker trust key generate NAME |

## Description

`docker trust key generate` generates a key-pair to be used with signing,
and loads the private key into the local Docker trust keystore.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --dir |  | Directory to generate key in, defaults to current directory |

## Examples

### Generate a key-pair

```console
$ docker trust key generate alice

Generating key for alice...
Enter passphrase for new alice key with ID 17acf3c:
Repeat passphrase for new alice key with ID 17acf3c:
Successfully generated and loaded private key. Corresponding public key available: alice.pub
$ ls
alice.pub
```

The private signing key is encrypted by the passphrase and loaded into the Docker trust keystore.
All passphrase requests to sign with the key will be referred to by the provided `NAME`.

The public key component `alice.pub` will be available in the current working directory, and can
be used directly by `docker trust signer add`.

Provide the `--dir` argument to specify a directory to generate the key in:

```console
$ docker trust key generate alice --dir /foo

Generating key for alice...
Enter passphrase for new alice key with ID 17acf3c:
Repeat passphrase for new alice key with ID 17acf3c:
Successfully generated and loaded private key. Corresponding public key available: alice.pub
$ ls /foo
alice.pub
```

---

# docker trust key load

# docker trust key load

| Description | Load a private key file for signing |
| --- | --- |
| Usage | docker trust key load [OPTIONS] KEYFILE |

## Description

`docker trust key load` adds private keys to the local Docker trust keystore.

To add a signer to a repository use `docker trust signer add`.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --name | signer | Name for the loaded key |

## Examples

### Load a single private key

For a private key `alice.pem` with permissions `-rw-------`

```console
$ docker trust key load alice.pem

Loading key from "alice.pem"...
Enter passphrase for new signer key with ID f8097df:
Repeat passphrase for new signer key with ID f8097df:
Successfully imported key from alice.pem
```

To specify a name use the `--name` flag:

```console
$ docker trust key load --name alice-key alice.pem

Loading key from "alice.pem"...
Enter passphrase for new alice-key key with ID f8097df:
Repeat passphrase for new alice-key key with ID f8097df:
Successfully imported key from alice.pem
```

---

# docker trust key

# docker trust key

| Description | Manage keys for signing Docker images |
| --- | --- |
| Usage | docker trust key |

## Description

Manage keys for signing Docker images

## Subcommands

| Command | Description |
| --- | --- |
| docker trust key generate | Generate and load a signing key-pair |
| docker trust key load | Load a private key file for signing |

---

# docker trust revoke

# docker trust revoke

| Description | Remove trust for an image |
| --- | --- |
| Usage | docker trust revoke [OPTIONS] IMAGE[:TAG] |

## Description

`docker trust revoke` removes signatures from tags in signed repositories.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -y, --yes |  | Do not prompt for confirmation |

## Examples

### Revoke signatures from a signed tag

Here's an example of a repository with two signed tags:

```console
$ docker trust inspect --pretty example/trust-demo
SIGNED TAG          DIGEST                                                              SIGNERS
red                 852cc04935f930a857b630edc4ed6131e91b22073bcc216698842e44f64d2943    alice
blue                f1c38dbaeeb473c36716f6494d803fbfbe9d8a76916f7c0093f227821e378197    alice, bob

List of signers and their keys for example/trust-demo:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

When `alice`, one of the signers, runs `docker trust revoke`:

```console
$ docker trust revoke example/trust-demo:red
Enter passphrase for delegation key with ID 27d42a8:
Successfully deleted signature for example/trust-demo:red
```

After revocation, the tag is removed from the list of released tags:

```console
$ docker trust inspect --pretty example/trust-demo
SIGNED TAG          DIGEST                                                              SIGNERS
blue                f1c38dbaeeb473c36716f6494d803fbfbe9d8a76916f7c0093f227821e378197    alice, bob

List of signers and their keys for example/trust-demo:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

### Revoke signatures on all tags in a repository

When no tag is specified, `docker trust` revokes all signatures that you have a signing key for.

```console
$ docker trust inspect --pretty example/trust-demo
SIGNED TAG          DIGEST                                                              SIGNERS
red                 852cc04935f930a857b630edc4ed6131e91b22073bcc216698842e44f64d2943    alice
blue                f1c38dbaeeb473c36716f6494d803fbfbe9d8a76916f7c0093f227821e378197    alice, bob

List of signers and their keys for example/trust-demo:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

When `alice`, one of the signers, runs `docker trust revoke`:

```console
$ docker trust revoke example/trust-demo
Confirm you would like to delete all signature data for example/trust-demo? [y/N] y
Enter passphrase for delegation key with ID 27d42a8:
Successfully deleted signature for example/trust-demo
```

All tags that have `alice`'s signature on them are removed from the list of released tags:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo

List of signers and their keys for example/trust-demo:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

---

# docker trust sign

# docker trust sign

| Description | Sign an image |
| --- | --- |
| Usage | docker trust sign IMAGE:TAG |

## Description

`docker trust sign` adds signatures to tags to create signed repositories.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --local |  | Sign a locally tagged image |

## Examples

### Sign a tag as a repository admin

Given an image:

```console
$ docker trust inspect --pretty example/trust-demo

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  c24134c079c35e698060beabe110bb83ab285d0d978de7d92fed2c8c83570a41   (Repo Admin)

Administrative keys for example/trust-demo:
Repository Key: 36d4c3601102fa7c5712a343c03b94469e5835fb27c191b529c06fd19c14a942
Root Key:       246d360f7c53a9021ee7d4259e3c5692f3f1f7ad4737b1ea8c7b8da741ad980b
```

Sign a new tag with `docker trust sign`:

```console
$ docker trust sign example/trust-demo:v2

Signing and pushing trust metadata for example/trust-demo:v2
The push refers to a repository [docker.io/example/trust-demo]
eed4e566104a: Layer already exists
77edfb6d1e3c: Layer already exists
c69f806905c2: Layer already exists
582f327616f1: Layer already exists
a3fbb648f0bd: Layer already exists
5eac2de68a97: Layer already exists
8d4d1ab5ff74: Layer already exists
v2: digest: sha256:8f6f460abf0436922df7eb06d28b3cdf733d2cac1a185456c26debbff0839c56 size: 1787
Signing and pushing trust metadata
Enter passphrase for repository key with ID 36d4c36:
Successfully signed docker.io/example/trust-demo:v2
```

Use `docker trust inspect --pretty` to list the new signature:

```console
$ docker trust inspect --pretty example/trust-demo

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  c24134c079c35e698060beabe110bb83ab285d0d978de7d92fed2c8c83570a41   (Repo Admin)
v2                  8f6f460abf0436922df7eb06d28b3cdf733d2cac1a185456c26debbff0839c56   (Repo Admin)

Administrative keys for example/trust-demo:
Repository Key: 36d4c3601102fa7c5712a343c03b94469e5835fb27c191b529c06fd19c14a942
Root Key:       246d360f7c53a9021ee7d4259e3c5692f3f1f7ad4737b1ea8c7b8da741ad980b
```

### Sign a tag as a signer

Given an image:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo

List of signers and their keys for example/trust-demo:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

Sign a new tag with `docker trust sign`:

```console
$ docker trust sign example/trust-demo:v1

Signing and pushing trust metadata for example/trust-demo:v1
The push refers to a repository [docker.io/example/trust-demo]
26b126eb8632: Layer already exists
220d34b5f6c9: Layer already exists
8a5132998025: Layer already exists
aca233ed29c3: Layer already exists
e5d2f035d7a4: Layer already exists
v1: digest: sha256:74d4bfa917d55d53c7df3d2ab20a8d926874d61c3da5ef6de15dd2654fc467c4 size: 1357
Signing and pushing trust metadata
Enter passphrase for delegation key with ID 27d42a8:
Successfully signed docker.io/example/trust-demo:v1
```

`docker trust inspect --pretty` lists the new signature:

```console
$ docker trust inspect --pretty example/trust-demo

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  74d4bfa917d55d53c7df3d2ab20a8d926874d61c3da5ef6de15dd2654fc467c4   alice

List of signers and their keys for example/trust-demo:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

---

# docker trust signer add

# docker trust signer add

| Description | Add a signer |
| --- | --- |
| Usage | docker trust signer add OPTIONS NAME REPOSITORY [REPOSITORY...] |

## Description

`docker trust signer add` adds signers to signed repositories.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --key |  | Path to the signer's public key file |

## Examples

### Add a signer to a repository

To add a new signer, `alice`, to this repository:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo

List of signers and their keys:

SIGNER              KEYS
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 642692c14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

Add `alice` with `docker trust signer add`:

```console
$ docker trust signer add alice example/trust-demo --key alice.crt
  Adding signer "alice" to example/trust-demo...
  Enter passphrase for repository key with ID 642692c:
Successfully added signer: alice to example/trust-demo
```

`docker trust inspect --pretty` now lists `alice` as a valid signer:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo

List of signers and their keys:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 642692c14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

---

# docker trust signer remove

# docker trust signer remove

| Description | Remove a signer |
| --- | --- |
| Usage | docker trust signer remove [OPTIONS] NAME REPOSITORY [REPOSITORY...] |

## Description

`docker trust signer remove` removes signers from signed repositories.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Do not prompt for confirmation before removing the most recent signer |

## Examples

### Remove a signer from a repository

To remove an existing signer, `alice`, from this repository:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo

List of signers and their keys:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

Remove `alice` with `docker trust signer remove`:

```console
$ docker trust signer remove alice example/trust-demo

Removing signer "alice" from image example/trust-demo...
Enter passphrase for repository key with ID 642692c:
Successfully removed alice from example/trust-demo
```

`docker trust inspect --pretty` now doesn't list `alice` as a valid signer:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo

List of signers and their keys:

SIGNER              KEYS
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

### Remove a signer from multiple repositories

To remove an existing signer, `alice`, from multiple repositories:

```console
$ docker trust inspect --pretty example/trust-demo

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  74d4bfa917d55d53c7df3d2ab20a8d926874d61c3da5ef6de15dd2654fc467c4   alice, bob

List of signers and their keys:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 95b9e5514c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

```console
$ docker trust inspect --pretty example/trust-demo2

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  74d4bfa917d55d53c7df3d2ab20a8d926874d61c3da5ef6de15dd2654fc467c4   alice, bob

List of signers and their keys:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo2:
Repository Key: ece554f14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4553d2ab20a8d9268
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

Remove `alice` from both images with a single `docker trust signer remove` command:

```console
$ docker trust signer remove alice example/trust-demo example/trust-demo2

Removing signer "alice" from image example/trust-demo...
Enter passphrase for repository key with ID 95b9e55:
Successfully removed alice from example/trust-demo

Removing signer "alice" from image example/trust-demo2...
Enter passphrase for repository key with ID ece554f:
Successfully removed alice from example/trust-demo2
```

Run `docker trust inspect --pretty` to confirm that `alice` is no longer listed as a valid
signer of either `example/trust-demo` or `example/trust-demo2`:

```console
$ docker trust inspect --pretty example/trust-demo

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  74d4bfa917d55d53c7df3d2ab20a8d926874d61c3da5ef6de15dd2654fc467c4   bob

List of signers and their keys:

SIGNER              KEYS
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: ecc457614c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

```console
$ docker trust inspect --pretty example/trust-demo2

SIGNED TAG          DIGEST                                                             SIGNERS
v1                  74d4bfa917d55d53c7df3d2ab20a8d926874d61c3da5ef6de15dd2654fc467c4   bob

List of signers and their keys:

SIGNER              KEYS
bob                 5600f5ab76a2

Administrative keys for example/trust-demo2:
Repository Key: ece554f14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4553d2ab20a8d9268
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

`docker trust signer remove` removes signers to repositories on a best effort basis.
It continues to remove the signer from subsequent repositories if one attempt fails:

```console
$ docker trust signer remove alice example/unauthorized example/authorized

Removing signer "alice" from image example/unauthorized...
No signer alice for image example/unauthorized

Removing signer "alice" from image example/authorized...
Enter passphrase for repository key with ID c6772a0:
Successfully removed alice from example/authorized

Error removing signer from: example/unauthorized
```

---

# docker trust signer

# docker trust signer

| Description | Manage entities who can sign Docker images |
| --- | --- |
| Usage | docker trust signer |

## Description

Manage entities who can sign Docker images

## Subcommands

| Command | Description |
| --- | --- |
| docker trust signer add | Add a signer |
| docker trust signer remove | Remove a signer |

---

# docker trust

# docker trust

| Description | Manage trust on Docker images |
| --- | --- |
| Usage | docker trust |

## Description

Manage trust on Docker images

## Subcommands

| Command | Description |
| --- | --- |
| docker trust inspect | Return low-level information about keys and signatures |
| docker trust key | Manage keys for signing Docker images |
| docker trust revoke | Remove trust for an image |
| docker trust sign | Sign an image |
| docker trust signer | Manage entities who can sign Docker images |

---

# docker version

# docker version

| Description | Show the Docker version information |
| --- | --- |
| Usage | docker version [OPTIONS] |

## Description

The version command prints the current version number for all independently
versioned Docker components. Use the [--format](#format) option to customize
the output.

The version command (`docker version`) outputs the version numbers of Docker
components, while the `--version` flag (`docker --version`) outputs the version
number of the Docker CLI you are using.

### Default output

The default output renders all version information divided into two sections;
the `Client` section contains information about the Docker CLI and client
components, and the `Server` section contains information about the Docker
Engine and components used by the Docker Engine, such as the containerd and runc
OCI Runtimes.

The information shown may differ depending on how you installed Docker and
what components are in use. The following example shows the output on a macOS
machine running Docker Desktop:

```console
$ docker version

Client: Docker Engine - Community
 Version:           28.5.1
 API version:       1.51
 Go version:        go1.24.8
 Git commit:        e180ab8
 Built:             Wed Oct  8 12:16:17 2025
 OS/Arch:           darwin/arm64
 Context:           remote-test-server

Server: Docker Desktop 4.19.0 (12345)
 Engine:
  Version:          27.5.1
  API version:      1.47 (minimum version 1.24)
  Go version:       go1.22.11
  Git commit:       4c9b3b0
  Built:            Wed Jan 22 13:41:24 2025
  OS/Arch:          linux/amd64
  Experimental:     true
 containerd:
  Version:          v1.7.25
  GitCommit:        bcc810d6b9066471b0b6fa75f557a15a1cbf31bb
 runc:
  Version:          1.2.4
  GitCommit:        v1.2.4-0-g6c52b3f
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

### Client and server versions

Docker uses a client/server architecture, which allows you to use the Docker CLI
on your local machine to control a Docker Engine running on a remote machine,
which can be (for example) a machine running in the cloud or inside a virtual machine.

The following example switches the Docker CLI to use a
[context](https://docs.docker.com/reference/cli/docker/context/)
named `remote-test-server`, which runs an older version of the Docker Engine
on a Linux server:

```console
$ docker context use remote-test-server
remote-test-server

$ docker version

Client: Docker Engine - Community
 Version:           28.5.1
 API version:       1.51
 Go version:        go1.24.8
 Git commit:        e180ab8
 Built:             Wed Oct  8 12:16:17 2025
 OS/Arch:           darwin/arm64
 Context:           remote-test-server

Server: Docker Engine - Community
 Engine:
  Version:          27.5.1
  API version:      1.47 (minimum version 1.24)
  Go version:       go1.22.11
  Git commit:       4c9b3b0
  Built:            Wed Jan 22 13:41:24 2025
  OS/Arch:          linux/amd64
  Experimental:     true
 containerd:
  Version:          v1.7.25
  GitCommit:        bcc810d6b9066471b0b6fa75f557a15a1cbf31bb
 runc:
  Version:          1.2.4
  GitCommit:        v1.2.4-0-g6c52b3f
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

### API version and version negotiation

The API version used by the client depends on the Docker Engine that the Docker
CLI is connecting with. When connecting with the Docker Engine, the Docker CLI
and Docker Engine perform API version negotiation, and select the highest API
version that is supported by both the Docker CLI and the Docker Engine.

For example, if the CLI is connecting with Docker Engine version 27.5, it downgrades
to API version 1.47 (refer to the
[API version matrix](https://docs.docker.com/reference/api/engine/#api-version-matrix)
to learn about the supported API versions for Docker Engine):

```console
$ docker version --format '{{.Client.APIVersion}}'

1.47
```

Be aware that API version can also be overridden using the `DOCKER_API_VERSION`
environment variable, which can be useful for debugging purposes, and disables
API version negotiation. The following example illustrates an environment where
the `DOCKER_API_VERSION` environment variable is set. Unsetting the environment
variable removes the override, and re-enables API version negotiation:

```console
$ env | grep DOCKER_API_VERSION
DOCKER_API_VERSION=1.50

$ docker version --format '{{.Client.APIVersion}}'
1.50

$ unset DOCKER_API_VERSION
$ docker version --format '{{.Client.APIVersion}}'
1.51
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |

## Examples

### Format the output (--format)

The formatting option (`--format`) pretty-prints the output using a Go template,
which allows you to customize the output format, or to obtain specific information
from the output. Refer to the
[format command and log output](https://docs.docker.com/config/formatting/)
page for details of the format.

### Get the server version

```console
$ docker version --format '{{.Server.Version}}'

28.5.1
```

### Get the client API version

The following example prints the API version that is used by the client:

```console
$ docker version --format '{{.Client.APIVersion}}'

1.51
```

The version shown is the API version that is negotiated between the client
and the Docker Engine. Refer to [API version and version negotiation](#api-version-and-version-negotiation)
above for more information.

### Dump raw JSON data

```console
$ docker version --format '{{json .}}'

{"Client":"Version":"28.5.1","ApiVersion":"1.51", ...}
```

---

# docker volume create

# docker volume create

| Description | Create a volume |
| --- | --- |
| Usage | docker volume create [OPTIONS] [VOLUME] |

## Description

Creates a new volume that containers can consume and store data in. If a name is
not specified, Docker generates a random name.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --availability | active | API 1.42+SwarmCluster Volume availability (active,pause,drain) |
| -d, --driver | local | Specify volume driver name |
| --group |  | API 1.42+SwarmCluster Volume group (cluster volumes) |
| --label |  | Set metadata for a volume |
| --limit-bytes |  | API 1.42+SwarmMinimum size of the Cluster Volume in bytes |
| -o, --opt |  | Set driver specific options |
| --required-bytes |  | API 1.42+SwarmMaximum size of the Cluster Volume in bytes |
| --scope | single | API 1.42+SwarmCluster Volume access scope (single,multi) |
| --secret |  | API 1.42+SwarmCluster Volume secrets |
| --sharing | none | API 1.42+SwarmCluster Volume access sharing (none,readonly,onewriter,all) |
| --topology-preferred |  | API 1.42+SwarmA topology that the Cluster Volume would be preferred in |
| --topology-required |  | API 1.42+SwarmA topology that the Cluster Volume must be accessible from |
| --type | block | API 1.42+SwarmCluster Volume access type (mount,block) |

## Examples

Create a volume and then configure the container to use it:

```console
$ docker volume create hello

hello

$ docker run -d -v hello:/world busybox ls /world
```

The mount is created inside the container's `/world` directory. Docker doesn't
support relative paths for mount points inside the container.

Multiple containers can use the same volume. This is useful if two containers
need access to shared data. For example, if one container writes and the other
reads the data.

Volume names must be unique among drivers. This means you can't use the same
volume name with two different drivers. Attempting to create two volumes with
the same name results in an error:

```console
A volume named  "hello"  already exists with the "some-other" driver. Choose a different volume name.
```

If you specify a volume name already in use on the current driver, Docker
assumes you want to reuse the existing volume and doesn't return an error.

### Driver-specific options (-o, --opt)

Some volume drivers may take options to customize the volume creation. Use the
`-o` or `--opt` flags to pass driver options:

```console
$ docker volume create --driver fake \
    --opt tardis=blue \
    --opt timey=wimey \
    foo
```

These options are passed directly to the volume driver. Options for
different volume drivers may do different things (or nothing at all).

The built-in `local` driver accepts no options on Windows. On Linux and with
Docker Desktop, the `local` driver accepts options similar to the Linux `mount`
command. You can provide multiple options by passing the `--opt` flag multiple
times. Some `mount` options (such as the `o` option) can take a comma-separated
list of options. Complete list of available mount options can be found
[here](https://man7.org/linux/man-pages/man8/mount.8.html).

For example, the following creates a `tmpfs` volume called `foo` with a size of
100 megabyte and `uid` of 1000.

```console
$ docker volume create --driver local \
    --opt type=tmpfs \
    --opt device=tmpfs \
    --opt o=size=100m,uid=1000 \
    foo
```

Another example that uses `btrfs`:

```console
$ docker volume create --driver local \
    --opt type=btrfs \
    --opt device=/dev/sda2 \
    foo
```

Another example that uses `nfs` to mount the `/path/to/dir` in `rw` mode from
`192.168.1.1`:

```console
$ docker volume create --driver local \
    --opt type=nfs \
    --opt o=addr=192.168.1.1,rw \
    --opt device=:/path/to/dir \
    foo
```

---

# docker volume inspect

# docker volume inspect

| Description | Display detailed information on one or more volumes |
| --- | --- |
| Usage | docker volume inspect [OPTIONS] VOLUME [VOLUME...] |

## Description

Returns information about a volume. By default, this command renders all results
in a JSON array. You can specify an alternate format to execute a
given template for each result. Go's
[text/template](https://pkg.go.dev/text/template) package describes all the
details of the format.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |

## Examples

```console
$ docker volume create myvolume

myvolume
```

Use the `docker volume inspect` comment to inspect the configuration of the volume:

```console
$ docker volume inspect myvolume
```

The output is in JSON format, for example:

```json
[
  {
    "CreatedAt": "2020-04-19T11:00:21Z",
    "Driver": "local",
    "Labels": {},
    "Mountpoint": "/var/lib/docker/volumes/8140a838303144125b4f54653b47ede0486282c623c3551fbc7f390cdc3e9cf5/_data",
    "Name": "myvolume",
    "Options": {},
    "Scope": "local"
  }
]
```

### Format the output (--format)

Use the `--format` flag to format the output using a Go template, for example,
to print the `Mountpoint` property:

```console
$ docker volume inspect --format '{{ .Mountpoint }}' myvolume

/var/lib/docker/volumes/myvolume/_data
```

---

# docker volume ls

# docker volume ls

| Description | List volumes |
| --- | --- |
| Usage | docker volume ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker volume list |

## Description

List all the volumes known to Docker. You can filter using the `-f` or
`--filter` flag. Refer to the [filtering](#filter) section for more
information about available filter options.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --cluster |  | API 1.42+SwarmDisplay only cluster volumes, and use cluster volume list formatting |
| -f, --filter |  | Provide filter values (e.g.dangling=true) |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -q, --quiet |  | Only display volume names |

## Examples

### Create a volume

```console
$ docker volume create rosemary

rosemary

$ docker volume create tyler

tyler

$ docker volume ls

DRIVER              VOLUME NAME
local               rosemary
local               tyler
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- dangling (Boolean - true or false, 0 or 1)
- driver (a volume driver's name)
- label (`label=<key>` or `label=<key>=<value>`)
- name (a volume's name)

#### dangling

The `dangling` filter matches on all volumes not referenced by any containers

```console
$ docker run -d  -v tyler:/tmpwork  busybox

f86a7dd02898067079c99ceacd810149060a70528eff3754d0b0f1a93bd0af18
$ docker volume ls -f dangling=true
DRIVER              VOLUME NAME
local               rosemary
```

#### driver

The `driver` filter matches volumes based on their driver.

The following example matches volumes that are created with the `local` driver:

```console
$ docker volume ls -f driver=local

DRIVER              VOLUME NAME
local               rosemary
local               tyler
```

#### label

The `label` filter matches volumes based on the presence of a `label` alone or
a `label` and a value.

First, create some volumes to illustrate this;

```console
$ docker volume create the-doctor --label is-timelord=yes

the-doctor
$ docker volume create daleks --label is-timelord=no

daleks
```

The following example filter matches volumes with the `is-timelord` label
regardless of its value.

```console
$ docker volume ls --filter label=is-timelord

DRIVER              VOLUME NAME
local               daleks
local               the-doctor
```

As the above example demonstrates, both volumes with `is-timelord=yes`, and
`is-timelord=no` are returned.

Filtering on both `key` *and* `value` of the label, produces the expected result:

```console
$ docker volume ls --filter label=is-timelord=yes

DRIVER              VOLUME NAME
local               the-doctor
```

Specifying multiple label filter produces an "and" search; all conditions
should be met;

```console
$ docker volume ls --filter label=is-timelord=yes --filter label=is-timelord=no

DRIVER              VOLUME NAME
```

#### name

The `name` filter matches on all or part of a volume's name.

The following filter matches all volumes with a name containing the `rose` string.

```console
$ docker volume ls -f name=rose

DRIVER              VOLUME NAME
local               rosemary
```

### Format the output (--format)

The formatting options (`--format`) pretty-prints volumes output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .Name | Volume name |
| .Driver | Volume driver |
| .Scope | Volume scope (local, global) |
| .Mountpoint | The mount point of the volume on the host |
| .Labels | All labels assigned to the volume |
| .Label | Value of a specific label for this volume. For example{{.Label "project.version"}} |

When using the `--format` option, the `volume ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Name` and `Driver` entries separated by a colon (`:`) for all volumes:

```console
$ docker volume ls --format "{{.Name}}: {{.Driver}}"

vol1: local
vol2: local
vol3: local
```

To list all volumes in JSON format, use the `json` directive:

```console
$ docker volume ls --format json
{"Driver":"local","Labels":"","Links":"N/A","Mountpoint":"/var/lib/docker/volumes/docker-cli-dev-cache/_data","Name":"docker-cli-dev-cache","Scope":"local","Size":"N/A"}
```

---

# docker volume prune

# docker volume prune

| Description | Remove unused local volumes |
| --- | --- |
| Usage | docker volume prune [OPTIONS] |

## Description

Remove all unused local volumes. Unused local volumes are those which are not
referenced by any containers. By default, it only removes anonymous volumes.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | API 1.42+Remove all unused volumes, not just anonymous ones |
| --filter |  | Provide filter values (e.g.label=<label>) |
| -f, --force |  | Do not prompt for confirmation |

## Examples

```console
$ docker volume prune

WARNING! This will remove anonymous local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Deleted Volumes:
07c7bdf3e34ab76d921894c2b834f073721fccfbbcba792aa7648e3a7a664c2e
my-named-vol

Total reclaimed space: 36 B
```

### Filtering (--all, -a)

Use the `--all` flag to prune both unused anonymous and named volumes.

### Filtering (--filter)

The filtering flag (`--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove volumes with (or without, in case `label!=...` is used) the specified labels.

The `label` filter accepts two formats. One is the `label=...` (`label=<key>` or `label=<key>=<value>`),
which removes volumes with the specified labels. The other
format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes
volumes without the specified labels.

---

# docker volume rm

# docker volume rm

| Description | Remove one or more volumes |
| --- | --- |
| Usage | docker volume rm [OPTIONS] VOLUME [VOLUME...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker volume remove |

## Description

Remove one or more volumes. You can't remove a volume that's in use by a container.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | API 1.25+Force the removal of one or more volumes |

## Examples

```console
$ docker volume rm hello

hello
```

---

# docker volume update

# docker volume update

| Description | Update a volume (cluster volumes only) |
| --- | --- |
| Usage | docker volume update [OPTIONS] [VOLUME] |

Swarm
This command works with the Swarm orchestrator.

## Description

Update a volume (cluster volumes only)

## Options

| Option | Default | Description |
| --- | --- | --- |
| --availability | active | API 1.42+SwarmCluster Volume availability (active,pause,drain) |

---

# docker volume

# docker volume

| Description | Manage volumes |
| --- | --- |
| Usage | docker volume COMMAND |

## Description

Manage volumes. You can use subcommands to create, inspect, list, remove, or
prune volumes.

## Subcommands

| Command | Description |
| --- | --- |
| docker volume create | Create a volume |
| docker volume inspect | Display detailed information on one or more volumes |
| docker volume ls | List volumes |
| docker volume prune | Remove unused local volumes |
| docker volume rm | Remove one or more volumes |
| docker volume update | Update a volume (cluster volumes only) |
