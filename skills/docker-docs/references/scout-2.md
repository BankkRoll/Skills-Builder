# Docker Scout metrics exporter and more

# Docker Scout metrics exporter

> Learn how to scrape data from Docker Scout using Prometheus to create your own vulnerability and policy dashboards with Grafana

# Docker Scout metrics exporter

   Table of contents

---

Docker Scout exposes a metrics HTTP endpoint that lets you scrape vulnerability
and policy data from Docker Scout, using Prometheus or Datadog. With this you
can create your own, self-hosted Docker Scout dashboards for visualizing supply
chain metrics.

## Metrics

The metrics endpoint exposes the following metrics:

| Metric | Description | Labels | Type |
| --- | --- | --- | --- |
| scout_stream_vulnerabilities | Vulnerabilities in a stream | streamName,severity | Gauge |
| scout_policy_compliant_images | Compliant images for a policy in a stream | id,displayName,streamName | Gauge |
| scout_policy_evaluated_images | Total images evaluated against a policy in a stream | id,displayName,streamName | Gauge |

> **Streams**
>
>
>
> In Docker Scout, the streams concept is a superset of
> [environments](https://docs.docker.com/scout/integrations/environment/).
> Streams include all runtime environments that you've defined,
> as well as the special `latest-indexed` stream.
> The `latest-indexed` stream contains the most recently pushed (and analyzed) tag for each repository.
>
>
>
> Streams is mostly an internal concept in Docker Scout,
> with the exception of the data exposed through this metrics endpoint.

## Creating an access token

To export metrics from your organization, first make sure your organization is enrolled in Docker Scout.
Then, create a Personal Access Token (PAT) - a secret token that allows the exporter to authenticate with the Docker Scout API.

The PAT does not require any specific permissions, but it must be created by a user who is an owner of the Docker organization.
To create a PAT, follow the steps in
[Create an access token](https://docs.docker.com/security/access-tokens/).

Once you have created the PAT, store it in a secure location.
You will need to provide this token to the exporter when scraping metrics.

## Prometheus

This section describes how to scrape the metrics endpoint using Prometheus.

### Add a job for your organization

In the Prometheus configuration file, add a new job for your organization.
The job should include the following configuration;
replace `ORG` with your organization name:

```yaml
scrape_configs:
  - job_name: ORG
    metrics_path: /v1/exporter/org/ORG/metrics
    scheme: https
    static_configs:
      - targets:
          - api.scout.docker.com
```

The address in the `targets` field is set to the domain name of the Docker Scout API, `api.scout.docker.com`.
Make sure that there's no firewall rule in place preventing the server from communicating with this endpoint.

### Add bearer token authentication

To scrape metrics from the Docker Scout Exporter endpoint using Prometheus, you need to configure Prometheus to use the PAT as a bearer token.
The exporter requires the PAT to be passed in the `Authorization` header of the request.

Update the Prometheus configuration file to include the `authorization` configuration block.
This block defines the PAT as a bearer token stored in a file:

```yaml
scrape_configs:
  - job_name: $ORG
    authorization:
      type: Bearer
      credentials_file: /etc/prometheus/token
```

The content of the file should be the PAT in plain text:

```console
dckr_pat_...
```

If you are running Prometheus in a Docker container or Kubernetes pod, mount the file into the container using a volume or secret.

Finally, restart Prometheus to apply the changes.

### Prometheus sample project

If you don't have a Prometheus server set up, you can run a [sample project](https://github.com/dockersamples/scout-metrics-exporter) using Docker Compose.
The sample includes a Prometheus server that scrapes metrics for a Docker organization enrolled in Docker Scout,
alongside Grafana with a pre-configured dashboard to visualize the vulnerability and policy metrics.

1. Clone the starter template for bootstrapping a set of Compose services
  for scraping and visualizing the Docker Scout metrics endpoint:
  ```console
  $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
  $ cd scout-metrics-exporter/prometheus
  ```
2. [Create a Docker access token](https://docs.docker.com/security/access-tokens/)
  and store it in a plain text file at `/prometheus/prometheus/token` under the template directory.
  token
  ```plaintext
  $ echo $DOCKER_PAT > ./prometheus/token
  ```
3. In the Prometheus configuration file at `/prometheus/prometheus/prometheus.yml`,
  replace `ORG` in the `metrics_path` property on line 6 with the namespace of your Docker organization.
  prometheus/prometheus.yml
  | 12345678910111213 | global:scrape_interval:60sscrape_timeout:40sscrape_configs:-job_name:Docker Scout policymetrics_path:/v1/exporter/org/ORG/metricsscheme:httpsstatic_configs:-targets:-api.scout.docker.comauthorization:type:Bearercredentials_file:/etc/prometheus/token |
  | --- | --- |
4. Start the compose services.
  ```console
  docker compose up -d
  ```
  This command starts two services: the Prometheus server and Grafana.
  Prometheus scrapes metrics from the Docker Scout endpoint,
  and Grafana visualizes the metrics using a pre-configured dashboard.

To stop the demo and clean up any resources created, run:

```console
docker compose down -v
```

### Access to Prometheus

After starting the services, you can access the Prometheus expression browser by visiting [http://localhost:9090](http://localhost:9090).
The Prometheus server runs in a Docker container and is accessible on port 9090.

After a few seconds, you should see the metrics endpoint as a target in the
Prometheus UI at [http://localhost:9090/targets](http://localhost:9090/targets).

![Docker Scout metrics exporter Prometheus target](https://docs.docker.com/scout/images/scout-metrics-prom-target.png)Docker Scout metrics exporter Prometheus target ![Docker Scout metrics exporter Prometheus target](https://docs.docker.com/scout/images/scout-metrics-prom-target.png)

### Viewing the metrics in Grafana

To view the Grafana dashboards, go to [http://localhost:3000/dashboards](http://localhost:3000/dashboards),
and sign in using the credentials defined in the Docker Compose file (username: `admin`, password: `grafana`).

![Vulnerability dashboard in Grafana](https://docs.docker.com/scout/images/scout-metrics-grafana-vulns.png)Vulnerability dashboard in Grafana ![Vulnerability dashboard in Grafana](https://docs.docker.com/scout/images/scout-metrics-grafana-vulns.png)![Policy dashboard in Grafana](https://docs.docker.com/scout/images/scout-metrics-grafana-policy.png)Policy dashboard in Grafana ![Policy dashboard in Grafana](https://docs.docker.com/scout/images/scout-metrics-grafana-policy.png)

The dashboards are pre-configured to visualize the vulnerability and policy metrics scraped by Prometheus.

## Datadog

This section describes how to scrape the metrics endpoint using Datadog.
Datadog pulls data for monitoring by running a customizable
[agent](https://docs.datadoghq.com/agent/?tab=Linux) that scrapes available
endpoints for any exposed metrics. The OpenMetrics and Prometheus checks are
included in the agent, so you don’t need to install anything else on your
containers or hosts.

This guide assumes you have a Datadog account and a Datadog API Key. Refer to
the [Datadog documentation](https://docs.datadoghq.com/agent) to get started.

### Configure the Datadog agent

To start collecting the metrics, you will need to edit the agent’s
configuration file for the OpenMetrics check. If you're running the agent as a
container, such file must be mounted at
`/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml`.

The following example shows a Datadog configuration that:

- Specifies the OpenMetrics endpoint targeting the `dockerscoutpolicy` Docker organization
- A `namespace` that all collected metrics will be prefixed with
- The [metrics](#metrics) you want the agent to scrape (`scout_*`)
- An `auth_token` section for the Datadog agent to authenticate to the Metrics
  endpoint, using a Docker PAT as a Bearer token.

```yaml
instances:
  - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/dockerscoutpolicy/metrics"
    namespace: "scout-metrics-exporter"
    metrics:
      - scout_*
    auth_token:
      reader:
        type: file
        path: /var/run/secrets/scout-metrics-exporter/token
      writer:
        type: header
        name: Authorization
        value: Bearer TOKEN
```

> Important
>
> Do not replace the `<TOKEN>` placeholder in the previous configuration
> example. It must stay as it is. Only make sure the Docker PAT is correctly
> mounted into the Datadog agent in the specified filesystem path. Save the
> file as `conf.yaml` and restart the agent.

When creating a Datadog agent configuration of your own, make sure to edit the
`openmetrics_endpoint` property to target your organization, by replacing
`dockerscoutpolicy` with the namespace of your Docker organization.

### Datadog sample project

If you don't have a Datadog server set up, you can run a [sample project](https://github.com/dockersamples/scout-metrics-exporter)
using Docker Compose. The sample includes a Datadog agent, running as a
container, that scrapes metrics for a Docker organization enrolled in Docker
Scout. This sample project assumes that you have a Datadog account, an API key,
and a Datadog site.

1. Clone the starter template for bootstrapping a Datadog Compose service for
  scraping the Docker Scout metrics endpoint:
  ```console
  $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
  $ cd scout-metrics-exporter/datadog
  ```
2. [Create a Docker access token](https://docs.docker.com/security/access-tokens/)
  and store it in a plain text file at `/datadog/token` under the template directory.
  token
  ```plaintext
  $ echo $DOCKER_PAT > ./token
  ```
3. In the `/datadog/compose.yaml` file, update the `DD_API_KEY` and `DD_SITE` environment variables
  with the values for your Datadog deployment.
  ```yaml
  datadog-agent:
      container_name: datadog-agent
      image: gcr.io/datadoghq/agent:7
      environment:
        - DD_API_KEY=${DD_API_KEY} # e.g. 1b6b3a42...
        - DD_SITE=${DD_SITE} # e.g. datadoghq.com
        - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock:ro
        - ./conf.yaml:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml:ro
        - ./token:/var/run/secrets/scout-metrics-exporter/token:ro
  ```
  The `volumes` section mounts the Docker socket from the host to the
  container. This is required to obtain an accurate hostname when running as a
  container ([more details here](https://docs.datadoghq.com/agent/troubleshooting/hostname_containers/)).
  It also mounts the agent's config file and the Docker access token.
4. Edit the `/datadog/config.yaml` file by replacing the placeholder `<ORG>` in
  the `openmetrics_endpoint` property with the namespace of the Docker
  organization that you want to collect metrics for.
  ```yaml
  instances:
    - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/<ORG>/metrics"
      namespace: "scout-metrics-exporter"
  # ...
  ```
5. Start the Compose services.
  ```console
  docker compose up -d
  ```

If configured properly, you should see the OpenMetrics check under Running
Checks when you run the agent’s status command whose output should look similar
to:

```text
openmetrics (4.2.0)
-------------------
  Instance ID: openmetrics:scout-prometheus-exporter:6393910f4d92f7c2 [OK]
  Configuration Source: file:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml
  Total Runs: 1
  Metric Samples: Last Run: 236, Total: 236
  Events: Last Run: 0, Total: 0
  Service Checks: Last Run: 1, Total: 1
  Average Execution Time : 2.537s
  Last Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
  Last Successful Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
```

For a comprehensive list of options, take a look at this [example config file](https://github.com/DataDog/integrations-core/blob/master/openmetrics/datadog_checks/openmetrics/data/conf.yaml.example) for the generic OpenMetrics check.

### Visualizing your data

Once the agent is configured to grab Prometheus metrics, you can use them to build comprehensive Datadog graphs, dashboards, and alerts.

Go into your [Metric summary page](https://app.datadoghq.com/metric/summary?filter=scout_prometheus_exporter)
to see the metrics collected from this example. This configuration will collect
all exposed metrics starting with `scout_` under the namespace
`scout_metrics_exporter`.

![datadog_metrics_summary](https://docs.docker.com/scout/images/datadog_metrics_summary.png)  ![datadog_metrics_summary](https://docs.docker.com/scout/images/datadog_metrics_summary.png)

The following screenshots show examples of a Datadog dashboard containing
graphs about vulnerability and policy compliance for a specific [stream](#stream).

![datadog_dashboard_1](https://docs.docker.com/scout/images/datadog_dashboard_1.png)  ![datadog_dashboard_1](https://docs.docker.com/scout/images/datadog_dashboard_1.png)![datadog_dashboard_2](https://docs.docker.com/scout/images/datadog_dashboard_2.png)  ![datadog_dashboard_2](https://docs.docker.com/scout/images/datadog_dashboard_2.png)

> The reason why the lines in the graphs look flat is due to the own nature of
> vulnerabilities (they don't change too often) and the short time interval
> selected in the date picker.

## Scrape interval

By default, Prometheus and Datadog scrape metrics at a 15 second interval.
Because of the own nature of vulnerability data, the metrics exposed through this API are unlikely to change at a high frequency.
For this reason, the metrics endpoint has a 60-minute cache by default,
which means a scraping interval of 60 minutes or higher is recommended.
If you set the scrape interval to less than 60 minutes, you will see the same data in the metrics for multiple scrapes during that time window.

To change the scrape interval:

- Prometheus: set the `scrape_interval` field in the Prometheus configuration
  file at the global or job level.
- Datadog: set the `min_collection_interval` property in the Datadog agent
  configuration file, see [Datadog documentation](https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval).

## Revoke an access token

If you suspect that your PAT has been compromised or is no longer needed, you can revoke it at any time.
To revoke a PAT, follow the steps in the
[Create and manage access tokens](https://docs.docker.com/security/access-tokens/).

Revoking a PAT immediately invalidates the token, and prevents Prometheus from scraping metrics using that token.
You will need to create a new PAT and update the Prometheus configuration to use the new token.

---

# Use Scout with different artifact types

> Some of the Docker Scout commands support image references prefixes for controlling the location of the images or files that you want to analyze.

# Use Scout with different artifact types

   Table of contents

---

Some of the Docker Scout CLI commands support prefixes for specifying
the location or type of artifact that you would like to analyze.

By default, image analysis with the `docker scout cves` command
targets images in the local image store of the Docker Engine.
The following command always uses a local image if it exists:

```console
$ docker scout cves <image>
```

If the image doesn't exist locally, Docker pulls the image before running the analysis.
Analyzing the same image again would use the same local version by default,
even if the tag has since changed in the registry.

By adding a `registry://` prefix to the image reference,
you can force Docker Scout to analyze the registry version of the image:

```console
$ docker scout cves registry://<image>
```

## Supported prefixes

The supported prefixes are:

| Prefix | Description |
| --- | --- |
| image://(default) | Use a local image, or fall back to a registry lookup |
| local:// | Use an image from the local image store (don't do a registry lookup) |
| registry:// | Use an image from a registry (don't use a local image) |
| oci-dir:// | Use an OCI layout directory |
| archive:// | Use a tarball archive, as created bydocker save |
| fs:// | Use a local directory or file |

You can use prefixes with the following commands:

- `docker scout compare`
- `docker scout cves`
- `docker scout quickview`
- `docker scout recommendations`
- `docker scout sbom`

## Examples

This section contains a few examples showing how you can use prefixes
to specify artifacts for `docker scout` commands.

### Analyze a local project

The `fs://` prefix lets you analyze local source code directly,
without having to build it into a container image.
The following `docker scout quickview` command gives you an
at-a-glance vulnerability summary of the source code in the current working directory:

```console
$ docker scout quickview fs://.
```

To view the details of vulnerabilities found in your local source code, you can
use the `docker scout cves --details fs://.` command. Combine it with
other flags to narrow down the results to the packages and vulnerabilities that
you're interested in.

```console
$ docker scout cves --details --only-severity high fs://.
    ✓ File system read
    ✓ Indexed 323 packages
    ✗ Detected 1 vulnerable package with 1 vulnerability

​## Overview

                    │        Analyzed path
────────────────────┼──────────────────────────────
  Path              │  /Users/david/demo/scoutfs
    vulnerabilities │    0C     1H     0M     0L

​## Packages and Vulnerabilities

   0C     1H     0M     0L  fastify 3.29.0
pkg:npm/fastify@3.29.0

    ✗ HIGH CVE-2022-39288 [OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities]
      https://scout.docker.com/v/CVE-2022-39288

      fastify is a fast and low overhead web framework, for Node.js. Affected versions of
      fastify are subject to a denial of service via malicious use of the Content-Type
      header. An attacker can send an invalid Content-Type header that can cause the
      application to crash. This issue has been addressed in commit  fbb07e8d  and will be
      included in release version 4.8.1. Users are advised to upgrade. Users unable to
      upgrade may manually filter out http content with malicious Content-Type headers.

      Affected range : <4.8.1
      Fixed version  : 4.8.1
      CVSS Score     : 7.5
      CVSS Vector    : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H

1 vulnerability found in 1 package
  LOW       0
  MEDIUM    0
  HIGH      1
  CRITICAL  0
```

### Compare a local project to an image

With `docker scout compare`, you can compare the analysis of source code on
your local filesystem with the analysis of a container image.
The following example compares local source code (`fs://.`)
with a registry image `registry://docker/scout-cli:latest`.
In this case, both the baseline and target for the comparison use prefixes.

```console
$ docker scout compare fs://. --to registry://docker/scout-cli:latest --ignore-unchanged
WARN 'docker scout compare' is experimental and its behaviour might change in the future
    ✓ File system read
    ✓ Indexed 268 packages
    ✓ SBOM of image already cached, 234 packages indexed

  ## Overview

                           │              Analyzed File System              │              Comparison Image
  ─────────────────────────┼────────────────────────────────────────────────┼─────────────────────────────────────────────
    Path / Image reference │  /Users/david/src/docker/scout-cli-plugin      │  docker/scout-cli:latest
                           │                                                │  bb0b01303584
      platform             │                                                │ linux/arm64
      provenance           │ https://github.com/dvdksn/scout-cli-plugin.git │ https://github.com/docker/scout-cli-plugin
                           │  6ea3f7369dbdfec101ac7c0fa9d78ef05ffa6315      │  67cb4ef78bd69545af0e223ba5fb577b27094505
      vulnerabilities      │    0C     0H     1M     1L                     │    0C     0H     1M     1L
                           │                                                │
      size                 │ 7.4 MB (-14 MB)                                │ 21 MB
      packages             │ 268 (+34)                                      │ 234
                           │                                                │

  ## Packages and Vulnerabilities

    +   55 packages added
    -   21 packages removed
       213 packages unchanged
```

The previous example is truncated for brevity.

### View the SBOM of an image tarball

The following example shows how you can use the `archive://` prefix
to get the SBOM of an image tarball, created with `docker save`.
The image in this case is `docker/scout-cli:latest`,
and the SBOM is exported to file `sbom.spdx.json` in SPDX format.

```console
$ docker pull docker/scout-cli:latest
latest: Pulling from docker/scout-cli
257973a141f5: Download complete
1f2083724dd1: Download complete
5c8125a73507: Download complete
Digest: sha256:13318bb059b0f8b0b87b35ac7050782462b5d0ac3f96f9f23d165d8ed68d0894
$ docker save docker/scout-cli:latest -o scout-cli.tar
$ docker scout sbom --format spdx -o sbom.spdx.json archive://scout-cli.tar
```

## Learn more

Read about the commands and supported flags in the CLI reference documentation:

- [docker scout quickview](https://docs.docker.com/reference/cli/docker/scout/quickview/)
- [docker scout cves](https://docs.docker.com/reference/cli/docker/scout/cves/)
- [docker scout compare](https://docs.docker.com/reference/cli/docker/scout/compare/)

---

# Configure Docker Scout with environment variables

> Configure how the behavior of Docker Scout CLI commands using these environment variables

# Configure Docker Scout with environment variables

   Table of contents

---

The following environment variables are available to configure the Docker Scout
CLI commands, and the corresponding `docker/scout-cli` container image:

| Name | Format | Description |
| --- | --- | --- |
| DOCKER_SCOUT_CACHE_FORMAT | String | Format of the local image cache; can beociortar(default:oci) |
| DOCKER_SCOUT_CACHE_DIR | String | Directory where the local SBOM cache is stored (default:$HOME/.docker/scout) |
| DOCKER_SCOUT_NO_CACHE | Boolean | When set totrue, disables the use of local SBOM cache |
| DOCKER_SCOUT_OFFLINE | Boolean | Useoffline modewhen indexing SBOM |
| DOCKER_SCOUT_REGISTRY_TOKEN | String | Token for authenticating to a registry when pulling images |
| DOCKER_SCOUT_REGISTRY_USER | String | Username for authenticating to a registry when pulling images |
| DOCKER_SCOUT_REGISTRY_PASSWORD | String | Password or personal access token for authenticating to a registry when pulling images |
| DOCKER_SCOUT_HUB_USER | String | Docker Hub username for authenticating to the Docker Scout backend |
| DOCKER_SCOUT_HUB_PASSWORD | String | Docker Hub password or personal access token for authenticating to the Docker Scout backend |
| DOCKER_SCOUT_NEW_VERSION_WARN | Boolean | Warn about new versions of the Docker Scout CLI |
| DOCKER_SCOUT_EXPERIMENTAL_WARN | Boolean | Warn about experimental features |
| DOCKER_SCOUT_EXPERIMENTAL_POLICY_OUTPUT | Boolean | Disable experimental output for policy evaluation |

## Offline mode

Under normal operation, Docker Scout cross-references external systems, such as
npm, NuGet, or proxy.golang.org, to retrieve additional information about
packages found in your image.

When `DOCKER_SCOUT_OFFLINE` is set to `true`, Docker Scout image analysis runs
in offline mode. Offline mode means Docker Scout doesn't make outbound requests
to external systems.

To use offline mode:

```console
$ export DOCKER_SCOUT_OFFLINE=true
```

---

# Create an exception using the GUI

> Create an exception for a vulnerability in an image using the Docker Scout Dashboard or Docker Desktop.

# Create an exception using the GUI

   Table of contents

---

The Docker Scout Dashboard and Docker Desktop provide a user-friendly interface
for creating
[exceptions](https://docs.docker.com/scout/explore/exceptions/) for
vulnerabilities found in container images. Exceptions let you acknowledge
accepted risks or address false positives in image analysis.

## Prerequisites

To create an in the Docker Scout Dashboard or Docker Desktop, you need a Docker
account with **Editor** or **Owner** permissions for the Docker organization
that owns the image.

## Steps

To create an exception for a vulnerability in an image using the Docker Scout
Dashboard or Docker Desktop:

1. Go to the [Images page](https://scout.docker.com/reports/images).
2. Select the image tag that contains the vulnerability you want to create an
  exception for.
3. Open the **Image layers** tab.
4. Select the layer that contains the vulnerability you want to create an
  exception for.
5. In the **Vulnerabilities** tab, find the vulnerability you want to create an
  exception for. Vulnerabilities are grouped by package. Find the package that
  contains the vulnerability you want to create an exception for, and then
  expand the package.
6. Select the **Create exception** button next to the vulnerability.

Selecting the **Create exception** button opens the **Create exception** side panel.
In this panel, you can provide the details of the exception:

- **Exception type**: The type of exception. The only supported types are:
  - **Accepted risk**: The vulnerability is not addressed due to its minimal
    security risk, high remediation costs, dependence on an upstream fix, or
    similar.
  - **False positive**: The vulnerability presents no security risk in your
    specific use case, configuration, or because of measures in place that
    block exploitation
    If you select **False positive**, you must provide a justification for why
    the vulnerability is a false positive:
- **Additional details**: Any additional information that you want to
  provide about the exception.
- **Scope**: The scope of the exception. The scope can be:
  - **Image**: The exception applies to the selected image.
  - **All images in repository**: The exception applies to all images in the
    repository.
  - **Specific repository**: The exception applies to all images in the
    specified repositories.
  - **All images in my organization**: The exception applies to all images in
    your organization.
- **Package scope**: The scope of the exception. The package scope can be:
  - **Selected package**: The exception applies to the selected package.
  - **Any packages**: The exception applies to all packages vulnerable to this
    CVE.

When you've filled in the details, select the **Create** button to create the
exception.

The exception is now created and factored into the analysis results for the
images that you selected. The exception is also listed on the **Exceptions**
tab of the [Vulnerabilities page](https://scout.docker.com/reports/vulnerabilities/exceptions)
in the Docker Scout Dashboard.

1. Open the **Images** view in Docker Desktop.
2. Open the **Hub** tab.
3. Select the image tag that contains the vulnerability you want to create an
  exception for.
4. Select the layer that contains the vulnerability you want to create an
  exception for.
5. In the **Vulnerabilities** tab, find the vulnerability you want to create an
  exception for.
6. Select the **Create exception** button next to the vulnerability.

Selecting the **Create exception** button opens the **Create exception** side panel.
In this panel, you can provide the details of the exception:

- **Exception type**: The type of exception. The only supported types are:
  - **Accepted risk**: The vulnerability is not addressed due to its minimal
    security risk, high remediation costs, dependence on an upstream fix, or
    similar.
  - **False positive**: The vulnerability presents no security risk in your
    specific use case, configuration, or because of measures in place that
    block exploitation
    If you select **False positive**, you must provide a justification for why
    the vulnerability is a false positive:
- **Additional details**: Any additional information that you want to
  provide about the exception.
- **Scope**: The scope of the exception. The scope can be:
  - **Image**: The exception applies to the selected image.
  - **All images in repository**: The exception applies to all images in the
    repository.
  - **Specific repository**: The exception applies to all images in the
    specified repositories.
  - **All images in my organization**: The exception applies to all images in
    your organization.
- **Package scope**: The scope of the exception. The package scope can be:
  - **Selected package**: The exception applies to the selected package.
  - **Any packages**: The exception applies to all packages vulnerable to this
    CVE.

When you've filled in the details, select the **Create** button to create the
exception.

The exception is now created and factored into the analysis results for the
images that you selected. The exception is also listed on the **Exceptions**
tab of the [Vulnerabilities page](https://scout.docker.com/reports/vulnerabilities/exceptions)
in the Docker Scout Dashboard.

---

# Create an exception using the VEX

> Create an exception for a vulnerability in an image using VEX documents.

# Create an exception using the VEX

   Table of contents

---

Vulnerability Exploitability eXchange (VEX) is a standard format for
documenting vulnerabilities in the context of a software package or product.
Docker Scout supports VEX documents to create
[exceptions](https://docs.docker.com/scout/explore/exceptions/) for vulnerabilities in images.

> Note
>
> You can also create exceptions using the Docker Scout Dashboard or Docker
> Desktop. The GUI provides a user-friendly interface for creating exceptions,
> and it's easy to manage exceptions for multiple images. It also lets you
> create exceptions for multiple images, or your entire organization, all at
> once. For more information, see
> [Create an exception using the GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/).

## Prerequisites

To create exceptions using OpenVEX documents, you need:

- The latest version of Docker Desktop or the Docker Scout CLI plugin
- The [vexctl](https://github.com/openvex/vexctl) command line tool.
- The
  [containerd image store](https://docs.docker.com/desktop/features/containerd/) must be enabled
- Write permissions to the registry repository where the image is stored

## Introduction to VEX

The VEX standard is defined by a working group by the United States
Cybersecurity and Infrastructure Security Agency (CISA). At the core of VEX are
exploitability assessments. These assessments describe the status of a given
CVE for a product. The possible vulnerability statuses in VEX are:

- Not affected: No remediation is required regarding this vulnerability.
- Affected: Actions are recommended to remediate or address this vulnerability.
- Fixed: These product versions contain a fix for the vulnerability.
- Under investigation: It is not yet known whether these product versions are affected by the vulnerability. An update will be provided in a later release.

There are multiple implementations and formats of VEX. Docker Scout supports
the [OpenVex](https://github.com/openvex/spec) implementation. Regardless of
the specific implementation, the core idea is the same: to provide a framework
for describing the impact of vulnerabilities. Key components of VEX regardless
of implementation includes:

VEX documentA type of security advisory for storing VEX statements.
The format of the document depends on the specific implementation.VEX statementDescribes the status of a vulnerability in a product,
whether it's exploitable, and whether there are ways to remediate the issue.Justification and impactDepending on the vulnerability status, statements include a justification
or impact statement describing why a product is or isn't affected.Action statementsDescribe how to remediate or mitigate the vulnerability.

## vexctlexample

The following example command creates a VEX document stating that:

- The software product described by this VEX document is the Docker image
  `example/app:v1`
- The image contains the npm package `express@4.17.1`
- The npm package is affected by a known vulnerability: `CVE-2022-24999`
- The image is unaffected by the CVE, because the vulnerable code is never
  executed in containers that run this image

```console
$ vexctl create \
  --author="author@example.com" \
  --product="pkg:docker/example/app@v1" \
  --subcomponents="pkg:npm/express@4.17.1" \
  --vuln="CVE-2022-24999" \
  --status="not_affected" \
  --justification="vulnerable_code_not_in_execute_path" \
  --file="CVE-2022-24999.vex.json"
```

Here's a description of the options in this example:

`--author`The email of the author of the VEX document.`--product`Package URL (PURL) of the Docker image. A PURL is an identifier
for the image in a standardized format, defined in the PURL
[specification](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#docker).

Docker image PURL strings begin with a `pkg:docker` type prefix, followed by
the image repository and version (the image tag or SHA256 digest). Unlike
image tags, where the version is specified like `example/app:v1`, in PURL the
image repository and version are separated by an `@`.

`--subcomponents`PURL of the vulnerable package in the image. In this example, the
vulnerability exists in an npm package, so the `--subcomponents` PURL is the
identifier for the npm package name and version (`pkg:npm/express@4.17.1`).

If the same vulnerability exists in multiple packages, `vexctl` lets you
specify the `--subcomponents` flag multiple times for a single `create`
command.

You can also omit `--subcomponents`, in which case the VEX statement applies
to the entire image.

`--vuln`ID of the CVE that the VEX statement addresses.`--status`This is the status label of the vulnerability. This describes the
relationship between the software (`--product`) and the CVE (`--vuln`).
The possible values for the status label in OpenVEX are:

- `not_affected`
- `affected`
- `fixed`
- `under_investigation`

In this example, the VEX statement asserts that the Docker image is
`not_affected` by the vulnerability. The `not_affected` status is the only
status that results in CVE suppression, where the CVE is filtered out of the
analysis results. The other statuses are useful for documentation purposes,
but they do not work for creating exceptions. For more information about all
the possible status labels, see [Status Labels](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-labels)
in the OpenVEX specification.

`--justification`Justifies the `not_affected` status label, informing why the product is not
affected by the vulnerability. In this case, the justification given is
`vulnerable_code_not_in_execute_path`, signalling that the vulnerability
can't be executed as used by the product.

In OpenVEX, status justifications can have one of the five possible values:

- `component_not_present`
- `vulnerable_code_not_present`
- `vulnerable_code_not_in_execute_path`
- `vulnerable_code_cannot_be_controlled_by_adversary`
- `inline_mitigations_already_exist`

For more information about these values and their definitions, see
[Status Justifications](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-justifications)
in the OpenVEX specification.

`--file`Filename of the VEX document output

## Example JSON document

Here's the OpenVEX JSON generated by this command:

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://openvex.dev/docs/public/vex-749f79b50f5f2f0f07747c2de9f1239b37c2bda663579f87a35e5f0fdfc13de5",
  "author": "author@example.com",
  "timestamp": "2024-05-27T13:20:22.395824+02:00",
  "version": 1,
  "statements": [
    {
      "vulnerability": {
        "name": "CVE-2022-24999"
      },
      "timestamp": "2024-05-27T13:20:22.395829+02:00",
      "products": [
        {
          "@id": "pkg:docker/example/app@v1",
          "subcomponents": [
            {
              "@id": "pkg:npm/express@4.17.1"
            }
          ]
        }
      ],
      "status": "not_affected",
      "justification": "vulnerable_code_not_in_execute_path"
    }
  ]
}
```

Understanding how VEX documents are supposed to be structured can be a bit of a
mouthful. The [OpenVEX specification](https://github.com/openvex/spec)
describes the format and all the possible properties of documents and
statements. For the full details, refer to the specification to learn more
about the available fields and how to create a well-formed OpenVEX document.

To learn more about the available flags and syntax of the `vexctl` CLI tool and
how to install it, refer to the [vexctlGitHub repository](https://github.com/openvex/vexctl).

## Verifying VEX documents

To test whether the VEX documents you create are well-formed and produce the
expected results, use the `docker scout cves` command with the `--vex-location`
flag to apply a VEX document to a local image analysis using the CLI.

The following command invokes a local image analysis that incorporates all VEX
documents in the specified location, using the `--vex-location` flag. In this
example, the CLI is instructed to look for VEX documents in the current working
directory.

```console
$ docker scout cves IMAGE --vex-location .
```

The output of the `docker scout cves` command displays the results with any VEX
statements found in under the `--vex-location` location factored into the
results. For example, CVEs assigned a status of `not_affected` are filtered out
from the results. If the output doesn't seem to take the VEX statements into
account, that's an indication that the VEX documents might be invalid in some
way.

Things to look out for include:

- The PURL of a Docker image must begin with `pkg:docker/` followed by the image name.
- In a Docker image PURL, the image name and version is separated by `@`.
  An image named `example/myapp:1.0` has the following PURL: `pkg:docker/example/myapp@1.0`.
- Remember to specify an `author` (it's a mandatory field in OpenVEX)
- The [OpenVEX specification](https://github.com/openvex/spec) describes how
  and when to use `justification`, `impact_statement`, and other fields in the
  VEX documents. Specifying these in an incorrect way results in an invalid
  document. Make sure your VEX documents comply with the OpenVEX specification.

## Attach VEX documents to images

When you've created a VEX document,
you can attach it to your image in the following ways:

- Attach the document as an [attestation](#attestation)
- Embed the document in the [image filesystem](#image-filesystem)

You can't remove a VEX document from an image once it's been added. For
documents attached as attestations, you can create a new VEX document and
attach it to the image again. Doing so will overwrite the previous VEX document
(but it won't remove the attestation). For images where the VEX document has
been embedded in the image's filesystem, you need to rebuild the image to
change the VEX document.

### Attestation

To attach VEX documents as an attestation, you can use the `docker scout attestation add` CLI command. Using attestations is the recommended option for
attaching exceptions to images when using VEX.

You can attach attestations to images that have already been pushed to a
registry. You don't need to build or push the image again. Additionally, having
the exceptions attached to the image as attestations means consumers can
inspect the exceptions for an image, directly from the registry.

To attach an attestation to an image:

1. Build the image and push it to a registry.
  ```console
  $ docker build --provenance=true --sbom=true --tag IMAGE --push .
  ```
2. Attach the exception to the image as an attestation.
  ```console
  $ docker scout attestation add \
    --file <cve-id>.vex.json \
    --predicate-type https://openvex.dev/ns/v0.2.0 \
    IMAGE
  ```
  The options for this command are:
  - `--file`: the location and filename of the VEX document
  - `--predicate-type`: the in-toto `predicateType` for OpenVEX

### Image filesystem

Embedding VEX documents directly on the image filesystem is a good option if
you know the exceptions ahead of time, before you build the image. And it's
relatively easy; just `COPY` the VEX document to the image in your Dockerfile.

The downside with this approach is that you can't change or update the
exception later. Image layers are immutable, so anything you put in the image's
filesystem is there forever. Attaching the document as an
[attestation](#attestation) provides better flexibility.

> Note
>
> VEX documents embedded in the image filesystem are not considered for images
> that have attestations. If your image has **any** attestations, Docker Scout
> will only look for exceptions in the attestations, and not in the image
> filesystem.
>
>
>
> If you want to use the VEX document embedded in the image filesystem, you
> must remove the attestation from the image. Note that provenance attestations
> may be added automatically for images. To ensure that no attestations are
> added to the image, you can explicitly disable both SBOM and provenance
> attestations using the `--provenance=false` and `--sbom=false` flags when
> building the image.

To embed a VEX document on the image filesystem, `COPY` the file into the image
as part of the image build. The following example shows how to copy all VEX
documents under `.vex/` in the build context, to `/var/lib/db` in the image.

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine
COPY .vex/* /var/lib/db/
```

The filename of the VEX document must match the `*.vex.json` glob pattern.
It doesn't matter where on the image's filesystem you store the file.

Note that the copied files must be part of the filesystem of the final image,
For multi-stage builds, the documents must persist in the final stage.

---

# Docker Scout SBOMs

> Use Docker Scout to extract the SBOM for your project.

# Docker Scout SBOMs

   Table of contents

---

[Image analysis](https://docs.docker.com/scout/explore/analysis/) uses image SBOMs to understand what packages and versions an image contains.
Docker Scout uses SBOM attestations if available on the image (recommended).
If no SBOM attestation is available, Docker Scout creates one by indexing the image contents.

## View from CLI

To view the contents of the SBOM that Docker Scout generates, you can use the
`docker scout sbom` command.

```console
$ docker scout sbom [IMAGE]
```

By default, this prints the SBOM in a JSON format to stdout.
The default JSON format produced by `docker scout sbom` isn't SPDX-JSON.
To output SPDX, use the `--format spdx` flag:

```console
$ docker scout sbom --format spdx [IMAGE]
```

To generate a human-readable list, use the `--format list` flag:

```console
$ docker scout sbom --format list alpine

           Name             Version    Type
───────────────────────────────────────────────
  alpine-baselayout       3.4.3-r1     apk
  alpine-baselayout-data  3.4.3-r1     apk
  alpine-keys             2.4-r1       apk
  apk-tools               2.14.0-r2    apk
  busybox                 1.36.1-r2    apk
  busybox-binsh           1.36.1-r2    apk
  ca-certificates         20230506-r0  apk
  ca-certificates-bundle  20230506-r0  apk
  libc-dev                0.7.2-r5     apk
  libc-utils              0.7.2-r5     apk
  libcrypto3              3.1.2-r0     apk
  libssl3                 3.1.2-r0     apk
  musl                    1.2.4-r1     apk
  musl-utils              1.2.4-r1     apk
  openssl                 3.1.2-r0     apk
  pax-utils               1.3.7-r1     apk
  scanelf                 1.3.7-r1     apk
  ssl_client              1.36.1-r2    apk
  zlib                    1.2.13-r1    apk
```

For more information about the `docker scout sbom` command, refer to the
[CLI
reference](https://docs.docker.com/reference/cli/docker/scout/sbom/).

## Attach as build attestation

You can generate the SBOM and attach it to the image at build-time as an
[attestation](https://docs.docker.com/build/metadata/attestations/). BuildKit provides a default
SBOM generator which is different from what Docker Scout uses.
You can configure BuildKit to use the Docker Scout SBOM generator
using the `--attest` flag for the `docker build` command.
The Docker Scout SBOM indexer provides richer results
and ensures better compatibility with the Docker Scout image analysis.

```console
$ docker build --tag <org>/<image> \
  --attest type=sbom,generator=docker/scout-sbom-indexer:latest \
  --push .
```

To build images with SBOM attestations, you must use either the
[containerd
image store](https://docs.docker.com/desktop/features/containerd/) feature, or use a `docker-container`
builder together with the `--push` flag to push the image (with attestations)
directly to a registry. The classic image store doesn't support manifest lists
or image indices, which is required for adding attestations to an image.

## Extract to file

The command for extracting the SBOM of an image to an SPDX JSON file is
different depending on whether the image has been pushed to a registry or if
it's a local image.

### Remote image

To extract the SBOM of an image and save it to a file, you can use the `docker buildx imagetools inspect` command. This command only works for images in a
registry.

```console
$ docker buildx imagetools inspect <image> --format "{{ json .SBOM }}" > sbom.spdx.json
```

### Local image

To extract the SPDX file for a local image, build the image with the `local`
exporter and use the `scout-sbom-indexer` SBOM generator plugin.

The following command saves the SBOM to a file at `build/sbom.spdx.json`.

```console
$ docker build --attest type=sbom,generator=docker/scout-sbom-indexer:latest \
  --output build .
```
