# Local and tar exporters and more

# Local and tar exporters

> The local and tar exporters save the build result to the local filesystem

# Local and tar exporters

   Table of contents

---

The `local` and `tar` exporters output the root filesystem of the build result
into a local directory. They're useful for producing artifacts that aren't
container images.

- `local` exports files and directories.
- `tar` exports the same, but bundles the export into a tarball.

## Synopsis

Build a container image using the `local` exporter:

```console
$ docker buildx build --output type=local[,parameters] .
$ docker buildx build --output type=tar[,parameters] .
```

The following table describes the available parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| dest | String |  | Path to copy files to |
| platform-split | Boolean | true | localexporter only. Split multi-platform outputs into platform subdirectories. |

## Multi-platform builds with local exporter

The `platform-split` parameter controls how multi-platform build outputs are
organized.

Consider this Dockerfile that creates platform-specific files:

```dockerfile
FROM busybox AS build
ARG TARGETOS
ARG TARGETARCH
RUN mkdir /out && echo foo > /out/hello-$TARGETOS-$TARGETARCH

FROM scratch
COPY --from=build /out /
```

### Split by platform (default)

By default, the local exporter creates a separate subdirectory for each
platform:

```console
$ docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --output type=local,dest=./output \
  .
```

This produces the following directory structure:

```text
output/
├── linux_amd64/
│   └── hello-linux-amd64
└── linux_arm64/
    └── hello-linux-arm64
```

### Merge all platforms

To merge files from all platforms into the same directory, set
`platform-split=false`:

```console
$ docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --output type=local,dest=./output,platform-split=false \
  .
```

This produces a flat directory structure:

```text
output/
├── hello-linux-amd64
└── hello-linux-arm64
```

Files from all platforms merge into a single directory. If multiple platforms
produce files with identical names, the export fails with an error.

### Single-platform builds

Single-platform builds export directly to the destination directory without
creating a platform subdirectory:

```console
$ docker buildx build \
  --platform linux/amd64 \
  --output type=local,dest=./output \
  .
```

This produces:

```text
output/
└── hello-linux-amd64
```

To include the platform subdirectory even for single-platform builds, explicitly
set `platform-split=true`:

```console
$ docker buildx build \
  --platform linux/amd64 \
  --output type=local,dest=./output,platform-split=true \
  .
```

This produces:

```text
output/
└── linux_amd64/
    └── hello-linux-amd64
```

## Further reading

