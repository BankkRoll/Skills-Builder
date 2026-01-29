# Docker contexts and more

# Docker contexts

> Learn about managing multiple daemons from a single client with contexts

# Docker contexts

   Table of contents

---

## Introduction

This guide shows how you can use contexts to manage Docker daemons from a single client.

Each context contains all information required to manage resources on the daemon.
The `docker context` command makes it easy to configure these contexts and switch between them.

As an example, a single Docker client might be configured with two contexts:

- A default context running locally
- A remote, shared context

Once these contexts are configured,
you can use the `docker context use <context-name>` command
to switch between them.

## Prerequisites

To follow the examples in this guide, you'll need:

- A Docker client that supports the top-level `context` command

Run `docker context` to verify that your Docker client supports contexts.

## The anatomy of a context

A context is a combination of several properties. These include:

- Name and description
- Endpoint configuration
- TLS info

To list available contexts, use the `docker context ls` command.

```console
$ docker context ls
NAME        DESCRIPTION                               DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
```

This shows a single context called "default".
It's configured to talk to a daemon through the local `/var/run/docker.sock` Unix socket.

The asterisk in the `NAME` column indicates that this is the active context.
This means all `docker` commands run against this context,
unless overridden with environment variables such as `DOCKER_HOST` and `DOCKER_CONTEXT`,
or on the command-line with the `--context` and `--host` flags.

Dig a bit deeper with `docker context inspect`.
The following example shows how to inspect the context called `default`.

```console
$ docker context inspect default
[
    {
        "Name": "default",
        "Metadata": {},
        "Endpoints": {
            "docker": {
                "Host": "unix:///var/run/docker.sock",
                "SkipTLSVerify": false
            }
        },
        "TLSMaterial": {},
        "Storage": {
            "MetadataPath": "\u003cIN MEMORY\u003e",
            "TLSPath": "\u003cIN MEMORY\u003e"
        }
    }
]
```

### Create a new context

You can create new contexts with the `docker context create` command.

The following example creates a new context called `docker-test` and specifies
the host endpoint of the context to TCP socket `tcp://docker:2375`.

```console
$ docker context create docker-test --docker host=tcp://docker:2375
docker-test
Successfully created context "docker-test"
```

The new context is stored in a `meta.json` file below `~/.docker/contexts/`.
Each new context you create gets its own `meta.json` stored in a dedicated sub-directory of `~/.docker/contexts/`.

You can view the new context with `docker context ls` and `docker context inspect <context-name>`.

```console
$ docker context ls
NAME          DESCRIPTION                             DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
docker-test                                           tcp://docker:2375
```

The current context is indicated with an asterisk ("*").

## Use a different context

You can use `docker context use` to switch between contexts.

The following command will switch the `docker` CLI to use the `docker-test` context.

```console
$ docker context use docker-test
docker-test
Current context is now "docker-test"
```

Verify the operation by listing all contexts and ensuring the asterisk ("*") is against the `docker-test` context.

```console
$ docker context ls
NAME            DESCRIPTION                           DOCKER ENDPOINT               ERROR
default                                               unix:///var/run/docker.sock
docker-test *                                         tcp://docker:2375
```

`docker` commands will now target endpoints defined in the `docker-test` context.

You can also set the current context using the `DOCKER_CONTEXT` environment variable.
The environment variable overrides the context set with `docker context use`.

Use the appropriate command below to set the context to `docker-test` using an environment variable.

```ps
> $env:DOCKER_CONTEXT='docker-test'
```

```console
$ export DOCKER_CONTEXT=docker-test
```

Run `docker context ls` to verify that the `docker-test` context is now the
active context.

You can also use the global `--context` flag to override the context.
The following command uses a context called `production`.

```console
$ docker --context production container ls
```

## Exporting and importing Docker contexts

You can use the `docker context export` and `docker context import` commands
to export and import contexts on different hosts.

The `docker context export` command exports an existing context to a file.
The file can be imported on any host that has the `docker` client installed.

### Exporting and importing a context

The following example exports an existing context called `docker-test`.
It will be written to a file called `docker-test.dockercontext`.

