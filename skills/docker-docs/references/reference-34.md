# docker scout repo enable and more

# docker scout repo enable

# docker scout repo enable

| Description | Enable Docker Scout |
| --- | --- |
| Usage | docker scout repo enable [REPOSITORY] |

## Description

The docker scout repo enable command enables Docker Scout on repositories.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all |  | Enable all repositories of the organization. Can not be used with --filter. |
| --filter |  | Regular expression to filter repositories by name |
| --integration |  | Name of the integration to use for enabling an image |
| --org |  | Namespace of the Docker organization |
| --registry |  | Container Registry |

## Examples

### Enable a specific repository

```console
$ docker scout repo enable my/repository
```

### Enable all repositories of the organization

```console
$ docker scout repo enable --all
```

### Enable some repositories based on a filter

```console
$ docker scout repo enable --filter namespace/backend
```

### Enable a repository from a specific registry

```console
$ docker scout repo enable my/repository --registry 123456.dkr.ecr.us-east-1.amazonaws.com
```

---

# docker scout repo list

# docker scout repo list

| Description | List Docker Scout repositories |
| --- | --- |
| Usage | docker scout repo list |

## Description

The docker scout repo list command shows all repositories in an organization.

If ORG is not provided the default configured organization will be used.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --filter |  | Regular expression to filter repositories by name |
| --only-disabled |  | Filter to disabled repositories only |
| --only-enabled |  | Filter to enabled repositories only |
| --only-registry |  | Filter to a specific registry only:- hub.docker.com- ecr (AWS ECR) |
| --org |  | Namespace of the Docker organization |

---

# docker scout repo

# docker scout repo

| Description | Commands to list, enable, and disable Docker Scout on repositories |
| --- | --- |

## Description

Commands to list, enable, and disable Docker Scout on repositories

## Subcommands

| Command | Description |
| --- | --- |
| docker scout repo disable | Disable Docker Scout |
| docker scout repo enable | Enable Docker Scout |
| docker scout repo list | List Docker Scout repositories |

---

# docker scout sbom

# docker scout sbom

| Description | Generate or display SBOM of an image |
| --- | --- |
| Usage | docker scout sbom [IMAGE|DIRECTORY|ARCHIVE] |

## Description

The `docker scout sbom` command analyzes a software artifact to generate a
Software Bill Of Materials (SBOM).

The SBOM contains a list of all packages in the image.
You can use the `--format` flag to filter the output of the command
to display only packages of a specific type.

If no image is specified, the most recently built image is used.

The following artifact types are supported:

- Images
- OCI layout directories
- Tarball archives, as created by `docker save`
- Local directory or file

By default, the tool expects an image reference, such as:

- `redis`
- `curlimages/curl:7.87.0`
- `mcr.microsoft.com/dotnet/runtime:7.0`

If the artifact you want to analyze is an OCI directory, a tarball archive, a local file or directory,
or if you want to control from where the image will be resolved, you must prefix the reference with one of the following:

