# Search code, repositories, users, issues, pull requests... and more

# Search code, repositories, users, issues, pull requests...

> Ubuntu 22 builders now available for GCP Buildpacks

**April 25, 2023 Update**

We are now targeting June 5, 2023 for the switchover from `latest` to `google-22`

**April 24, 2023 Update**

In order to reduce the chance of breaking users between `v1` and `google-22`, we're increasing the language support in `google-22` by adding:

- Python 3.8
- Python 3.9
- Ruby 3.0

These languages are still in support by their respective OSS communities, so we feel comfortable adding those in.

**April 6, 2023 Update:**

We're pumping the brakes on the switchover because we're worried about the potential for breaking `cloud run deploy --source`. Trying to create a few more guardrails for those users before making the official cutover. Will try to keep this thread updated with dates

---

Hi folks!

Today, we're excited to introduce the Ubuntu 22 (Jammy Jellyfish) builders into GCP’s buildpacks. This new builder uses Ubuntu 22 as the base image for both the run and build environments. You can find the new builder under the `:google-22` tag here [https://gcr.io/buildpacks/builder:google-22](https://gcr.io/buildpacks/builder:google-22)

**IMPORTANT** With the release of this builder we will also be planning to switch over the `:latest` tag to point to `:google-22` on March 6, 2023 June 5, 2023.

# Why is this important?

## Ubuntu 18 ESM