```console
$ docker context export docker-test
Written file "docker-test.dockercontext"
```

Check the contents of the export file.

```console
$ cat docker-test.dockercontext
```

Import this file on another host using `docker context import`
to create context with the same configuration.

```console
$ docker context import docker-test docker-test.dockercontext
docker-test
Successfully imported context "docker-test"
```

You can verify that the context was imported with `docker context ls`.

The format of the import command is `docker context import <context-name> <context-file>`.

## Updating a context

You can use `docker context update` to update fields in an existing context.

The following example updates the description field in the existing `docker-test` context.

```console
$ docker context update docker-test --description "Test context"
docker-test
Successfully updated context "docker-test"
```

---

# Docker object labels

> Learn about labels, a tool to manage metadata on Docker objects.

# Docker object labels

   Table of contents

---

Labels are a mechanism for applying metadata to Docker objects, including:

- Images
- Containers
- Local daemons
- Volumes
- Networks
- Swarm nodes
- Swarm services

You can use labels to organize your images, record licensing information, annotate
relationships between containers, volumes, and networks, or in any way that makes
sense for your business or application.

## Label keys and values

A label is a key-value pair, stored as a string. You can specify multiple labels
for an object, but each key must be unique within an object. If the
same key is given multiple values, the most-recently-written value overwrites
all previous values.

### Key format recommendations

A label key is the left-hand side of the key-value pair. Keys are alphanumeric
strings which may contain periods (`.`), underscores (`_`), slashes (`/`), and hyphens (`-`). Most Docker users use
images created by other organizations, and the following guidelines help to
prevent inadvertent duplication of labels across objects, especially if you plan
to use labels as a mechanism for automation.

- Authors of third-party tools should prefix each label key with the
  reverse DNS notation of a domain they own, such as `com.example.some-label`.
- Don't use a domain in your label key without the domain owner's permission.
- The `com.docker.*`, `io.docker.*`, and `org.dockerproject.*` namespaces are
  reserved by Docker for internal use.
- Label keys should begin and end with a lower-case letter and should only
  contain lower-case alphanumeric characters, the period character (`.`), and
  the hyphen character (`-`). Consecutive periods or hyphens aren't allowed.
- The period character (`.`) separates namespace "fields". Label keys without
  namespaces are reserved for CLI use, allowing users of the CLI to interactively
  label Docker objects using shorter typing-friendly strings.

These guidelines aren't currently enforced and additional guidelines may apply
to specific use cases.

### Value guidelines

Label values can contain any data type that can be represented as a string,
including (but not limited to) JSON, XML, CSV, or YAML. The only requirement is
that the value be serialized to a string first, using a mechanism specific to
the type of structure. For instance, to serialize JSON into a string, you might
use the `JSON.stringify()` JavaScript method.

Since Docker doesn't deserialize the value, you can't treat a JSON or XML
document as a nested structure when querying or filtering by label value unless
you build this functionality into third-party tooling.

## Manage labels on objects

Each type of object with support for labels has mechanisms for adding and
managing them and using them as they relate to that type of object. These links
provide a good place to start learning about how you can use labels in your
Docker deployments.

Labels on images, containers, local daemons, volumes, and networks are static for
the lifetime of the object. To change these labels you must recreate the object.
Labels on Swarm nodes and services can be updated dynamically.

