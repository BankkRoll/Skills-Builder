# docker login and more

# docker login

# docker login

| Description | Authenticate to a registry |
| --- | --- |
| Usage | docker login [OPTIONS] [SERVER] |

## Description

Authenticate to a registry.

You can authenticate to any public or private registry for which you have
credentials. Authentication may be required for pulling and pushing images.
Other commands, such as `docker scout` and `docker build`, may also require
authentication to access subscription-only features or data related to your
Docker organization.

Authentication credentials are stored in the configured [credential
store](#credential-stores). If you use Docker Desktop, credentials are
automatically saved to the native keychain of your operating system. If you're
not using Docker Desktop, you can configure the credential store in the Docker
configuration file, which is located at `$HOME/.docker/config.json` on Linux or
`%USERPROFILE%/.docker/config.json` on Windows. If you don't configure a
credential store, Docker stores credentials in the `config.json` file in a
base64-encoded format. This method is less secure than configuring and using a
credential store.

`docker login` also supports [credential helpers](#credential-helpers) to help
you handle credentials for specific registries.

### Authentication methods

You can authenticate to a registry using a username and access token or
password. Docker Hub also supports a web-based sign-in flow, which signs you in
to your Docker account without entering your password. For Docker Hub, the
`docker login` command uses a device code flow by default, unless the
`--username` flag is specified. The device code flow is a secure way to sign
in. See [Authenticate to Docker Hub using device code](#authenticate-to-docker-hub-with-web-based-login).

### Credential stores

The Docker Engine can keep user credentials in an external credential store,
such as the native keychain of the operating system. Using an external store
is more secure than storing credentials in the Docker configuration file.

To use a credential store, you need an external helper program to interact
with a specific keychain or external store. Docker requires the helper
program to be in the client's host `$PATH`.

You can download the helpers from the `docker-credential-helpers` [releases page](https://github.com/docker/docker-credential-helpers/releases).
Helpers are available for the following credential stores:

- D-Bus Secret Service
- Apple macOS keychain
- Microsoft Windows Credential Manager
- [pass](https://www.passwordstore.org/)

With Docker Desktop, the credential store is already installed and configured
for you. Unless you want to change the credential store used by Docker Desktop,
you can skip the following steps.

#### Configure the credential store

You need to specify the credential store in `$HOME/.docker/config.json`
to tell the Docker Engine to use it. The value of the config property should be
the suffix of the program to use (i.e. everything after `docker-credential-`).
For example, to use `docker-credential-osxkeychain`:

```json
{
  "credsStore": "osxkeychain"
}
```

If you are currently logged in, run `docker logout` to remove
the credentials from the file and run `docker login` again.

#### Default behavior

By default, Docker looks for the native binary on each of the platforms, i.e.
`osxkeychain` on macOS, `wincred` on Windows, and `pass` on Linux. A special
case is that on Linux, Docker will fall back to the `secretservice` binary if
it cannot find the `pass` binary. If none of these binaries are present, it
stores the base64-encoded credentials in the `config.json` configuration file.

#### Credential helper protocol

Credential helpers can be any program or script that implements the credential
helper protocol. This protocol is inspired by Git, but differs in the
information shared.

The helpers always use the first argument in the command to identify the action.
There are only three possible values for that argument: `store`, `get`, and `erase`.

The `store` command takes a JSON payload from the standard input. That payload carries
the server address, to identify the credential, the username, and either a password
or an identity token.

```json
{
  "ServerURL": "https://index.docker.io/v1",
  "Username": "david",
  "Secret": "passw0rd1"
}
```

If the secret being stored is an identity token, the Username should be set to
`<token>`.

The `store` command can write error messages to `STDOUT` that the Docker Engine
will show if there was an issue.

The `get` command takes a string payload from the standard input. That payload carries
the server address that the Docker Engine needs credentials for. This is
an example of that payload: `https://index.docker.io/v1`.

The `get` command writes a JSON payload to `STDOUT`. Docker reads the user name
and password from this payload:

```json
{
  "Username": "david",
  "Secret": "passw0rd1"
}
```

The `erase` command takes a string payload from `STDIN`. That payload carries
the server address that the Docker Engine wants to remove credentials for. This is
an example of that payload: `https://index.docker.io/v1`.

The `erase` command can write error messages to `STDOUT` that the Docker Engine
will show if there was an issue.

### Credential helpers

Credential helpers are similar to [credential stores](#credential-stores), but
act as the designated programs to handle credentials for specific registries.
The default credential store will not be used for operations concerning
credentials of the specified registries.

#### Configure credential helpers

If you are currently logged in, run `docker logout` to remove
the credentials from the default store.

Credential helpers are specified in a similar way to `credsStore`, but
allow for multiple helpers to be configured at a time. Keys specify the
registry domain, and values specify the suffix of the program to use
(i.e. everything after `docker-credential-`). For example:

```json
{
  "credHelpers": {
    "myregistry.example.com": "secretservice",
    "docker.internal.example": "pass",
  }
}
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| -p, --password |  | Password or Personal Access Token (PAT) |
| --password-stdin |  | Take the Password or Personal Access Token (PAT) from stdin |
| -u, --username |  | Username |

## Examples

### Authenticate to Docker Hub with web-based login

By default, the `docker login` command authenticates to Docker Hub, using a
device code flow. This flow lets you authenticate to Docker Hub without
entering your password. Instead, you visit a URL in your web browser, enter a
code, and authenticate.

```console
$ docker login

USING WEB-BASED LOGIN
To sign in with credentials on the command line, use 'docker login -u <username>'

Your one-time device confirmation code is: LNFR-PGCJ
Press ENTER to open your browser or submit your device code here: https://login.docker.com/activate

Waiting for authentication in the browser…
```

After entering the code in your browser, you are authenticated to Docker Hub
using the account you're currently signed in with on the Docker Hub website or
in Docker Desktop. If you aren't signed in, you are prompted to sign in after
entering the device code.

### Authenticate to a self-hosted registry

If you want to authenticate to a self-hosted registry you can specify this by
adding the server name.

```console
$ docker login registry.example.com
```

By default, the `docker login` command assumes that the registry listens on
port 443 or 80. If the registry listens on a different port, you can specify it
by adding the port number to the server name.

```console
$ docker login registry.example.com:1337
```

> Note
>
> Registry addresses should not include URL path components, only the hostname
> and (optionally) the port. Registry addresses with URL path components may
> result in an error. For example, `docker login registry.example.com/foo/`
> is incorrect, while `docker login registry.example.com` is correct.
>
>
>
> The exception to this rule is the Docker Hub registry, which may use the
> `/v1/` path component in the address for historical reasons.

### Authenticate to a registry with a username and password

To authenticate to a registry with a username and password, you can use the
`--username` or `-u` flag. The following example authenticates to Docker Hub
with the username `moby`. The password is entered interactively.

```console
$ docker login -u moby
```

### Provide a password using STDIN (--password-stdin)

To run the `docker login` command non-interactively, you can set the
`--password-stdin` flag to provide a password through `STDIN`. Using
`STDIN` prevents the password from ending up in the shell's history,
or log-files.

The following example reads a password from a file, and passes it to the
`docker login` command using `STDIN`:

```console
$ cat ~/my_password.txt | docker login --username foo --password-stdin
```

---

# docker logout

# docker logout

| Description | Log out from a registry |
| --- | --- |
| Usage | docker logout [SERVER] |

## Description

Log out from a registry.
If no server is specified, the default is defined by the daemon.

## Examples

```console
$ docker logout localhost:8080
```

---

# docker manifest annotate

# docker manifest annotate

| Description | Add additional information to a local image manifest |
| --- | --- |
| Usage | docker manifest annotate [OPTIONS] MANIFEST_LIST MANIFEST |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Add additional information to a local image manifest

## Options

| Option | Default | Description |
| --- | --- | --- |
| --arch |  | Set architecture |
| --os |  | Set operating system |
| --os-features |  | Set operating system feature |
| --os-version |  | Set operating system version |
| --variant |  | Set architecture variant |

---

# docker manifest create

# docker manifest create

| Description | Create a local manifest list for annotating and pushing to a registry |
| --- | --- |
| Usage | docker manifest create MANIFEST_LIST MANIFEST [MANIFEST...] |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Create a local manifest list for annotating and pushing to a registry

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --amend |  | Amend an existing manifest list |
| --insecure |  | Allow communication with an insecure registry |

---

# docker manifest inspect

# docker manifest inspect

| Description | Display an image manifest, or manifest list |
| --- | --- |
| Usage | docker manifest inspect [OPTIONS] [MANIFEST_LIST] MANIFEST |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Display an image manifest, or manifest list

## Options

| Option | Default | Description |
| --- | --- | --- |
| --insecure |  | Allow communication with an insecure registry |
| -v, --verbose |  | Output additional info including layers and platform |

---

# docker manifest push

# docker manifest push

| Description | Push a manifest list to a repository |
| --- | --- |
| Usage | docker manifest push [OPTIONS] MANIFEST_LIST |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Push a manifest list to a repository

## Options

| Option | Default | Description |
| --- | --- | --- |
| --insecure |  | Allow push to an insecure registry |
| -p, --purge |  | Remove the local manifest list after push |

---

# docker manifest rm

# docker manifest rm

| Description | Delete one or more manifest lists from local storage |
| --- | --- |
| Usage | docker manifest rm MANIFEST_LIST [MANIFEST_LIST...] |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Delete one or more manifest lists from local storage

---

# docker manifest

# docker manifest

| Description | Manage Docker image manifests and manifest lists |
| --- | --- |
| Usage | docker manifest COMMAND |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The `docker manifest` command by itself performs no action. In order to operate
on a manifest or manifest list, one of the subcommands must be used.

A single manifest is information about an image, such as layers, size, and
digest. The `docker manifest` command also gives you additional information,
such as the OS and architecture an image was built for.

A manifest list is a list of image layers that is created by specifying one or
more (ideally more than one) image names. It can then be used in the same way as
an image name in `docker pull` and `docker run` commands, for example.

Ideally a manifest list is created from images that are identical in function for
different os/arch combinations. For this reason, manifest lists are often referred
to as "multi-arch images". However, a user could create a manifest list that points
to two images -- one for Windows on AMD64, and one for Darwin on AMD64.

### manifest inspect

```console
$ docker manifest inspect --help

Usage:  docker manifest inspect [OPTIONS] [MANIFEST_LIST] MANIFEST

Display an image manifest, or manifest list

Options:
      --help       Print usage
      --insecure   Allow communication with an insecure registry
  -v, --verbose    Output additional info including layers and platform
```

### manifest create

```console
Usage:  docker manifest create MANIFEST_LIST MANIFEST [MANIFEST...]

Create a local manifest list for annotating and pushing to a registry

Options:
  -a, --amend      Amend an existing manifest list
      --insecure   Allow communication with an insecure registry
      --help       Print usage
```

### manifest annotate

```console
Usage:  docker manifest annotate [OPTIONS] MANIFEST_LIST MANIFEST

Add additional information to a local image manifest

Options:
      --arch string               Set architecture
      --help                      Print usage
      --os string                 Set operating system
      --os-version string         Set operating system version
      --os-features stringSlice   Set operating system feature
      --variant string            Set architecture variant
```

### manifest push

```console
Usage:  docker manifest push [OPTIONS] MANIFEST_LIST

Push a manifest list to a repository

Options:
      --help       Print usage
      --insecure   Allow push to an insecure registry
  -p, --purge      Remove the local manifest list after push
```

### Working with insecure registries

The manifest command interacts solely with a registry. Because of this,
it has no way to query the engine for the list of allowed insecure registries.
To allow the CLI to interact with an insecure registry, some `docker manifest`
commands have an `--insecure` flag. For each transaction, such as a `create`,
which queries a registry, the `--insecure` flag must be specified. This flag
tells the CLI that this registry call may ignore security concerns like missing
or self-signed certificates. Likewise, on a `manifest push` to an insecure
registry, the `--insecure` flag must be specified. If this is not used with an
insecure registry, the manifest command fails to find a registry that meets the
default requirements.

## Examples

### Inspect an image's manifest object

```console
$ docker manifest inspect hello-world
{
        "schemaVersion": 2,
        "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
        "config": {
                "mediaType": "application/vnd.docker.container.image.v1+json",
                "size": 1520,
                "digest": "sha256:1815c82652c03bfd8644afda26fb184f2ed891d921b20a0703b46768f9755c57"
        },
        "layers": [
                {
                        "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                        "size": 972,
                        "digest": "sha256:b04784fba78d739b526e27edc02a5a8cd07b1052e9283f5fc155828f4b614c28"
                }
        ]
}
```

### Inspect an image's manifest and get the os/arch info

The `docker manifest inspect` command takes an optional `--verbose` flag that
gives you the image's name (Ref), as well as the architecture and OS (Platform).

Just as with other Docker commands that take image names, you can refer to an image with or
without a tag, or by digest (e.g. `hello-world@sha256:f3b3b28a45160805bb16542c9531888519430e9e6d6ffc09d72261b0d26ff74f`).

Here is an example of inspecting an image's manifest with the `--verbose` flag:

```console
$ docker manifest inspect --verbose hello-world
{
        "Ref": "docker.io/library/hello-world:latest",
        "Digest": "sha256:f3b3b28a45160805bb16542c9531888519430e9e6d6ffc09d72261b0d26ff74f",
        "SchemaV2Manifest": {
                "schemaVersion": 2,
                "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
                "config": {
                        "mediaType": "application/vnd.docker.container.image.v1+json",
                        "size": 1520,
                        "digest": "sha256:1815c82652c03bfd8644afda26fb184f2ed891d921b20a0703b46768f9755c57"
                },
                "layers": [
                        {
                                "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                                "size": 972,
                                "digest": "sha256:b04784fba78d739b526e27edc02a5a8cd07b1052e9283f5fc155828f4b614c28"
                        }
                ]
        },
        "Platform": {
                "architecture": "amd64",
                "os": "linux"
        }
}
```

### Create and push a manifest list

To create a manifest list, you first `create` the manifest list locally by
specifying the constituent images you would like to have included in your
manifest list. Keep in mind that this is pushed to a registry, so if you want to
push to a registry other than the docker registry, you need to create your
manifest list with the registry name or IP and port.
This is similar to tagging an image and pushing it to a foreign registry.

After you have created your local copy of the manifest list, you may optionally
`annotate` it. Annotations allowed are the architecture and operating system
(overriding the image's current values), os features, and an architecture variant.

Finally, you need to `push` your manifest list to the desired registry. Below are
descriptions of these three commands, and an example putting them all together.

```console
$ docker manifest create 45.55.81.106:5000/coolapp:v1 \
    45.55.81.106:5000/coolapp-ppc64le-linux:v1 \
    45.55.81.106:5000/coolapp-arm-linux:v1 \
    45.55.81.106:5000/coolapp-amd64-linux:v1 \
    45.55.81.106:5000/coolapp-amd64-windows:v1

Created manifest list 45.55.81.106:5000/coolapp:v1
```

```console
$ docker manifest annotate 45.55.81.106:5000/coolapp:v1 45.55.81.106:5000/coolapp-arm-linux --arch arm
```

```console
$ docker manifest push 45.55.81.106:5000/coolapp:v1
Pushed manifest 45.55.81.106:5000/coolapp@sha256:9701edc932223a66e49dd6c894a11db8c2cf4eccd1414f1ec105a623bf16b426 with digest: sha256:f67dcc5fc786f04f0743abfe0ee5dae9bd8caf8efa6c8144f7f2a43889dc513b
Pushed manifest 45.55.81.106:5000/coolapp@sha256:f3b3b28a45160805bb16542c9531888519430e9e6d6ffc09d72261b0d26ff74f with digest: sha256:b64ca0b60356a30971f098c92200b1271257f100a55b351e6bbe985638352f3a
Pushed manifest 45.55.81.106:5000/coolapp@sha256:39dc41c658cf25f33681a41310372f02728925a54aac3598310bfb1770615fc9 with digest: sha256:df436846483aff62bad830b730a0d3b77731bcf98ba5e470a8bbb8e9e346e4e8
Pushed manifest 45.55.81.106:5000/coolapp@sha256:f91b1145cd4ac800b28122313ae9e88ac340bb3f1e3a4cd3e59a3648650f3275 with digest: sha256:5bb8e50aa2edd408bdf3ddf61efb7338ff34a07b762992c9432f1c02fc0e5e62
sha256:050b213d49d7673ba35014f21454c573dcbec75254a08f4a7c34f66a47c06aba
```

### Inspect a manifest list

```console
$ docker manifest inspect coolapp:v1
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 424,
         "digest": "sha256:f67dcc5fc786f04f0743abfe0ee5dae9bd8caf8efa6c8144f7f2a43889dc513b",
         "platform": {
            "architecture": "arm",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 424,
         "digest": "sha256:b64ca0b60356a30971f098c92200b1271257f100a55b351e6bbe985638352f3a",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 425,
         "digest": "sha256:df436846483aff62bad830b730a0d3b77731bcf98ba5e470a8bbb8e9e346e4e8",
         "platform": {
            "architecture": "ppc64le",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 425,
         "digest": "sha256:5bb8e50aa2edd408bdf3ddf61efb7338ff34a07b762992c9432f1c02fc0e5e62",
         "platform": {
            "architecture": "s390x",
            "os": "linux"
         }
      }
   ]
}
```

### Push to an insecure registry

Here is an example of creating and pushing a manifest list using a known
insecure registry.

```console
$ docker manifest create --insecure myprivateregistry.mycompany.com/repo/image:1.0 \
    myprivateregistry.mycompany.com/repo/image-linux-ppc64le:1.0 \
    myprivateregistry.mycompany.com/repo/image-linux-s390x:1.0 \
    myprivateregistry.mycompany.com/repo/image-linux-arm:1.0 \
    myprivateregistry.mycompany.com/repo/image-linux-armhf:1.0 \
    myprivateregistry.mycompany.com/repo/image-windows-amd64:1.0 \
    myprivateregistry.mycompany.com/repo/image-linux-amd64:1.0

$ docker manifest push --insecure myprivateregistry.mycompany.com/repo/image:tag
```

> Note
>
> The `--insecure` flag is not required to annotate a manifest list,
> since annotations are to a locally-stored copy of a manifest list. You may also
> skip the `--insecure` flag if you are performing a `docker manifest inspect`
> on a locally-stored manifest list. Be sure to keep in mind that locally-stored
> manifest lists are never used by the engine on a `docker pull`.

## Subcommands

| Command | Description |
| --- | --- |
| docker manifest annotate | Add additional information to a local image manifest |
| docker manifest create | Create a local manifest list for annotating and pushing to a registry |
| docker manifest inspect | Display an image manifest, or manifest list |
| docker manifest push | Push a manifest list to a repository |
| docker manifest rm | Delete one or more manifest lists from local storage |

---

# docker mcp catalog add

# docker mcp catalog add

| Description | Add a server to a catalog |
| --- | --- |
| Usage | docker mcp catalog add <catalog> <server-name> <catalog-file> |

## Description

Add an MCP server definition to an existing catalog by copying it from another catalog file.
The server definition includes all configuration, tools, and metadata.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --force |  | Overwrite existing server in the catalog |

## Examples

# Add a server from another catalog file

docker mcp catalog add my-catalog github-server ./github-catalog.yaml

# Add with force to overwrite existing server

docker mcp catalog add my-catalog slack-bot ./team-catalog.yaml --force

---

# docker mcp catalog bootstrap

# docker mcp catalog bootstrap

| Description | Create a starter catalog file with Docker and Docker Hub server entries as examples |
| --- | --- |
| Usage | docker mcp catalog bootstrap <output-file-path> |

## Description

Create a starter catalog file with Docker Hub and Docker CLI server entries as examples.
This command extracts the official Docker server definitions and creates a properly formatted
catalog file that users can modify and use as a foundation for their custom catalogs.

The output file is standalone and not automatically imported - users can modify it and then
import it or use it as a source for the 'catalog add' command.

---

# docker mcp catalog create

# docker mcp catalog create

| Description | Create a new empty catalog |
| --- | --- |
| Usage | docker mcp catalog create <name> |

## Description

Create a new empty catalog for organizing custom MCP servers. The catalog will be stored locally and can be populated using 'docker mcp catalog add'.

## Examples

# Create a new catalog for development servers

docker mcp catalog create dev-servers

# Create a catalog for production monitoring tools

docker mcp catalog create prod-monitoring

---

# docker mcp catalog export

# docker mcp catalog export

| Description | Export a configured catalog to a file |
| --- | --- |
| Usage | docker mcp catalog export <catalog-name> <file-path> |

## Description

Export a user-managed catalog to a file. This command only works with catalogs
that have been imported or configured manually. The canonical Docker MCP catalog
cannot be exported as it is managed by Docker.

---

# docker mcp catalog fork

# docker mcp catalog fork

| Description | Create a copy of an existing catalog |
| --- | --- |
| Usage | docker mcp catalog fork <src-catalog> <new-name> |

## Description

Create a new catalog by copying all servers from an existing catalog. Useful for creating variations of existing catalogs.

## Examples

# Fork the Docker catalog to customize it

docker mcp catalog fork docker-mcp my-custom-docker

# Fork a team catalog for personal use

docker mcp catalog fork team-servers my-servers

---

# docker mcp catalog import

# docker mcp catalog import

| Description | Import a catalog from URL or file |
| --- | --- |
| Usage | docker mcp catalog import <alias|url|file> |

## Description

Import an MCP server catalog from a URL or local file. The catalog will be downloaded
and stored locally for use with the MCP gateway.

When --mcp-registry flag is used, the argument must be an existing catalog name, and the
command will import servers from the MCP registry URL into that catalog.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --dry-run |  | Show Imported Data but do not update the Catalog |
| --mcp-registry |  | Import server from MCP registry URL into existing catalog |

## Examples

# Import from URL

docker mcp catalog import [https://example.com/my-catalog.yaml](https://example.com/my-catalog.yaml)

# Import from local file

docker mcp catalog import ./shared-catalog.yaml

# Import from MCP registry URL into existing catalog

docker mcp catalog import my-catalog --mcp-registry [https://registry.example.com/server](https://registry.example.com/server)

---

# docker mcp catalog init

# docker mcp catalog init

| Description | Initialize the catalog system |
| --- | --- |
| Usage | docker mcp catalog init |

## Description

Initialize the local catalog management system by creating the necessary configuration files and directories.

## Examples

# Initialize catalog system

docker mcp catalog init

---

# docker mcp catalog ls

# docker mcp catalog ls

| Description | List all configured catalogs |
| --- | --- |
| Usage | docker mcp catalog ls |

## Description

List all configured catalogs including Docker's official catalog and any locally managed catalogs.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format |  | Output format. Supported: "json", "yaml". |

## Examples

# List all catalogs

docker mcp catalog ls

# List catalogs in JSON format

docker mcp catalog ls --format=json

---

# docker mcp catalog reset

# docker mcp catalog reset

| Description | Reset the catalog system |
| --- | --- |
| Usage | docker mcp catalog reset |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp catalog empty |

## Description

Reset the local catalog management system by removing all user-managed catalogs and configuration. This does not affect Docker's official catalog.

## Examples

# Reset all user catalogs

docker mcp catalog reset

---

# docker mcp catalog rm

# docker mcp catalog rm

| Description | Remove a catalog |
| --- | --- |
| Usage | docker mcp catalog rm <name> |

## Description

Remove a locally configured catalog. This will delete the catalog and all its server definitions.
The Docker official catalog cannot be removed.

## Examples

# Remove a catalog

docker mcp catalog rm old-servers

---

# docker mcp catalog show

# docker mcp catalog show

| Description | Display catalog contents |
| --- | --- |
| Usage | docker mcp catalog show [name] |

## Description

Display the contents of a catalog including all server definitions and metadata.
If no name is provided, shows the Docker official catalog.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format |  | Supported: "json", "yaml". |

## Examples

# Show Docker's official catalog

docker mcp catalog show

# Show a specific catalog in JSON format

docker mcp catalog show my-catalog --format=json

---

# docker mcp catalog update

# docker mcp catalog update

| Description | Update catalog(s) from remote sources |
| --- | --- |
| Usage | docker mcp catalog update [name] |

## Description

Update one or more catalogs by re-downloading from their original sources.
If no name is provided, updates all catalogs that have remote sources.

## Examples

# Update all catalogs

docker mcp catalog update

# Update specific catalog

docker mcp catalog update team-servers

---

# docker mcp catalog

# docker mcp catalog

| Description | Manage MCP server catalogs |
| --- | --- |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp catalogs |

## Description

Manage MCP server catalogs for organizing and configuring custom MCP servers alongside Docker's official catalog.

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp catalog add | Add a server to a catalog |
| docker mcp catalog bootstrap | Create a starter catalog file with Docker and Docker Hub server entries as examples |
| docker mcp catalog create | Create a new empty catalog |
| docker mcp catalog export | Export a configured catalog to a file |
| docker mcp catalog fork | Create a copy of an existing catalog |
| docker mcp catalog import | Import a catalog from URL or file |
| docker mcp catalog init | Initialize the catalog system |
| docker mcp catalog ls | List all configured catalogs |
| docker mcp catalog reset | Reset the catalog system |
| docker mcp catalog rm | Remove a catalog |
| docker mcp catalog show | Display catalog contents |
| docker mcp catalog update | Update catalog(s) from remote sources |

---

# docker mcp client connect

# docker mcp client connect

| Description | Connect the Docker MCP Toolkit to a client. Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed |
| --- | --- |
| Usage | docker mcp client connect [OPTIONS] <mcp-client>
Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed |

## Description

Connect the Docker MCP Toolkit to a client. Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed

## Options

| Option | Default | Description |
| --- | --- | --- |
| -g, --global |  | Change the system wide configuration or the clients setup in your current git repo. |
| -q, --quiet |  | Only display errors. |

---

# docker mcp client disconnect

# docker mcp client disconnect

| Description | Disconnect the Docker MCP Toolkit from a client. Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed |
| --- | --- |
| Usage | docker mcp client disconnect [OPTIONS] <mcp-client>
Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed |

## Description

Disconnect the Docker MCP Toolkit from a client. Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed

## Options

| Option | Default | Description |
| --- | --- | --- |
| -g, --global |  | Change the system wide configuration or the clients setup in your current git repo. |
| -q, --quiet |  | Only display errors. |

---

# docker mcp client ls

# docker mcp client ls

| Description | List client configurations |
| --- | --- |
| Usage | docker mcp client ls |

## Description

List client configurations

## Options

| Option | Default | Description |
| --- | --- | --- |
| -g, --global |  | Change the system wide configuration or the clients setup in your current git repo. |
| --json |  | Print as JSON. |

---

# docker mcp client manual

# docker mcp client manual-instructions

| Description | Display the manual instructions to connect the MCP client |
| --- | --- |
| Usage | docker mcp client manual-instructions |

## Description

Display the manual instructions to connect the MCP client

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Print as JSON. |

---

# docker mcp client

# docker mcp client

| Description | Manage MCP clients |
| --- | --- |

## Description

Manage MCP clients

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp client connect | Connect the Docker MCP Toolkit to a client. Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed |
| docker mcp client disconnect | Disconnect the Docker MCP Toolkit from a client. Supported clients: claude-code claude-desktop codex continue cursor gemini goose gordon lmstudio opencode sema4 vscode zed |
| docker mcp client ls | List client configurations |
| docker mcp client manual-instructions | Display the manual instructions to connect the MCP client |

---

# docker mcp config dump

# docker mcp config dump

| Description | Dump the whole configuration |
| --- | --- |
| Usage | docker mcp config dump |

## Description

Dump the whole configuration

---

# docker mcp config read

# docker mcp config read

| Description | Read the configuration |
| --- | --- |
| Usage | docker mcp config read |

## Description

Read the configuration

---

# docker mcp config reset

# docker mcp config reset

| Description | Reset the configuration |
| --- | --- |
| Usage | docker mcp config reset |

## Description

Reset the configuration

---

# docker mcp config restore

# docker mcp config restore

| Description | Restore the whole configuration |
| --- | --- |
| Usage | docker mcp config restore |

## Description

Restore the whole configuration

---

# docker mcp config write

# docker mcp config write

| Description | Write the configuration |
| --- | --- |
| Usage | docker mcp config write |

## Description

Write the configuration

---

# docker mcp config

# docker mcp config

| Description | Manage the configuration |
| --- | --- |

## Description

Manage the configuration

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp config dump | Dump the whole configuration |
| docker mcp config read | Read the configuration |
| docker mcp config reset | Reset the configuration |
| docker mcp config restore | Restore the whole configuration |
| docker mcp config write | Write the configuration |

---

# docker mcp feature disable

# docker mcp feature disable

| Description | Disable an experimental feature |
| --- | --- |
| Usage | docker mcp feature disable <feature-name> |

## Description

Disable an experimental feature that was previously enabled.

---

# docker mcp feature enable

# docker mcp feature enable

| Description | Enable an experimental feature |
| --- | --- |
| Usage | docker mcp feature enable <feature-name> |

## Description

Enable an experimental feature.

Available features:
oauth-interceptor Enable GitHub OAuth flow interception for automatic authentication
mcp-oauth-dcr Enable Dynamic Client Registration (DCR) for automatic OAuth client setup
dynamic-tools Enable internal MCP management tools (mcp-find, mcp-add, mcp-remove)

---

# docker mcp feature ls

# docker mcp feature ls

| Description | List all available features and their status |
| --- | --- |
| Usage | docker mcp feature ls |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp feature list |

## Description

List all available experimental features and show whether they are enabled or disabled.

---

# docker mcp feature

# docker mcp feature

| Description | Manage experimental features |
| --- | --- |

## Description

Manage experimental features for Docker MCP Gateway.

Features are stored in your Docker configuration file (~/.docker/config.json)
and control optional functionality that may change in future versions.

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp feature disable | Disable an experimental feature |
| docker mcp feature enable | Enable an experimental feature |
| docker mcp feature ls | List all available features and their status |

---

# docker mcp gateway run

# docker mcp gateway run

| Description | Run the gateway |
| --- | --- |
| Usage | docker mcp gateway run |

## Description

Run the gateway

## Options

| Option | Default | Description |
| --- | --- | --- |
| --additional-catalog |  | Additional catalog paths to append to the default catalogs |
| --additional-config |  | Additional config paths to merge with the default config.yaml |
| --additional-registry |  | Additional registry paths to merge with the default registry.yaml |
| --additional-tools-config |  | Additional tools paths to merge with the default tools.yaml |
| --block-network |  | Block tools from accessing forbidden network resources |
| --block-secrets | true | Block secrets from being/received sent to/from tools |
| --catalog | [docker-mcp.yaml] | Paths to docker catalogs (absolute or relative to ~/.docker/mcp/catalogs/) |
| --config | [config.yaml] | Paths to the config files (absolute or relative to ~/.docker/mcp/) |
| --cpus | 1 | CPUs allocated to each MCP Server (default is 1) |
| --debug-dns |  | Debug DNS resolution |
| --dry-run |  | Start the gateway but do not listen for connections (useful for testing the configuration) |
| --enable-all-servers |  | Enable all servers in the catalog (instead of using individual --servers options) |
| --interceptor |  | List of interceptors to use (format: when:type:path, e.g. 'before:exec:/bin/path') |
| --log-calls | true | Log calls to the tools |
| --long-lived |  | Containers are long-lived and will not be removed until the gateway is stopped, useful for stateful servers |
| --mcp-registry |  | MCP registry URLs to fetch servers from (can be repeated) |
| --memory | 2Gb | Memory allocated to each MCP Server (default is 2Gb) |
| --oci-ref |  | OCI image references to use |
| --port |  | TCP port to listen on (default is to listen on stdio) |
| --registry | [registry.yaml] | Paths to the registry files (absolute or relative to ~/.docker/mcp/) |
| --secrets | docker-desktop | Colon separated paths to search for secrets. Can bedocker-desktopor a path to a .env file (default to using Docker Desktop's secrets API) |
| --servers |  | Names of the servers to enable (if non empty, ignore --registry flag) |
| --static |  | Enable static mode (aka pre-started servers) |
| --tools |  | List of tools to enable |
| --tools-config | [tools.yaml] | Paths to the tools files (absolute or relative to ~/.docker/mcp/) |
| --transport | stdio | stdio, sse or streaming (default is stdio) |
| --verbose |  | Verbose output |
| --verify-signatures |  | Verify signatures of the server images |
| --watch | true | Watch for changes and reconfigure the gateway |

---

# docker mcp gateway

# docker mcp gateway

| Description | Manage the MCP Server gateway |
| --- | --- |

## Description

Manage the MCP Server gateway

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp gateway run | Run the gateway |
