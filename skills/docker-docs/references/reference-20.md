# docker buildx imagetools create and more

# docker buildx imagetools create

# docker buildx imagetools create

| Description | Create a new image based on source images |
| --- | --- |
| Usage | docker buildx imagetools create [OPTIONS] [SOURCE...] |

## Description

Create a new manifest list based on source manifests. The source manifests can
be manifest lists or single platform distribution manifests and must already
exist in the registry where the new manifest is created.

If only one source is specified and that source is a manifest list or image index,
create performs a carbon copy. If one source is specified and that source is *not*
a list or index, the output will be a manifest list, however you can disable this
behavior with `--prefer-index=false` which attempts to preserve the source manifest
format in the output.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --annotation |  | Add annotation to the image |
| --append |  | Append to existing manifest |
| --dry-run |  | Show final image instead of pushing |
| -f, --file |  | Read source descriptor from file |
| -p, --platform |  | Filter specified platforms of target image |
| --prefer-index | true | When only a single source is specified, prefer outputting an image index or manifest list instead of performing a carbon copy |
| --progress | auto | Set type of progress output (auto,none,plain,rawjson,tty). Use plain to show container output |
| -t, --tag |  | Set reference for new image |

## Examples

### Add annotations to an image (--annotation)

The `--annotation` flag lets you add annotations the image index, manifest,
and descriptors when creating a new image.

The following command creates a `foo/bar:latest` image with the
`org.opencontainers.image.authors` annotation on the image index.

```console
$ docker buildx imagetools create \
  --annotation "index:org.opencontainers.image.authors=dvdksn" \
  --tag foo/bar:latest \
  foo/bar:alpha foo/bar:beta foo/bar:gamma
```

> Note
>
> The `imagetools create` command supports adding annotations to the image
> index and descriptor, using the following type prefixes:
>
>
>
> - `index:`
> - `manifest-descriptor:`
>
>
>
> It doesn't support annotating manifests or OCI layouts.