For more information on the `local` or `tar` exporters, see the
[BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#local-directory).

---

# OCI and Docker exporters

> The OCI and Docker exporters create an image layout tarball on the local filesystem

# OCI and Docker exporters

   Table of contents

---

The `oci` exporter outputs the build result into an
[OCI image layout](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)
tarball. The `docker` exporter behaves the same way, except it exports a Docker
image layout instead.

The
[dockerdriver](https://docs.docker.com/build/builders/drivers/docker/) doesn't support these exporters. You
must use `docker-container` or some other driver if you want to generate these
outputs.

## Synopsis

Build a container image using the `oci` and `docker` exporters:

```console
$ docker buildx build --output type=oci[,parameters] .
```

```console
$ docker buildx build --output type=docker[,parameters] .
```

The following table describes the available parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| name | String |  | Specify image name(s) |
| dest | String |  | Path |
| tar | true,false | true | Bundle the output into a tarball layout |
| compression | uncompressed,gzip,estargz,zstd | gzip | Compression type, seecompression |
| compression-level | 0..22 |  | Compression level, seecompression |
| force-compression | true,false | false | Forcefully apply compression, seecompression |
| oci-mediatypes | true,false |  | Use OCI media types in exporter manifests. Defaults totruefortype=oci, andfalsefortype=docker. SeeOCI Media types |
| annotation.<key> | String |  | Attach an annotation with the respectivekeyandvalueto the built image,seeannotations |

## Annotations

These exporters support adding OCI annotation using `annotation` parameter,
followed by the annotation name using dot notation. The following example sets
the `org.opencontainers.image.title` annotation:

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

For more information about annotations, see
[BuildKit documentation](https://github.com/moby/buildkit/blob/master/docs/annotations.md).

## Further reading

For more information on the `oci` or `docker` exporters, see the
[BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#docker-tarball).

---

# Exporters overview

> Build exporters define the output format of your build result

# Exporters overview

   Table of contents

---

Exporters save your build results to a specified output type. You specify the
exporter to use with the
[--outputCLI option](https://docs.docker.com/reference/cli/docker/buildx/build/#output).
Buildx supports the following exporters:

- `image`: exports the build result to a container image.
- `registry`: exports the build result into a container image, and pushes it to
  the specified registry.
- `local`: exports the build root filesystem into a local directory.
- `tar`: packs the build root filesystem into a local tarball.
- `oci`: exports the build result to the local filesystem in the
  [OCI image layout](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md)
  format.
- `docker`: exports the build result to the local filesystem in the
  [Docker Image Specification v1.2.0](https://github.com/moby/moby/blob/v25.0.0/image/spec/v1.2.md)
  format.
- `cacheonly`: doesn't export a build output, but runs the build and creates a
  cache.

## Using exporters

To specify an exporter, use the following command syntax:

```console
$ docker buildx build --tag <registry>/<image> \
  --output type=TYPE .
```

Most common use cases don't require that you specify which exporter to use
explicitly. You only need to specify the exporter if you intend to customize
the output, or if you want to save it to disk. The `--load` and `--push`
options allow Buildx to infer the exporter settings to use.

For example, if you use the `--push` option in combination with `--tag`, Buildx
automatically uses the `image` exporter, and configures the exporter to push the
results to the specified registry.

To get the full flexibility out of the various exporters BuildKit has to offer,
you use the `--output` flag that lets you configure exporter options.

## Use cases

Each exporter type is designed for different use cases. The following sections
describe some common scenarios, and how you can use exporters to generate the
output that you need.

### Load to image store

Buildx is often used to build container images that can be loaded to an image
store. That's where the `docker` exporter comes in. The following example shows
how to build an image using the `docker` exporter, and have that image loaded to
the local image store, using the `--output` option:

```console
$ docker buildx build \
  --output type=docker,name=<registry>/<image> .
```

Buildx CLI will automatically use the `docker` exporter and load it to the image
store if you supply the `--tag` and `--load` options:

```console
$ docker buildx build --tag <registry>/<image> --load .
```

Building images using the `docker` driver are automatically loaded to the local
image store.

Images loaded to the image store are available to `docker run` immediately
after the build finishes, and you'll see them in the list of images when you run
the `docker images` command.

### Push to registry

To push a built image to a container registry, you can use the `registry` or
`image` exporters.

When you pass the `--push` option to the Buildx CLI, you instruct BuildKit to
push the built image to the specified registry:

```console
$ docker buildx build --tag <registry>/<image> --push .
```

Under the hood, this uses the `image` exporter, and sets the `push` parameter.
It's the same as using the following long-form command using the `--output`
option:

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true .
```

You can also use the `registry` exporter, which does the same thing:

```console
$ docker buildx build \
  --output type=registry,name=<registry>/<image> .
```

### Export image layout to file

You can use either the `oci` or `docker` exporters to save the build results to
image layout on your local filesystem. Both of these exporters generate a tar
archive file containing the corresponding image layout. The `dest` parameter
defines the target output path for the tarball.

```console
$ docker buildx build --output type=oci,dest=./image.tar .
[+] Building 0.8s (7/7) FINISHED
 ...
 => exporting to oci image format                                                                     0.0s
 => exporting layers                                                                                  0.0s
 => exporting manifest sha256:c1ef01a0a0ef94a7064d5cbce408075730410060e253ff8525d1e5f7e27bc900        0.0s
 => exporting config sha256:eadab326c1866dd247efb52cb715ba742bd0f05b6a205439f107cf91b3abc853          0.0s
 => sending tarball                                                                                   0.0s
$ mkdir -p out && tar -C out -xf ./image.tar
$ tree out
out
├── blobs
│   └── sha256
│       ├── 9b18e9b68314027565b90ff6189d65942c0f7986da80df008b8431276885218e
│       ├── c78795f3c329dbbbfb14d0d32288dea25c3cd12f31bd0213be694332a70c7f13
│       ├── d1cf38078fa218d15715e2afcf71588ee482352d697532cf316626164699a0e2
│       ├── e84fa1df52d2abdfac52165755d5d1c7621d74eda8e12881f6b0d38a36e01775
│       └── fe9e23793a27fe30374308988283d40047628c73f91f577432a0d05ab0160de7
├── index.json
├── manifest.json
└── oci-layout
```

### Export filesystem

If you don't want to build an image from your build results, but instead export
the filesystem that was built, you can use the `local` and `tar` exporters.

The `local` exporter unpacks the filesystem into a directory structure in the
specified location. The `tar` exporter creates a tarball archive file.

```console
$ docker buildx build --output type=local,dest=<path/to/output> .
```

The `local` exporter is useful in [multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
since it allows you to export only a minimal number of build artifacts, such as
self-contained binaries.

### Cache-only export

The `cacheonly` exporter can be used if you just want to run a build, without
exporting any output. This can be useful if, for example, you want to run a test
build. Or, if you want to run the build first, and create exports using
subsequent commands. The `cacheonly` exporter creates a build cache, so any
successive builds are instant.

```console
$ docker buildx build --output type=cacheonly
```

If you don't specify an exporter, and you don't provide short-hand options like
`--load` that automatically selects the appropriate exporter, Buildx defaults to
using the `cacheonly` exporter. Except if you build using the `docker` driver,
in which case you use the `docker` exporter.

Buildx logs a warning message when using `cacheonly` as a default:

```console
$ docker buildx build .
WARNING: No output specified with docker-container driver.
         Build result will only remain in the build cache.
         To push result image into registry use --push or
         to load image into docker use --load
```

## Multiple exporters

Requires: Docker Buildx [0.13.0](https://github.com/docker/buildx/releases/tag/v0.13.0) and later

You can use multiple exporters for any given build by specifying the `--output`
flag multiple times. This requires **both Buildx and BuildKit** version 0.13.0
or later.

The following example runs a single build, using three
different exporters:

- The `registry` exporter to push the image to a registry
- The `local` exporter to extract the build results to the local filesystem
- The `--load` flag (a shorthand for the `image` exporter) to load the results to the local image store.

```console
$ docker buildx build \
  --output type=registry,tag=<registry>/<image> \
  --output type=local,dest=<path/to/output> \
  --load .
```

## Configuration options

This section describes some configuration options available for exporters.

The options described here are common for at least two or more exporter types.
Additionally, the different exporters types support specific parameters as well.
See the detailed page about each exporter for more information about which
configuration parameters apply.

The common parameters described here are:

- [Compression](#compression)
- [OCI media type](#oci-media-types)

### Compression

When you export a compressed output, you can configure the exact compression
algorithm and level to use. While the default values provide a good
out-of-the-box experience, you can tweak the parameters to optimize for
storage versus compute costs. Changing the compression parameters can reduce storage
space required, and improve image download times, but will increase build times.

To select the compression algorithm, you can use the `compression` option. For
example, to build an `image` with `compression=zstd`:

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true,compression=zstd .
```

Use the `compression-level=<value>` option alongside the `compression` parameter
to choose a compression level for the algorithms which support it:

- 0-9 for `gzip` and `estargz`
- 0-22 for `zstd`

As a general rule, the higher the number, the smaller the resulting file will
be, and the longer the compression will take to run.

Use the `force-compression=true` option to force re-compressing layers imported
from a previous image, if the requested compression algorithm is different from
the previous compression algorithm.

> Note
>
> The `gzip` and `estargz` compression methods use the [compress/gzippackage](https://pkg.go.dev/compress/gzip),
> while `zstd` uses the [github.com/klauspost/compress/zstdpackage](https://github.com/klauspost/compress/tree/master/zstd).

### OCI media types

The `image`, `registry`, `oci` and `docker` exporters create container images.
These exporters support both Docker media types (default) and OCI media types

To export images with OCI media types set, use the `oci-mediatypes` property.

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true,oci-mediatypes=true .
```

## What's next

Read about each of the exporters to learn about how they work and how to use
them:

- [Image and registry exporters](https://docs.docker.com/build/exporters/image-registry/)
- [OCI and Docker exporters](https://docs.docker.com/build/exporters/oci-docker/).
- [Local and tar exporters](https://docs.docker.com/build/exporters/local-tar/)

---

# Annotations

> Annotations specify additional metadata about OCI images

# Annotations

   Table of contents

---

Annotations provide descriptive metadata for images. Use annotations to record
arbitrary information and attach it to your image, which helps consumers and
tools understand the origin, contents, and how to use the image.

Annotations are similar to, and in some sense overlap with,
[labels](https://docs.docker.com/engine/manage-resources/labels/). Both
serve the same purpose: to attach metadata to a resource. As a general principle,
you can think of the difference between annotations and labels as follows:

- Annotations describe OCI image components, such as [manifests](https://github.com/opencontainers/image-spec/blob/main/manifest.md), [indexes](https://github.com/opencontainers/image-spec/blob/main/image-index.md),
  and [descriptors](https://github.com/opencontainers/image-spec/blob/main/descriptor.md).
- Labels describe Docker resources, such as images, containers, networks, and
  volumes.

The OCI image [specification](https://github.com/opencontainers/image-spec/blob/main/annotations.md) defines the format of annotations, as well as a set
of pre-defined annotation keys. Adhering to the specified standards ensures
that metadata about images can be surfaced automatically and consistently, by
tools like Docker Scout.

Annotations are not to be confused with
[attestations](https://docs.docker.com/build/metadata/attestations/):

- Attestations contain information about how an image was built and what it contains.
  An attestation is attached as a separate manifest on the image index.
  Attestations are not standardized by the Open Container Initiative.
- Annotations contain arbitrary metadata about an image.
  Annotations attach to the image [config](https://github.com/opencontainers/image-spec/blob/main/config.md) as labels,
  or on the image index or manifest as properties.

## Add annotations

You can add annotations to an image at build-time, or when creating the image
manifest or index.

> Note
>
> The Docker Engine image store doesn't support loading images with
> annotations. To build with annotations, make sure to push the image directly
> to a registry, using the `--push` CLI flag or the
> [registry exporter](https://docs.docker.com/build/exporters/image-registry/).

To specify annotations on the command line, use the `--annotation` flag for the
`docker build` command:

```console
$ docker build --push --annotation "foo=bar" .
```

If you're using
[Bake](https://docs.docker.com/build/bake/), you can use the `annotations`
attribute to specify annotations for a given target:

```hcl
target "default" {
  output = ["type=registry"]
  annotations = ["foo=bar"]
}
```

For examples on how to add annotations to images built with GitHub Actions, see
[Add image annotations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/annotations/)

You can also add annotations to an image created using `docker buildx imagetools create`. This command only supports adding annotations to an index
or manifest descriptors, see
[CLI reference](https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/#annotation).

## Inspect annotations

To view annotations on an **image index**, use the `docker buildx imagetools inspect` command. This shows you any annotations for the index and descriptors
(references to manifests) that the index contains. The following example shows
an `org.opencontainers.image.documentation` annotation on a descriptor, and an
`org.opencontainers.image.authors` annotation on the index.

```console
$ docker buildx imagetools inspect IMAGE --raw
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb",
      "size": 911,
      "annotations": {
        "org.opencontainers.image.documentation": "https://foo.example/docs",
      },
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
  ],
  "annotations": {
    "org.opencontainers.image.authors": "dvdksn"
  }
}
```

To inspect annotations on a manifest, use the `docker buildx imagetools inspect` command and specify `<IMAGE>@<DIGEST>`, where `<DIGEST>` is the digest
of the manifest:

```console
$ docker buildx imagetools inspect IMAGE@sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb --raw
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:4368b6959a78b412efa083c5506c4887e251f1484ccc9f0af5c406d8f76ece1d",
    "size": 850
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:2c03dbb20264f09924f9eab176da44e5421e74a78b09531d3c63448a7baa7c59",
      "size": 3333033
    },
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:4923ad480d60a548e9b334ca492fa547a3ce8879676685b6718b085de5aaf142",
      "size": 61887305
    }
  ],
  "annotations": {
    "index,manifest:org.opencontainers.image.vendor": "foocorp",
    "org.opencontainers.image.source": "https://git.example/foo.git",
  }
}
```

## Specify annotation level

By default, annotations are added to the image manifest. You can specify which
level (OCI image component) to attach the annotation to by prefixing the
annotation string with a special type declaration:

```console
$ docker build --annotation "TYPE:KEY=VALUE" .
```

The following types are supported:

- `manifest`: annotates manifests.
- `index`: annotates the root index.
- `manifest-descriptor`: annotates manifest descriptors in the index.
- `index-descriptor`: annotates the index descriptor in the image layout.

For example, to build an image with the annotation `foo=bar` attached to the
image index:

```console
$ docker build --tag IMAGE --push --annotation "index:foo=bar" .
```

Note that the build must produce the component that you specify, or else the
build will fail. For example, the following does not work, because the `docker`
exporter does not produce an index:

```console
$ docker build --output type=docker --annotation "index:foo=bar" .
```

Likewise, the following example also does not work, because buildx creates a
`docker` output by default under some circumstances, such as when provenance
attestations are explicitly disabled:

```console
$ docker build --provenance=false --annotation "index:foo=bar" .
```

It is possible to specify types, separated by a comma, to add the annotation to
more than one level. The following example creates an image with the annotation
`foo=bar` on both the image index and the image manifest:

```console
$ docker build --tag IMAGE --push --annotation "index,manifest:foo=bar" .
```

You can also specify a platform qualifier within square brackets in the type
prefix, to annotate only components matching specific OS and architectures. The
following example adds the `foo=bar` annotation only to the `linux/amd64`
manifest:

```console
$ docker build --tag IMAGE --push --annotation "manifest[linux/amd64]:foo=bar" .
```

## Related information

Related articles:

- [Add image annotations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/annotations/)
- [Annotations OCI specification](https://github.com/opencontainers/image-spec/blob/main/annotations.md)

Reference information:

- [docker buildx build --annotation](https://docs.docker.com/reference/cli/docker/buildx/build/#annotation)
- [Bake file reference:annotations](https://docs.docker.com/build/bake/reference/#targetannotations)
- [docker buildx imagetools create --annotation](https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/#annotation)

---

# Image attestation storage

# Image attestation storage

   Table of contents

---

Buildkit supports creating and attaching attestations to build artifacts. These
attestations can provide valuable information from the build process,
including, but not limited to: [SBOMs](https://en.wikipedia.org/wiki/Software_supply_chain),
[SLSA Provenance](https://slsa.dev/provenance), build logs, etc.

This document describes the current custom format used to store attestations,
which is designed to be compatible with current registry implementations today.
In the future, we may support exporting attestations in additional formats.

Attestations are stored as manifest objects in the image index, similar in
style to OCI artifacts.

## Properties

### Attestation Manifest

Attestation manifests are attached to the root image index object, under a
separate [OCI image manifest](https://github.com/opencontainers/image-spec/blob/main/manifest.md).
Each attestation manifest can contain multiple [attestation blobs](#attestation-blob),
with all the of the attestations in a manifest applying to a single platform
manifest. All properties of standard OCI and Docker manifests continue to
apply.

The image `config` descriptor will point to a valid [image config](https://github.com/opencontainers/image-spec/blob/main/config.md),
however, it will not contain attestation-specific details, and should be
ignored as it is only included for compatibility purposes.

Each image layer in `layers` will contain a descriptor for a single
[attestation blob](#attestation-blob). The `mediaType` of each layer will be
set in accordance to its contents, one of:

- `application/vnd.in-toto+json` (currently, the only supported option)
  Indicates an in-toto attestation blob

Any unknown `mediaType`s should be ignored.

To assist attestation traversal, the following annotations may be set on each
layer descriptor:

- `in-toto.io/predicate-type`
  This annotation will be set if the enclosed attestation is an in-toto
  attestation (currently, the only supported option). The annotation will
  be set to contain the same value as the `predicateType` property present
  inside the attestation.
  When present, this annotation may be used to find the specific attestation(s)
  they are looking for to avoid pulling the contents of the others.

### Attestation Blob

The contents of each layer will be a blob dependent on its `mediaType`.

- `application/vnd.in-toto+json`
  The blob contents will contain a full [in-toto attestation statement](https://github.com/in-toto/attestation/blob/main/spec/README.md#statement):
  ```json
  {
    "_type": "https://in-toto.io/Statement/v0.1",
    "subject": [
      {
        "name": "NAME",
        "digest": {"ALGORITHM": "HEX_VALUE"}
      },
      ...
    ],
    "predicateType": "URI",
    "predicate": { ... }
  }
  ```
  The subject of the attestation should be set to be the same digest as the
  target manifest described in the [Attestation Manifest Descriptor](#attestation-manifest-descriptor),
  or some object within.

### Attestation Manifest Descriptor

Attestation manifests are attached to the root [image index](https://github.com/opencontainers/image-spec/blob/main/image-index.md),
in the `manifests` key, after all the original runnable manifests. All
properties of standard OCI and Docker manifest descriptors continue to apply.

To prevent container runtimes from accidentally pulling or running the image
described in the manifest, the `platform` property of the attestation manifest
will be set to `unknown/unknown`, as follows:

```json
"platform": {
  "architecture": "unknown",
  "os": "unknown"
}
```

To assist index traversal, the following annotations will be set on the
manifest descriptor descriptor:

- `vnd.docker.reference.type`
  This annotation describes the type of the artifact, and will be set
  to `attestation-manifest`. If any other value is specified, the entire
  manifest should be ignored.
- `vnd.docker.reference.digest`
  This annotation will contain the digest of the object in the image index that
  the attestation manifest refers to.
  When present, this annotation can be used to find the matching attestation
  manifest for a selected image manifest.

## Examples

*Example showing an SBOM attestation attached to alinux/amd64image*

#### Image index (sha256:94acc2ca70c40f3f6291681f37ce9c767e3d251ce01c7e4e9b98ccf148c26260):

This image index defines two descriptors: an AMD64 image `sha256:23678f31..` and an attestation manifest `sha256:02cb9aa7..` for that image.

```json
{
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "schemaVersion": 2,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:23678f31b3b3586c4fb318aecfe64a96a1f0916ba8faf9b2be2abee63fa9e827",
      "size": 1234,
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:02cb9aa7600e73fcf41ee9f0f19cc03122b2d8be43d41ce4b21335118f5dd943",
      "size": 1234,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:23678f31b3b3586c4fb318aecfe64a96a1f0916ba8faf9b2be2abee63fa9e827",
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

#### Attestation manifest (sha256:02cb9aa7600e73fcf41ee9f0f19cc03122b2d8be43d41ce4b21335118f5dd943):

This attestation manifest contains one attestation that is an in-toto attestation that contains a "https://spdx.dev/Document" predicate, signifying that it is defining a SBOM for the image.

```json
{
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "schemaVersion": 2,
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:a781560066f20ec9c28f2115a95a886e5e71c7c7aa9d8fd680678498b82f3ea3",
    "size": 123
  },
  "layers": [
    {
      "mediaType": "application/vnd.in-toto+json",
      "digest": "sha256:133ae3f9bcc385295b66c2d83b28c25a9f294ce20954d5cf922dda860429734a",
      "size": 1234,
      "annotations": {
        "in-toto.io/predicate-type": "https://spdx.dev/Document"
      }
    }
  ]
}
```

#### Image config (sha256:a781560066f20ec9c28f2115a95a886e5e71c7c7aa9d8fd680678498b82f3ea3):

```json
{
  "architecture": "unknown",
  "os": "unknown",
  "config": {},
  "rootfs": {
    "type": "layers",
    "diff_ids": [
      "sha256:133ae3f9bcc385295b66c2d83b28c25a9f294ce20954d5cf922dda860429734a"
    ]
  }
}
```

#### Layer content (sha256:1ea07d5e55eb47ad0e6bbfa2ec180fb580974411e623814e519064c88f022f5c):

Attestation body containing the SBOM data listing the packages used during the build in SPDX format.

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://spdx.dev/Document",
  "subject": [
    {
      "name": "_",
      "digest": {
        "sha256": "23678f31b3b3586c4fb318aecfe64a96a1f0916ba8faf9b2be2abee63fa9e827"
      }
    }
  ],
  "predicate": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "spdxVersion": "SPDX-2.2",
    ...
```

---

# SBOM attestations

> SBOM attestations describe what software artifacts an image contains and the artifacts used to create the image.

# SBOM attestations

   Table of contents

---

SBOM attestations help ensure
[software supply chain transparency](https://docs.docker.com/guides/docker-scout/s3c/) by verifying the software artifacts an image contains and the artifacts used to create the image. Metadata included in an
[SBOM](https://docs.docker.com/guides/docker-scout/sbom/) for describing software artifacts may include:

- Name of the artifact
- Version
- License type
- Authors
- Unique package identifier

Indexing the contents of an image during the build has benefits over scanning a final image. When scanning happens as part of the build, you can detect software you used to build the image, which may not show up in the final image.

Docker supports SBOM generation and attestation through an SLSA-compliant build process using BuildKit and attestations. The SBOMs generated by
[BuildKit](https://docs.docker.com/build/buildkit/) follow the SPDX standard and attach to the final image as a JSON-encoded SPDX document, using the format defined by the [in-toto SPDX predicate](https://github.com/in-toto/attestation/blob/main/spec/predicates/spdx.md). On this page, you’ll learn how to create, manage, and verify SBOM attestations using Docker tooling.

## Create SBOM attestations

To create an SBOM attestation, pass the `--attest type=sbom` option to the
`docker buildx build` command:

```console
$ docker buildx build --tag <namespace>/<image>:<version> \
    --attest type=sbom --push .
```

Alternatively, you can use the shorthand `--sbom=true` option instead of `--attest type=sbom`.

For an example on how to add SBOM attestations with GitHub Actions, see
[Add attestations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/attestations/).

## Verify SBOM attestations

Always validate the generated SBOM for your image before you push your image to a registry.

To validate, you can build the image using the `local` exporter.
Building with the `local` exporter saves the build result to your local filesystem instead of creating an image.
Attestations are written to a JSON file in the root directory of your export.

```console
$ docker buildx build \
  --sbom=true \
  --output type=local,dest=out .
```

The SBOM file appears in the root directory of the output, named `sbom.spdx.json`:

```console
$ ls -1 ./out | grep sbom
sbom.spdx.json
```

## Arguments

By default, BuildKit only scans the final stage of an image. The resulting SBOM
doesn't include build-time dependencies installed in earlier stages, or that
exist in the build context. This may cause you to overlook vulnerabilities in
those dependencies, which could impact the security of your final build
artifacts.

For instance, you might use
[multi-stage builds](https://docs.docker.com/build/building/multi-stage/),
with a `FROM scratch` stanza for your final stage to achieve a smaller image size.

```dockerfile
FROM alpine AS build
# build the software ...

FROM scratch
COPY --from=build /path/to/bin /bin
ENTRYPOINT [ "/bin" ]
```

Scanning the resulting image built using this Dockerfile example would not
reveal build-time dependencies used in the `build` stage.

To include build-time dependencies from your Dockerfile, you can set the build
arguments `BUILDKIT_SBOM_SCAN_CONTEXT` and `BUILDKIT_SBOM_SCAN_STAGE`. This
expands the scanning scope to include the build context and additional stages.

You can set the arguments as global arguments (after declaring the Dockerfile
syntax directive, before the first `FROM` command) or individually in each
stage. If set globally, the value propagates to each stage in the Dockerfile.

The `BUILDKIT_SBOM_SCAN_CONTEXT` and `BUILDKIT_SBOM_SCAN_STAGE` build arguments
are special values. You can't perform variable substitution using these
arguments, and you can't set them using environment variables from within the
Dockerfile. The only way to set these values is using explicit `ARG` command in
the Dockerfile.

### Scan build context

To scan the build context, set the `BUILDKIT_SBOM_SCAN_CONTEXT` to `true`.

```dockerfile
# syntax=docker/dockerfile:1
ARG BUILDKIT_SBOM_SCAN_CONTEXT=true
FROM alpine AS build
# ...
```

You can use the `--build-arg` CLI option to override the value specified in the
Dockerfile.

```console
$ docker buildx build --tag <image>:<version> \
    --attest type=sbom \
    --build-arg BUILDKIT_SBOM_SCAN_CONTEXT=false .
```

Note that passing the option as a CLI argument only, without having declared it
using `ARG` in the Dockerfile, will have no effect. You must specify the `ARG`
in the Dockerfile, whereby you can override the context scanning behavior using
`--build-arg`.

### Scan stages

To scan more than just the final stage, set the `BUILDKIT_SBOM_SCAN_STAGE`
argument to true, either globally or in the specific stages that you want to
scan. The following table demonstrates the different possible settings for this
argument.

| Value | Description |
| --- | --- |
| BUILDKIT_SBOM_SCAN_STAGE=true | Enables scanning for the current stage |
| BUILDKIT_SBOM_SCAN_STAGE=false | Disables scanning for the current stage |
| BUILDKIT_SBOM_SCAN_STAGE=base,bin | Enables scanning for the stages namedbaseandbin |

Only stages that are built will be scanned. Stages that aren't dependencies of
the target stage won't be built, or scanned.

The following Dockerfile example uses multi-stage builds to build a static website with
[Hugo](https://gohugo.io/).

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine as hugo
ARG BUILDKIT_SBOM_SCAN_STAGE=true
WORKDIR /src
COPY <<config.yml ./
title: My Hugo website
config.yml
RUN apk add --upgrade hugo && hugo

FROM scratch
COPY --from=hugo /src/public /
```

Setting `ARG BUILDKIT_SBOM_SCAN_STAGE=true` in the `hugo` stage ensures that the final SBOM
includes the information that Alpine Linux and Hugo were used to create the website.

Building this image with the `local` exporter creates two JSON files:

```console
$ docker buildx build \
  --sbom=true \
  --output type=local,dest=out .
$ ls -1 out | grep sbom
sbom-hugo.spdx.json
sbom.spdx.json
```

## Inspecting SBOMs

To explore created SBOMs exported through the `image` exporter, you can use
[imagetools inspect](https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/).

Using the `--format` option, you can specify a template for the output. All
SBOM-related data is available under the `.SBOM` attribute. For example, to get
the raw contents of an SBOM in SPDX format:

```console
$ docker buildx imagetools inspect <namespace>/<image>:<version> \
    --format "{{ json .SBOM.SPDX }}"
{
  "SPDXID": "SPDXRef-DOCUMENT",
  ...
}
```

> Tip
>
> If the image is multi-platform, you can check the SBOM for a platform-specific index using `--format '{{ json (index .SBOM "linux/amd64").SPDX }}'`.

You can also construct more complex expressions using the full functionality
of Go templates. For example, you can list all the installed packages and their
version identifiers:

```console
$ docker buildx imagetools inspect <namespace>/<image>:<version> \
    --format "{{ range .SBOM.SPDX.packages }}{{ .name }}@{{ .versionInfo }}{{ println }}{{ end }}"
adduser@3.118ubuntu2
apt@2.0.9
base-files@11ubuntu5.6
base-passwd@3.5.47
...
```

## SBOM generator

BuildKit generates the SBOM using a scanner plugin. By default, it uses is the
[BuildKit Syft scanner](https://github.com/docker/buildkit-syft-scanner)
plugin. This plugin is built on top of
[Anchore's Syft](https://github.com/anchore/syft),
an open source tool for generating an SBOM.

You can select a different plugin to use with the `generator` option, specifying
an image that implements the
[BuildKit SBOM scanner protocol](https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md).

```console
$ docker buildx build --attest type=sbom,generator=<image> .
```

> Tip
>
> The Docker Scout SBOM generator is available. See
> [Docker Scout SBOMs](https://docs.docker.com/scout/how-tos/view-create-sboms/).

## SBOM attestation example

The following JSON example shows what an SBOM attestation might look like.

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://spdx.dev/Document",
  "subject": [
    {
      "name": "pkg:docker/<registry>/<image>@<tag/digest>?platform=<platform>",
      "digest": {
        "sha256": "e8275b2b76280af67e26f068e5d585eb905f8dfd2f1918b3229db98133cb4862"
      }
    }
  ],
  "predicate": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
      "created": "2022-12-16T15:27:25.517047753Z",
      "creators": ["Organization: Anchore, Inc", "Tool: syft-v0.60.3"],
      "licenseListVersion": "3.18"
    },
    "dataLicense": "CC0-1.0",
    "documentNamespace": "https://anchore.com/syft/dir/run/src/core/sbom-cba61a72-fa95-4b60-b63f-03169eac25ca",
    "name": "/run/src/core/sbom",
    "packages": [
      {
        "SPDXID": "SPDXRef-b074348b8f56ea64",
        "downloadLocation": "NOASSERTION",
        "externalRefs": [
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:org:repo:\\(devel\\):*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "PACKAGE_MANAGER",
            "referenceLocator": "pkg:golang/github.com/org/repo@(devel)",
            "referenceType": "purl"
          }
        ],
        "filesAnalyzed": false,
        "licenseConcluded": "NONE",
        "licenseDeclared": "NONE",
        "name": "github.com/org/repo",
        "sourceInfo": "acquired package info from go module information: bin/server",
        "versionInfo": "(devel)"
      },
      {
        "SPDXID": "SPDXRef-1b96f57f8fed62d8",
        "checksums": [
          {
            "algorithm": "SHA256",
            "checksumValue": "0c13f1f3c1636491f716c2027c301f21f9dbed7c4a2185461ba94e3e58443408"
          }
        ],
        "downloadLocation": "NOASSERTION",
        "externalRefs": [
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go-chi:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go_chi:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "PACKAGE_MANAGER",
            "referenceLocator": "pkg:golang/github.com/go-chi/chi/v5@v5.0.0",
            "referenceType": "purl"
          }
        ],
        "filesAnalyzed": false,
        "licenseConcluded": "NONE",
        "licenseDeclared": "NONE",
        "name": "github.com/go-chi/chi/v5",
        "sourceInfo": "acquired package info from go module information: bin/server",
        "versionInfo": "v5.0.0"
      }
    ],
    "relationships": [
      {
        "relatedSpdxElement": "SPDXRef-1b96f57f8fed62d8",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-043f7360d3c66bc31ba45388f16423aa58693289126421b71d884145f8837fe1"
      },
      {
        "relatedSpdxElement": "SPDXRef-b074348b8f56ea64",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-043f7360d3c66bc31ba45388f16423aa58693289126421b71d884145f8837fe1"
      }
    ],
    "spdxVersion": "SPDX-2.2"
  }
}
```