- Images and containers
  - [Adding labels to images](https://docs.docker.com/reference/dockerfile/#label)
  - [Overriding a container's labels at runtime](https://docs.docker.com/reference/cli/docker/container/run/#label)
  - [Inspecting labels on images or containers](https://docs.docker.com/reference/cli/docker/inspect/)
  - [Filtering images by label](https://docs.docker.com/reference/cli/docker/image/ls/#filter)
  - [Filtering containers by label](https://docs.docker.com/reference/cli/docker/container/ls/#filter)
- Local Docker daemons
  - [Adding labels to a Docker daemon at runtime](https://docs.docker.com/reference/cli/dockerd/)
  - [Inspecting a Docker daemon's labels](https://docs.docker.com/reference/cli/docker/system/info/)
- Volumes
  - [Adding labels to volumes](https://docs.docker.com/reference/cli/docker/volume/create/)
  - [Inspecting a volume's labels](https://docs.docker.com/reference/cli/docker/volume/inspect/)
  - [Filtering volumes by label](https://docs.docker.com/reference/cli/docker/volume/ls/#filter)
- Networks
  - [Adding labels to a network](https://docs.docker.com/reference/cli/docker/network/create/)
  - [Inspecting a network's labels](https://docs.docker.com/reference/cli/docker/network/inspect/)
  - [Filtering networks by label](https://docs.docker.com/reference/cli/docker/network/ls/#filter)
- Swarm nodes
  - [Adding or updating a Swarm node's labels](https://docs.docker.com/reference/cli/docker/node/update/#label-add)
  - [Inspecting a Swarm node's labels](https://docs.docker.com/reference/cli/docker/node/inspect/)
  - [Filtering Swarm nodes by label](https://docs.docker.com/reference/cli/docker/node/ls/#filter)
- Swarm services
  - [Adding labels when creating a Swarm service](https://docs.docker.com/reference/cli/docker/service/create/#label)
  - [Updating a Swarm service's labels](https://docs.docker.com/reference/cli/docker/service/update/)
  - [Inspecting a Swarm service's labels](https://docs.docker.com/reference/cli/docker/service/inspect/)
  - [Filtering Swarm services by label](https://docs.docker.com/reference/cli/docker/service/ls/#filter)

---

# Prune unused Docker objects

> Free up disk space by removing unused resources with the prune command

# Prune unused Docker objects

   Table of contents

---

Docker takes a conservative approach to cleaning up unused objects (often
referred to as "garbage collection"), such as images, containers, volumes, and
networks. These objects are generally not removed unless you explicitly ask
Docker to do so. This can cause Docker to use extra disk space. For each type of
object, Docker provides a `prune` command. In addition, you can use `docker system prune` to clean up multiple types of objects at once. This topic shows
how to use these `prune` commands.

## Prune images

The `docker image prune` command allows you to clean up unused images. By
default, `docker image prune` only cleans up *dangling* images. A dangling image
is one that isn't tagged, and isn't referenced by any container. To remove
dangling images:

```console
$ docker image prune

WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
```

To remove all images which aren't used by existing containers, use the `-a`
flag:

```console
$ docker image prune -a

WARNING! This will remove all images without at least one container associated to them.
Are you sure you want to continue? [y/N] y
```

By default, you are prompted to continue. To bypass the prompt, use the `-f` or
`--force` flag.

You can limit which images are pruned using filtering expressions with the
`--filter` flag. For example, to only consider images created more than 24
hours ago:

```console
$ docker image prune -a --filter "until=24h"
```

Other filtering expressions are available. See the
[docker image prunereference](https://docs.docker.com/reference/cli/docker/image/prune/)
for more examples.

## Prune containers

When you stop a container, it isn't automatically removed unless you started it
with the `--rm` flag. To see all containers on the Docker host, including
stopped containers, use `docker ps -a`. You may be surprised how many containers
exist, especially on a development system! A stopped container's writable layers
still take up disk space. To clean this up, you can use the `docker container prune` command.

```console
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
```

By default, you're prompted to continue. To bypass the prompt, use the `-f` or
`--force` flag.

By default, all stopped containers are removed. You can limit the scope using
the `--filter` flag. For instance, the following command only removes
stopped containers older than 24 hours:

```console
$ docker container prune --filter "until=24h"
```

Other filtering expressions are available. See the
[docker container prunereference](https://docs.docker.com/reference/cli/docker/container/prune/)
for more examples.

## Prune volumes

Volumes can be used by one or more containers, and take up space on the Docker
host. Volumes are never removed automatically, because to do so could destroy
data.

```console
$ docker volume prune

WARNING! This will remove all volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
```

By default, you are prompted to continue. To bypass the prompt, use the `-f` or
`--force` flag.

By default, all unused volumes are removed. You can limit the scope using
the `--filter` flag. For instance, the following command only removes
volumes which aren't labelled with the `keep` label:

```console
$ docker volume prune --filter "label!=keep"
```

Other filtering expressions are available. See the
[docker volume prunereference](https://docs.docker.com/reference/cli/docker/volume/prune/)
for more examples.

## Prune networks

Docker networks don't take up much disk space, but they do create `iptables`
rules, bridge network devices, and routing table entries. To clean these things
up, you can use `docker network prune` to clean up networks which aren't used
by any containers.

```console
$ docker network prune

WARNING! This will remove all networks not used by at least one container.
Are you sure you want to continue? [y/N] y
```

By default, you're prompted to continue. To bypass the prompt, use the `-f` or
`--force` flag.

By default, all unused networks are removed. You can limit the scope using
the `--filter` flag. For instance, the following command only removes
networks older than 24 hours:

```console
$ docker network prune --filter "until=24h"
```

Other filtering expressions are available. See the
[docker network prunereference](https://docs.docker.com/reference/cli/docker/network/prune/)
for more examples.

## Prune everything

The `docker system prune` command is a shortcut that prunes images, containers,
and networks. Volumes aren't pruned by default, and you must specify the
`--volumes` flag for `docker system prune` to prune volumes.

```console
$ docker system prune

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - unused build cache

Are you sure you want to continue? [y/N] y
```

To also prune volumes, add the `--volumes` flag:

```console
$ docker system prune --volumes

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all volumes not used by at least one container
        - all dangling images
        - all build cache

Are you sure you want to continue? [y/N] y
```

By default, you're prompted to continue. To bypass the prompt, use the `-f` or
`--force` flag.

By default, all unused containers, networks, and images are removed. You can
limit the scope using the `--filter` flag. For instance, the following command
removes items older than 24 hours:

```console
$ docker system prune --filter "until=24h"
```

Other filtering expressions are available. See the
[docker system prunereference](https://docs.docker.com/reference/cli/docker/system/prune/)
for more examples.

---

# Use CA certificates with Docker

> Learn how to install and use CA certificates on the Docker host and in Linux containers

# Use CA certificates with Docker

   Table of contents

---

> Caution
>
> Best practices should be followed when using Man-in-the-Middle (MITM) CA
> certificates in production containers. If compromised, attackers could
> intercept sensitive data, spoof a trusted service, or perform
> man-in-the-middle attacks. Consult your security team before you proceed.

If your company uses a proxy that inspects HTTPS traffic, you might need to add
the required root certificates to your host machine and your Docker containers
or images. This is because Docker and its containers, when pulling images or
making network requests, need to trust the proxy’s certificates.

On the host, adding the root certificate ensures that any Docker commands (like
`docker pull`) work without issues. For containers, you'll need to add the root
certificate to the container's trust store either during the build process or
at runtime. This ensures that applications running inside the containers can
communicate through the proxy without encountering security warnings or
connection failures.

## Add CA certificate to the host

The following sections describe how to install CA certificates on your macOS or
Windows host. For Linux, refer to the documentation for your distribution.

### macOS

1. Download the CA certificate for your MITM proxy software.
2. Open the **Keychain Access** app.
3. In Keychain Access, select **System**, then switch to the **Certificates** tab.
4. Drag-and-drop the downloaded certificate into the list of certificates. Enter your password if prompted.
5. Find the newly added certificate, double-click it, and expand the **Trust** section.
6. Set **Always Trust** for the certificate. Enter your password if prompted.
7. Start Docker Desktop and verify that `docker pull` works, assuming Docker Desktop is configured to use the MITM proxy.

### Windows

Choose whether you want to install the certificate using the Microsoft
Management Console (MMC) or your web browser.

1. Download CA certificate for the MITM proxy software.
2. Open the Microsoft Management Console (`mmc.exe`).
3. Add the **Certificates Snap-In** in the MMC.
  1. Select **File** → **Add/Remove Snap-in**, and then select **Certificates** → **Add >**.
  2. Select **Computer Account** and then **Next**.
  3. Select **Local computer** and then select **Finish**.
4. Import the CA certificate:
  1. From the MMC, expand **Certificates (Local Computer)**.
  2. Expand the **Trusted Root Certification Authorities** section.
  3. Right-click **Certificates** and select **All Tasks** and **Import…**.
  4. Follow the prompts to import your CA certificate.
5. Select **Finish** and then **Close**.
6. Start Docker Desktop and verify that `docker pull` succeeds (assuming Docker Desktop is already configured to use the MITM proxy server).

> Note
>
> Depending on the SDK and/or runtime/framework in use, further steps may be
> required beyond adding the CA certificate to the operating system's trust
> store.

1. Download the CA certificate for your MITM proxy software.
2. Open your web browser, go to **Settings** and open **Manage certificates**
3. Select the **Trusted Root Certification Authorities** tab.
4. Select **Import**, then browse for the downloaded CA certificate.
5. Select **Open**, then choose **Place all certificates in the following store**.
6. Ensure **Trusted Root Certification Authorities** is selected and select **Next**.
7. Select **Finish** and then **Close**.
8. Start Docker Desktop and verify that `docker pull` succeeds (assuming Docker Desktop is already configured to use the MITM proxy server).

## Add CA certificates to Linux images and containers

If you need to run containerized workloads that rely on internal or custom
certificates, such as in environments with corporate proxies or secure
services, you must ensure that the containers trust these certificates. Without
adding the necessary CA certificates, applications inside your containers may
encounter failed requests or security warnings when attempting to connect to
HTTPS endpoints.

By [adding CA certificates to images](#add-certificates-to-images) at build
time, you ensure that any containers started from the image will trust the
specified certificates. This is particularly important for applications that
require seamless access to internal APIs, databases, or other services during
production.

In cases where rebuilding the image isn't feasible, you can instead [add
certificates to containers](#add-certificates-to-containers) directly. However,
certificates added at runtime won’t persist if the container is destroyed or
recreated, so this method is typically used for temporary fixes or testing
scenarios.

## Add certificates to images

> Note
>
> The following commands are for an Ubuntu base image. If your build uses a
> different Linux distribution, use equivalent commands for package management
> (`apt-get`, `update-ca-certificates`, and so on).

To add ca certificate to a container image when you're building it, add the
following instructions to your Dockerfile.

```dockerfile
# Install the ca-certificate package
RUN apt-get update && apt-get install -y ca-certificates
# Copy the CA certificate from the context to the build container
COPY your_certificate.crt /usr/local/share/ca-certificates/
# Update the CA certificates in the container
RUN update-ca-certificates
```

### Add certificates to containers

> Note
>
> The following commands are for an Ubuntu-based container. If your container
> uses a different Linux distribution, use equivalent commands for package
> management (`apt-get`, `update-ca-certificates`, and so on).

To add a CA certificate to a running Linux container:

1. Download the CA certificate for your MITM proxy software.
2. If the certificate is in a format other than `.crt`, convert it to `.crt` format:
  Example command
  ```console
  $ openssl x509 -in cacert.der -inform DER -out myca.crt
  ```
3. Copy the certificate into the running container:
  ```console
  $ docker cp myca.crt <containerid>:/tmp
  ```
4. Attach to the container:
  ```console
  $ docker exec -it <containerid> sh
  ```
5. Ensure the `ca-certificates` package is installed (required for updating certificates):
  ```console
  # apt-get update && apt-get install -y ca-certificates
  ```
6. Copy the certificate to the correct location for CA certificates:
  ```console
  # cp /tmp/myca.crt /usr/local/share/ca-certificates/root_cert.crt
  ```
7. Update the CA certificates:
  ```console
  # update-ca-certificates
  ```
  Example output
  ```plaintext
  Updating certificates in /etc/ssl/certs...
  rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
  1 added, 0 removed; done.
  ```
8. Verify that the container can communicate via the MITM proxy:
  ```console
  # curl https://example.com
  ```
  Example output
  ```plaintext
  <!doctype html>
  <html>
  <head>
      <title>Example Domain</title>
  ...
  ```
