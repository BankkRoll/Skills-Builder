# Share your extension and more

# Share your extension

> Share your extension with a share link

# Share your extension

   Table of contents

---

Once your extension image is accessible on Docker Hub, anyone with access to the image can install the extension.

People can install your extension by typing `docker extension install my/awesome-extension:latest` in to the terminal.

However, this option doesn't provide a preview of the extension before it's installed.

## Create a share URL

Docker lets you share your extensions using a URL.

When people navigate to this URL, it opens Docker Desktop and displays a preview of your extension in the same way as an extension in the Marketplace. From the preview, users can then select **Install**.

![Navigate to extension link](https://docs.docker.com/extensions/extensions-sdk/extensions/images/open-share.png)  ![Navigate to extension link](https://docs.docker.com/extensions/extensions-sdk/extensions/images/open-share.png)

To generate this link you can either:

- Run the following command:
  ```console
  $ docker extension share my/awesome-extension:0.0.1
  ```
- Once you have installed your extension locally, navigate to the **Manage** tab and select **Share**.
  ![Share button](https://docs.docker.com/extensions/extensions-sdk/extensions/images/list-preview.png)  ![Share button](https://docs.docker.com/extensions/extensions-sdk/extensions/images/list-preview.png)

> Note
>
> Previews of the extension description or screenshots, for example, are created using [extension labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/).

---

# Validate your extension

> Step three in the extension creation process

# Validate your extension

---

Validate your extension before you share or publish it. Validating the extension ensures that the extension:

- Is built with the [image labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/) it requires to display correctly in the marketplace
- Installs and runs without problems

The Extensions CLI lets you validate your extension before installing and running it locally.

The validation checks if the extension’s `Dockerfile` specifies all the required labels and if the metadata file is valid against the JSON schema file.

To validate, run:

```console
$ docker extension validate <name-of-your-extension>
```

If your extension is valid, the following message displays:

```console
The extension image "name-of-your-extension" is valid
```

Before the image is built, it's also possible to validate only the `metadata.json` file:

```console
$ docker extension validate /path/to/metadata.json
```

The JSON schema used to validate the `metadata.json` file against can be found under the [releases page](https://github.com/docker/extensions-sdk/releases/latest).

---

# Part two: Publish

> General steps in how to publish an extension

# Part two: Publish

   Table of contents

---

This section describes how to make your extension available and more visible, so users can discover it and install it with a single click.

## Release your extension

After you have developed your extension and tested it locally, you are ready to release the extension and make it available for others to install and use (either internally with your team, or more publicly).

Releasing your extension consists of:

- Providing information about your extension: description, screenshots, etc. so users can decide to install your extension
- [Validating](https://docs.docker.com/extensions/extensions-sdk/extensions/validate/) that the extension is built in the right format and includes the required information
- Making the extension image available on [Docker Hub](https://hub.docker.com/)

See [Package and release your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/) for more details about the release process.

## Promote your extension

Once your extension is available on Docker Hub, users who have access to the extension image can install it using the Docker CLI.

### Use a share extension link

You can also [generate a share URL](https://docs.docker.com/extensions/extensions-sdk/extensions/share/) in order to share your extension within your team, or promote your extension on the internet. The share link lets users view the extension description and screenshots.

### Publish your extension in the Marketplace

You can publish your extension in the Extensions Marketplace to make it more discoverable. You must [submit your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/publish/) if you want to have it published in the Marketplace.

## What happens next

### New releases

Once you have released your extension, you can push a new release just by pushing a new version of the extension image, with an incremented tag (still using `semver` conventions).
Extensions published in the Marketplace benefit from update notifications to all Desktop users that have installed the extension. For more details, see [new releases and updates](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/#new-releases-and-updates).

### Extension support and user feedback

In addition to providing a description of your extension's features and screenshots, you should also specify additional URLs using [extension labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/). This direct users to your website for reporting bugs and feedback, and accessing documentation and support.

> Already built an extension?
>
>
>
> Let us know about your experience using the [feedback form](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form).

---

# Invoke host binaries

> Add invocations to host binaries from the frontend with the extension SDK.

# Invoke host binaries

   Table of contents

---

In some cases, your extension may need to invoke some command from the host. For example, you
might want to invoke the CLI of your cloud provider to create a new resource, or the CLI of a tool your extension
provides, or even a shell script that you want to run on the host.

You could do that by executing the CLI from a container with the extension SDK. But this CLI needs to access the host's filesystem, which isn't easy nor fast if it runs in a container.

This page describes how to run executables on the host (binaries, shell scripts) that are shipped as part of your extension and deployed to the host. As extensions can run on multiple platforms, this
means that you need to ship the executables for all the platforms you want to support.

Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).

> Note
>
> Note that extensions run with user access rights, this API is not restricted to binaries listed in the [host section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) of the extension metadata (some extensions might install software during user interaction, and invoke newly installed binaries even if not listed in the extension metadata).

In this example, the CLI is a simple `Hello world` script that must be invoked with a parameter and returns a
string.

## Add the executables to the extension

Create a `bash` script for macOS and Linux, in the file `binaries/unix/hello.sh` with the following content:

```bash
#!/bin/sh
echo "Hello, $1!"
```

Create a `batch script` for Windows in another file `binaries/windows/hello.cmd` with the following content:

```bash
@echo off
echo "Hello, %1!"
```

Then update the `Dockerfile` to copy the `binaries` folder into the extension's container filesystem and make the
files executable.

```dockerfile
# Copy the binaries into the right folder
COPY --chmod=0755 binaries/windows/hello.cmd /windows/hello.cmd
COPY --chmod=0755 binaries/unix/hello.sh /linux/hello.sh
COPY --chmod=0755 binaries/unix/hello.sh /darwin/hello.sh
```

## Invoke the executable from the UI

In your extension, use the Docker Desktop Client object to [invoke the shell script](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/#invoke-an-extension-binary-on-the-host)
provided by the extension with the `ddClient.extension.host.cli.exec()` function.
In this example, the binary returns a string as result, obtained by `result?.stdout`, as soon as the extension view is rendered.

```typescript
export function App() {
  const ddClient = createDockerDesktopClient();
  const [hello, setHello] = useState("");

  useEffect(() => {
    const run = async () => {
      let binary = "hello.sh";
      if (ddClient.host.platform === 'win32') {
        binary = "hello.cmd";
      }

      const result = await ddClient.extension.host?.cli.exec(binary, ["world"]);
      setHello(result?.stdout);

    };
    run();
  }, [ddClient]);

  return (
    <div>
      {hello}
    </div>
  );
}
```

> Important
>
> We don't have an example for Vue yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> and let us know if you'd like a sample with Vue.

> Important
>
> We don't have an example for Angular yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> and let us know if you'd like a sample with Angular.

> Important
>
> We don't have an example for Svelte yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> and let us know if you'd like a sample with Svelte.

## Configure the metadata file

The host binaries must be specified in the `metadata.json` file so that Docker Desktop copies them on to the host when installing
the extension. Once the extension is uninstalled, the binaries that were copied are removed as well.

```json
{
  "vm": {
    ...
  },
  "ui": {
    ...
  },
  "host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/hello.sh"
          }
        ],
        "linux": [
          {
            "path": "/linux/hello.sh"
          }
        ],
        "windows": [
          {
            "path": "/windows/hello.cmd"
          }
        ]
      }
    ]
  }
}
```

The `path` must reference the path of the binary inside the container.

---

# Interacting with Kubernetes from an extension

> How to connect to a Kubernetes cluster from an extension

# Interacting with Kubernetes from an extension

   Table of contents

---

The Extensions SDK does not provide any API methods to directly interact with the Docker Desktop managed Kubernetes cluster or any other created using other tools such as KinD. However, this page provides a way for you to use other SDK APIs to interact indirectly with a Kubernetes cluster from your extension.

To request an API that directly interacts with Docker Desktop-managed Kubernetes, you can upvote [this issue](https://github.com/docker/extensions-sdk/issues/181) in the Extensions SDK GitHub repository.

## Prerequisites

### Turn on Kubernetes

You can use the built-in Kubernetes in Docker Desktop to start a Kubernetes single-node cluster.
A `kubeconfig` file is used to configure access to Kubernetes when used in conjunction with the `kubectl` command-line tool, or other clients.
Docker Desktop conveniently provides the user with a local preconfigured `kubeconfig` file and `kubectl` command within the user’s home area. It is a convenient way to fast-tracking access for those looking to leverage Kubernetes from Docker Desktop.

## Ship thekubectlas part of the extension

If your extension needs to interact with Kubernetes clusters, it is recommended that you include the `kubectl` command line tool as part of your extension. By doing this, users who install your extension get `kubectl` installed on their host.

To find out how to ship the `kubectl` command line tool for multiple platforms as part of your Docker Extension image, see [Build multi-arch extensions](https://docs.docker.com/extensions/extensions-sdk/extensions/multi-arch/#adding-multi-arch-binaries).

## Examples

The following code snippets have been put together in the [Kubernetes Sample Extension](https://github.com/docker/extensions-sdk/tree/main/samples/kubernetes-sample-extension). It shows how to interact with a Kubernetes cluster by shipping the `kubectl` command-line tool.

### Check the Kubernetes API server is reachable

Once the `kubectl` command-line tool is added to the extension image in the `Dockerfile`, and defined in the `metadata.json`, the Extensions framework deploys `kubectl` to the users' host when the extension is installed.

You can use the JS API `ddClient.extension.host?.cli.exec` to issue `kubectl` commands to, for instance, check whether the Kubernetes API server is reachable given a specific context:

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "cluster-info",
  "--request-timeout",
  "2s",
  "--context",
  "docker-desktop",
]);
```

### List Kubernetes contexts

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "config",
  "view",
  "-o",
  "jsonpath='{.contexts}'",
]);
```

### List Kubernetes namespaces

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "get",
  "namespaces",
  "--no-headers",
  "-o",
  'custom-columns=":metadata.name"',
  "--context",
  "docker-desktop",
]);
```

## Persisting the kubeconfig file

Below there are different ways to persist and read the `kubeconfig` file from the host filesystem. Users can add, edit, or remove Kubernetes context to the `kubeconfig` file at any time.

> Warning
>
>
>
> The `kubeconfig` file is very sensitive and if found can give an attacker administrative access to the Kubernetes Cluster.

### Extension's backend container

If you need your extension to persist the `kubeconfig` file after it's been read, you can have a backend container that exposes an HTTP POST endpoint to store the content of the file either in memory or somewhere within the container filesystem. This way, if the user navigates out of the extension to another part of Docker Desktop and then comes back, you don't need to read the `kubeconfig` file again.

```typescript
export const updateKubeconfig = async () => {
  const kubeConfig = await ddClient.extension.host?.cli.exec("kubectl", [
    "config",
    "view",
    "--raw",
    "--minify",
    "--context",
    "docker-desktop",
  ]);
  if (kubeConfig?.stderr) {
    console.log("error", kubeConfig?.stderr);
    return false;
  }

  // call backend container to store the kubeconfig retrieved into the container's memory or filesystem
  try {
    await ddClient.extension.vm?.service?.post("/store-kube-config", {
      data: kubeConfig?.stdout,
    });
  } catch (err) {
    console.log("error", JSON.stringify(err));
  }
};
```

### Docker volume

Volumes are the preferred mechanism for persisting data generated by and used by Docker containers. You can make use of them to persist the `kubeconfig` file.
By persisting the `kubeconfig` in a volume you won't need to read the `kubeconfig` file again when the extension pane closes. This makes it ideal for persisting data when navigating out of the extension to other parts of Docker Desktop.

```typescript
const kubeConfig = await ddClient.extension.host?.cli.exec("kubectl", [
  "config",
  "view",
  "--raw",
  "--minify",
  "--context",
  "docker-desktop",
]);
if (kubeConfig?.stderr) {
  console.log("error", kubeConfig?.stderr);
  return false;
}

await ddClient.docker.cli.exec("run", [
  "--rm",
  "-v",
  "my-vol:/tmp",
  "alpine",
  "/bin/sh",
  "-c",
  `"touch /tmp/.kube/config && echo '${kubeConfig?.stdout}' > /tmp/.kube/config"`,
]);
```

### Extension'slocalStorage

`localStorage` is one of the mechanisms of a browser's web storage. It allows users to save data as key-value pairs in the browser for later use.
`localStorage` does not clear data when the browser (the extension pane) closes. This makes it ideal for persisting data when navigating out of the extension to other parts of Docker Desktop.

```typescript
localStorage.setItem("kubeconfig", kubeConfig);
```

```typescript
localStorage.getItem("kubeconfig");
```

---

# Authentication

> Docker extension OAuth 2.0 flow

# Authentication

   Table of contents

---

> Note
>
> This page assumes that you already have an Identity Provider (IdP), such as Google, Entra ID (formerly Azure AD) or Okta, which handles the authentication process and returns an access token.

Learn how you can let users authenticate from your extension using OAuth 2.0 via a web browser, and return to your extension.

In OAuth 2.0, the term "grant type" refers to the way an application gets an access token. Although OAuth 2.0 defines several grant types, this page only describes how to authorize users from your extension using the Authorization Code grant type.

## Authorization code grant flow

The Authorization Code grant type is used by confidential and public clients to exchange an authorization code for an access token.

After the user returns to the client via the redirect URL, the application gets the authorization code from the URL and uses it to request an access token.

![Flow for OAuth 2.0](https://docs.docker.com/extensions/extensions-sdk/guides/images/oauth.png)  ![Flow for OAuth 2.0](https://docs.docker.com/extensions/extensions-sdk/guides/images/oauth.png)

The image above shows that:

- The Docker extension asks the user to authorize access to their data.
- If the user grants access, the extension then requests an access token from the service provider, passing the access grant from the user and authentication details to identify the client.
- The service provider then validates these details and returns an access token.
- The extension uses the access token to request the user data with the service provider.

### OAuth 2.0 terminology

- Auth URL: The endpoint for the API provider authorization server, to retrieve the auth code.
- Redirect URI: The client application callback URL to redirect to after auth. This must be registered with the API provider.

Once the user enters the username and password, they're successfully authenticated.

## Open a browser page to authenticate the user

From the extension UI, you can provide a button that, when selected, opens a new window in a browser to authenticate the user.

Use the [ddClient.host.openExternal](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard/#open-a-url) API to open a browser to the auth URL. For
example:

```typescript
window.ddClient.openExternal("https://authorization-server.com/authorize?
  response_type=code
  &client_id=T70hJ3ls5VTYG8ylX3CZsfIu
  &redirect_uri=${REDIRECT_URI});
```

## Get the authorization code and access token

You can get the authorization code from the extension UI by listing `docker-desktop://dashboard/extension-tab?extensionId=awesome/my-extension` as the `redirect_uri` in the OAuth app you're using and concatenating the authorization code as a query parameter. The extension UI code will then be able to read the corresponding code query-param.

> Important
>
> Using this feature requires the extension SDK 0.3.3 in Docker Desktop. You need to ensure that the required SDK version for your extension set with `com.docker.desktop.extension.api.version` in [image labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/) is higher than 0.3.3.

#### Authorization

This step is where the user enters their credentials in the browser. After the authorization is complete, the user is redirected back to your extension user interface, and the extension UI code can consume the authorization code that's part of the query parameters in the URL.

#### Exchange the Authorization Code

Next, you exchange the authorization code for an access token.

The extension must send a `POST` request to the 0Auth authorization server with the following parameters:

```text
POST https://authorization-server.com/token
&client_id=T70hJ3ls5VTYG8ylX3CZsfIu
&client_secret=YABbyHQShPeO1T3NDQZP8q5m3Jpb_UPNmIzqhLDCScSnRyVG
&redirect_uri=${REDIRECT_URI}
&code=N949tDLuf9ai_DaOKyuFBXStCNMQzuQbtC1QbvLv-AXqPJ_f
```

> Note
>
> The client's credentials are included in the `POST` query params in this example. OAuth authorization servers may require that the credentials are sent as a HTTP Basic Authentication header or might support different formats. See your OAuth provider docs for details.

### Store the access token

The Docker Extensions SDK doesn't provide a specific mechanism to store secrets.

It's highly recommended that you use an external source of storage to store the access token.

> Note
>
> The user interface Local Storage is isolated between extensions (an extension can't access another extension's local storage), and each extension's local storage gets deleted when users uninstall an extension.

## What's next

Learn how to [publish and distribute your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/)

---

# Use the Docker socket from the extension backend

> Docker extension metadata

# Use the Docker socket from the extension backend

---

Extensions can invoke Docker commands directly from the frontend with the SDK.

In some cases, it is useful to also interact with Docker Engine from the backend.

Extension backend containers can mount the Docker socket and use it to
interact with Docker Engine from the extension backend logic. Learn more about the
[Docker Engine socket](https://docs.docker.com/reference/cli/dockerd/#examples)

However, when mounting the Docker socket from an extension container that lives in the Desktop virtual machine, you want
to mount the Docker socket from inside the VM, and not mount `/var/run/docker.sock` from the host filesystem (using
the Docker socket from the host can lead to permission issues in containers).

In order to do so, you can use `/var/run/docker.sock.raw`. Docker Desktop mounts the socket that lives in the Desktop VM, and not from the host.

```yaml
services:
  myExtension:
    image: ${DESKTOP_PLUGIN_IMAGE}
    volumes:
      - /var/run/docker.sock.raw:/var/run/docker.sock
```

---

# The build and publish process

> Understand the process of creating an extension.

# The build and publish process

   Table of contents

---

This documentation is structured so that it matches the steps you need to take when creating your extension.

There are two main parts to creating a Docker extension:

1. Build the foundations
2. Publish the extension

> Note
>
> You do not need to pay to create a Docker extension. The [Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) is licensed under the Apache 2.0 License and is free to use. Anyone can create new extensions and share them without constraints.
>
>
>
> There is also no constraint on how each extension should be licensed, this is up to you to decide when creating a new extension.

## Part one: Build the foundations

The build process consists of:

- Installing the latest version of Docker Desktop.
- Setting up the directory with files, including the extension’s source code and the required extension-specific files.
- Creating the `Dockerfile` to build, publish, and run your extension in Docker Desktop.
- Configuring the metadata file which is required at the root of the image filesystem.
- Building and installing the extension.

For further inspiration, see the other examples in the [samples folder](https://github.com/docker/extensions-sdk/tree/main/samples).

> Tip
>
> Whilst creating your extension, make sure you follow the [design](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/) and [UI styling](https://docs.docker.com/extensions/extensions-sdk/design/) guidelines to ensure visual consistency and [level AA accessibility standards](https://www.w3.org/WAI/WCAG2AA-Conformance).

## Part two: Publish and distribute your extension

Docker Desktop displays published extensions in the Extensions Marketplace. The Extensions Marketplace is a curated space where developers can discover extensions to improve their developer experience and upload their own extension to share with the world.

If you want your extension published in the Marketplace, read the [publish documentation](https://docs.docker.com/extensions/extensions-sdk/extensions/publish/).

> Already built an extension?
>
>
>
> Let us know about your experience using the [feedback form](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form).

## What’s next?

If you want to get up and running with creating a Docker Extension, see the [Quickstart guide](https://docs.docker.com/extensions/extensions-sdk/quickstart/).

Alternatively, get started with reading the "Part one: Build" section for more in-depth information about each step of the extension creation process.

For an in-depth tutorial of the entire build process, we recommend the following video walkthrough from DockerCon 2022.

---

# Quickstart

> Guide on how to build an extension quickly

# Quickstart

   Table of contents

---

Follow this guide to get started with creating a basic Docker extension. The Quickstart guide automatically generates boilerplate files for you.

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/release-notes/)
- [NodeJS](https://nodejs.org/)
- [Go](https://go.dev/dl/)

> Note
>
> NodeJS and Go are only required when you follow the quickstart guide to create an extension. It uses the `docker extension init` command to automatically generate boilerplate files. This command uses a template based on a ReactJS and Go application.

In Docker Desktop settings, ensure you can install the extension you're developing. You may need to navigate to the **Extensions** tab in Docker Desktop settings and deselect **Allow only extensions distributed through the Docker Marketplace**.

## Step one: Set up your directory

To set up your directory, use the `init` subcommand and provide a name for your extension.

```console
$ docker extension init <my-extension>
```

The command asks a series of questions about your extension, such as its name, a description, and the name of your Hub repository. This helps the CLI generate a set of boilerplate files for you to get started. It stores the boilerplate files in the `my-extension` directory.

The automatically generated extension contains:

- A Go backend service in the `backend` folder that listens on a socket. It has one endpoint `/hello` that returns a JSON payload.
- A React frontend in the `frontend` folder that can call the backend and output the backend’s response.

For more information and guidelines on building the UI, see the [Design and UI styling section](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/).

## Step two: Build the extension

To build the extension, move into the newly created directory and run:

```console
$ docker build -t <name-of-your-extension> .
```

`docker build` builds the extension and generates an image named the same as the chosen hub repository. For example, if you typed `john/my-extension` as the answer to the following question:

```console
? Hub repository (eg. namespace/repository on hub): john/my-extension`
```

The `docker build` generates an image with name `john/my-extension`.

## Step three: Install and preview the extension

To install the extension in Docker Desktop, run:

```console
$ docker extension install <name-of-your-extension>
```

To preview the extension in Docker Desktop, once the installation is complete and you should
see a **Quickstart** item underneath the **Extensions** menu. Selecting this item opens the extension's frontend.

> Tip
>
> During UI development, it’s helpful to use hot reloading to test your changes without rebuilding your entire
> extension. See [Preview whilst developing the UI](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/#hot-reloading-whilst-developing-the-ui) for more information.

You may also want to inspect the containers that belong to the extension. By default, extension containers are
hidden from the Docker Dashboard. You can change this in **Settings**, see
[how to show extension containers](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/#show-the-extension-containers) for more information.

## Step four: Submit and publish your extension to the Marketplace

If you want to make your extension available to all Docker Desktop users, you can submit it for publication in the Marketplace. For more information, see [Publish](https://docs.docker.com/extensions/extensions-sdk/extensions/).

## Clean up

To remove the extension, run:

```console
$ docker extension rm <name-of-your-extension>
```

## What's next

- Build a more [advanced frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) for your extension.
- Learn how to [test and debug](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/) your extension.
- Learn how to [setup CI for your extension](https://docs.docker.com/extensions/extensions-sdk/dev/continuous-integration/).
- Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).
- Learn more about [designing the UI](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/).

---

# Overview of the Extensions SDK

> Overall index for Docker Extensions SDK documentation

# Overview of the Extensions SDK

---

The resources in this section help you create your own Docker extension.

The Docker CLI tool provides a set of commands to help you build and publish your extension, packaged as a
specially formatted Docker image.

At the root of the image filesystem is a `metadata.json` file which describes the content of the extension.
It's a fundamental element of a Docker extension.

An extension can contain a UI part and backend parts that run either on the host or in the Desktop virtual machine.
For further information, see [Architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).

You distribute extensions through Docker Hub. However, you can develop them locally without the need to push
the extension to Docker Hub. See [Extensions distribution](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/) for further details.

> Already built an extension?
>
>
>
> Let us know about your experience using the [feedback form](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form).

[The build and publish processUnderstand the process for building and publishing an extension.](https://docs.docker.com/extensions/extensions-sdk/process/)[Quickstart guideFollow the quickstart guide to create a basic Docker extension quickly.](https://docs.docker.com/extensions/extensions-sdk/quickstart/)[View the design guidelinesEnsure your extension aligns to Docker's design guidelines and principles.](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/)[Publish your extensionUnderstand how to publish your extension to the Marketplace.](https://docs.docker.com/extensions/extensions-sdk/extensions/)[Interacting with KubernetesFind information on how to interact indirectly with a Kubernetes cluster from your Docker extension.](https://docs.docker.com/extensions/extensions-sdk/guides/kubernetes/)[Multi-arch extensionsBuild your extension for multiple architectures.](https://docs.docker.com/extensions/extensions-sdk/extensions/multi-arch/)

---

# Marketplace extensions

> Extensions

# Marketplace extensions

   Table of contents

---

There are two types of extensions available in the Extensions Marketplace:

- Docker-reviewed extensions
- Self-published extensions

Docker-reviewed extensions are manually reviewed by the Docker Extensions team to ensure an extra level of trust
and quality. They appear as **Reviewed** in the Marketplace.

Self-published extensions are autonomously published by extension developers and go through an automated validation process. They appear as **Not reviewed** in the Marketplace.

## Install an extension

> Note
>
> For some extensions, a separate account needs to be created before use.

To install an extension:

1. Open Docker Desktop.
2. From the Docker Desktop Dashboard, select the **Extensions** tab.
  The Extensions Marketplace opens on the **Browse** tab.
3. Browse the available extensions.
  You can sort the list of extensions by **Recently added**, **Most installed**, or alphabetically. Alternatively, use the **Content** or **Categories** drop-down menu to search for extensions by whether they have been reviewed or not, or by category.
4. Choose an extension and select **Install**.

From here, you can select **Open** to access the extension or install additional extensions. The extension also appears in the left-hand menu and in the **Manage** tab.

## Update an extension

You can update any extension outside of Docker Desktop releases. To update an extension to the latest version, navigate to the Docker Desktop Dashboard and select the **Manage** tab.

The **Manage** tab displays with all your installed extensions. If an extension has a new version available, it displays an **Update** button.

## Uninstall an extension

You can uninstall an extension at any time.

> Note
>
> Any data used by the extension that's stored in a volume must be manually deleted.

1. Navigate to the Docker Desktop Dashboard and select the **Manage** tab.
  This displays a list of extensions you've installed.
2. Select the ellipsis to the right of extension you want to uninstall.
3. Select **Uninstall**.

---

# Non

> Extensions

# Non-marketplace extensions

   Table of contents

---

## Install an extension not available in the Marketplace

> Warning
>
> Docker Extensions that are not in the Marketplace haven't gone through Docker's review process.
> Extensions can install binaries, invoke commands and access files on your machine. Installing them is at your own risk.

The Extensions Marketplace is the trusted and official place to install extensions from within Docker Desktop. These extensions have gone through a review process by Docker. However, other extensions can also be installed in Docker Desktop if you trust the extension author.

Given the nature of a Docker Extension (i.e. a Docker image) you can find other places where users have their extension's source code published. For example on GitHub, GitLab or even hosted in image registries like DockerHub or GHCR.
You can install an extension that has been developed by the community or internally at your company from a teammate. You are not limited to installing extensions just from the Marketplace.

> Note
>
> Ensure the option **Allow only extensions distributed through the Docker Marketplace** is disabled. Otherwise, this prevents any extension not listed in the Marketplace, via the Extension SDK tools from, being installed.
> You can change this option in **Settings**.

To install an extension which is not present in the Marketplace, you can use the Extensions CLI that is bundled with Docker Desktop.

In a terminal, type `docker extension install IMAGE[:TAG]` to install an extension by its image reference and optionally a tag. Use the `-f` or `--force` flag to avoid interactive confirmation.

Go to the Docker Desktop Dashboard to see the new extension installed.

## List installed extensions

Regardless whether the extension was installed from the Marketplace or manually by using the Extensions CLI, you can use the `docker extension ls` command to display the list of extensions installed.
As part of the output you'll see the extension ID, the provider, version, the title and whether it runs a backend container or has deployed binaries to the host, for example:

```console
$ docker extension ls
ID                  PROVIDER            VERSION             UI                    VM                  HOST
john/my-extension   John                latest              1 tab(My-Extension)   Running(1)          -
```

Go to the Docker Desktop Dashboard, select **Add Extensions** and on the **Managed** tab to see the new extension installed.
Notice that an `UNPUBLISHED` label displays which indicates that the extension has not been installed from the Marketplace.

## Update an extension

To update an extension which isn't present in the Marketplace, in a terminal type `docker extension update IMAGE[:TAG]` where the `TAG` should be different from the extension that's already installed.

For instance, if you installed an extension with `docker extension install john/my-extension:0.0.1`, you can update it by running `docker extension update john/my-extension:0.0.2`.
Go to the Docker Desktop Dashboard to see the new extension updated.

> Note
>
> Extensions that aren't installed through the Marketplace don't receive update notifications from Docker Desktop.

## Uninstall an extension

To uninstall an extension which is not present in the Marketplace, you can either navigate to the **Managed** tab in the Marketplace and select the **Uninstall** button, or from a terminal type `docker extension uninstall IMAGE[:TAG]`.

---

# Configure a private marketplace for extensions

> How to configure and use Docker Extensions' private marketplace

# Configure a private marketplace for extensions

   Table of contents

---

Availability: Beta
For: Administrators

Learn how to configure and set up a private marketplace with a curated list of extensions for your Docker Desktop users.

Docker Extensions' private marketplace is designed specifically for organizations who don’t give developers root access to their machines. It makes use of
[Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/) so administrators have complete control over the private marketplace.

## Prerequisites

- [Download and install Docker Desktop 4.26.0 or later](https://docs.docker.com/desktop/release-notes/).
- You must be an administrator for your organization.
- You have the ability to push the `extension-marketplace` folder and `admin-settings.json` file to the locations specified below through device management software such as [Jamf](https://www.jamf.com/).

## Step one: Initialize the private marketplace

1. Create a folder locally for the content that will be deployed to your developers’ machines:
  ```console
  $ mkdir my-marketplace
  $ cd my-marketplace
  ```
2. Initialize the configuration files for your marketplace:
  ```console
  $ /Applications/Docker.app/Contents/Resources/bin/extension-admin init
  ```
  ```console
  $ C:\Program Files\Docker\Docker\resources\bin\extension-admin init
  ```
  ```console
  $ /opt/docker-desktop/extension-admin init
  ```

This creates 2 files:

- `admin-settings.json`, which activates the private marketplace feature once it’s applied to Docker Desktop on your developers’ machines.
- `extensions.txt`, which determines which extensions to list in your private marketplace.

> Important
>
> If your org is using
> [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/) via the [Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/), you will not need the `admins-settings.json` file. Delete the generated file and keep only the `extensions.txt` file.

## Step two: Set the behaviour

The generated `admin-settings.json` file includes various settings you can modify.

> Important
>
> If your org is managing settings via the [Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/), you will define the same settings in the Admin Console instead of the `admin-settings.json` file.

Each setting has a `value` that you can set, including a `locked` field that lets you lock the setting and make it unchangeable by your developers.

- `extensionsEnabled` enables Docker Extensions.
- `extensionsPrivateMarketplace` activates the private marketplace and ensures Docker Desktop connects to content defined and controlled by the administrator instead of the public Docker marketplace.
- `onlyMarketplaceExtensions` allows or blocks developers from installing other extensions by using the command line. Teams developing new extensions must have this setting unlocked (`"locked": false`) to install and test extensions being developed.
- `extensionsPrivateMarketplaceAdminContactURL` defines a contact link for developers to request new extensions in the private marketplace. If `value` is empty then no link is shown to your developers on Docker Desktop, otherwise this can be either an HTTP link or a “mailto:” link. For example,
  ```json
  "extensionsPrivateMarketplaceAdminContactURL": {
    "locked": true,
    "value": "mailto:admin@acme.com"
  }
  ```

To find out more information about the `admin-settings.json` file, see
[Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/).

## Step three: List allowed extensions

The generated `extensions.txt` file defines the list of extensions that are available in your private marketplace.

Each line in the file is an allowed extension and follows the format of `org/repo:tag`.

For example, if you want to permit the Disk Usage extension you would enter the following into your `extensions.txt` file:

```console
docker/disk-usage-extension:0.2.8
```

If no tag is provided, the latest tag available for the image is used. You can also comment out lines with `#` so the extension is ignored.

This list can include different types of extension images:

- Extensions from the public marketplace or any public image stored in Docker Hub.
- Extension images stored in Docker Hub as private images. Developers need to be signed in and have pull access to these images.
- Extension images stored in a private registry. Developers need to be signed in and have pull access to these images.

> Important
>
> Your developers can only install the version of the extension that you’ve listed.

## Step four: Generate the private marketplace

Once the list in `extensions.txt` is ready, you can generate the marketplace:

```console
$ /Applications/Docker.app/Contents/Resources/bin/extension-admin generate
```

```console
$ C:\Program Files\Docker\Docker\resources\bin\extension-admin generate
```

```console
$ /opt/docker-desktop/extension-admin generate
```

This creates an `extension-marketplace` directory and downloads the marketplace metadata for all the allowed extensions.

The marketplace content is generated from extension image information as image labels, which is the [same format as public extensions](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/). It includes the extension title, description, screenshots, links, etc.

## Step five: Test the private marketplace setup

It's recommended that you try the private marketplace on your Docker Desktop installation.

1. Run the following command in your terminal. This command automatically copies the generated files to the location where Docker Desktop reads the configuration files. Depending on your operating system, the location is:
  - Mac: `/Library/Application\ Support/com.docker.docker`
  - Windows: `C:\ProgramData\DockerDesktop`
  - Linux: `/usr/share/docker-desktop`
  ```console
  $ sudo /Applications/Docker.app/Contents/Resources/bin/extension-admin apply
  ```
  ```console
  $ C:\Program Files\Docker\Docker\resources\bin\extension-admin apply
  ```
  ```console
  $ sudo /opt/docker-desktop/extension-admin apply
  ```
2. Quit and re-open Docker Desktop.
3. Sign in with a Docker account.

> Important
>
> > If your org is managing settings via the [Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/), with Docker Desktop version 4.59 and earlier you need to manually delete the `admin-settings.json` file that has been created in the target folder by the `apply` command before step 2.

When you select the **Extensions** tab, you should see the private marketplace listing only the extensions you have allowed in `extensions.txt`.

![Extensions Private Marketplace](https://docs.docker.com/assets/images/extensions-private-marketplace.webp)  ![Extensions Private Marketplace](https://docs.docker.com/assets/images/extensions-private-marketplace.webp)

## Step six: Distribute the private marketplace

Once you’ve confirmed that the private marketplace configuration works, the final step is to distribute the files to the developers’ machines with the MDM software your organization uses. For example, [Jamf](https://www.jamf.com/).

The files to distribute are:

- `admin-settings.json` (except if your org is managing settings via the [Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/))
- the entire `extension-marketplace` folder and its subfolders

These files must be placed on developer's machines. Depending on your operating system, the target location is (as mentioned above):

- Mac: `/Library/Application\ Support/com.docker.docker`
- Windows: `C:\ProgramData\DockerDesktop`
- Linux: `/usr/share/docker-desktop`

Make sure your developers are signed in to Docker Desktop in order for the private marketplace configuration to take effect. As an administrator, you should
[enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

## Feedback

Give feedback or report any bugs you may find by emailing `extensions@docker.com`.