- `image://` (default) use a local image, or fall back to a registry lookup
- `local://` use an image from the local image store (don't do a registry lookup)
- `registry://` use an image from a registry (don't use a local image)
- `oci-dir://` use an OCI layout directory
- `archive://` use a tarball archive, as created by `docker save`
- `fs://` use a local directory or file

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | json | Output format:- list: list of packages of the image- json: json representation of the SBOM- spdx: spdx representation of the SBOM- cyclonedx: cyclone dx representation of the SBOM |
| --only-package-type |  | Comma separated list of package types (like apk, deb, rpm, npm, pypi, golang, etc)Can only be used with --format list |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |

## Examples

### Display the list of packages

```console
$ docker scout sbom --format list alpine
```

### Only display packages of a specific type

```console
$ docker scout sbom --format list --only-package-type apk alpine
```

### Display the full SBOM in JSON format

```console
$ docker scout sbom alpine
```

### Display the full SBOM of the most recently built image

```console
$ docker scout sbom
```

### Write SBOM to a file

```console
$ docker scout sbom --output alpine.sbom alpine
```

---

# docker scout stream

# docker scout stream

| Description | Manage streams (experimental) |
| --- | --- |
| Usage | docker scout stream [STREAM] [IMAGE] |

> Warning
>
> This command is deprecated
>
>
>
> It may be removed in a future Docker version. For more information, see the
> [Docker roadmap](https://github.com/docker/roadmap/issues/209)

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The `docker scout stream` command lists the deployment streams and records an image to it.

Once recorded, streams can be referred to by their name, eg. in the `docker scout compare` command using `--to-stream`.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to record |

## Examples

### List existing streams

```console
$ %[1]s %[2]s
prod-cluster-123
stage-cluster-234
```

### List images of a stream

```console
$ %[1]s %[2]s prod-cluster-123
namespace/repo:tag@sha256:9a4df4fadc9bbd44c345e473e0688c2066a6583d4741679494ba9228cfd93e1b
namespace/other-repo:tag@sha256:0001d6ce124855b0a158569c584162097fe0ca8d72519067c2c8e3ce407c580f
```

### Record an image to a stream, for a specific platform

```console
$ %[1]s %[2]s stage-cluster-234 namespace/repo:stage-latest --platform linux/amd64
✓ Pulled
✓ Successfully recorded namespace/repo:stage-latest in stream stage-cluster-234
```

---

# docker scout version

# docker scout version

| Description | Show Docker Scout version information |
| --- | --- |
| Usage | docker scout version |

## Description

Show Docker Scout version information

## Examples

```console
$ docker scout version

      ⢀⢀⢀             ⣀⣀⡤⣔⢖⣖⢽⢝
   ⡠⡢⡣⡣⡣⡣⡣⡣⡢⡀    ⢀⣠⢴⡲⣫⡺⣜⢞⢮⡳⡵⡹⡅
  ⡜⡜⡜⡜⡜⡜⠜⠈⠈        ⠁⠙⠮⣺⡪⡯⣺⡪⡯⣺
 ⢘⢜⢜⢜⢜⠜               ⠈⠪⡳⡵⣹⡪⠇
 ⠨⡪⡪⡪⠂    ⢀⡤⣖⢽⡹⣝⡝⣖⢤⡀    ⠘⢝⢮⡚       _____                 _
  ⠱⡱⠁    ⡴⡫⣞⢮⡳⣝⢮⡺⣪⡳⣝⢦    ⠘⡵⠁      / ____| Docker        | |
   ⠁    ⣸⢝⣕⢗⡵⣝⢮⡳⣝⢮⡺⣪⡳⣣    ⠁      | (___   ___ ___  _   _| |_
        ⣗⣝⢮⡳⣝⢮⡳⣝⢮⡳⣝⢮⢮⡳            \___ \ / __/ _ \| | | | __|
   ⢀    ⢱⡳⡵⣹⡪⡳⣝⢮⡳⣝⢮⡳⡣⡏    ⡀       ____) | (_| (_) | |_| | |_
  ⢀⢾⠄    ⠫⣞⢮⡺⣝⢮⡳⣝⢮⡳⣝⠝    ⢠⢣⢂     |_____/ \___\___/ \__,_|\__|
  ⡼⣕⢗⡄    ⠈⠓⠝⢮⡳⣝⠮⠳⠙     ⢠⢢⢣⢣
 ⢰⡫⡮⡳⣝⢦⡀              ⢀⢔⢕⢕⢕⢕⠅
 ⡯⣎⢯⡺⣪⡳⣝⢖⣄⣀        ⡀⡠⡢⡣⡣⡣⡣⡣⡃
⢸⢝⢮⡳⣝⢮⡺⣪⡳⠕⠗⠉⠁    ⠘⠜⡜⡜⡜⡜⡜⡜⠜⠈
⡯⡳⠳⠝⠊⠓⠉             ⠈⠈⠈⠈

version: v1.0.9 (go1.21.3 - darwin/arm64)
git commit: 8bf95bf60d084af341f70e8263342f71b0a3cd16
```

---

# docker scout vex get

# docker scout vex get

| Description | Get VEX attestation for image |
| --- | --- |
| Usage | docker scout vex get OPTIONS IMAGE |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The docker scout vex get command gets a VEX attestation for images.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --key | https://registry.scout.docker.com/keyring/dhi/latest.pub | Signature key to use for verification |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |
| --skip-tlog |  | Skip signature verification against public transaction log |
| --verify |  | Verify the signature on the attestation |

---

# docker scout vex

# docker scout vex

| Description | Manage VEX attestations on images |
| --- | --- |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout vex |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Manage VEX attestations on images

## Subcommands

| Command | Description |
| --- | --- |
| docker scout vex get | Get VEX attestation for image |

---

# docker scout watch

# docker scout watch

| Description | Watch repositories in a registry and push images and indexes to Docker Scout |
| --- | --- |
| Usage | docker scout watch |

## Description

The docker scout watch command watches repositories in a registry and pushes images or image indexes to Docker Scout.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all-images |  | Push all images instead of only the ones pushed during the watch command is running |
| --dry-run |  | Watch images and prepare them, but do not push them |
| --interval | 60 | Interval in seconds between checks |
| --org |  | Namespace of the Docker organization to which image will be pushed |
| --refresh-registry |  | Refresh the list of repositories of a registry at every run. Only with --registry. |
| --registry |  | Registry to watch |
| --repository |  | Repository to watch |
| --sbom | true | Create and upload SBOMs |
| --tag |  | Regular expression to match tags to watch |
| --workers | 3 | Number of concurrent workers |

## Examples

Watch for new images from two repositories and push them
$ docker scout watch --org my-org --repository registry-1.example.com/repo-1 --repository registry-2.example.com/repo-2[0m

Only push images with a specific tag
$ docker scout watch --org my-org --repository registry.example.com/my-service --tag latest[0m

Watch all repositories of a registry
$ docker scout watch --org my-org --registry registry.example.com[0m

Push all images and not just the new ones
$ docker scout watch --org my-org --repository registry.example.com/my-service --all-images[0m

---

# docker scout

# docker scout

| Description | Command line tool for Docker Scout |
| --- | --- |
| Usage | docker scout [command] |

## Description

Command line tool for Docker Scout

## Subcommands

| Command | Description |
| --- | --- |
| docker scout attestation | Manage attestations on images |
| docker scout cache | Manage Docker Scout cache and temporary files |
| docker scout compare | Compare two images and display differences (experimental) |
| docker scout config | Manage Docker Scout configuration |
| docker scout cves | Display CVEs identified in a software artifact |
| docker scout enroll | Enroll an organization with Docker Scout |
| docker scout environment | Manage environments (experimental) |
| docker scout integration | Commands to list, configure, and delete Docker Scout integrations |
| docker scout policy | Evaluate policies against an image and display the policy evaluation results (experimental) |
| docker scout push | Push an image or image index to Docker Scout |
| docker scout quickview | Quick overview of an image |
| docker scout recommendations | Display available base image updates and remediation recommendations |
| docker scout repo | Commands to list, enable, and disable Docker Scout on repositories |
| docker scout sbom | Generate or display SBOM of an image |
| docker scout stream | Manage streams (experimental) |
| docker scout version | Show Docker Scout version information |
| docker scout vex | Manage VEX attestations on images |
| docker scout watch | Watch repositories in a registry and push images and indexes to Docker Scout |

---

# docker search

# docker search

| Description | Search Docker Hub for images |
| --- | --- |
| Usage | docker search [OPTIONS] TERM |

## Description

Search [Docker Hub](https://hub.docker.com) for images

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Pretty-print search using a Go template |
| --limit |  | Max number of search results |
| --no-trunc |  | Don't truncate output |

## Examples

### Search images by name

This example displays images with a name containing 'busybox':

```console
$ docker search busybox

NAME                             DESCRIPTION                                     STARS     OFFICIAL
busybox                          Busybox base image.                             316       [OK]
progrium/busybox                                                                 50
radial/busyboxplus               Full-chain, Internet enabled, busybox made...   8
odise/busybox-python                                                             2
azukiapp/busybox                 This image is meant to be used as the base...   2
ofayau/busybox-jvm               Prepare busybox to install a 32 bits JVM.       1
shingonoide/archlinux-busybox    Arch Linux, a lightweight and flexible Lin...   1
odise/busybox-curl                                                               1
ofayau/busybox-libc32            Busybox with 32 bits (and 64 bits) libs         1
peelsky/zulu-openjdk-busybox                                                     1
skomma/busybox-data              Docker image suitable for data volume cont...   1
elektritter/busybox-teamspeak    Lightweight teamspeak3 container based on...    1
socketplane/busybox                                                              1
oveits/docker-nginx-busybox      This is a tiny NginX docker image based on...   0
ggtools/busybox-ubuntu           Busybox ubuntu version with extra goodies       0
nikfoundas/busybox-confd         Minimal busybox based distribution of confd     0
openshift/busybox-http-app                                                       0
jllopis/busybox                                                                  0
swyckoff/busybox                                                                 0
powellquiring/busybox                                                            0
williamyeh/busybox-sh            Docker image for BusyBox's sh                   0
simplexsys/busybox-cli-powered   Docker busybox images, with a few often us...   0
fhisamoto/busybox-java           Busybox java                                    0
scottabernethy/busybox                                                           0
marclop/busybox-solr
```

### Display non-truncated description (--no-trunc)

This example displays images with a name containing 'busybox',
at least 3 stars and the description isn't truncated in the output:

```console
$ docker search --filter=stars=3 --no-trunc busybox

NAME                 DESCRIPTION                                                                               STARS     OFFICIAL
busybox              Busybox base image.                                                                       325       [OK]
progrium/busybox                                                                                               50
radial/busyboxplus   Full-chain, Internet enabled, busybox made from scratch. Comes in git and cURL flavors.   8
```

### Limit search results (--limit)

The flag `--limit` is the maximum number of results returned by a search. If no
value is set, the default is set by the daemon.

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there is more
than one filter, then pass multiple flags (e.g. `--filter is-official=true --filter stars=3`).

The currently supported filters are:

- stars (int - number of stars the image has)
- is-automated (boolean - true or false) - is the image automated or not (deprecated)
- is-official (boolean - true or false) - is the image official or not

#### stars

This example displays images with a name containing 'busybox' and at
least 3 stars:

```console
$ docker search --filter stars=3 busybox

NAME                 DESCRIPTION                                     STARS     OFFICIAL
busybox              Busybox base image.                             325       [OK]
progrium/busybox                                                     50
radial/busyboxplus   Full-chain, Internet enabled, busybox made...   8
```

#### is-official

This example displays images with a name containing 'busybox', at least
3 stars and are official builds:

```console
$ docker search --filter is-official=true --filter stars=3 busybox

NAME      DESCRIPTION           STARS     OFFICIAL
busybox   Busybox base image.   325       [OK]
```

### Format the output (--format)

The formatting option (`--format`) pretty-prints search output
using a Go template.

Valid placeholders for the Go template are:

| Placeholder | Description |
| --- | --- |
| .Name | Image Name |
| .Description | Image description |
| .StarCount | Number of stars for the image |
| .IsOfficial | "OK" if image is official |

When you use the `--format` option, the `search` command will
output the data exactly as the template declares. If you use the
`table` directive, column headers are included as well.

The following example uses a template without headers and outputs the
`Name` and `StarCount` entries separated by a colon (`:`) for all images:

```console
$ docker search --format "{{.Name}}: {{.StarCount}}" nginx

nginx: 5441
jwilder/nginx-proxy: 953
richarvey/nginx-php-fpm: 353
million12/nginx-php: 75
webdevops/php-nginx: 70
h3nrik/nginx-ldap: 35
bitnami/nginx: 23
evild/alpine-nginx: 14
million12/nginx: 9
maxexcloo/nginx: 7
```

This example outputs a table format:

```console
$ docker search --format "table {{.Name}}\t{{.IsOfficial}}" nginx

NAME                                     OFFICIAL
nginx                                    [OK]
jwilder/nginx-proxy
richarvey/nginx-php-fpm
jrcs/letsencrypt-nginx-proxy-companion
million12/nginx-php
webdevops/php-nginx
```

---

# docker secret create

# docker secret create

| Description | Create a secret from a file or STDIN as content |
| --- | --- |
| Usage | docker secret create [OPTIONS] SECRET [file|-] |

Swarm
This command works with the Swarm orchestrator.

## Description

Creates a secret using standard input or from a file for the secret content.

For detailed information about using secrets, refer to
[manage sensitive data with Docker secrets](https://docs.docker.com/engine/swarm/secrets/).

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --driver |  | API 1.31+Secret driver |
| -l, --label |  | Secret labels |
| --template-driver |  | API 1.37+Template driver |

## Examples

### Create a secret

```console
$ printf "my super secret password" | docker secret create my_secret -

onakdyv307se2tl7nl20anokv

$ docker secret ls

ID                          NAME                CREATED             UPDATED
onakdyv307se2tl7nl20anokv   my_secret           6 seconds ago       6 seconds ago
```

### Create a secret with a file

```console
$ docker secret create my_secret ./secret.json

dg426haahpi5ezmkkj5kyl3sn

$ docker secret ls

ID                          NAME                CREATED             UPDATED
dg426haahpi5ezmkkj5kyl3sn   my_secret           7 seconds ago       7 seconds ago
```

### Create a secret with labels (--label)

```console
$ docker secret create \
  --label env=dev \
  --label rev=20170324 \
  my_secret ./secret.json

eo7jnzguqgtpdah3cm5srfb97
```

```console
$ docker secret inspect my_secret

[
    {
        "ID": "eo7jnzguqgtpdah3cm5srfb97",
        "Version": {
            "Index": 17
        },
        "CreatedAt": "2017-03-24T08:15:09.735271783Z",
        "UpdatedAt": "2017-03-24T08:15:09.735271783Z",
        "Spec": {
            "Name": "my_secret",
            "Labels": {
                "env": "dev",
                "rev": "20170324"
            }
        }
    }
]
```

---

# docker secret inspect

# docker secret inspect

| Description | Display detailed information on one or more secrets |
| --- | --- |
| Usage | docker secret inspect [OPTIONS] SECRET [SECRET...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Inspects the specified secret.

By default, this renders all results in a JSON array. If a format is specified,
the given template will be executed for each result.

Go's [text/template](https://pkg.go.dev/text/template) package
describes all the details of the format.

For detailed information about using secrets, refer to
[manage sensitive data with Docker secrets](https://docs.docker.com/engine/swarm/secrets/).

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --pretty |  | Print the information in a human friendly format |

## Examples

### Inspect a secret by name or ID

You can inspect a secret, either by its name or ID.

For example, given the following secret:

```console
$ docker secret ls

ID                          NAME                CREATED             UPDATED
eo7jnzguqgtpdah3cm5srfb97   my_secret           3 minutes ago       3 minutes ago
```

```console
$ docker secret inspect secret.json
```

The output is in JSON format, for example:

```json
[
  {
    "ID": "eo7jnzguqgtpdah3cm5srfb97",
    "Version": {
      "Index": 17
    },
    "CreatedAt": "2017-03-24T08:15:09.735271783Z",
    "UpdatedAt": "2017-03-24T08:15:09.735271783Z",
    "Spec": {
      "Name": "my_secret",
      "Labels": {
        "env": "dev",
        "rev": "20170324"
      }
    }
  }
]
```

### Format the output (--format)

You can use the `--format` option to obtain specific information about a
secret. The following example command outputs the creation time of the
secret.

```console
$ docker secret inspect --format='{{.CreatedAt}}' eo7jnzguqgtpdah3cm5srfb97

2017-03-24 08:15:09.735271783 +0000 UTC
```

---

# docker secret ls

# docker secret ls

| Description | List secrets |
| --- | --- |
| Usage | docker secret ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker secret list |

Swarm
This command works with the Swarm orchestrator.

## Description

Run this command on a manager node to list the secrets in the swarm.

For detailed information about using secrets, refer to
[manage sensitive data with Docker secrets](https://docs.docker.com/engine/swarm/secrets/).

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -q, --quiet |  | Only display IDs |

## Examples

```console
$ docker secret ls

ID                          NAME                        CREATED             UPDATED
6697bflskwj1998km1gnnjr38   q5s5570vtvnimefos1fyeo2u2   6 weeks ago         6 weeks ago
9u9hk4br2ej0wgngkga6rp4hq   my_secret                   5 weeks ago         5 weeks ago
mem02h8n73mybpgqjf0kfi1n0   test_secret                 3 seconds ago       3 seconds ago
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

- [id](#id) (secret's ID)
- [label](#label) (`label=<key>` or `label=<key>=<value>`)
- [name](#name) (secret's name)

#### id

The `id` filter matches all or prefix of a secret's id.

```console
$ docker secret ls -f "id=6697bflskwj1998km1gnnjr38"

ID                          NAME                        CREATED             UPDATED
6697bflskwj1998km1gnnjr38   q5s5570vtvnimefos1fyeo2u2   6 weeks ago         6 weeks ago
```

#### label

The `label` filter matches secrets based on the presence of a `label` alone or
a `label` and a value.

The following filter matches all secrets with a `project` label regardless of
its value:

```console
$ docker secret ls --filter label=project

ID                          NAME                        CREATED             UPDATED
mem02h8n73mybpgqjf0kfi1n0   test_secret                 About an hour ago   About an hour ago
```

The following filter matches only services with the `project` label with the
`project-a` value.

```console
$ docker service ls --filter label=project=test

ID                          NAME                        CREATED             UPDATED
mem02h8n73mybpgqjf0kfi1n0   test_secret                 About an hour ago   About an hour ago
```

#### name

The `name` filter matches on all or prefix of a secret's name.

The following filter matches secret with a name containing a prefix of `test`.

```console
$ docker secret ls --filter name=test_secret

ID                          NAME                        CREATED             UPDATED
mem02h8n73mybpgqjf0kfi1n0   test_secret                 About an hour ago   About an hour ago
```

### Format the output (--format)

The formatting option (`--format`) pretty prints secrets output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Secret ID |
| .Name | Secret name |
| .CreatedAt | Time when the secret was created |
| .UpdatedAt | Time when the secret was updated |
| .Labels | All labels assigned to the secret |
| .Label | Value of a specific label for this secret. For example{{.Label "secret.ssh.key"}} |

When using the `--format` option, the `secret ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, will include column headers as well.

The following example uses a template without headers and outputs the
`ID` and `Name` entries separated by a colon (`:`) for all images:

```console
$ docker secret ls --format "{{.ID}}: {{.Name}}"

77af4d6b9913: secret-1
b6fa739cedf5: secret-2
78a85c484f71: secret-3
```

To list all secrets with their name and created date in a table format you
can use:

```console
$ docker secret ls --format "table {{.ID}}\t{{.Name}}\t{{.CreatedAt}}"

ID                  NAME                      CREATED
77af4d6b9913        secret-1                  5 minutes ago
b6fa739cedf5        secret-2                  3 hours ago
78a85c484f71        secret-3                  10 days ago
```

To list all secrets in JSON format, use the `json` directive:

```console
$ docker secret ls --format json
{"CreatedAt":"28 seconds ago","Driver":"","ID":"4y7hvwrt1u8e9uxh5ygqj7mzc","Labels":"","Name":"mysecret","UpdatedAt":"28 seconds ago"}
```

---

# docker secret rm

# docker secret rm

| Description | Remove one or more secrets |
| --- | --- |
| Usage | docker secret rm SECRET [SECRET...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker secret remove |

Swarm
This command works with the Swarm orchestrator.

## Description

Removes the specified secrets from the swarm.

For detailed information about using secrets, refer to
[manage sensitive data with Docker secrets](https://docs.docker.com/engine/swarm/secrets/).

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Examples

This example removes a secret:

```console
$ docker secret rm secret.json
sapth4csdo5b6wz2p5uimh5xg
```

> Warning
>
> Unlike `docker rm`, this command does not ask for confirmation before removing
> a secret.

---

# docker secret

# docker secret

| Description | Manage Swarm secrets |
| --- | --- |
| Usage | docker secret |

Swarm
This command works with the Swarm orchestrator.

## Description

Manage secrets.

## Subcommands

| Command | Description |
| --- | --- |
| docker secret create | Create a secret from a file or STDIN as content |
| docker secret inspect | Display detailed information on one or more secrets |
| docker secret ls | List secrets |
| docker secret rm | Remove one or more secrets |