For more information about annotations, see
[Annotations](https://docs.docker.com/build/building/annotations/).

### Append new sources to an existing manifest list (--append)

Use the `--append` flag to append the new sources to an existing manifest list
in the destination.

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

### Show final image instead of pushing (--dry-run)

Use the `--dry-run` flag to not push the image, just show it.

### Read source descriptor from a file (-f, --file)

```text
-f FILE or --file FILE
```

Reads source from files. A source can be a manifest digest, manifest reference,
or a JSON of OCI descriptor object.

In order to define annotations or additional platform properties like `os.version` and
`os.features` you need to add them in the OCI descriptor object encoded in JSON.

```console
$ docker buildx imagetools inspect --raw alpine | jq '.manifests[0] | .platform."os.version"="10.1"' > descr.json
$ docker buildx imagetools create -f descr.json myuser/image
```

The descriptor in the file is merged with existing descriptor in the registry if it exists.

The supported fields for the descriptor are defined in [OCI spec](https://github.com/opencontainers/image-spec/blob/master/descriptor.md#properties) .

### Set reference for new image (-t, --tag)

```text
-t IMAGE or --tag IMAGE
```

Use the `-t` or `--tag` flag to set the name of the image to be created.

```console
$ docker buildx imagetools create --dry-run alpine@sha256:5c40b3c27b9f13c873fefb2139765c56ce97fd50230f1f2d5c91e55dec171907 sha256:c4ba6347b0e4258ce6a6de2401619316f982b7bcc529f73d2a410d0097730204
$ docker buildx imagetools create -t tonistiigi/myapp -f image1 -f image2
```

---

# docker buildx imagetools inspect

# docker buildx imagetools inspect

| Description | Show details of an image in the registry |
| --- | --- |
| Usage | docker buildx imagetools inspect [OPTIONS] NAME |

## Description

Show details of an image in the registry.

```console
$ docker buildx imagetools inspect alpine
Name:      docker.io/library/alpine:latest
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc984380bc0118285c70fa8c9300

Manifests:
  Name:      docker.io/library/alpine:latest@sha256:e7d88de73db3d3fd9b2d63aa7f447a10fd0220b7cbf39803c803f2af9ba256b3
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/amd64

  Name:      docker.io/library/alpine:latest@sha256:e047bc2af17934d38c5a7fa9f46d443f1de3a7675546402592ef805cfa929f9d
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm/v6

  Name:      docker.io/library/alpine:latest@sha256:8483ecd016885d8dba70426fda133c30466f661bb041490d525658f1aac73822
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm/v7

  Name:      docker.io/library/alpine:latest@sha256:c74f1b1166784193ea6c8f9440263b9be6cae07dfe35e32a5df7a31358ac2060
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm64/v8

  Name:      docker.io/library/alpine:latest@sha256:2689e157117d2da668ad4699549e55eba1ceb79cb7862368b30919f0488213f4
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/386

  Name:      docker.io/library/alpine:latest@sha256:2042a492bcdd847a01cd7f119cd48caa180da696ed2aedd085001a78664407d6
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/ppc64le

  Name:      docker.io/library/alpine:latest@sha256:49e322ab6690e73a4909f787bcbdb873631264ff4a108cddfd9f9c249ba1d58e
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/s390x
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | `{{.Manifest}}` | Format the output using the given Go template |
| --raw |  | Show original, unformatted JSON manifest |

## Examples

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

### Format the output (--format)

Format the output using the given Go template. Defaults to `{{.Manifest}}` if
unset. Following fields are available:

- `.Name`: provides the reference of the image
- `.Manifest`: provides the manifest or manifest list
- `.Image`: provides the image config

#### .Name

```console
$ docker buildx imagetools inspect alpine --format "{{.Name}}"
Name: docker.io/library/alpine:latest
```

#### .Manifest

```console
$ docker buildx imagetools inspect crazymax/loop --format "{{.Manifest}}"
Name:      docker.io/crazymax/loop:latest
MediaType: application/vnd.docker.distribution.manifest.v2+json
Digest:    sha256:08602e7340970e92bde5e0a2e887c1fde4d9ae753d1e05efb4c8ef3b609f97f1
```

```console
$ docker buildx imagetools inspect moby/buildkit:master --format "{{.Manifest}}"
Name:      docker.io/moby/buildkit:master
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:3183f7ce54d1efb44c34b84f428ae10aaf141e553c6b52a7ff44cc7083a05a66

Manifests:
  Name:      docker.io/moby/buildkit:master@sha256:667d28c9fb33820ce686887a717a148e89fa77f9097f9352996bbcce99d352b1
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/amd64

  Name:      docker.io/moby/buildkit:master@sha256:71789527b64ab3d7b3de01d364b449cd7f7a3da758218fbf73b9c9aae05a6775
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm/v7

  Name:      docker.io/moby/buildkit:master@sha256:fb64667e1ce6ab0d05478f3a8402af07b27737598dcf9a510fb1d792b13a66be
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm64

  Name:      docker.io/moby/buildkit:master@sha256:1c3ddf95a0788e23f72f25800c05abc4458946685e2b66788c3d978cde6da92b
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/s390x

  Name:      docker.io/moby/buildkit:master@sha256:05bcde6d460a284e5bc88026cd070277e8380355de3126cbc8fe8a452708c6b1
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/ppc64le

  Name:      docker.io/moby/buildkit:master@sha256:c04c57765304ab84f4f9807fff3e11605c3a60e16435c734b02c723680f6bd6e
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/riscv64
```

#### JSON output

A `json` template function is also available if you want to render fields in
JSON format:

```console
$ docker buildx imagetools inspect crazymax/buildkit:attest --format "{{json .Manifest}}"
```

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "digest": "sha256:7007b387ccd52bd42a050f2e8020e56e64622c9269bf7bbe257b326fe99daf19",
  "size": 855,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:fbd10fe50b4b174bb9ea273e2eb9827fa8bf5c88edd8635a93dc83e0d1aecb55",
      "size": 673,
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:a9de632c16998489fd63fbca42a03431df00639cfb2ecb8982bf9984b83c5b2b",
      "size": 839,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:fbd10fe50b4b174bb9ea273e2eb9827fa8bf5c88edd8635a93dc83e0d1aecb55",
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

```console
$ docker buildx imagetools inspect crazymax/buildkit:attest --format "{{json .Image}}"
```

```json
{
  "created": "2022-12-01T11:46:47.713777178Z",
  "architecture": "amd64",
  "os": "linux",
  "config": {
    "Env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    ],
    "Cmd": [
      "/bin/sh"
    ]
  },
  "rootfs": {
    "type": "layers",
    "diff_ids": [
      "sha256:ded7a220bb058e28ee3254fbba04ca90b679070424424761a53a043b93b612bf",
      "sha256:d85d09ab4b4e921666ccc2db8532e857bf3476b7588e52c9c17741d7af14204f"
    ]
  },
  "history": [
    {
      "created": "2022-11-22T22:19:28.870801855Z",
      "created_by": "/bin/sh -c #(nop) ADD file:587cae71969871d3c6456d844a8795df9b64b12c710c275295a1182b46f630e7 in / "
    },
    {
      "created": "2022-11-22T22:19:29.008562326Z",
      "created_by": "/bin/sh -c #(nop)  CMD [\"/bin/sh\"]",
      "empty_layer": true
    },
    {
      "created": "2022-12-01T11:46:47.713777178Z",
      "created_by": "RUN /bin/sh -c apk add curl # buildkit",
      "comment": "buildkit.dockerfile.v0"
    }
  ]
}
```

```console
$ docker buildx imagetools inspect moby/buildkit:master --format "{{json .Manifest}}"
```

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "digest": "sha256:d895e8fdcf5e2bb39acb5966f97fc4cd87a2d13d27c939c320025eb4aca5440c",
  "size": 4654,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:ac9dd4fbec9e36b562f910618975a2936533f8e411a3fea2858aacc0ac972e1c",
      "size": 1054,
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:0f4dc6797db467372cbf52c7236816203654a839f64a6542c9135d1973c9d744",
      "size": 1054,
      "platform": {
        "architecture": "arm",
        "os": "linux",
        "variant": "v7"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:d62bb533d95afe17c4a9caf1e7c57a3b0a7a67409ccfa7af947aeb0f670ffb87",
      "size": 1054,
      "platform": {
        "architecture": "arm64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:b4944057e0c68203cdcc3dceff3b2df3c7d9e3dd801724fa977b01081da7771e",
      "size": 1054,
      "platform": {
        "architecture": "s390x",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:825702a51eb4234904fc9253d8b0bf0a584787ffd8fc3fd6fa374188233ce399",
      "size": 1054,
      "platform": {
        "architecture": "ppc64le",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:dfb27c6acc9b9f3a7c9d47366d137089565062f43c8063c9f5e408d34c87ee4a",
      "size": 1054,
      "platform": {
        "architecture": "riscv64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:f2fe69bccc878e658caf21dfc99eaf726fb20d28f17398c1d66a90e62cc019f9",
      "size": 1113,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:ac9dd4fbec9e36b562f910618975a2936533f8e411a3fea2858aacc0ac972e1c",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
        "architecture": "unknown",
        "os": "unknown"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:9e112f8d4e383186f36369fba7b454e246d2e9ca5def797f1b84ede265e9f3ca",
      "size": 1113,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:0f4dc6797db467372cbf52c7236816203654a839f64a6542c9135d1973c9d744",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
        "architecture": "unknown",
        "os": "unknown"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:09d593587f8665269ec6753eaed7fbdb09968f71587dd53e06519502cbc16775",
      "size": 1113,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:d62bb533d95afe17c4a9caf1e7c57a3b0a7a67409ccfa7af947aeb0f670ffb87",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
        "architecture": "unknown",
        "os": "unknown"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:985a3f4544dfb042db6a8703f5f76438667dd7958aba14cb04bebe3b4cbd9307",
      "size": 1113,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:b4944057e0c68203cdcc3dceff3b2df3c7d9e3dd801724fa977b01081da7771e",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
        "architecture": "unknown",
        "os": "unknown"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:cfccb6afeede7dc29bf8abef4815d56f2723fa482ea63c9cd519cd991c379294",
      "size": 1113,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:825702a51eb4234904fc9253d8b0bf0a584787ffd8fc3fd6fa374188233ce399",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
        "architecture": "unknown",
        "os": "unknown"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:2e93733432c6a14cb57db33928b3a17d7ca298b3babe24d9f56dca2754dbde3b",
      "size": 1113,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:dfb27c6acc9b9f3a7c9d47366d137089565062f43c8063c9f5e408d34c87ee4a",
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

The following command provides [SLSA](https://github.com/moby/buildkit/blob/master/docs/attestations/slsa-provenance.md)
JSON output:

```console
$ docker buildx imagetools inspect crazymax/buildkit:attest --format "{{json .Provenance}}"
```

```json
{
  "SLSA": {
    "builder": {
      "id": ""
    },
    "buildType": "https://mobyproject.org/buildkit@v1",
    "materials": [
      {
        "uri": "pkg:docker/docker/buildkit-syft-scanner@stable-1",
        "digest": {
          "sha256": "b45f1d207e16c3a3a5a10b254ad8ad358d01f7ea090d382b95c6b2ee2b3ef765"
        }
      },
      {
        "uri": "pkg:docker/alpine@latest?platform=linux%2Famd64",
        "digest": {
          "sha256": "8914eb54f968791faf6a8638949e480fef81e697984fba772b3976835194c6d4"
        }
      }
    ],
    "invocation": {
      "configSource": {},
      "parameters": {
        "frontend": "dockerfile.v0",
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
        "platform": "linux/amd64"
      }
    },
    "metadata": {
      "buildInvocationID": "02tdha2xkbxvin87mz9drhag4",
      "buildStartedOn": "2022-12-01T11:50:07.264704131Z",
      "buildFinishedOn": "2022-12-01T11:50:08.243788739Z",
      "reproducible": false,
      "completeness": {
        "parameters": true,
        "environment": true,
        "materials": false
      },
      "https://mobyproject.org/buildkit@v1#metadata": {}
    }
  }
}
```

The following command provides [SBOM](https://github.com/moby/buildkit/blob/master/docs/attestations/sbom.md)
JSON output:

```console
$ docker buildx imagetools inspect crazymax/buildkit:attest --format "{{json .SBOM}}"
```

```json
{
  "SPDX": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
      "created": "2022-12-01T11:46:48.063400162Z",
      "creators": [
        "Tool: syft-v0.60.3",
        "Tool: buildkit-1ace2bb",
        "Organization: Anchore, Inc"
      ],
      "licenseListVersion": "3.18"
    },
    "dataLicense": "CC0-1.0",
    "documentNamespace": "https://anchore.com/syft/dir/run/src/core-0a4ccc6d-1a72-4c3a-a40e-3df1a2ffca94",
    "files": [...],
    "spdxVersion": "SPDX-2.2"
  }
}
```

```console
$ docker buildx imagetools inspect crazymax/buildkit:attest --format "{{json .}}"
```

```json
{
  "name": "crazymax/buildkit:attest",
  "manifest": {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.index.v1+json",
    "digest": "sha256:7007b387ccd52bd42a050f2e8020e56e64622c9269bf7bbe257b326fe99daf19",
    "size": 855,
    "manifests": [
      {
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "digest": "sha256:fbd10fe50b4b174bb9ea273e2eb9827fa8bf5c88edd8635a93dc83e0d1aecb55",
        "size": 673,
        "platform": {
          "architecture": "amd64",
          "os": "linux"
        }
      },
      {
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "digest": "sha256:a9de632c16998489fd63fbca42a03431df00639cfb2ecb8982bf9984b83c5b2b",
        "size": 839,
        "annotations": {
          "vnd.docker.reference.digest": "sha256:fbd10fe50b4b174bb9ea273e2eb9827fa8bf5c88edd8635a93dc83e0d1aecb55",
          "vnd.docker.reference.type": "attestation-manifest"
        },
        "platform": {
          "architecture": "unknown",
          "os": "unknown"
        }
      }
    ]
  },
  "image": {
    "created": "2022-12-01T11:46:47.713777178Z",
    "architecture": "amd64",
    "os": "linux",
    "config": {
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
      ],
      "Cmd": [
        "/bin/sh"
      ]
    },
    "rootfs": {
      "type": "layers",
      "diff_ids": [
        "sha256:ded7a220bb058e28ee3254fbba04ca90b679070424424761a53a043b93b612bf",
        "sha256:d85d09ab4b4e921666ccc2db8532e857bf3476b7588e52c9c17741d7af14204f"
      ]
    },
    "history": [
      {
        "created": "2022-11-22T22:19:28.870801855Z",
        "created_by": "/bin/sh -c #(nop) ADD file:587cae71969871d3c6456d844a8795df9b64b12c710c275295a1182b46f630e7 in / "
      },
      {
        "created": "2022-11-22T22:19:29.008562326Z",
        "created_by": "/bin/sh -c #(nop)  CMD [\"/bin/sh\"]",
        "empty_layer": true
      },
      {
        "created": "2022-12-01T11:46:47.713777178Z",
        "created_by": "RUN /bin/sh -c apk add curl # buildkit",
        "comment": "buildkit.dockerfile.v0"
      }
    ]
  }
}
```

#### Multi-platform

Multi-platform images are supported for `.Image`, `.SLSA` and `.SBOM` fields.
If you want to pick up a specific platform, you can specify it using the `index`
go template function:

```console
$ docker buildx imagetools inspect --format '{{json (index .Image "linux/s390x")}}' moby/buildkit:master
```

```json
{
  "created": "2022-11-30T17:42:26.414957336Z",
  "architecture": "s390x",
  "os": "linux",
  "config": {
    "Env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    ],
    "Entrypoint": [
      "buildkitd"
    ],
    "Volumes": {
      "/var/lib/buildkit": {}
    }
  },
  "rootfs": {
    "type": "layers",
    "diff_ids": [
      "sha256:41048e32d0684349141cf05f629c5fc3c5915d1f3426b66dbb8953a540e01e1e",
      "sha256:2651209b9208fff6c053bc3c17353cb07874e50f1a9bc96d6afd03aef63de76a",
      "sha256:88577322e65f094ce8ac27435880f1a8a9baadb569258026bb141770451bafcb",
      "sha256:de8f9a790e4ed10ff1f1f8ea923c9da4f97246a7e200add2dc6650eba3f10a20"
    ]
  },
  "history": [
    {
      "created": "2021-11-24T20:41:23.709681315Z",
      "created_by": "/bin/sh -c #(nop) ADD file:cd24c711a2ef431b3ff94f9a02bfc42f159bc60de1d0eceecafea4e8af02441d in / "
    },
    {
      "created": "2021-11-24T20:41:23.94211262Z",
      "created_by": "/bin/sh -c #(nop)  CMD [\"/bin/sh\"]",
      "empty_layer": true
    },
    {
      "created": "2022-01-26T18:15:21.449825391Z",
      "created_by": "RUN /bin/sh -c apk add --no-cache fuse3 git openssh pigz xz   \u0026\u0026 ln -s fusermount3 /usr/bin/fusermount # buildkit",
      "comment": "buildkit.dockerfile.v0"
    },
    {
      "created": "2022-08-25T00:39:25.652811078Z",
      "created_by": "COPY examples/buildctl-daemonless/buildctl-daemonless.sh /usr/bin/ # buildkit",
      "comment": "buildkit.dockerfile.v0"
    },
    {
      "created": "2022-11-30T17:42:26.414957336Z",
      "created_by": "VOLUME [/var/lib/buildkit]",
      "comment": "buildkit.dockerfile.v0",
      "empty_layer": true
    },
    {
      "created": "2022-11-30T17:42:26.414957336Z",
      "created_by": "COPY / /usr/bin/ # buildkit",
      "comment": "buildkit.dockerfile.v0"
    },
    {
      "created": "2022-11-30T17:42:26.414957336Z",
      "created_by": "ENTRYPOINT [\"buildkitd\"]",
      "comment": "buildkit.dockerfile.v0",
      "empty_layer": true
    }
  ]
}
```

### Show original JSON manifest (--raw)

Use the `--raw` option to print the raw JSON manifest.

```console
$ docker buildx imagetools inspect --raw crazymax/loop
```

```json
{
  "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
  "schemaVersion": 2,
  "config": {
    "mediaType": "application/vnd.docker.container.image.v1+json",
    "digest": "sha256:a98999183d2c7a8845f6d56496e51099ce6e4359ee7255504174b05430c4b78b",
    "size": 2762
  },
  "layers": [
    {
      "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
      "digest": "sha256:8663204ce13b2961da55026a2034abb9e5afaaccf6a9cfb44ad71406dcd07c7b",
      "size": 2818370
    },
    {
      "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
      "digest": "sha256:f0868a92f8e1e5018ed4e60eb845ed4ff0e2229897f4105e5a4735c1d6fd874f",
      "size": 1821402
    },
    {
      "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
      "digest": "sha256:d010066dbdfcf7c12fca30cd4b567aa7218eb6762ab53169d043655b7a8d7f2e",
      "size": 404457
    }
  ]
}
```

```console
$ docker buildx imagetools inspect --raw moby/buildkit:master | jq
```

```json
{
  "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
  "schemaVersion": 2,
  "manifests": [
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:f9f41c85124686c2afe330a985066748a91d7a5d505777fe274df804ab5e077e",
      "size": 1158,
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:82097c2be19c617aafb3c3e43c88548738d4b2bf3db5c36666283a918b390266",
      "size": 1158,
      "platform": {
        "architecture": "arm",
        "os": "linux",
        "variant": "v7"
      }
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:b6b91e6c823d7220ded7d3b688e571ba800b13d91bbc904c1d8053593e3ee42c",
      "size": 1158,
      "platform": {
        "architecture": "arm64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:797061bcc16778de048b96f769c018ec24da221088050bbe926ea3b8d51d77e8",
      "size": 1158,
      "platform": {
        "architecture": "s390x",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:b93d3a84d18c4d0b8c279e77343d854d9b5177df7ea55cf468d461aa2523364e",
      "size": 1159,
      "platform": {
        "architecture": "ppc64le",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:d5c950dd1b270d437c838187112a0cb44c9258248d7a3a8bcb42fae8f717dc01",
      "size": 1158,
      "platform": {
        "architecture": "riscv64",
        "os": "linux"
      }
    }
  ]
}
```

---

# docker buildx imagetools

# docker buildx imagetools

| Description | Commands to work on images in registry |
| --- | --- |
| Usage | docker buildx imagetools |

## Description

The `imagetools` commands contains subcommands for working with manifest lists
in container registries. These commands are useful for inspecting manifests
to check multi-platform configuration and attestations.

## Examples

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx imagetools create | Create a new image based on source images |
| docker buildx imagetools inspect | Show details of an image in the registry |

---

# docker buildx inspect

# docker buildx inspect

| Description | Inspect current builder instance |
| --- | --- |
| Usage | docker buildx inspect [NAME] |

## Description

Shows information about the current or specified builder.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --bootstrap |  | Ensure builder has booted before inspecting |

## Examples

### Ensure that the builder is running before inspecting (--bootstrap)

Use the `--bootstrap` option to ensure that the builder is running before
inspecting it. If the driver is `docker-container`, then `--bootstrap` starts
the BuildKit container and waits until it's operational. Bootstrapping is
automatically done during build, and therefore not necessary. The same BuildKit
container is used during the lifetime of the associated builder node (as
displayed in `buildx ls`).

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

### Get information about a builder instance

By default, `inspect` shows information about the current builder. Specify the
name of the builder to inspect to get information about that builder.
The following example shows information about a builder instance named
`elated_tesla`:

> Note
>
> The asterisk (`*`) next to node build platform(s) indicate they have been
> manually set during `buildx create`. Otherwise the platforms were
> automatically detected.

```console
$ docker buildx inspect elated_tesla
Name:          elated_tesla
Driver:        docker-container
Last Activity: 2022-11-30 12:42:47 +0100 CET

Nodes:
Name:           elated_tesla0
Endpoint:       unix:///var/run/docker.sock
Driver Options: env.BUILDKIT_STEP_LOG_MAX_SPEED="10485760" env.JAEGER_TRACE="localhost:6831" image="moby/buildkit:latest" network="host" env.BUILDKIT_STEP_LOG_MAX_SIZE="10485760"
Status:         running
Flags:          --debug --allow-insecure-entitlement security.insecure --allow-insecure-entitlement network.host
BuildKit:       v0.10.6
Platforms:      linux/arm64*, linux/arm/v7, linux/arm/v6
Labels:
 org.mobyproject.buildkit.worker.executor:         oci
 org.mobyproject.buildkit.worker.hostname:         docker-desktop
 org.mobyproject.buildkit.worker.network:          host
 org.mobyproject.buildkit.worker.oci.process-mode: sandbox
 org.mobyproject.buildkit.worker.selinux.enabled:  false
 org.mobyproject.buildkit.worker.snapshotter:      overlayfs
GC Policy rule#0:
 All:           false
 Filters:       type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration: 48h0m0s
 Keep Bytes:    488.3MiB
GC Policy rule#1:
 All:           false
 Keep Duration: 1440h0m0s
 Keep Bytes:    24.21GiB
GC Policy rule#2:
 All:        false
 Keep Bytes: 24.21GiB
GC Policy rule#3:
 All:        true
 Keep Bytes: 24.21GiB
```

`debug` flag can also be used to get more information about the builder:

```console
$ docker --debug buildx inspect elated_tesla
```

---

# docker buildx ls

# docker buildx ls

| Description | List builder instances |
| --- | --- |
| Usage | docker buildx ls |

## Description

Lists all builder instances and the nodes for each instance.

```console
$ docker buildx ls
NAME/NODE           DRIVER/ENDPOINT                   STATUS    BUILDKIT   PLATFORMS
elated_tesla*       docker-container
 \_ elated_tesla0    \_ unix:///var/run/docker.sock   running   v0.10.3    linux/amd64
 \_ elated_tesla1    \_ ssh://ubuntu@1.2.3.4          running   v0.10.3    linux/arm64*, linux/arm/v7, linux/arm/v6
default             docker
 \_ default          \_ default                       running   v0.8.2     linux/amd64
```

Each builder has one or more nodes associated with it. The current builder's
name is marked with a `*` in `NAME/NODE` and explicit node to build against for
the target platform marked with a `*` in the `PLATFORMS` column.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | table | Format the output |
| --no-trunc |  | Don't truncate output |

## Examples

### Format the output (--format)

The formatting options (`--format`) pretty-prints builder instances output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .Name | Builder or node name |
| .DriverEndpoint | Driver (for builder) or Endpoint (for node) |
| .LastActivity | Builder last activity |
| .Status | Builder or node status |
| .Buildkit | BuildKit version of the node |
| .Platforms | Available node's platforms |
| .Error | Error |
| .Builder | Builder object |

When using the `--format` option, the `ls` command will either output the data
exactly as the template declares or, when using the `table` directive, includes
column headers as well.

The following example uses a template without headers and outputs the
`Name` and `DriverEndpoint` entries separated by a colon (`:`):

```console
$ docker buildx ls --format "{{.Name}}: {{.DriverEndpoint}}"
elated_tesla: docker-container
elated_tesla0: unix:///var/run/docker.sock
elated_tesla1: ssh://ubuntu@1.2.3.4
default: docker
default: default
```

The `Builder` placeholder can be used to access the builder object and its
fields. For example, the following template outputs the builder's and
nodes' names with their respective endpoints:

```console
$ docker buildx ls --format "{{.Builder.Name}}: {{range .Builder.Nodes}}\n  {{.Name}}: {{.Endpoint}}{{end}}"
elated_tesla:
  elated_tesla0: unix:///var/run/docker.sock
  elated_tesla1: ssh://ubuntu@1.2.3.4
default: docker
  default: default
```

---

# docker buildx policy eval

# docker buildx policy eval

| Description | Evaluate policy for a source |
| --- | --- |
| Usage | docker buildx policy eval [OPTIONS] source |

## Description

Evaluate policy for a source

## Options

| Option | Default | Description |
| --- | --- | --- |
| --fields |  | Fields to evaluate |
| --filename | Dockerfile | Policy filename to evaluate |
| --print |  | Print policy output |

---

# docker buildx policy test

# docker buildx policy test

| Description | Run policy tests |
| --- | --- |
| Usage | docker buildx policy test <path> |

## Description

Run policy tests

## Options

| Option | Default | Description |
| --- | --- | --- |
| --filename | Dockerfile | Name of the Dockerfile to validate |
| --run |  | Run only tests with name containing this substring |

---

# docker buildx policy

# docker buildx policy

| Description | Commands for working with build policies |
| --- | --- |

## Description

Commands for working with build policies

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx policy eval | Evaluate policy for a source |
| docker buildx policy test | Run policy tests |

---

# docker buildx prune

# docker buildx prune

| Description | Remove build cache |
| --- | --- |
| Usage | docker buildx prune |

## Description

Clears the build cache of the selected builder.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Include internal/frontend images |
| --filter |  | Provide filter values |
| -f, --force |  | Do not prompt for confirmation |
| --max-used-space |  | Maximum amount of disk space allowed to keep for cache |
| --min-free-space |  | Target amount of free disk space after pruning |
| --reserved-space |  | Amount of disk space always allowed to keep for cache |
| --verbose |  | Provide a more verbose output |

## Examples

### Include internal/frontend images (--all)

The `--all` flag to allow clearing internal helper images and frontend images
set using the `#syntax=` directive or the `BUILDKIT_SYNTAX` build argument.

### Provide filter values (--filter)

You can finely control which cache records to delete using the `--filter` flag.

The filter format is in the form of `<key><op><value>`, known as selectors. All
selectors must match the target object for the filter to be true. We define the
operators `=` for equality, `!=` for not equal and `~=` for a regular
expression.

Valid filter keys are:

- `until` flag to keep records that have been used in the last duration time.
  Value is a duration string, e.g. `24h` or `2h30m`, with allowable units of
  `(h)ours`, `(m)inutes` and `(s)econds`.
- `id` flag to target a specific image ID.
- `parents` flag to target records that are parents of the
  specified image ID. Multiple parent IDs are separated by a semicolon (`;`).
- `description` flag to target records whose description is the specified
  substring.
- `inuse` flag to target records that are actively in use and therefore not
  reclaimable.
- `mutable` flag to target records that are mutable.
- `immutable` flag to target records that are immutable.
- `shared` flag to target records that are shared with other resources,
  typically images.
- `private` flag to target records that are not shared.
- `type` flag to target records by type. Valid types are:
  - `internal`
  - `frontend`
  - `source.local`
  - `source.git.checkout`
  - `exec.cachemount`
  - `regular`

Examples:

```console
docker buildx prune --filter "until=24h"
docker buildx prune --filter "description~=golang"
docker buildx prune --filter "parents=dpetmoi6n0yqanxjqrbnofz9n;kgoj0q6g57i35gdyrv546alz7"
docker buildx prune --filter "type=source.local"
docker buildx prune --filter "type!=exec.cachemount"
```

> Note
>
> Multiple `--filter` flags are ANDed together.

### Maximum amount of disk space allowed to keep for cache (--max-used-space)

The `--max-used-space` flag allows setting a maximum amount of disk space
that the build cache can use. If the cache is using more disk space than this
value, the least recently used cache records are deleted until the total
used space is less than or equal to the specified value.

The value is specified in bytes. You can use a human-readable memory string,
e.g. `128mb`, `2gb`, etc. Units are case-insensitive.

### Target amount of free disk space after pruning (--min-free-space)

The `--min-free-space` flag allows setting a target amount of free disk space
that should be available after pruning. If the available disk space is less
than this value, the least recently used cache records are deleted until
the available free space is greater than or equal to the specified value.

The value is specified in bytes. You can use a human-readable memory string,
e.g. `128mb`, `2gb`, etc. Units are case-insensitive.

### Amount of disk space always allowed to keep for cache (--reserved-space)

The `--reserved-space` flag allows setting an amount of disk space that
should always be kept for the build cache. If the available disk space is less
than this value, the least recently used cache records are deleted until
the available free space is greater than or equal to the specified value.

The value is specified in bytes. You can use a human-readable memory string,
e.g. `128mb`, `2gb`, etc. Units are case-insensitive.

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

---

# docker buildx rm

# docker buildx rm

| Description | Remove one or more builder instances |
| --- | --- |
| Usage | docker buildx rm [OPTIONS] [NAME...] |

## Description

Removes the specified or current builder. It is a no-op attempting to remove the
default builder.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all-inactive |  | Remove all inactive builders |
| -f, --force |  | Do not prompt for confirmation |
| --keep-daemon |  | Keep the BuildKit daemon running |
| --keep-state |  | Keep BuildKit state |

## Examples

### Remove all inactive builders (--all-inactive)

Remove builders that are not in running state.

```console
$ docker buildx rm --all-inactive
WARNING! This will remove all builders that are not in running state. Are you sure you want to continue? [y/N] y
```

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

### Do not prompt for confirmation (--force)

Do not prompt for confirmation before removing inactive builders.

```console
$ docker buildx rm --all-inactive --force
```

### Keep the BuildKit daemon running (--keep-daemon)

Keep the BuildKit daemon running after the buildx context is removed. This is
useful when you manage BuildKit daemons and buildx contexts independently.
Only supported by the
[docker-container](https://docs.docker.com/build/drivers/docker-container/)
and
[kubernetes](https://docs.docker.com/build/drivers/kubernetes/) drivers.

### Keep BuildKit state (--keep-state)

Keep BuildKit state, so it can be reused by a new builder with the same name.
Currently, only supported by the
[docker-containerdriver](https://docs.docker.com/build/drivers/docker-container/).

---

# docker buildx stop

# docker buildx stop

| Description | Stop builder instance |
| --- | --- |
| Usage | docker buildx stop [NAME] |

## Description

Stops the specified or current builder. This does not prevent buildx build to
restart the builder. The implementation of stop depends on the driver.

## Examples

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

---

# docker buildx use

# docker buildx use

| Description | Set the current builder instance |
| --- | --- |
| Usage | docker buildx use [OPTIONS] NAME |

## Description

Switches the current builder instance. Build commands invoked after this command
will run on a specified builder. Alternatively, a context name can be used to
switch to the default builder of that context.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --default |  | Set builder as default for current context |
| --global |  | Builder persists context changes |

## Examples

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

---

# docker buildx version

# docker buildx version

| Description | Show buildx version information |
| --- | --- |
| Usage | docker buildx version |

## Description

View version information

```console
$ docker buildx version
github.com/docker/buildx v0.11.2 9872040b6626fb7d87ef7296fd5b832e8cc2ad17
```

---

# docker buildx

# docker buildx

| Description | Docker Buildx |
| --- | --- |
| Usage | docker buildx |

## Description

Extended build capabilities with BuildKit

## Options

| Option | Default | Description |
| --- | --- | --- |
| --builder |  | Override the configured builder instance |
| -D, --debug |  | Enable debug logging |

## Examples

### Override the configured builder instance (--builder)

You can also use the `BUILDX_BUILDER` environment variable.

## Subcommands

| Command | Description |
| --- | --- |
| docker buildx bake | Build from a file |
| docker buildx build | Start a build |
| docker buildx create | Create a new builder instance |
| docker buildx dap | Start debug adapter protocol compatible debugger |
| docker buildx debug | Start debugger |
| docker buildx du | Disk usage |
| docker buildx history | Commands to work on build records |
| docker buildx imagetools | Commands to work on images in registry |
| docker buildx inspect | Inspect current builder instance |
| docker buildx ls | List builder instances |
| docker buildx policy | Commands for working with build policies |
| docker buildx prune | Remove build cache |
| docker buildx rm | Remove one or more builder instances |
| docker buildx stop | Stop builder instance |
| docker buildx use | Set the current builder instance |
| docker buildx version | Show buildx version information |

---

# docker checkpoint create

# docker checkpoint create

| Description | Create a checkpoint from a running container |
| --- | --- |
| Usage | docker checkpoint create [OPTIONS] CONTAINER CHECKPOINT |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Create a checkpoint from a running container

## Options

| Option | Default | Description |
| --- | --- | --- |
| --checkpoint-dir |  | Use a custom checkpoint storage directory |
| --leave-running |  | Leave the container running after checkpoint |

---

# docker checkpoint ls

# docker checkpoint ls

| Description | List checkpoints for a container |
| --- | --- |
| Usage | docker checkpoint ls [OPTIONS] CONTAINER |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker checkpoint list |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

List checkpoints for a container

## Options

| Option | Default | Description |
| --- | --- | --- |
| --checkpoint-dir |  | Use a custom checkpoint storage directory |

---

# docker checkpoint rm

# docker checkpoint rm

| Description | Remove a checkpoint |
| --- | --- |
| Usage | docker checkpoint rm [OPTIONS] CONTAINER CHECKPOINT |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker checkpoint remove |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Remove a checkpoint

## Options

| Option | Default | Description |
| --- | --- | --- |
| --checkpoint-dir |  | Use a custom checkpoint storage directory |

---

# docker checkpoint

# docker checkpoint

| Description | Manage checkpoints |
| --- | --- |
| Usage | docker checkpoint |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Checkpoint and Restore is an experimental feature that allows you to freeze a running
container by specifying a checkpoint, which turns the container state into a collection of files
on disk. Later, the container can be restored from the point it was frozen.

This is accomplished using a tool called [CRIU](https://criu.org), which is an
external dependency of this feature. A good overview of the history of
checkpoint and restore in Docker is available in this
[Kubernetes blog post](https://kubernetes.io/blog/2015/07/how-did-quake-demo-from-dockercon-work/).

### Installing CRIU

If you use a Debian system, you can add the CRIU PPA and install with `apt-get` [from the CRIU launchpad](https://launchpad.net/~criu/+archive/ubuntu/ppa).

Alternatively, you can [build CRIU from source](https://criu.org/Installation).

You need at least version 2.0 of CRIU to run checkpoint and restore in Docker.

### Use cases for checkpoint and restore

This feature is currently focused on single-host use cases for checkpoint and
restore. Here are a few:

- Restarting the host machine without stopping/starting containers
- Speeding up the start time of slow start applications
- "Rewinding" processes to an earlier point in time
- "Forensic debugging" of running processes

Another primary use case of checkpoint and restore outside of Docker is the live
migration of a server from one machine to another. This is possible with the
current implementation, but not currently a priority (and so the workflow is
not optimized for the task).

### Using checkpoint and restore

A new top level command `docker checkpoint` is introduced, with three subcommands:

- `docker checkpoint create` (creates a new checkpoint)
- `docker checkpoint ls` (lists existing checkpoints)
- `docker checkpoint rm` (deletes an existing checkpoint)

Additionally, a `--checkpoint` flag is added to the `docker container start` command.

The options for `docker checkpoint create`:

```console
Usage:  docker checkpoint create [OPTIONS] CONTAINER CHECKPOINT

Create a checkpoint from a running container

  --leave-running=false    Leave the container running after checkpoint
  --checkpoint-dir         Use a custom checkpoint storage directory
```

And to restore a container:

```console
Usage:  docker start --checkpoint CHECKPOINT_ID [OTHER OPTIONS] CONTAINER
```

Example of using checkpoint and restore on a container:

```console
$ docker run --security-opt=seccomp:unconfined --name cr -d busybox /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'
abc0123

$ docker checkpoint create cr checkpoint1

# <later>
$ docker start --checkpoint checkpoint1 cr
abc0123
```

This process just logs an incrementing counter to stdout. If you run `docker logs`
in-between running/checkpoint/restoring, you should see that the counter
increases while the process is running, stops while it's frozen, and
resumes from the point it left off once you restore.

### Known limitations

`seccomp` is only supported by CRIU in very up-to-date kernels.

External terminals (i.e. `docker run -t ..`) aren't supported.
If you try to create a checkpoint for a container with an external terminal,
it fails:

```console
$ docker checkpoint create cr checkpoint1
Error response from daemon: Cannot checkpoint container c1: rpc error: code = 2 desc = exit status 1: "criu failed: type NOTIFY errno 0\nlog file: /var/lib/docker/containers/eb62ebdbf237ce1a8736d2ae3c7d88601fc0a50235b0ba767b559a1f3c5a600b/checkpoints/checkpoint1/criu.work/dump.log\n"

$ cat /var/lib/docker/containers/eb62ebdbf237ce1a8736d2ae3c7d88601fc0a50235b0ba767b559a1f3c5a600b/checkpoints/checkpoint1/criu.work/dump.log
Error (mount.c:740): mnt: 126:./dev/console doesn't have a proper root mount
```

## Subcommands

| Command | Description |
| --- | --- |
| docker checkpoint create | Create a checkpoint from a running container |
| docker checkpoint ls | List checkpoints for a container |
| docker checkpoint rm | Remove a checkpoint |

---

# docker compose alpha dry

# docker compose alpha dry-run

| Description | EXPERIMENTAL - Dry run command allow you to test a command without applying changes |
| --- | --- |
| Usage | docker compose alpha dry-run -- [COMMAND...] |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

EXPERIMENTAL - Dry run command allow you to test a command without applying changes

---

# docker compose alpha scale

# docker compose alpha scale

| Description | Scale services |
| --- | --- |
| Usage | docker compose alpha scale [SERVICE=REPLICAS...] |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Scale services

## Options

| Option | Default | Description |
| --- | --- | --- |
| --no-deps |  | Don't start linked services. |

---

# docker compose alpha viz

# docker compose alpha viz

| Description | EXPERIMENTAL - Generate a graphviz graph from your compose file |
| --- | --- |
| Usage | docker compose alpha viz [OPTIONS] |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

EXPERIMENTAL - Generate a graphviz graph from your compose file

## Options

| Option | Default | Description |
| --- | --- | --- |
| --image |  | Include service's image name in output graph |
| --indentation-size | 1 | Number of tabs or spaces to use for indentation |
| --networks |  | Include service's attached networks in output graph |
| --ports |  | Include service's exposed ports in output graph |
| --spaces |  | If given, space character ' ' will be used to indent,otherwise tab character '\t' will be used |

---

# docker compose alpha

# docker compose alpha

| Description | Experimental commands |
| --- | --- |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Experimental commands

## Subcommands

| Command | Description |
| --- | --- |
| docker compose alpha dry-run | EXPERIMENTAL - Dry run command allow you to test a command without applying changes |
| docker compose alpha scale | Scale services |
| docker compose alpha viz | EXPERIMENTAL - Generate a graphviz graph from your compose file |

---

# docker compose attach

# docker compose attach

| Description | Attach local standard input, output, and error streams to a service's running container |
| --- | --- |
| Usage | docker compose attach [OPTIONS] SERVICE |

## Description

Attach local standard input, output, and error streams to a service's running container

## Options

| Option | Default | Description |
| --- | --- | --- |
| --detach-keys |  | Override the key sequence for detaching from a container. |
| --index |  | index of the container if service has multiple replicas. |
| --no-stdin |  | Do not attach STDIN |
| --sig-proxy | true | Proxy all received signals to the process |

---

# docker compose bridge convert

# docker compose bridge convert

| Description | Convert compose files to Kubernetes manifests, Helm charts, or another model |
| --- | --- |
| Usage | docker compose bridge convert |

## Description

Convert compose files to Kubernetes manifests, Helm charts, or another model

## Options

| Option | Default | Description |
| --- | --- | --- |
| -o, --output | out | The output directory for the Kubernetes resources |
| --templates |  | Directory containing transformation templates |
| -t, --transformation |  | Transformation to apply to compose model (default: docker/compose-bridge-kubernetes) |

---

# docker compose bridge transformations create

# docker compose bridge transformations create

| Description | Create a new transformation |
| --- | --- |
| Usage | docker compose bridge transformations create [OPTION] PATH |

## Description

Create a new transformation

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --from |  | Existing transformation to copy (default: docker/compose-bridge-kubernetes) |