Using the GCP’s buildpacks project, the default builder `gcr.io/buildpacks/builder:v1` uses Ubuntu 18 as the container base image.  With Ubuntu 18 moving into Extended Security Maintenance in[April, 2023](https://wiki.ubuntu.com/Releases), it will be receiving [fewer security and maintenance updates](https://ubuntu.com/security/esm).

## Support for Node.js 18 and newer languages

When Node.js 18 launched last year (2022), it was built with a newer version of  `glibc/Ubuntu` that wasn’t available on Ubuntu 18 ([#248](https://github.com/GoogleCloudPlatform/buildpacks/issues/248)). The introduction of the Ubuntu 22 builder fixes this. Moving forward, we will be pushing to make the Ubuntu 22 builder the **default builder  image** so that our users get full use of modern OS environments.

## Improved Security & Smaller Images

Ubuntu 22 currently falls under Canonical’s Standard Support until [April 2027](https://wiki.ubuntu.com/Releases). As some of ya'll have already pointed this out to us in  [#232](https://github.com/GoogleCloudPlatform/buildpacks/issues/232), [#236](https://github.com/GoogleCloudPlatform/buildpacks/issues/236) and [#270](https://github.com/GoogleCloudPlatform/buildpacks/issues/270), this leads to container images that have "fixable" CVEs in them.

The Ubuntu 22 builder utilizes the updated [jammy packages repo](https://packages.ubuntu.com/jammy/) with updated dependencies. Using the Ubuntu 22 builder, you can produce images that are ~27% smaller and with half as many CVEs:

Building a [sample-go](https://github.com/GoogleCloudPlatform/buildpack-samples/tree/master/sample-go) app we see the following improvements between the builders:

|  | Ubuntu-18 Builder | Ubuntu-22 Builder |
| --- | --- | --- |
| Total CVEs | 34 | 11 |
| Fixable CVEs | 5 | 1 |
| Critical | 0 | 0 |
| High | 1 | 0 |
| Medium | 18 | 4 |
| Low | 15 | 7 |
| Image Size | 71.8 MB | 54.6 MB |

# Using the new Builder

The new build can be found at [https://gcr.io/buildpacks/builder:google-22](https://gcr.io/buildpacks/builder:google-22)

There are three ways to use the new builder:

- Locally with `pack` CLI
- Remotely with Cloud Build

## Locally with pack CLI

You can utilize the `--builder` flag to specify the new `google-22` tag on the builder image as follows:

```
pack build --builder=gcr.io/buildpacks/builder:google-22 <image name>
```

For more detailed instructions on building an image with `pack`, see[Local builds with GCP’s buildpacks](https://cloud.google.com/docs/buildpacks/build-application#local_builds)

## Remotely with Cloud Build

Cloud Build supports additional parameters on the `--pack` flag. Note that the fields after `--pack` is one continuous string, with the two parameters separated by a comma `,`

```
gcloud builds submit \
    --pack builder=gcr.io/buildpacks/builder:google-22,image=<region>.pkg.dev/<project>/<repository>/<image-name>
```

For more detailed instructions on building an image remote with Cloud Build, see [Remote builds with GCP’s buildpacks](https://cloud.google.com/docs/buildpacks/build-application#remote_builds)

# Supported Language Version

I'll be updating our docs page soon, but the new builder supports the following language versions:

| Language | Min Version | Max version | Applications | Functions |
| --- | --- | --- | --- | --- |
| Python | 3.10.0 | 3.11.x | ✓ | ✓ |
| Node.js | 14.19.2 | 18.x.x | ✓ | ✓ |
| Go | 1.x | Latest | ✓ | ✓ |
| Java | 8 | 19 | ✓ | ✓ |
| .NET | 6.0.0 | 7.0.x | ✓ | ✓ |
| PHP | 8.1.6 | 8.2.x | ✓ | ✓ |
| Ruby | 3.1.0 | 3.2.x | ✓ | ✓ |

# Other questions you might have

## Where can I find the builder code and image?

- GitHub Source Code: [https://github.com/GoogleCloudPlatform/buildpacks/tree/main/stacks/google_22](https://github.com/GoogleCloudPlatform/buildpacks/tree/main/stacks/google_22)
- Container Registry: [https://gcr.io/buildpacks/builder:google-22](https://gcr.io/buildpacks/builder:google-22)

## What packages are installed onto the builder images

Each builder comes with a build image and a run image.

- [Build image packages](https://github.com/GoogleCloudPlatform/buildpacks/blob/main/stacks/google_22/build-packages.txt)
- [Run image packages](https://github.com/GoogleCloudPlatform/buildpacks/blob/main/stacks/google_22/run-packages.txt)

## Why is there still 1 fixable CVE in the sample app?

We think it has to do with an outdated dependency, likely the pack CLI. We’ve gotten in touch with the Skaffold team and have requested them to update their images with the newest version of pack. This work is being tracked here  [GoogleContainerTools/skaffold#8290](https://github.com/GoogleContainerTools/skaffold/issues/8290)

## Will this break existing apps?

No...not yet! By default, [gcr.io/buildpacks/builder](http://gcr.io/buildpacks/builder) points to the latest tag,  which in turn points to the v1 tag for our most up-to-date Ubuntu 18 builder.

## What's the switchover plan to makegoogle-22the default builder?

Our plan is as follows:

**Announcement**

- Announce the new Ubuntu 22 builder google-22 in our [OSS repo](https://github.com/GoogleCloudPlatform/buildpacks)and our docs  (hey, this is it!)
- Update all documents and examples to explicitly show build with google-22 builder wherever possible  (in progress)
- Between now and March 6, 2023 June 5, 2023, `:latest` will point to `:v1`

**Feedback**

- Collect feedback from users on the `google-22` builder

**Switchover**

- After March 6, 2023 June 5, 2023 `:latest` points to `:google-22`
- `:v1` tag will still be available for users who want to build with the older environment

---

# Building a Go applicationStay organized with collectionsSave and categorize content based on your preferences.

# Building a Go applicationStay organized with collectionsSave and categorize content based on your preferences.

## Specifying the Go Version

By default the Go buildpack uses the latest stable version of the Go compiler. If your application requires a specific version, you can use the `GOOGLE_GO_VERSION` environment variable to provide a semver constraint that will be used to select an available Go version.

 See more code actions.  ?lit$229252482$ ?lit$229252482$   ?lit$229252482$Light code theme  ?lit$229252482$   ?lit$229252482$Dark code theme  ?lit$229252482$

```
pack build sample-go --builder=gcr.io/buildpacks/builder \
  --env GOOGLE_GO_VERSION="17.x.x"
```

## Compilation Flags

The Go buildpack compiles your application source into an executable using the `go build command`. The following environment variables can be used to configure the build behavior:

- `GOOGLE_BUILDABLE`
  Specifies path to a buildable unit.
  Example: `./maindir` for Go will build the package rooted at `maindir`.
- `GOOGLE_CLEAR_SOURCE`
  Omit the source code from the application image. If the application depends on static files, such as Go templates, setting this variable may cause the application to misbehave.
  Example: `true`, `True`, `1` will clear the source.
- `GOOGLE_GOGCFLAGS`
  Passed to `go build` and `go run` as `-gcflags` value with no interpretation.
  Example: `all=-N -l` enables race condition analysis and changes how source filepaths are recorded in the binary.
- `GOOGLE_GOLDFLAGS`
  Passed to go build and go run as `-ldflags` value with no interpretation.
  Example: `-s -w` is used to strip and reduce binary size.

## Managing Dependencies

We recommend that you use [Go modules](https://go.dev/blog/using-go-modules) to manage dependencies in your Go app. The Go buildpack uses the `go build` command to build your app and therefore matches the behavior of Go itself. To ensure that your app uses module-aware mode, you should include a `go.mod` file in your application root.

### Vendoring dependencies

Vendoring copies the packages your app uses into the application directory instead of downloading modules from their sources during the build process. Go provides the go build command [to vendor the packages your app needs](https://pkg.go.dev/cmd/go#hdr-Modules_and_vendoring) into a directory named `vendor` in your app's root directory.

## Configure the Application Entrypoint

By default, the Go buildpack will configure the application container entry invoke the `main` executable produced when compiling your application source. If you need to override this, you can do so by providing a `Procfile` or passing the `GOOGLE_ENTRYPOINT` environment variable.

## Environment Variables

The Go buildpack supports the following environment variables to customize your container

### GO

See Go documentation on [Environment Variables](https://pkg.go.dev/cmd/go#hdr-Environment_variables)

**Example:** `GOFLAGS=-flag=value` passes `-flag=value` to `go` commands.

   Was this helpful?

---

# Building a Java applicationStay organized with collectionsSave and categorize content based on your preferences.

# Building a Java applicationStay organized with collectionsSave and categorize content based on your preferences.

## Specify a Java version

By default, buildpacks use the [latest supported version of Java](https://cloud.google.com/docs/buildpacks/runtime-support#java) unless you specify a version. If your
application requires a specific version, you can use the
`GOOGLE_RUNTIME_VERSION` environment variable to specify a JDK version:

 See more code actions.  ?lit$391960732$ ?lit$391960732$   ?lit$391960732$Light code theme  ?lit$391960732$   ?lit$391960732$Dark code theme  ?lit$391960732$

```
pack build sample-java --builder=gcr.io/buildpacks/builder \
  --env GOOGLE_RUNTIME_VERSION=21
```

You can also use a `project.toml` project descriptor to encode
the environment variable alongside your project files. See instructions on
[building the application with environment variables](https://docs.cloud.google.com/docs/buildpacks/set-environment-variables#build_the_application_with_environment_variables)).

## Manage dependencies

Dependency configuration is supported for projects that use
Maven or Gradle.

### Configure Maven

Maven configurations can be applied using the `MAVEN_OPTS` environment variable.
See [documentation](https://maven.apache.org/configure.html) for
additional instructions.

Examples:

- `MAVEN_OPTS=-Xms256m -Xmx512m` passes these flags to the JVM
  running Maven.
- `MAVEN_OPTS=--add-opens java.base/java.lang=ALL-UNNAMED` to
  suppress "illegal reflective access" warnings from Maven.

To manage your project's dependency on Maven itself, you can use the
[Maven Wrapper](https://maven.apache.org/wrapper/). If you do not use the
Maven Wrapper, buildpacks defaults to using a recent version of Maven
when running `pack build`.

### Configure Gradle

Gradle configurations can be applied using the `GRADLE_OPTS` environment
variable. See
[documentation](https://docs.gradle.org/current/userguide/build_environment.html#sec:gradle_configuration_properties)
for additional instructions.

Example:

`GRADLE_OPTS=-Xms256m -Xmx512m` passes these flags to the JVM running Gradle.

### Google Cloud hosted Maven Central mirror

You can use the hosted mirror of Maven Central by specifying the
[available URLs](https://storage-download.googleapis.com/maven-central/index.html).

#### Mirror repositories in Maven

To configure a mirror, follow the
[Using Mirrors for Repositories](https://maven.apache.org/guides/mini/guide-mirror-settings.html)
instructions in the Maven project documentation.

Create a copy of the `settings.xml` from the default location of
`~/.m2/settings.xml` to inside your application source directory and specify
`GOOGLE_BUILD_ARGS=--settings <path/to/settings>`.

**Note:**  is relative to the source directory.

Example `settings.xml` file:

```
<settings>
  <mirrors>
    <mirror>
      <id>google-maven-central</id>
      <name>Cloud Storage Maven Central mirror</name>
      <url>https://maven-central.storage-download.googleapis.com/maven2/</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

#### Mirror repositories in Gradle

To configure a mirror, follow the
[Declaring Repositories](https://docs.gradle.org/current/userguide/declaring_repositories.html)
instructions in the Gradle project documentation.

Example `build.gradle` entry:

```
repositories {
      maven {
          url "https://maven-central.storage-download.googleapis.com/maven2/"
      }
  }
```

   Was this helpful?

---

# Building a Node.js applicationStay organized with collectionsSave and categorize content based on your preferences.

# Building a Node.js applicationStay organized with collectionsSave and categorize content based on your preferences.

## Specifying versions of Node.js

The buildpacks project provides support for the Current and Active LTS releases of Node.js. Older releases of Node.js are available but may not be actively maintained by the project.

### Usingpackage.json

You can specify the Node.js version of your application during deployment by configuring the `engines.node` field in `package.json`. To configure the buildpack to use the latest version of Node.js v16 when deploying your app, you can use the following values in your `package.json`:

```
"engines": {
  "node": "16.x.x"
}
```

### UsingGOOGLE_NODEJS_VERSION

It is also possible to specify the Node.js version via the `GOOGLE_NODEJS_VERSION` environment variable.
If both configurations are set, the `GOOGLE_NODEJS_VERSION` value takes precedence
over the `engines.node` property. If no value is provided, then the most recent LTS version of Node.js is used

To configure the buildpack to use Node.js 16 when deploying your app:

```
pack build --builder=gcr.io/buildpacks/builder \
   sample-functions-framework-node \
   --env GOOGLE_NODEJS_VERSION=16.x.x
```

You can also use a `project.toml` project descriptor to encode
the environment variable alongside your project files. See instructions on
[building the application with environment variables](https://docs.cloud.google.com/docs/buildpacks/set-environment-variables#build_the_application_with_environment_variables)).

### Tips

- `engines.node` field can take a semver constraint. The specific library we use for the Node.js buildpacks is [Masterminds/semver](https://github.com/Masterminds/semver)
- Avoid using greater than (>) specifiers in `engines.node`
- When deploying the application into App Engine standard environment, the `engines.node` property should be compatible with the runtime specified in `app.yaml`
- Additional documentation about the `engines.node` configuration option in `package.json` can be found in the official NPM documentation under the [engines topic](https://docs.npmjs.com/cli/v8/configuring-npm/package-json)
- When deploying a function onto Cloud Run functions, the `engines.node` property should be compatible with the runtime used to deploy your function

## Installing dependencies

### Using NPM

- NPM is the default package manager.
- Whenever possible, use `package-lock.json` to improve cache performance.
- By default only production dependencies are installed.
- You can specify the npm version section using the `engines.npm` field in your
  `package.json` file.

### Using Yarn

- Yarn is used instead when you include the `yarn.lock` file in your project.
- You can specify the yarn version to use in the `engines.yarn` field of your
  `package.json` file.
- We support Yarn2 PnP mode if your project includes a `.yarn/cache`.

### Using Pnpm

- Pnpm is used instead when you include the `pnpm-lock.yaml` file in your
  project.
- You can specify a version of pnpm in the `engines.pnpm` field of your
  `package.json` file.
- For a working example, see the
  [sample-node-pnpm](https://github.com/GoogleCloudPlatform/buildpack-samples/tree/master/sample-node-pnpm)
  app.

## Using private modules

You can use a [private npm module](https://docs.npmjs.com/private-modules/intro) by providing settings for authenticating with
the registry in a `.npmrc` file in the function's directory. If you're using
Yarn version 2 or later as your package manager, this file is named
`.yarnrc.yml`.

### Private modules from Artifact Registry

An [Artifact Registry Node.js package repository](https://cloud.google.com/artifact-registry/docs/nodejs/quickstart)
can host private modules for your function. When you deploy a Buildpacks
function, the build process automatically generates Artifact Registry credentials
for the [Cloud Build service account](https://cloud.google.com/build/docs/cloud-build-service-account).
You only need to list the Artifact Registry repository in your `.npmrc` file
when using NPM or Yarn version 1. For example, when using NPM or Yarn version 1:

```
@SCOPE:registry=https://REGION_ID-npm.pkg.dev/PROJECT_ID/REPOSITORY_NAME
//REGION_ID-npm.pkg.dev/PROJECT_ID/REPOSITORY_NAME:always-auth=true
```

If you're using Yarn version 2 or later, you only need to list the Artifact Registry
repository in your `.yarnrc.yml` file without additional credentials.
For example:

```
npmScopes:
  SCOPE:
    npmRegistryServer: https://REGION_ID-npm.pkg.dev/PROJECT_ID/REPOSITORY_NAME
    npmAlwaysAuth: true
```

### Private modules from other repositories

The [npm documentation](https://docs.npmjs.com/getting-started/working_with_tokens) explains how to create custom read-only
access tokens. We discourage using the `.npmrc` file created in the home
directory because it contains a read-write token. Write permissions are not
required during deployment, and could pose a security risk.

Do not include the `.npmrc` file if you're not using private repositories,
as it can increase the deployment time for your functions.

#### File format

If you're using an `.npmrc` file to set a custom auth token, it should include
the line shown below.

```
//REGISTRY_DOMAIN/:_authToken=AUTH_TOKEN
```

Replace:

- REGISTRY_DOMAIN: the domain name of your private
  npm registry. For example if your repository host is `npmjs.org`, set this field
  to `registry.npmjs.org`.
- AUTH_TOKEN: the authorization token for your npm registry.
  This can either be the literal text value of the token or the text string
  `${NPM_TOKEN}`, which the `npm` command replaces with the actual token value from the
  environment.
  You can set the `$NPM_TOKEN` environment variable with the
  [--set-build-env-vars](https://cloud.google.com/functions/docs/configuring/env-var#using_build_environment_variables)
  argument to your
  [gcloud functions deploy](https://cloud.google.com/sdk/gcloud/reference/functions/deploy) command.
  See the [NPM tutorial on private modules](https://docs.npmjs.com/using-private-packages-in-a-ci-cd-workflow#create-and-check-in-a-project-specific-npmrc-file)
  for more details of the NPM auth token.

## Executing custom build steps during deployment

By default, `npm run build` is run if a script is specified in your
`package.json` file. However, you can instead specify custom build steps to
override the default behavior and run only the scripts that you want
during the build. You can control the build steps by using either the
`GOOGLE_NODE_RUN_SCRIPTS` environment variable or `gcp-build` in your
`package.json` file.

You can only use one method. Note that the `GOOGLE_NODE_RUN_SCRIPTS`
environment variable takes precedence and overrides anything that is specified
for `gcp-build` in your `package.json`.

By default, when you configure custom build steps, both the `dependencies` and
`devDependencies` in your `package.json` file are installed first
before any scripts or commands are executed. To override the default behavior,
you can use the [NODE_ENV](#node_env) environment variable.

### UsingGOOGLE_NODE_RUN_SCRIPTS

You can pass the `GOOGLE_NODE_RUN_SCRIPTS` environment variable to the build to
control what scripts run. You can specify one or more scripts, or instead
pass an empty environment variable to prevent the default behavior from
running, like `GOOGLE_NODE_RUN_SCRIPTS=`. For complete details, see
[Environment variables](#google_node_run_scripts).

### Usingpackage.json

Adding `gcp-build` in your `package.json` file only runs
`npm run gcp-build`, meaning that it overrides the default
behavior. You can specify one or more commands, or instead specify an
empty string to prevent any command from running, like `"gcp-build":""`.

```
"scripts": {
  ...
  "gcp-build": "npm run lint && npm run build"
  ...
}
```

## Application entrypoint

The Node.js buildpack will execute the command specified in the `scripts.start` field of your `package.json`.
If `scripts.start` is not set, the buildpack will run `npm start`.

We recommend using a Procfile because it takes `npm` or `yarn` out of the path.

## Environment variables

You can [set environment variables to configure builds](https://cloud.google.com/docs/buildpacks/set-environment-variables) of your container image.

The Node.js buildpack supports the following environment
variables to customize your container.

### NPM_CONFIG_<key>

See [documentation](https://docs.npmjs.com/misc/config#environment-variables).

**Example:** `NPM_CONFIG_FLAG=value` passes `-flag=value` to `npm` commands.

### NODE_ENV

Specifies the development environment during the build; set for `npm install`.

**Example:** `NODE_ENV=development` installs both the `dependencies` and `devDependencies` specified in `package.json`.

### GOOGLE_NODE_RUN_SCRIPTS

Specifies an ordered list of npm scripts from `package.json` to run after
installing dependencies. The list must be comma-separated and runs in the order
that you list each script.

When you specify `GOOGLE_NODE_RUN_SCRIPTS`, only the scripts that you list are
run. For example, if you want to prevent the default `npm run build` from
running, you specify the environment variable without a value.

**Examples:**

- `GOOGLE_NODE_RUN_SCRIPTS=lint,build` runs `npm run lint` and then `npm run build`.
- `GOOGLE_NODE_RUN_SCRIPTS=` runs no scripts.

---

# Configure the OS only runtimeStay organized with collectionsSave and categorize content based on your preferences.

> Configure the OS only runtime

# Configure the OS only runtimeStay organized with collectionsSave and categorize content based on your preferences.

The OS only runtime is a language-independent, general-purpose runtime for
Cloud Run [source](https://cloud.google.com/run/docs/deploying-source-code) deployments. It
includes the base Ubuntu operating system (OS) without any additional
language-specific runtime components. The OS only runtime lets you deploy Go
applications from source, and binaries such as Dart and Go. You can also deploy
your own application images that you built from scratch using this runtime.

The OS only runtime is compatible with [automatic base image
updates](https://cloud.google.com/run/docs/configuring/services/automatic-base-image-updates) for
Cloud Run. This means your application automatically receives operating
system-level security patches and updates, even when you don't use a specific
[supported language runtime](https://cloud.google.com/run/docs/runtime-support#support_schedule).

## Supported stack

The OS only runtime is available on the
[google-24](http://us-central1-docker.pkg.dev/serverless-runtimes/google-24-full/run%2Funiversal)
stack. For more information about the available OS only runtime versions, and the
support schedule, see the [Runtime lifecycle](https://cloud.google.com/docs/buildpacks/runtime-support#os-only).

## Compiled binaries

The OS only runtime lets you deploy pre-compiled binaries. You
can also target a base image using a runtime alias. For example, to use the
[google-24/osonly24](http://us-central1-docker.pkg.dev/serverless-runtimes/google-24/runtimes/osonly24) base image, specify the alias, `osonly24`.

For compiled languages, make sure you build the binary targeting a Linux OS
before you deploy.
For example, to compile a Go application targeting `linux/amd64`, run the
following command:

```
GOOS="linux" GOARCH=amd64 go build main.go
```

## Deploy to Cloud Run

Deploy your service from source to Cloud Run using the [gcloud beta
run deploy](https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy) command. Specify the
base image (for example, `osonly24`) using any of the following deployment methods:

To deploy a Go application from source with build to Cloud Run, run the following command:

```
gcloud beta run deploy SERVICE \
--source . \
--base-image=osonly24 \
--project PROJECT_ID \
--automatic-updates
```

Replace the following:

- SERVICE: the name of your Cloud Run service.
- PROJECT_ID: the Google Cloud project ID.

For more information on deploying from source with build, see [Deploy services from source code](https://cloud.google.com/run/docs/deploying-source-code#deploy-from-source).

To deploy from source to Cloud Run without using build, run the
following command:

```
gcloud beta run deploy SERVICE \
--source . \
--no-build \
--base-image=osonly24 \
--project PROJECT_ID \
--command COMMAND
```

Replace the following:

- SERVICE: the name of your Cloud Run service.
- PROJECT_ID: the Google Cloud project ID.
- COMMAND: the command that the container starts up with, for example,
  `./main`.

For more information on deploying from source without build, see [Deploy services from source code](https://cloud.google.com/run/docs/deploying-source-code#deploy_from_source_without_build).

---

# Google Cloud's buildpacksStay organized with collectionsSave and categorize content based on your preferences.

# Google Cloud's buildpacksStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud's buildpacks is an
[open-source project](https://github.com/GoogleCloudPlatform/buildpacks)
that takes your application source code and transforms it into production-ready
container images. The buildpacks published by Google Cloud implement
the
[Cloud Native Buildpack specification](https://buildpacks.io/)
and are designed to help you build and configure containers that you can
deploy to Google Cloud.

A buildpack is typically responsible for a language
component, toolchain, or app component; such as Python, `pip`, or a web server.
Buildpacks are grouped together into collections called
[builders](https://cloud.google.com/docs/buildpacks/builders) that can analyze project source code,
create a build plan, and generate a container image that is ready for deployment.

## Containerization with buildpacks

When you deploy to and serve your application (service) or function on the
[Google Cloud Serverless](https://cloud.google.com/serverless) products,
your code gets packaged into a runnable container using buildpacks.
On Cloud Run, you have the option to deploy a pre-built container or
[deploy your source code](https://cloud.google.com/run/docs/deploying-source-code)
to let Cloud Run manage the container build. On Cloud Run functions and
App Engine, the containerization process is fully-managed, meaning that when
you deploy your source code, all the container image packaging and converting
is done for you.

Each container image gets built with all the components needed for running your
deployment, including source code, system and library dependencies, configuration
data, and static assets. By default, the Google Cloud Serverless products
use the same underlying services, including Cloud Build for the deployment
pipeline, and either Container Registry or Artifact Registry for container image storage
and management.

When using Google Cloud's buildpacks:

- Builders and buildpacks are pre-configured to handle the build process
  and create a runnable container image for you.
- Buildpacks support
  [multiple programming languages](https://cloud.google.com/docs/buildpacks/builders) and automatically
  detects which lanaguage is used in your source code.
- You can
  [customize and extend buildpacks](https://cloud.google.com/docs/buildpacks/build-run-image)
  to install additional system dependencies. However, the default builder can
  handle the common tasks required by your programming language,
  including installing dependencies from the language's package repository
  and using the language's common dependency file.

## Use buildpacks to containerize your code

Buildpacks can be used locally or remotely to:

- [Build an application or service](https://cloud.google.com/docs/buildpacks/build-application)
- [Build a function](https://cloud.google.com/docs/buildpacks/build-function)

For programming languages that exclude a standard ways to start an application,
you can use a `Procfile` to define the process to invoke when a container starts.
A `Procfile` can be used to override the default start process for any
buildpacks type, but is mandatory for some, including
[Python](https://cloud.google.com/docs/buildpacks/python#application_entrypoint).

## What's next

- [Builders](https://cloud.google.com/docs/buildpacks/builders)
- [Build an application](https://cloud.google.com/docs/buildpacks/build-application)
- [Build a function](https://cloud.google.com/docs/buildpacks/build-function)
- Learn about
  [Cloud Native Buildpacks](https://buildpacks.io/docs/for-platform-operators/concepts/)

   Was this helpful?

---

# Building a PHP applicationStay organized with collectionsSave and categorize content based on your preferences.

# Building a PHP applicationStay organized with collectionsSave and categorize content based on your preferences.

## Specify the PHP version

By default the PHP Runtime buildpack uses the latest stable version of PHP. If
your application requires a specific version, you can specify one by including
a `composer.json` file in your application's root directory. For example:

 See more code actions.  ?lit$725890247$ ?lit$725890247$   ?lit$725890247$Light code theme  ?lit$725890247$   ?lit$725890247$Dark code theme  ?lit$725890247$

```
"require": {
  "php": "8.3.*",
}
```

## Configure Composer

By default, the Composer version is `2.1.3`. If you require a specific
version of Composer, you can use the `GOOGLE_COMPOSER_VERSION` environment
variable to specify any supported version of Composer using the full
semantic version. For example:

```
pack build sample-php --builder=gcr.io/buildpacks/builder \
  --env GOOGLE_COMPOSER_VERSION="2.2.20"
```

## Customizing NGINX configurations

To configure NGINX, you can use the `GOOGLE_CUSTOM_NGINX_CONFIG` environment
variable to specify your custom NGINX configuration file. For example:

```
pack build sample-php --builder=gcr.io/buildpacks/builder \
  --env GOOGLE_CUSTOM_NGINX_CONFIG="nginx-custom.conf"
```

When NGINX starts, your custom NGINX file is used.

   Was this helpful?

---

# Build a Python applicationStay organized with collectionsSave and categorize content based on your preferences.

> Build a Python application

# Build a Python applicationStay organized with collectionsSave and categorize content based on your preferences.

Buildpacks support language-idiomatic configuration through environment
variables.

## Specify the Python version

By default the Python Runtime buildpack uses the latest stable version of the Python interpreter. If your application requires a specific version, you can specify one by including a `.python-version` file in your application's root directory.

 See more code actions.  ?lit$783119286$ ?lit$783119286$   ?lit$783119286$Light code theme  ?lit$783119286$   ?lit$783119286$Dark code theme  ?lit$783119286$

```
3.14
```

### UseGOOGLE_PYTHON_VERSION

It is also possible to specify the Python version using the
`GOOGLE_PYTHON_VERSION` environment variable.
If both configurations are set, the `GOOGLE_PYTHON_VERSION` value takes
precedence over the `.python-version` file. By default, when both the
`.python-version` file and `GOOGLE_PYTHON_VERSION` environment variable are not
specified, then the latest LTS version of Python is used.

To configure the buildpack to use a [supported Python version](https://cloud.google.com/docs/buildpacks/runtime-support#python) when deploying your app:

```
pack build sample-python --builder=gcr.io/buildpacks/builder \
  --env GOOGLE_PYTHON_VERSION="3.14.x"
```

You can also use a `project.toml` project descriptor to encode
the environment variable alongside your project files. See instructions on
[building the application with environment variables](https://docs.cloud.google.com/docs/buildpacks/set-environment-variables#build_the_application_with_environment_variables)).

## Specify dependencies

Specify your application dependencies for [supported Python versions](https://cloud.google.com/docs/buildpacks/runtime-support#python) using any of the following approaches:

- Use a `requirements.txt` file in the root directory. This file must be in
  the same directory as the `main.py` file that contains your source code. The
  `requirements.txt` file contains one line per package. Each line contains
  the package name, and optionally, the requested version. To prevent your
  build from being affected by dependency version changes, consider pinning
  your dependency packages to a specific version.
  The following is an example `requirements.txt` file:
  ```
  functions-framework
  requests==2.20.0
  numpy
  ```
- Use a `pyproject.toml` file to specify dependencies. If you manage your
  application dependencies in a `pyproject.toml` file instead of the
  `requirements.txt` file, the Python buildpack determines
  the package manager based on the configuration you specify in the
  `pyproject.toml` file. For more information, see [Deploy Python applications
  with apyproject.tomlfile](https://cloud.google.com/docs/buildpacks/python#deploy-with-toml).
  If your application uses both the `pyproject.toml` file and the
  `requirements.txt` file, the `requirements.txt` file takes precedence.
  - The following is an example `pyproject.toml` file:
    ```
    [project]
    name = "demo-app"
    version = "0.1.0"
    description = ""
    requires-python = ">=3.10"
    dependencies = [
        "flask>=3.1.1",
        "gunicorn>=23.0.0",
    ]
    [build-system]
    requires = ["setuptools>=61.0"]
    build-backend = "setuptools.build_meta"
    ```

## Package manager

If you manage your dependencies using a `requirements.txt file`, the default package
manager varies based on the Python version you configure.

If you use a `pyproject.toml` file to manage dependencies instead of a
`requirements.txt` file, the Python buildpack determines the
package manager based on your configuration settings in the `pyproject.toml`
file. The buildpack supports pip, uv and Poetry package
managers. For more information, see [Deploy Python applications with apyproject.tomlfile](https://cloud.google.com/docs/buildpacks/python#deploy-with-toml).

Starting from Python version 3.14 and later, the Python
buildpack uses the [uv](https://docs.astral.sh/uv/)
package manager as the default installer for the dependencies you specify
in your `requirements.txt` file.

To use [pip](http://pip.readthedocs.org/) as the package manager,
configure the environment variable `GOOGLE_PYTHON_PACKAGE_MANAGER="pip"`.

For Python version 3.13 and earlier, the Python
buildpack uses the [pip](http://pip.readthedocs.org/)
package manager to install dependencies you define in the
[requirements.txt](http://pip.readthedocs.org/en/stable/user_guide/#requirements-files)
file.

To use [uv](https://docs.astral.sh/uv/) as the package manager,
configure the environment variable `GOOGLE_PYTHON_PACKAGE_MANAGER="uv"`.

### Configure pip

It is possible to configure the behavior of pip [using environment variables](https://pip.pypa.io/en/stable/topics/configuration/):

```
pack build sample-python --builder=gcr.io/buildpacks/builder \
  --env PIP_DEFAULT_TIMEOUT='60'
```

### Private dependencies from Artifact Registry

An [Artifact Registry Python repository](https://cloud.google.com/artifact-registry/docs/python/store-python)
can host private dependencies for your Python function. When building an application on
Cloud Build, the Python buildpack will automatically generate Artifact Registry
credentials for the [Cloud Build service account](https://cloud.google.com/build/docs/cloud-build-service-account).
You only need to include the Artifact Registry URL in your `requirements.txt`
without generating additional credentials. For example:

```
--extra-index-url REPOSITORY_URL
sampleapp
Flask==0.10.1
google-cloud-storage
```

## Application entrypoint

The following section describes the default entrypoint for the Python buildpack.

### Entrypoint for Cloud Run source deploys

This feature is only available if you [deploy your source code](https://cloud.google.com/run/docs/deploying-source-code) to Cloud Run with the Python runtime. This feature
isn't applicable if you are building your container image directly using
`pack build` outside of the Cloud Run source deploy process.

The [Python buildpack](https://cloud.google.com/docs/buildpacks/python) supports
modern web frameworks such as [FastAPI](https://fastapi.tiangolo.com/), [Gradio](https://www.gradio.app/), [Streamlit](https://streamlit.io/), and [Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

#### Python version 3.12 and earlier

If you're using Python version 3.12 and earlier, the Python
buildpack defaults to using [Gunicorn](https://gunicorn.org/)
as the WSGI HTTP server for your workload. The Python buildpack sets the default entrypoint to `gunicorn -b :8080 main:app`.

#### Python version 3.13 and later

For Python version 3.13 and later, the Python buildpack
sets the default entrypoint for [Cloud Run source deploys](https://cloud.google.com/run/docs/deploying-source-code) based on the web server or framework configuration in your
`requirements.txt` file. This default setting applies only to Cloud Run
service source deployments, not to Cloud Run functions.

When you deploy a Cloud Run service from source using the Python runtime,
the buildpack determines the Python version and the default
entrypoint in the following ways:

- If you don't specify a Python version in your source files,
  the Python buildpack sets the default to the [latest supported Python version](https://cloud.google.com/docs/buildpacks/runtime-support#python). The buildpack determines the default entrypoint based on the web server or framework you've
  [configured in yourrequirements.txtfile](#default-entrypoint).
- If you don't specify a web server or a framework in your `requirements.txt` file, the Python buildpack defaults to using Gunicorn as the WSGI HTTP server for your workload. The Python buildpack sets the default entrypoint to `gunicorn -b :8080 main:app`.
- The Python buildpack sets the default entrypoint
  based on the following order of precedence, as defined in the `requirements.txt`
  file:
  1. `gunicorn`
  2. `uvicorn`
  3. `fastapi[standard]`
  4. `gradio`
  5. `streamlit`
  6. `google-adk`

#### Configure the web server or framework

For each common Python configurations in the `requirements.txt` file, the following table shows the default entrypoints when deploying to Cloud Run from source:

| Primary configuration | Default entrypoint | Environment variables |
| --- | --- | --- |
| gunicorn | gunicorn -b :8080 main:app |  |
| numpy | gunicorn -b :8080 main:app |  |
| fastapiuvicorn | uvicorn main:app --host 0.0.0.0 --port 8080 |  |
| fastapi[standard] | uvicorn main:app --host 0.0.0.0 --port 8080 |  |
| uvicorngunicorn | gunicorn -b :8080 main:app |  |
| gradio | python main.py | GRADIO_SERVER_NAME=0.0.0.0GRADIO_SERVER_PORT=8080 |
| streamlit | streamlit run main.py --server.address 0.0.0.0 --server.port 8080 |  |
| google-adk | adk api_server --host 0.0.0.0 --port 8080 |  |

To avoid deployment failures, use a [supported Python
version](https://cloud.google.com/docs/buildpacks/runtime-support#python) in your source files, and
specify a web server in your `requirements.txt` file.

Alternatively, you can also specify the entrypoint by running the following source deploy command:

```
gcloud run deploy SERVICE --source .  --set-build-env-vars GOOGLE_ENTRYPOINT="ENTRYPOINT"
```

Replace the following:

- SERVICE: the name of the service you want to
  deploy to.
- ENTRYPOINT: the default entrypoint you want to use for your source
  code.

If you're unable to deploy your source code to Cloud Run or find errors
in the logs, see the [Cloud Run troubleshooting guide](https://cloud.google.com/run/docs/troubleshooting#source-deploy-errors).

### Entrypoint for all other deployments

The Python buildpack uses [Gunicorn](https://gunicorn.org/)
as the default WSGI HTTP server for your workload. Apps built with the Python
buildpack start the `gunicorn` process with default settings,
similar to running:

```
gunicorn --bind :8080 main:app
```

### Customize the application entrypoint

You can customize the applications start command by using a `Procfile` or an environment variable. You might need to do this to customize the [default entrypoint configurations](https://cloud.google.com/docs/buildpacks/python#default-entrypoint).

You can create a `Procfile` with your custom settings in the root directory.
Example:

```
web: gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

Alternatively, you can use the `GOOGLE_ENTRYPOINT` environment variable with
the `pack` command. Example:

```
pack build sample-python \
  --builder gcr.io/buildpacks/builder
  --env "GOOGLE_ENTRYPOINT='gunicorn --bind :$PORT main:app'"
```

## Environment Variables

The Python buildpack supports the following environment variables to customize your container

### PIP_<key>

See pip [documentation](https://pip.pypa.io/en/stable/user_guide/#environment-variables).

**Example:** `PIP_DEFAULT_TIMEOUT=60` sets `--default-timeout=60` for `pip` commands.

## Deploy Python applications with apyproject.tomlfile

Python buildpacks support projects you configure
with the `pyproject.toml` file. This feature lets you deploy
applications you manage with Poetry, uv, or pip, directly to Cloud Run
and Cloud Run functions. This feature isn't available in App Engine.

The Python buildpack uses the `pyproject.toml` file only
when there isn't a `requirements.txt` file present in your root directory. If your application uses both
the `pyproject.toml` file and the `requirements.txt` file, then the `requirements.txt` file
takes precedence.

### Supported buildpacks configurations

Python buildpacks supports the following configurations:

- **pip buildpack**: Installs dependencies directly from
  `pyproject.toml` if it detects all the following conditions:
  - A `pyproject.toml` file is present in the root directory and you don't
    configure high-precedence tools such as a `poetry.lock` file, a `[tool.poetry]`
    section, or a `uv.lock` file.
  - You set the `GOOGLE_PYTHON_PACKAGE_MANAGER` environment variable to
    `pip`.
- **uv buildpack**: Supports Python projects you manage with
  [uv](https://docs.astral.sh/uv). This buildpack activates if it detects any
  of the following conditions:
  - A `uv.lock` file and a `pyproject.toml` file are present in the project
    root.
  - A `pyproject.toml` file is present in the project root, and you set the
    `GOOGLE_PYTHON_PACKAGE_MANAGER` environment variable to `uv`.
  - A `pyproject.toml` file is present and you don't include other high-precedence
    lock files such as `poetry.lock`, `uv.lock`, or configurations such as
    `[tool.poetry]`, and you don't set the
    `GOOGLE_PYTHON_PACKAGE_MANAGER` environment variable.
- **Poetry buildpack**: Supports Python projects you manage
  with [Poetry](https://python-poetry.org/). This
  buildpack activates if it detects any of the following
  conditions:
  - A `poetry.lock` file and a `pyproject.toml` file are present in the
    project root.
  - A `pyproject.toml` file is present in the project root and a
    `[tool.poetry]` section is present in the `pyproject.toml` file.

### Package manager precedence

The Python buildpacks determines the default package manager based on the
configuration in the following order of precedence:

1. The highest precedence is given to the `requirements.txt` file. Only if this
  file is present, the Python buildpack uses the [default package
  manager](#package-manager) to install dependencies at the build step. If
  a `requirements.txt` file isn't present, the detection process moves on to the next step.
2. The buildpack then checks the `pyproject.toml` file for
  a `poetry.lock` file or a `[tool.poetry]` section. If found, the build process proceeds to use
  Poetry to install dependencies.
3. If Poetry configuration isn't detected, the buildpack checks for a
  `uv.lock` file. If found, the build process proceeds to use uv to install dependencies.
4. If lock files aren't present, the buildpack checks the
  `GOOGLE_PYTHON_PACKAGE_MANAGER` environment variable for a `pip` or `uv`
  configuration.
5. Default. If you don't set an environment variable, and use only a `pyproject.toml`
  file without uv or Poetry, the buildpack defaults to using
  uv for all [supported Python versions](https://cloud.google.com/docs/buildpacks/runtime-support#python).

### Entrypoint with apyproject.tomlfile

When you deploy an application with a `pyproject.toml` file instead of using a
`requirements.txt` file, the Python buildpack uses a different
method to determine the entrypoint. For information about configuring an
application entrypoint with a `requirements.txt` file, see [Application entrypoint](#entrypoint).

The buildpack searches for an entrypoint in the following order of precedence:

1. If a `Procfile` exists in your root directory, or you configure the
  `GOOGLE_ENTRYPOINT` environment variable, these configurations always
  override any entrypoint determined by `pyproject.toml` scripts.
2. The Python buildpack utilizes the custom scripts you configure in
  the `[tool.poetry.scripts]` and the `[project.scripts]` sections. If you configure a [script](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#creating-executable-scripts) that includes `start`, this is your entrypoint.
  For example, `poetry run start` or `uv run start`.
3. If you don't configure a `start` script, but you define another script,
  the script you define is the default entrypoint. For example, `poetry run mycmd`
  or `uv run mycmd`.

Unlike `requirements.txt`-based builds, the Python buildpack
doesn't automatically install `gunicorn` for `pyproject.toml` projects. To use
`gunicorn` or any other server, you must explicitly add it to the dependencies in your `pyproject.toml` file.

If you don't configure [custom
scripts](https://github.com/GoogleCloudPlatform/buildpacks/tree/main/builders/testdata/python/generic/pyproject_script) in the `pyproject.toml` file, the buildpacks attempts
to detect common frameworks, such as `gunicorn`, `uvicorn` or `fastapi` from your
`pyproject.toml` dependencies and [determines a default entrypoint](#entrypoint).

   Was this helpful?
