# docker sandbox and more

# docker sandbox

# docker sandbox

| Description | Docker Sandbox |
| --- | --- |
| Usage | docker sandbox |

## Description

Local sandbox environments for AI agents, using Docker.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -D, --debug |  | Enable debug logging |

## Subcommands

| Command | Description |
| --- | --- |
| docker sandbox create | Create a sandbox for an agent |
| docker sandbox create cagent | Create a sandbox for cagent |
| docker sandbox create codex | Create a sandbox for codex |
| docker sandbox create gemini | Create a sandbox for gemini |
| docker sandbox create kiro | Create a sandbox for kiro |
| docker sandbox exec | Execute a command inside a sandbox |
| docker sandbox inspect | Display detailed information on one or more sandboxes |
| docker sandbox ls | List VMs |
| docker sandbox network | Manage sandbox networking |
| docker sandbox reset | Reset all VM sandboxes and clean up state |
| docker sandbox rm | Remove one or more sandboxes |
| docker sandbox run | Run an agent in a sandbox |
| docker sandbox stop | Stop one or more sandboxes without removing them |
| docker sandbox version | Show sandbox version information |

---

# docker scout attestation add

# docker scout attestation add

| Description | Add attestation to image |
| --- | --- |
| Usage | docker scout attestation add OPTIONS IMAGE [IMAGE...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout attest add |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The docker scout attestation add command adds attestations to images.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --file |  | File location of attestations to attach |
| --org |  | Namespace of the Docker organization |
| --predicate-type |  | Predicate-type for attestations |
| --referrer |  | Use OCI referrer API for pushing attestation |
| --referrer-repository | registry.scout.docker.com | Repository to push referrer to |

---

# docker scout attestation get

# docker scout attestation get

| Description | Get attestation for image |
| --- | --- |
| Usage | docker scout attestation get OPTIONS IMAGE [DIGEST] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout attest get |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The docker scout attestation get command gets attestations for images.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --key | https://registry.scout.docker.com/keyring/dhi/latest.pub | Signature key to use for verification |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --predicate |  | Get in-toto predicate only dropping the subject |
| --predicate-type |  | Predicate-type for attestation |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |
| --skip-tlog |  | Skip signature verification against public transaction log |
| --verify |  | Verify the signature on the attestation |

---

# docker scout attestation list

# docker scout attestation list

| Description | List attestations for image |
| --- | --- |
| Usage | docker scout attestation list OPTIONS IMAGE |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout attest list |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The docker scout attestation list command lists attestations for images.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | list | Output format:- list: list of attestations of the image- json: json representation of the attestation list (default "json") |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --predicate-type |  | Predicate-type for attestations |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |

---

# docker scout attestation

# docker scout attestation

| Description | Manage attestations on images |
| --- | --- |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout attest |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Manage attestations on images

## Subcommands

| Command | Description |
| --- | --- |
| docker scout attestation add | Add attestation to image |
| docker scout attestation get | Get attestation for image |
| docker scout attestation list | List attestations for image |

---

# docker scout cache df

# docker scout cache df

| Description | Show Docker Scout disk usage |
| --- | --- |
| Usage | docker scout cache df |

## Description

Docker Scout uses a temporary cache storage for generating image SBOMs.
The cache helps avoid regenerating or fetching resources unnecessarily.

This `docker scout cache df` command shows the cached data on the host.
Each cache entry is identified by the digest of the image.

You can use the `docker scout cache prune` command to delete cache data at any time.

## Examples

### List temporary and cache files

```console
$ docker scout cache df
Docker Scout temporary directory to generate SBOMs is located at:
   /var/folders/dw/d6h9w2sx6rv3lzwwgrnx7t5h0000gp/T/docker-scout
   this path can be configured using the DOCKER_SCOUT_CACHE_DIR environment variable

                               Image Digest                               │ Size
──────────────────────────────────────────────────────────────────────────┼────────
  sha256:c41ab5c992deb4fe7e5da09f67a8804a46bd0592bfdf0b1847dde0e0889d2bff │ 21 kB

Total: 21 kB

Docker Scout cached SBOMs are located at:
   /Users/user/.docker/scout/sbom

                               Image Digest                               │ Size of SBOM
──────────────────────────────────────────────────────────────────────────┼───────────────
  sha256:02bb6f428431fbc2809c5d1b41eab5a68350194fb508869a33cb1af4444c9b11 │ 42 kB
  sha256:03fc002fe4f370463a8f04d3a288cdffa861e462fc8b5be44ab62b296ad95183 │ 100 kB
  sha256:088134dd33e4a2997480a1488a41c11abebda465da5cf7f305a0ecf8ed494329 │ 194 kB
  sha256:0b80b2f17aff7ee5bfb135c69d0d6fe34070e89042b7aac73d1abcc79cfe6759 │ 852 kB
  sha256:0c9e8abe31a5f17d84d5c85d3853d2f948a4f126421e89e68753591f1b6fedc5 │ 930 kB
  sha256:0d49cae0723c8d310e413736b5e91e0c59b605ade2546f6e6ef8f1f3ddc76066 │ 510 kB
  sha256:0ef04748d071c2e631bb3edce8f805cb5512e746b682c83fdae6d8c0b243280b │ 1.0 MB
  sha256:13fd22925b638bb7d2131914bb8f8b0f5f582bee364aec682d9e7fe722bb486a │ 42 kB
  sha256:174c41d4fbc7f63e1f2bb7d2f7837318050406f2f27e5073a84a84f18b48b883 │ 115 kB

Total: 4 MB
```

---

# docker scout cache prune

# docker scout cache prune

| Description | Remove temporary or cached data |
| --- | --- |
| Usage | docker scout cache prune |

## Description

The `docker scout cache prune` command removes temporary data and SBOM cache.

By default, `docker scout cache prune` only deletes temporary data.
To delete temporary data and clear the SBOM cache, use the `--sboms` flag.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Do not prompt for confirmation |
| --sboms |  | Prune cached SBOMs |

## Examples

### Delete temporary data

```console
$ docker scout cache prune
? Are you sure to delete all temporary data? Yes
    ✓ temporary data deleted
```

### Delete temporary and cache data

```console
$ docker scout cache prune --sboms
? Are you sure to delete all temporary data and all cached SBOMs? Yes
    ✓ temporary data deleted
    ✓ cached SBOMs deleted
```

---

# docker scout cache

# docker scout cache

| Description | Manage Docker Scout cache and temporary files |
| --- | --- |

## Description

Manage Docker Scout cache and temporary files

## Subcommands

| Command | Description |
| --- | --- |
| docker scout cache df | Show Docker Scout disk usage |
| docker scout cache prune | Remove temporary or cached data |

---

# docker scout compare

# docker scout compare

| Description | Compare two images and display differences (experimental) |
| --- | --- |
| Usage | docker scout compare --to IMAGE|DIRECTORY|ARCHIVE [IMAGE|DIRECTORY|ARCHIVE] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout diff |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The `docker scout compare` command analyzes two images and displays a comparison.

> This command is **experimental** and its behaviour might change in the future

The intended use of this command is to compare two versions of the same image.
For instance, when a new image is built and compared to the version running in production.

If no image is specified, the most recently built image is used
as a comparison target.

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
- `sbom://` SPDX file or in-toto attestation file with SPDX predicate or `syft` json SBOM file

## Options

| Option | Default | Description |
| --- | --- | --- |
| -x, --exit-on |  | Comma separated list of conditions to fail the action step if worse or changed, options are: vulnerability, policy, package |
| --format | text | Output format of the generated vulnerability report:- text: default output, plain text with or without colors depending on the terminal- markdown: Markdown output |
| --hide-policies |  | Hide policy status from the output |
| --ignore-base |  | Filter out CVEs introduced from base image |
| --ignore-suppressed |  | Filter CVEs found in Scout exceptions based on the specified exception scope |
| --ignore-unchanged |  | Filter out unchanged packages |
| --multi-stage |  | Show packages from multi-stage Docker builds |
| --only-fixed |  | Filter to fixable CVEs |
| --only-package-type |  | Comma separated list of package types (like apk, deb, rpm, npm, pypi, golang, etc) |
| --only-policy |  | Comma separated list of policies to evaluate |
| --only-severity |  | Comma separated list of severities (critical, high, medium, low, unspecified) to filter CVEs by |
| --only-stage |  | Comma separated list of multi-stage Docker build stage names |
| --only-unfixed |  | Filter to unfixed CVEs |
| --only-vex-affected |  | Filter CVEs by VEX statements with status not affected |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |
| --to |  | Image, directory, or archive to compare to |
| --to-env |  | Name of environment to compare to |
| --to-latest |  | Latest image processed to compare to |
| --to-ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive. |
| --vex-author | [<.*@docker.com>] | List of VEX statement authors to accept |
| --vex-location |  | File location of directory or file containing VEX statements |

## Examples

### Compare the most recently built image to the latest tag

```console
$ docker scout compare --to namespace/repo:latest
```

### Compare local build to the same tag from the registry

```console
$ docker scout compare local://namespace/repo:latest --to registry://namespace/repo:latest
```

### Ignore base images

```console
$ docker scout compare --ignore-base --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

### Generate a markdown output

```console
$ docker scout compare --format markdown --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

### Only compare maven packages and only display critical vulnerabilities for maven packages

```console
$ docker scout compare --only-package-type maven --only-severity critical --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

### Show all policy results for both images

```console
docker scout compare --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

---

# docker scout config

# docker scout config

| Description | Manage Docker Scout configuration |
| --- | --- |
| Usage | docker scout config [KEY] [VALUE] |

## Description

`docker scout config` allows you to list, get and set Docker Scout configuration.

Available configuration key:

- `organization`: Namespace of the Docker organization to be used by default.

## Examples

### List existing configuration

```console
$ docker scout config
organization=my-org-namespace
```

### Print configuration value

```console
$ docker scout config organization
my-org-namespace
```

### Set configuration value

```console
$ docker scout config organization my-org-namespace
    ✓ Successfully set organization to my-org-namespace
```

---

# docker scout cves

# docker scout cves

| Description | Display CVEs identified in a software artifact |
| --- | --- |
| Usage | docker scout cves [OPTIONS] [IMAGE|DIRECTORY|ARCHIVE] |

## Description

The `docker scout cves` command analyzes a software artifact for vulnerabilities.

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
- `sbom://` SPDX file or in-toto attestation file with SPDX predicate or `syft` json SBOM file
  In case of `sbom://` prefix, if the file is not defined then it will try to read it from the standard input.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --details |  | Print details on default text output |
| --env |  | Name of environment |
| --epss |  | Display the EPSS scores and organize the package's CVEs according to their EPSS score |
| --epss-percentile |  | Exclude CVEs with EPSS scores less than the specified percentile (0 to 1) |
| --epss-score |  | Exclude CVEs with EPSS scores less than the specified value (0 to 1) |
| -e, --exit-code |  | Return exit code '2' if vulnerabilities are detected |
| --format | packages | Output format of the generated vulnerability report:- packages: default output, plain text with vulnerabilities grouped by packages- sarif: json Sarif output- spdx: json SPDX output- gitlab: json GitLab output- markdown: markdown output (including some html tags like collapsible sections)- sbom: json SBOM output |
| --ignore-base |  | Filter out CVEs introduced from base image |
| --ignore-suppressed |  | Filter CVEs found in Scout exceptions based on the specified exception scope |
| --locations |  | Print package locations including file paths and layer diff_id |
| --multi-stage |  | Show packages from multi-stage Docker builds |
| --only-base |  | Only show CVEs introduced by the base image |
| --only-cisa-kev |  | Filter to CVEs listed in the CISA KEV catalog |
| --only-cve-id |  | Comma separated list of CVE ids (like CVE-2021-45105) to search for |
| --only-fixed |  | Filter to fixable CVEs |
| --only-metric |  | Comma separated list of CVSS metrics (like AV:N or PR:L) to filter CVEs by |
| --only-package |  | Comma separated regular expressions to filter packages by |
| --only-package-type |  | Comma separated list of package types (like apk, deb, rpm, npm, pypi, golang, etc) |
| --only-severity |  | Comma separated list of severities (critical, high, medium, low, unspecified) to filter CVEs by |
| --only-stage |  | Comma separated list of multi-stage Docker build stage names |
| --only-unfixed |  | Filter to unfixed CVEs |
| --only-vex-affected |  | Filter CVEs by VEX statements with status not affected |
| --only-vuln-packages |  | When used with --format=only-packages ignore packages with no vulnerabilities |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |
| --vex-author | [<.*@docker.com>] | List of VEX statement authors to accept |
| --vex-location |  | File location of directory or file containing VEX statements |

## Examples

### Display vulnerabilities grouped by package

```console
$ docker scout cves alpine
Analyzing image alpine
✓ Image stored for indexing
✓ Indexed 18 packages
✓ No vulnerable package detected
```

### Display vulnerabilities from adocker savetarball

```console
$ docker save alpine > alpine.tar

$ docker scout cves archive://alpine.tar
Analyzing archive alpine.tar
✓ Archive read
✓ SBOM of image already cached, 18 packages indexed
✓ No vulnerable package detected
```

### Display vulnerabilities from an OCI directory

```console
$ skopeo copy --override-os linux docker://alpine oci:alpine

$ docker scout cves oci-dir://alpine
Analyzing OCI directory alpine
✓ OCI directory read
✓ Image stored for indexing
✓ Indexed 19 packages
✓ No vulnerable package detected
```

### Display vulnerabilities from the current directory

```console
$ docker scout cves fs://.
```

### Export vulnerabilities to a SARIF JSON file

```console
$ docker scout cves --format sarif --output alpine.sarif.json alpine
Analyzing image alpine
✓ SBOM of image already cached, 18 packages indexed
✓ No vulnerable package detected
✓ Report written to alpine.sarif.json
```

### Display markdown output

The following example shows how to generate the vulnerability report as markdown.

```console
$ docker scout cves --format markdown alpine
✓ Pulled
✓ SBOM of image already cached, 19 packages indexed
✗ Detected 1 vulnerable package with 3 vulnerabilities
<h2>:mag: Vulnerabilities of <code>alpine</code></h2>

<details open="true"><summary>:package: Image Reference</strong> <code>alpine</code></summary>
<table>
<tr><td>digest</td><td><code>sha256:e3bd82196e98898cae9fe7fbfd6e2436530485974dc4fb3b7ddb69134eda2407</code></td><tr><tr><td>vulnerabilities</td><td><img alt="critical: 0" src="https://img.shields.io/badge/critical-0-lightgrey"/> <img alt="high: 0" src="https://img.shields.io/badge/high-0-lightgrey"/> <img alt="medium: 2" src="https://img.shields.io/badge/medium-2-fbb552"/> <img alt="low: 0" src="https://img.shields.io/badge/low-0-lightgrey"/> <img alt="unspecified: 1" src="https://img.shields.io/badge/unspecified-1-lightgrey"/></td></tr>
<tr><td>platform</td><td>linux/arm64</td></tr>
<tr><td>size</td><td>3.3 MB</td></tr>
<tr><td>packages</td><td>19</td></tr>
</table>
</details></table>
</details>
...
```

### List all vulnerable packages of a certain type

The following example shows how to generate a list of packages, only including
packages of the specified type, and only showing packages that are vulnerable.

```console
$ docker scout cves --format only-packages --only-package-type golang --only-vuln-packages golang:1.18.0
✓ Pulled
✓ SBOM of image already cached, 296 packages indexed
✗ Detected 1 vulnerable package with 40 vulnerabilities

Name   Version   Type         Vulnerabilities
───────────────────────────────────────────────────────────
stdlib  1.18     golang     2C    29H     8M     1L
```

### Display EPSS score (--epss)

The `--epss` flag adds [Exploit Prediction Scoring System (EPSS)](https://www.first.org/epss/)
scores to the `docker scout cves` output. EPSS scores are estimates of the likelihood (probability)
that a software vulnerability will be exploited in the wild in the next 30 days.
The higher the score, the greater the probability that a vulnerability will be exploited.

```console
$ docker scout cves --epss nginx
 ✓ Provenance obtained from attestation
 ✓ SBOM obtained from attestation, 232 packages indexed
 ✓ Pulled
 ✗ Detected 23 vulnerable packages with a total of 39 vulnerabilities

...

 ✗ HIGH CVE-2023-52425
   https://scout.docker.com/v/CVE-2023-52425
   Affected range  : >=2.5.0-1
   Fixed version   : not fixed
   EPSS Score      : 0.000510
   EPSS Percentile : 0.173680
```

- `EPSS Score` is a floating point number between 0 and 1 representing the probability of exploitation in the wild in the next 30 days (following score publication).
- `EPSS Percentile` is the percentile of the current score, the proportion of all scored vulnerabilities with the same or a lower EPSS score.

You can use the `--epss-score` and `--epss-percentile` flags to filter the output
of `docker scout cves` based on these scores. For example,
to only show vulnerabilities with an EPSS score higher than 0.5:

```console
$ docker scout cves --epss --epss-score 0.5 nginx
 ✓ SBOM of image already cached, 232 packages indexed
 ✓ EPSS scores for 2024-03-01 already cached
 ✗ Detected 1 vulnerable package with 1 vulnerability

...

 ✗ LOW CVE-2023-44487
   https://scout.docker.com/v/CVE-2023-44487
   Affected range  : >=1.22.1-9
   Fixed version   : not fixed
   EPSS Score      : 0.705850
   EPSS Percentile : 0.979410
```

EPSS scores are updated on a daily basis.
By default, the latest available score is displayed.
You can use the `--epss-date` flag to manually specify a date
in the format `yyyy-mm-dd` for fetching EPSS scores.

```console
$ docker scout cves --epss --epss-date 2024-01-02 nginx
```

### List vulnerabilities from an SPDX file

The following example shows how to generate a list of vulnerabilities from an SPDX file using `syft`.

```console
$ syft -o spdx-json alpine:3.16.1 | docker scout cves sbom://
 ✔ Pulled image
 ✔ Loaded image                                                                                                                              alpine:3.16.1
 ✔ Parsed image                                                                    sha256:3d81c46cd8756ddb6db9ec36fa06a6fb71c287fb265232ba516739dc67a5f07d
 ✔ Cataloged contents                                                                     274a317d88b54f9e67799244a1250cad3fe7080f45249fa9167d1f871218d35f
   ├── ✔ Packages                        [14 packages]
   ├── ✔ File digests                    [75 files]
   ├── ✔ File metadata                   [75 locations]
   └── ✔ Executables                     [16 executables]
    ✗ Detected 2 vulnerable packages with a total of 11 vulnerabilities
```

---

# docker scout enroll

# docker scout enroll

| Description | Enroll an organization with Docker Scout |
| --- | --- |
| Usage | docker scout enroll ORG |

## Description

The `docker scout enroll` command enrolls an organization with Docker Scout.

---

# docker scout environment

# docker scout environment

| Description | Manage environments (experimental) |
| --- | --- |
| Usage | docker scout environment [ENVIRONMENT] [IMAGE] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout env |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The `docker scout environment` command lists the environments.
If you pass an image reference, the image is recorded to the specified environment.

Once recorded, environments can be referred to by their name. For example,
you can refer to the `production` environment with the `docker scout compare`
command as follows:

```console
$ docker scout compare --to-env production
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to record |

## Examples

### List existing environments

```console
$ docker scout environment
prod
staging
```

### List images of an environment

```console
$ docker scout environment staging
namespace/repo:tag@sha256:9a4df4fadc9bbd44c345e473e0688c2066a6583d4741679494ba9228cfd93e1b
namespace/other-repo:tag@sha256:0001d6ce124855b0a158569c584162097fe0ca8d72519067c2c8e3ce407c580f
```

### Record an image to an environment, for a specific platform

```console
$ docker scout environment staging namespace/repo:stage-latest --platform linux/amd64
✓ Pulled
✓ Successfully recorded namespace/repo:stage-latest in environment staging
```

---

# docker scout integration configure

# docker scout integration configure

| Description | Configure or update a new integration configuration |
| --- | --- |
| Usage | docker scout integration configure INTEGRATION |

## Description

The docker scout integration configure command creates or updates a new integration configuration for an organization.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --name |  | Name of integration configuration to create |
| --org |  | Namespace of the Docker organization |
| --parameter |  | Integration parameters in the form of --parameter NAME=VALUE |

---

# docker scout integration delete

# docker scout integration delete

| Description | Delete a new integration configuration |
| --- | --- |
| Usage | docker scout integration delete INTEGRATION |

## Description

The docker scout integration delete command deletes a new integration configuration for an organization.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --name |  | Name of integration configuration to delete |
| --org |  | Namespace of the Docker organization |

---

# docker scout integration list

# docker scout integration list

| Description | List integrations which can be installed |
| --- | --- |
| Usage | docker scout integration list [INTEGRATION] |

## Description

The docker scout integration list configured integrations for an organization.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --name |  | Name of integration configuration to list |
| --org |  | Namespace of the Docker organization |

---

# docker scout integration

# docker scout integration

| Description | Commands to list, configure, and delete Docker Scout integrations |
| --- | --- |

## Description

Commands to list, configure, and delete Docker Scout integrations

## Subcommands

| Command | Description |
| --- | --- |
| docker scout integration configure | Configure or update a new integration configuration |
| docker scout integration delete | Delete a new integration configuration |
| docker scout integration list | List integrations which can be installed |

---

# docker scout policy

# docker scout policy

| Description | Evaluate policies against an image and display the policy evaluation results (experimental) |
| --- | --- |
| Usage | docker scout policy [IMAGE | REPO] |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

The `docker scout policy` command evaluates policies against an image.
The image analysis is uploaded to Docker Scout where policies get evaluated.

The policy evaluation results may take a few minutes to become available.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -e, --exit-code |  | Return exit code '2' if policies are not met, '0' otherwise |
| --only-policy |  | Comma separated list of policies to evaluate |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to pull policy results from |
| --to-env |  | Name of the environment to compare to |
| --to-latest |  | Latest image processed to compare to |

## Examples

### Evaluate policies against an image and display the results

```console
$ docker scout policy dockerscoutpolicy/customers-api-service:0.0.1
```

### Evaluate policies against an image for a specific organization

```console
$ docker scout policy dockerscoutpolicy/customers-api-service:0.0.1 --org dockerscoutpolicy
```

### Evaluate policies against an image with a specific platform

```console
$ docker scout policy dockerscoutpolicy/customers-api-service:0.0.1 --platform linux/amd64
```

### Compare policy results for a repository in a specific environment

```console
$ docker scout policy dockerscoutpolicy/customers-api-service --to-env production
```

---

# docker scout push

# docker scout push

| Description | Push an image or image index to Docker Scout |
| --- | --- |
| Usage | docker scout push IMAGE |

## Description

The `docker scout push` command lets you push an image or analysis result to Docker Scout.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --author |  | Name of the author of the image |
| --dry-run |  | Do not push the image but process it |
| --org |  | Namespace of the Docker organization to which image will be pushed |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to be pushed |
| --sbom |  | Create and upload SBOMs |
| --secrets |  | Scan for secrets in the image |
| --timestamp |  | Timestamp of image or tag creation |

## Examples

### Push an image to Docker Scout

```console
$ docker scout push --org my-org registry.example.com/repo:tag
```

---

# docker scout quickview

# docker scout quickview

| Description | Quick overview of an image |
| --- | --- |
| Usage | docker scout quickview [IMAGE|DIRECTORY|ARCHIVE] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker scout qv |

## Description

The `docker scout quickview` command displays a quick overview of an image.
It displays a summary of the vulnerabilities in the specified image
and vulnerabilities from the base image.
If available, it also displays base image refresh and update recommendations.

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
- `sbom://` SPDX file or in-toto attestation file with SPDX predicate or `syft` json SBOM file
  In case of `sbom://` prefix, if the file is not defined then it will try to read it from the standard input.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --env |  | Name of the environment |
| --ignore-suppressed |  | Filter CVEs found in Scout exceptions based on the specified exception scope |
| --latest |  | Latest indexed image |
| --only-policy |  | Comma separated list of policies to evaluate |
| --only-vex-affected |  | Filter CVEs by VEX statements with status not affected |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |
| --vex-author | [<.*@docker.com>] | List of VEX statement authors to accept |
| --vex-location |  | File location of directory or file containing VEX statements |

## Examples

### Quick overview of an image

```console
$ docker scout quickview golang:1.19.4
    ...Pulling
    ✓ Pulled
    ✓ SBOM of image already cached, 278 packages indexed

  Your image  golang:1.19.4                          │    5C     3H     6M    63L
  Base image  buildpack-deps:bullseye-scm            │    5C     1H     3M    48L     6?
  Refreshed base image  buildpack-deps:bullseye-scm  │    0C     0H     0M    42L
                                                     │    -5     -1     -3     -6     -6
  Updated base image  buildpack-deps:sid-scm         │    0C     0H     1M    29L
                                                     │    -5     -1     -2    -19     -6
```

### Quick overview of the most recently built image

```console
$ docker scout qv
```

### Quick overview from an SPDX file

```console
$  syft -o spdx-json alpine:3.16.1 | docker scout quickview sbom://
 ✔ Loaded image                                                                                                                              alpine:3.16.1
 ✔ Parsed image                                                                    sha256:3d81c46cd8756ddb6db9ec36fa06a6fb71c287fb265232ba516739dc67a5f07d
 ✔ Cataloged contents                                                                     274a317d88b54f9e67799244a1250cad3fe7080f45249fa9167d1f871218d35f
   ├── ✔ Packages                        [14 packages]
   ├── ✔ File digests                    [75 files]
   ├── ✔ File metadata                   [75 locations]
   └── ✔ Executables                     [16 executables]

  Target   │ <stdin>        │    1C     2H     8M     0L
    digest │  274a317d88b5  │
```

---

# docker scout recommendations

# docker scout recommendations

| Description | Display available base image updates and remediation recommendations |
| --- | --- |
| Usage | docker scout recommendations [IMAGE|DIRECTORY|ARCHIVE] |

## Description

The `docker scout recommendations` command display recommendations for base images updates.
It analyzes the image and display recommendations to refresh or update the base image.
For each recommendation it shows a list of benefits, such as
fewer vulnerabilities or smaller image size.

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
| --only-refresh |  | Only display base image refresh recommendations |
| --only-update |  | Only display base image update recommendations |
| --org |  | Namespace of the Docker organization |
| -o, --output |  | Write the report to a file |
| --platform |  | Platform of image to analyze |
| --ref |  | Reference to use if the provided tarball contains multiple references.Can only be used with archive |
| --tag |  | Specify tag |

## Examples

### Display base image update recommendations

```console
$ docker scout recommendations golang:1.19.4
```

### Display base image refresh only recommendations

```console
$ docker scout recommendations --only-refresh golang:1.19.4
```

### Display base image update only recommendations

```console
$ docker scout recommendations --only-update golang:1.19.4
```

---

# docker scout repo disable

# docker scout repo disable

| Description | Disable Docker Scout |
| --- | --- |
| Usage | docker scout repo disable [REPOSITORY] |

## Description

The docker scout repo disable command disables Docker Scout on repositories.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all |  | Disable all repositories of the organization. Can not be used with --filter. |
| --filter |  | Regular expression to filter repositories by name |
| --integration |  | Name of the integration to use for enabling an image |
| --org |  | Namespace of the Docker organization |
| --registry |  | Container Registry |

## Examples

### Disable a specific repository

```console
$ docker scout repo disable my/repository
```

### Disable all repositories of the organization

```console
$ docker scout repo disable --all
```

### Disable some repositories based on a filter

```console
$ docker scout repo disable --filter namespace/backend
```

### Disable a repository from a specific registry

```console
$ docker scout repo disable my/repository --registry 123456.dkr.ecr.us-east-1.amazonaws.com
```
