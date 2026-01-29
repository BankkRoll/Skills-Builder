# MUI best practices and more

# MUI best practices

> Guidelines for using MUI to maximize compatibility with Docker Desktop

# MUI best practices

   Table of contents

---

This article assumes you're following our recommended practice by using our [Material UI theme](https://www.npmjs.com/package/@docker/docker-mui-theme).
Following the steps below maximizes compatibility with Docker Desktop and minimizes the work you need to do as an
extension author. They should be considered supplementary to the non-MUI-specific guidelines found in the
[UI Styling overview](https://docs.docker.com/extensions/extensions-sdk/design/).

## Assume the theme can change at any time

Resist the temptation to fine-tune your UI with precise colors, offsets and font sizings to make it look as attractive as possible. Any specializations you make today will be relative to the current MUI theme, and may look worse when the theme changes. Any part of the theme might change without warning, including (but not limited to):

- The font, or font sizes
- Border thicknesses or styles
- Colors:
  - Our palette members (e.g. `red-100`) could change their RGB values
  - The semantic colors (e.g. `error`, `primary`, `textPrimary`, etc) could be changed to use a different member of our palette
  - Background colors (e.g. those of the page, or of dialogs) could change
- Spacings:
  - The size of the basic unit of spacing,(exposed via `theme.spacing`. For instance, we may allow users to customize the density of the UI
  - The default spacing between paragraphs or grid items

The best way to build your UI, so that it’s robust against future theming changes, is to:

- Override the default styling as little as possible.
- Use semantic typography. e.g. use `Typography`s or `Link`s with appropriate `variant`s instead of using typographical HTML elements (`<a>`, `<p>`, `<h1>`, etc) directly.
- Use canned sizes. e.g. use `size="small"` on buttons, or `fontSize="small"` on icons, instead of specifying sizes in pixels.
- Prefer semantic colors. e.g. use `error` or `primary` over explicit color codes.
- Write as little CSS as possible. Write semantic markup instead. For example, if you want to space out paragraphs of text, use the `paragraph` prop on your `Typography` instances. If you want to space out something else, use a `Stack` or `Grid` with the default spacing.
- Use visual idioms you’ve seen in the Docker Desktop UI, since these are the main ones we’ll test any theme changes against.

## When you go custom, centralize it

Sometimes you’ll need a piece of UI that doesn’t exist in our design system. If so, we recommend that you first reach out to us. We may already have something in our internal design system, or we may be able to expand our design system to accommodate your use case.

If you still decide to build it yourself after contacting us, try and define the new UI in a reusable fashion. If you define your custom UI in just one place, it’ll make it easier to change in the future if our core theme changes. You could use:

- A new `variant` of an existing component - see [MUI docs](https://mui.com/material-ui/customization/theme-components/#creating-new-component-variants)
- A MUI mixin (a freeform bundle of reusable styling rules defined inside a theme)
- A new [reusable component](https://mui.com/material-ui/customization/how-to-customize/#2-reusable-component)

Some of the above options require you to extend our MUI theme. See the MUI documentation on [theme composition](https://mui.com/material-ui/customization/theming/#nesting-the-theme).

## What's next?

- Take a look at our [UI styling guide](https://docs.docker.com/extensions/extensions-sdk/design/).
- Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

---

# UI styling overview for Docker extensions

> Docker extension design

# UI styling overview for Docker extensions

   Table of contents

---

Our Design System is a constantly evolving set of specifications that aim to ensure visual consistency across Docker products, and meet [level AA accessibility standards](https://www.w3.org/WAI/WCAG2AA-Conformance). We've opened parts of it to extension authors, documenting basic styles (color, typography) and components. See: [Docker Extensions Styleguide](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771).

We require extensions to match the wider Docker Desktop UI to a certain degree, and reserve the right to make this stricter in the future.

To get started on your UI, follow the steps below.

## Step one: Choose your framework

### Recommended: React+MUI, using our theme

Docker Desktop's UI is written in React and [MUI](https://mui.com/) (using Material UI to specific). This is the only officially supported framework for building extensions, and the one that our `init` command automatically configures for you. Using it brings significant benefits to authors:

- You can use our [Material UI theme](https://www.npmjs.com/package/@docker/docker-mui-theme) to automatically replicate Docker Desktop's look and feel.
- In future, we'll release utilities and components specifically targeting this combination (e.g. custom MUI components, or React hooks for interacting with Docker).

Read our [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/) guide to learn future-proof ways to use MUI with Docker Desktop.

### Not recommended: Some other framework

You may prefer to use another framework, perhaps because you or your team are more familiar with it or because you have existing assets you want to reuse. This is possible, but highly discouraged. It means that:

- You'll need to manually replicate the look and feel of Docker Desktop. This takes a lot of effort, and if you don't match our theme closely enough, users will find your extension jarring and we may ask you to make changes during a review process.
- You'll have a higher maintenance burden. Whenever Docker Desktop's theme changes (which could happen in any release), you'll need to manually change your extension to match it.
- If your extension is open-source, deliberately avoiding common conventions will make it harder for the community to contribute to it.

## Step two: Follow the below recommendations

### Follow our MUI best practices (if applicable)

See our [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/) article.

### Only use colors from our palette

With minor exceptions, displaying your logo for example, you should only use colors from our palette. These can be found in our [style guide document](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771), and will also soon be available in our MUI theme and via CSS variables.

### Use counterpart colors in light/dark mode

Our colors have been chosen so that the counterpart colors in each variant of the palette should have the same essential characteristics. Anywhere you use `red-300` in light mode, you should use `red-300` in dark mode too.

## What's next?

- Take a look at our [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/).
- Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

---

# Extension Backend

> Docker extension API

# Extension Backend

   Table of contents

---

The `ddClient.extension.vm` object can be used to communicate with the backend defined in the [vm section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#vm-section) of the extension metadata.

## get

▸ **get**(`url`): `Promise`<`unknown`>

Performs an HTTP GET request to a backend service.

```typescript
ddClient.extension.vm.service
 .get("/some/service")
 .then((value: any) => console.log(value)
```

See
[Service API Reference](https://docs.docker.com/reference/api/extensions-sdk/HttpService/) for other methods such as POST, UPDATE, and DELETE.

> Deprecated extension backend communication
>
>
>
> The methods below that use `window.ddClient.backend` are deprecated and will be removed in a future version. Use the methods specified above.

The `window.ddClient.backend` object can be used to communicate with the backend
defined in the [vm section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#vm-section) of the
extension metadata. The client is already connected to the backend.

Example usages:

```typescript
window.ddClient.backend
  .get("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .post("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .put("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .patch("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .delete("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .head("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
  .then((value: any) => console.log(value));
```

## Run a command in the extension backend container

For example, execute the command `ls -l` inside the backend container:

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"]);
```

Stream the output of the command executed in the backend container. For example, spawn the command `ls -l` inside the backend container:

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
  stream: {
    onOutput(data) {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
    },
    onError(error) {
      console.error(error);
    },
    onClose(exitCode) {
      console.log("onClose with exit code " + exitCode);
    },
  },
});
```

For more details, refer to the
[Extension VM API Reference](https://docs.docker.com/reference/api/extensions-sdk/ExtensionVM/)

> Deprecated extension backend command execution
>
>
>
> This method is deprecated and will be removed in a future version. Use the specified method above.

If your extension ships with additional binaries that should be run inside the
backend container, you can use the `execInVMExtension` function:

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);
console.log(output);
```

## Invoke an extension binary on the host

Invoke a binary on the host. The binary is typically shipped with your extension using the [host section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) in the extension metadata. Note that extensions run with user access rights, this API is not restricted to binaries listed in the [host section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) of the extension metadata (some extensions might install software during user interaction, and invoke newly installed binaries even if not listed in the extension metadata).

For example, execute the shipped binary `kubectl -h` command in the host:

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

As long as the `kubectl` binary is shipped as part of your extension, you can spawn the `kubectl -h` command in the host and get the output stream:

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
  stream: {
    onOutput(data: { stdout: string } | { stderr: string }): void {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
    },
    onError(error: any): void {
      console.error(error);
    },
    onClose(exitCode: number): void {
      console.log("onClose with exit code " + exitCode);
    },
  },
});
```

You can stream the output of the command executed in the backend container or in the host.

For more details, refer to the
[Extension Host API Reference](https://docs.docker.com/reference/api/extensions-sdk/ExtensionHost/)

> Deprecated invocation of extension binary
>
>
>
> This method is deprecated and will be removed in a future version. Use the method specified above.

To execute a command in the host:

```typescript
window.ddClient.execHostCmd(`cliShippedOnHost xxx`).then((cmdResult: any) => {
  console.log(cmdResult);
});
```

To stream the output of the command executed in the backend container or in the host:

```typescript
window.ddClient.spawnHostCmd(
  `cliShippedOnHost`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // Once the command exits we get the status code
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> Note
>
> You cannot use this to chain commands in a single `exec()` invocation (like `cmd1 $(cmd2)` or using pipe between commands).
>
>
>
> You need to invoke `exec()` for each command and parse results to pass parameters to the next command if needed.

---

# Navigation

> Docker extension API

# Navigation

   Table of contents

---

`ddClient.desktopUI.navigate` enables navigation to specific screens of Docker Desktop such as the containers tab, the images tab, or a specific container's logs.

For example, navigate to a given container logs:

```typescript
const id = '8c7881e6a107';
try {
  await ddClient.desktopUI.navigate.viewContainerLogs(id);
} catch (e) {
  console.error(e);
  ddClient.desktopUI.toast.error(
    `Failed to navigate to logs for container "${id}".`
  );
}
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full container id, e.g.46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28. You can use the--no-truncflag as part of thedocker pscommand to display the full container id. |

#### Returns

`Promise`<`void`>

A promise that fails if the container doesn't exist.

For more details about all navigation methods, see the
[Navigation API reference](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/).

> Deprecated navigation methods
>
>
>
> These methods are deprecated and will be removed in a future version. Use the methods specified above.

```typescript
window.ddClient.navigateToContainers();
// id - the full container id, e.g. `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`
window.ddClient.navigateToContainer(id);
window.ddClient.navigateToContainerLogs(id);
window.ddClient.navigateToContainerInspect(id);
window.ddClient.navigateToContainerStats(id);

window.ddClient.navigateToImages();
window.ddClient.navigateToImage(id, tag);

window.ddClient.navigateToVolumes();
window.ddClient.navigateToVolume(volume);

window.ddClient.navigateToDevEnvironments();
```

---

# Dashboard

> Docker extension API

# Dashboard

   Table of contents

---

## User notifications

Toasts provide a brief notification to the user. They appear temporarily and
shouldn't interrupt the user experience. They also don't require user input to disappear.

### success

▸ **success**(`msg`): `void`

Use to display a toast message of type success.

```typescript
ddClient.desktopUI.toast.success("message");
```

### warning

▸ **warning**(`msg`): `void`

Use to display a toast message of type warning.

```typescript
ddClient.desktopUI.toast.warning("message");
```

### error

▸ **error**(`msg`): `void`

Use to display a toast message of type error.

```typescript
ddClient.desktopUI.toast.error("message");
```

For more details about method parameters and the return types available, see
[Toast API reference](https://docs.docker.com/reference/api/extensions-sdk/Toast/).

> Deprecated user notifications
>
>
>
> These methods are deprecated and will be removed in a future version. Use the methods specified above.

```typescript
window.ddClient.toastSuccess("message");
window.ddClient.toastWarning("message");
window.ddClient.toastError("message");
```

## Open a file selection dialog

This function opens a file selector dialog that asks the user to select a file or folder.

▸ **showOpenDialog**(`dialogProperties`): `Promise`<
[OpenDialogResult](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)>:

The `dialogProperties` parameter is a list of flags passed to Electron to customize the dialog's behaviour. For example, you can pass `multiSelections` to allow a user to select multiple files. See [Electron's documentation](https://www.electronjs.org/docs/latest/api/dialog) for a full list.

```typescript
const result = await ddClient.desktopUI.dialog.showOpenDialog({
  properties: ["openDirectory"],
});
if (!result.canceled) {
  console.log(result.paths);
}
```

## Open a URL

This function opens an external URL with the system default browser.

▸ **openExternal**(`url`): `void`

```typescript
ddClient.host.openExternal("https://docker.com");
```

> The URL must have the protocol `http` or `https`.

For more details about method parameters and the return types available, see
[Desktop host API reference](https://docs.docker.com/reference/api/extensions-sdk/Host/).

> Deprecated user notifications
>
>
>
> This method is deprecated and will be removed in a future version. Use the methods specified above.

```typescript
window.ddClient.openExternal("https://docker.com");
```

## Navigation to Dashboard routes

From your extension, you can also [navigate](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard-routes-navigation/) to other parts of the Docker Desktop Dashboard.

---

# Docker

> Docker extension API

# Docker

   Table of contents

---

## Docker objects

▸ **listContainers**(`options?`): `Promise`<`unknown`>

To get the list of containers:

```typescript
const containers = await ddClient.docker.listContainers();
```

▸ **listImages**(`options?`): `Promise`<`unknown`>

To get the list of local container images:

```typescript
const images = await ddClient.docker.listImages();
```

See the
[Docker API reference](https://docs.docker.com/reference/api/extensions-sdk/Docker/) for details about these methods.

> Deprecated access to Docker objects
>
>
>
> The methods below are deprecated and will be removed in a future version. Use the methods specified above.

```typescript
const containers = await window.ddClient.listContainers();

const images = await window.ddClient.listImages();
```

## Docker commands

Extensions can also directly execute the `docker` command line.

▸ **exec**(`cmd`, `args`): `Promise`<
[ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)>

```typescript
const result = await ddClient.docker.cli.exec("info", [
  "--format",
  '"{{ json . }}"',
]);
```

The result contains both the standard output and the standard error of the executed command:

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

In this example, the command output is JSON.
For convenience, the command result object also has methods to easily parse it:

- `result.lines(): string[]` splits output lines.
- `result.parseJsonObject(): any` parses a well-formed json output.
- `result.parseJsonLines(): any[]` parses each output line as a json object.

▸ **exec**(`cmd`, `args`, `options`): `void`

The command above streams the output as a result of the execution of a Docker command.
This is useful if you need to get the output as a stream or the output of the command is too long.

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    onOutput(data) {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
    },
    onError(error) {
      console.error(error);
    },
    onClose(exitCode) {
      console.log("onClose with exit code " + exitCode);
    },
    splitOutputLines: true,
  },
});
```

The child process created by the extension is killed (`SIGTERM`) automatically when you close the dashboard in Docker Desktop or when you exit the extension UI.
If needed, you can also use the result of the `exec(streamOptions)` call in order to kill (`SIGTERM`) the process.

```typescript
const logListener = await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    // ...
  },
});

// when done listening to logs or before starting a new one, kill the process
logListener.close();
```

This `exec(streamOptions)` API can also be used to listen to docker events:

```typescript
await ddClient.docker.cli.exec(
  "events",
  ["--format", "{{ json . }}", "--filter", "container=my-container"],
  {
    stream: {
      onOutput(data) {
        if (data.stdout) {
          const event = JSON.parse(data.stdout);
          console.log(event);
        } else {
          console.log(data.stderr);
        }
      },
      onClose(exitCode) {
        console.log("onClose with exit code " + exitCode);
      },
      splitOutputLines: true,
    },
  }
);
```

> Note
>
> You cannot use this to chain commands in a single `exec()` invocation (like `docker kill $(docker ps -q)` or using pipe between commands).
>
>
>
> You need to invoke `exec()` for each command and parse results to pass parameters to the next command if needed.

See the
[Exec API reference](https://docs.docker.com/reference/api/extensions-sdk/Exec/) for details about these methods.

> Deprecated execution of Docker commands
>
>
>
> This method is deprecated and will be removed in a future version. Use the one specified just below.

```typescript
const output = await window.ddClient.execDockerCmd(
  "info",
  "--format",
  '"{{ json . }}"'
);

window.ddClient.spawnDockerCmd("logs", ["-f", "..."], (data, error) => {
  console.log(data.stdout);
});
```

---

# Extension UI API

> Docker extension development overview

# Extension UI API

---

The extensions UI runs in a sandboxed environment and doesn't have access to any
electron or nodejs APIs.

The extension UI API provides a way for the frontend to perform different actions
and communicate with the Docker Desktop dashboard or the underlying system.

JavaScript API libraries, with Typescript support, are available in order to get all the API definitions in to your extension code.

- [@docker/extension-api-client](https://www.npmjs.com/package/@docker/extension-api-client) gives access to the extension API entrypoint `DockerDesktopClient`.
- [@docker/extension-api-client-types](https://www.npmjs.com/package/@docker/extension-api-client-types) can be added as a dev dependency in order to get types auto-completion in your IDE.

```Typescript
import { createDockerDesktopClient } from '@docker/extension-api-client';

export function App() {
  // obtain Docker Desktop client
  const ddClient = createDockerDesktopClient();
  // use ddClient to perform extension actions
}
```

The `ddClient` object gives access to various APIs:

- [Extension Backend](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/)
- [Docker](https://docs.docker.com/extensions/extensions-sdk/dev/api/docker/)
- [Dashboard](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard/)
- [Navigation](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard-routes-navigation/)

See also the [Extensions API reference](https://docs.docker.com/reference/api/extensions-sdk/).

---

# Continuous Integration (CI)

> Automatically test and validate your extension.

# Continuous Integration (CI)

   Table of contents

---

In order to help validate your extension and ensure it's functional, the Extension SDK provides tools to help you setup continuous integration for your extension.

> Important
>
> The [Docker Desktop Action](https://github.com/docker/desktop-action) and the [extension-test-helper library](https://www.npmjs.com/package/@docker/extension-test-helper) are both [experimental](https://docs.docker.com/release-lifecycle/#experimental).

## Setup CI environment with GitHub Actions

You need Docker Desktop to be able to install and validate your extension.
You can start Docker Desktop in GitHub Actions using the [Docker Desktop Action](https://github.com/docker/desktop-action), by adding the following to a workflow file:

```yaml
steps:
  - id: start_desktop
    uses: docker/desktop-action/start@v0.1.0
```

> Note
>
> This action supports only Github Action macOS runners at the moment. You need to specify `runs-on: macOS-latest` for your end to end tests.

Once the step has executed, the next steps use Docker Desktop and the Docker CLI to install and test the extension.

## Validating your extension with Puppeteer

Once Docker Desktop starts in CI, you can build, install, and validate your extension with Jest and Puppeteer.

First, build and install the extension from your test:

```ts
import { DesktopUI } from "@docker/extension-test-helper";
import { exec as originalExec } from "child_process";
import * as util from "util";

export const exec = util.promisify(originalExec);

// keep a handle on the app to stop it at the end of tests
let dashboard: DesktopUI;

beforeAll(async () => {
  await exec(`docker build -t my/extension:latest .`, {
    cwd: "my-extension-src-root",
  });

  await exec(`docker extension install -f my/extension:latest`);
});
```

Then open the Docker Desktop Dashboard and run some tests in your extension's UI:

```ts
describe("Test my extension", () => {
  test("should be functional", async () => {
    dashboard = await DesktopUI.start();

    const eFrame = await dashboard.navigateToExtension("my/extension");

    // use puppeteer APIs to manipulate the UI, click on buttons, expect visual display and validate your extension
    await eFrame.waitForSelector("#someElementId");
  });
});
```

Finally, close the Docker Desktop Dashboard and uninstall your extension:

```ts
afterAll(async () => {
  dashboard?.stop();
  await exec(`docker extension uninstall my/extension`);
});
```

## What's next

- Build an
  [advanced frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) extension.
- Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).
- Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

---

# Test and debug

> Test and debug your extension.

# Test and debug

   Table of contents

---

In order to improve the developer experience, Docker Desktop provides a set of tools to help you test and debug your extension.

### Open Chrome DevTools

In order to open the Chrome DevTools for your extension when you select the **Extensions** tab, run:

```console
$ docker extension dev debug <name-of-your-extensions>
```

Each subsequent click on the extension tab also opens Chrome DevTools. To stop this behaviour, run:

```console
$ docker extension dev reset <name-of-your-extensions>
```

After an extension is deployed, it is also possible to open Chrome DevTools from the UI extension part using a variation of the [Konami Code](https://en.wikipedia.org/wiki/Konami_Code). Select the **Extensions** tab, and then hit the key sequence `up, up, down, down, left, right, left, right, p, d, t`.

### Hot reloading whilst developing the UI

During UI development, it’s helpful to use hot reloading to test your changes without rebuilding your entire
extension. To do this, you can configure Docker Desktop to load your UI from a development server, such as the one
[Vite](https://vitejs.dev/) starts when invoked with `npm start`.

Assuming your app runs on the default port, start your UI app and then run:

```console
$ cd ui
$ npm run dev
```

This starts a development server that listens on port 3000.

You can now tell Docker Desktop to use this as the frontend source. In another terminal run:

```console
$ docker extension dev ui-source <name-of-your-extensions> http://localhost:3000
```

Close and reopen the Docker Desktop dashboard and go to your extension. All the changes to the frontend code are immediately visible.

Once finished, you can reset the extension configuration to the original settings. This will also reset opening Chrome DevTools if you used `docker extension dev debug <name-of-your-extensions>`:

```console
$ docker extension dev reset <name-of-your-extensions>
```

## Show the extension containers

If your extension is composed of one or more services running as containers in the Docker Desktop VM, you can access them easily from the dashboard in Docker Desktop.

1. In Docker Desktop, navigate to **Settings**.
2. Under the **Extensions** tab, select the **Show Docker Desktop Extensions system containers** option. You can now view your extension containers and their logs.

## Clean up

To remove the extension, run:

```console
$ docker extension rm <name-of-your-extension>
```

## What's next

- Build an
  [advanced frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) extension.
- Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).
- Explore our [design principles](https://docs.docker.com/extensions/extensions-sdk/design/design-principles/).
- Take a look at our [UI styling guidelines](https://docs.docker.com/extensions/extensions-sdk/design/).
- Learn how to [setup CI for your extension](https://docs.docker.com/extensions/extensions-sdk/dev/continuous-integration/).

---

# CLI reference

> Docker extension CLI

# CLI reference

---

The Extensions CLI is an extension development tool that is used to manage Docker extensions. Actions include install, list, remove, and validate extensions.

- `docker extension enable` turns on Docker extensions.
- `docker extension dev` commands for extension development.
- `docker extension disable` turns off Docker extensions.
- `docker extension init` creates a new Docker extension.
- `docker extension install` installs a Docker extension with the specified image.
- `docker extension ls` list installed Docker extensions.
- `docker extension rm` removes a Docker extension.
- `docker extension update` removes and re-installs a Docker extension.
- `docker extension validate` validates the extension metadata file against the JSON schema.

---

# Package and release your extension

> Docker extension distribution

# Package and release your extension

   Table of contents

---

This page contains additional information on how to package and distribute extensions.

## Package your extension

Docker extensions are packaged as Docker images. The entire extension runtime including the UI, backend services (host or VM), and any necessary binary must be included in the extension image.
Every extension image must contain a `metadata.json` file at the root of its filesystem that defines the [contents of the extension](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/).

The Docker image must have several [image labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/), providing information about the extension. See how to use [extension labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/) to provide extension overview information.

To package and release an extension, you must build a Docker image (`docker build`), and push the image to [Docker Hub](https://hub.docker.com/) (`docker push`) with a specific tag that lets you manage versions of the extension.

## Release your extension

Docker image tags must follow semver conventions in order to allow fetching the latest version of the extension, and to know if there are updates available. See [semver.org](https://semver.org/) to learn more about semantic versioning.

Extension images must be multi-arch images so that users can install extensions on ARM/AMD hardware. These multi-arch images can include ARM/AMD specific binaries. Mac users will automatically use the right image based on their architecture.
Extensions that install binaries on the host must also provide Windows binaries in the same extension image. See how to [build a multi-arch image](https://docs.docker.com/extensions/extensions-sdk/extensions/multi-arch/) for your extension.

You can implement extensions without any constraints on the code repository. Docker doesn't need access to the code repository in order to use the extension. Also, you can manage new releases of your extension, without any dependency on Docker Desktop releases.

## New releases and updates

You can release a new version of your Docker extension by pushing a new image with a new tag to Docker Hub.

Any new image pushed to an image repository corresponding to an extension defines a new version of that extension. Image tags are used to identify version numbers. Extension versions must follow semver to make it easy to understand and compare versions.

Docker Desktop scans the list of extensions published in the marketplace for new versions, and provides notifications to users when they can upgrade a specific extension. Extensions that aren't part of the Marketplace don't have automatic update notifications at the moment.

Users can download and install the newer version of any extension without updating Docker Desktop itself.

## Extension API dependencies

Extensions must specify the Extension API version they rely on. Docker Desktop checks the extension's required version, and only proposes to install extensions that are compatible with the current Docker Desktop version installed. Users might need to update Docker Desktop in order to install the latest extensions available.

Extension image labels must specify the API version that the extension relies upon. This allows Docker Desktop to inspect newer versions of extension images without downloading the full extension image upfront.

## License on extensions and the extension SDK

The [Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) is licensed under the Apache 2.0 License and is free to use.

There is no constraint on how each extension should be licensed, this is up to you to decide when creating a new extension.

---

# Extension image labels

> Docker extension labels

# Extension image labels

   Table of contents

---

Extensions use image labels to provide additional information such as a title, description, screenshots, and more.

This information is then displayed as an overview of the extension, so users can choose to install it.

![An extension overview, generated from labels](https://docs.docker.com/extensions/extensions-sdk/extensions/images/marketplace-details.png)  ![An extension overview, generated from labels](https://docs.docker.com/extensions/extensions-sdk/extensions/images/marketplace-details.png)

You can define
[image labels](https://docs.docker.com/reference/dockerfile/#label) in the extension's `Dockerfile`.

> Important
>
> If any of the **required** labels are missing in the `Dockerfile`, Docker Desktop considers the extension invalid and doesn't list it in the Marketplace.

Here is the list of labels you can or need to specify when building your extension:

| Label | Required | Description | Example |
| --- | --- | --- | --- |
| org.opencontainers.image.title | Yes | Human-readable title of the image (string). This appears in the UI for Docker Desktop. | my-extension |
| org.opencontainers.image.description | Yes | Human-readable description of the software packaged in the image (string) | This extension is cool. |
| org.opencontainers.image.vendor | Yes | Name of the distributing entity, organization, or individual. | Acme, Inc. |
| com.docker.desktop.extension.api.version | Yes | Version of the Docker Extension manager that the extension is compatible with. It must followsemantic versioning. | A specific version like0.1.0or, a constraint expression:>= 0.1.0,>= 1.4.7, < 2.0. For your first extension, you can usedocker extension versionto know the SDK API version and specify>= <SDK_API_VERSION>. |
| com.docker.desktop.extension.icon | Yes | The extension icon (format: .svg .png .jpg) | https://example.com/assets/image.svg |
| com.docker.extension.screenshots | Yes | A JSON array of image URLs and an alternative text displayed to users (in the order they appear in your metadata) in your extension's details page.Note:The recommended size for screenshots is 2400x1600 pixels. | [{"alt":"alternative text for image 1","url":"https://example.com/image1.png"},{"alt":"alternative text for image2","url":"https://example.com/image2.jpg"}] |
| com.docker.extension.detailed-description | Yes | Additional information in plain text or HTML about the extension to display in the details dialog. | My detailed descriptionor<h1>My detailed description</h1> |
| com.docker.extension.publisher-url | Yes | The publisher website URL to display in the details dialog. | https://example.com |
| com.docker.extension.additional-urls | No | A JSON array of titles and additional URLs displayed to users (in the order they appear in your metadata) in your extension's details page. Docker recommends you display the following links if they apply: documentation, support, terms of service, and privacy policy links. | [{"title":"Documentation","url":"https://example.com/docs"},{"title":"Support","url":"https://example.com/bar/support"},{"title":"Terms of Service","url":"https://example.com/tos"},{"title":"Privacy policy","url":"https://example.com/privacy"}] |
| com.docker.extension.changelog | Yes | Changelog in plain text or HTML containing the change for the current version only. | Extension changelogor<p>Extension changelog<ul><li>New feature A</li><li>Bug fix on feature B</li></ul></p> |
| com.docker.extension.account-info | No | Whether the user needs to register to a SaaS platform to use some features of the extension. | requiredin case it does, leave it empty otherwise. |
| com.docker.extension.categories | No | The list of Marketplace categories that your extension belongs to:ci-cd,container-orchestration,cloud-deployment,cloud-development,database,kubernetes,networking,image-registry,security,testing-tools,utility-tools,volumes. If you don't specify this label, users won't be able to find your extension in the Extensions Marketplace when filtering by a category. Extensions published to the Marketplace before the 22nd of September 2022 have been auto-categorized by Docker. | Specified as comma separated values in case of having multiple categories e.g:kubernetes,securityor a single value e.g.kubernetes. |

> Tip
>
> Docker Desktop applies CSS styles to the provided HTML content. You can make sure that it renders correctly
> [within the Marketplace](#preview-the-extension-in-the-marketplace). It is recommended that you follow the
> [styling guidelines](https://docs.docker.com/extensions/extensions-sdk/design/).

## Preview the extension in the Marketplace

You can validate that the image labels render as you expect.

When you create and install your unpublished extension, you can preview the extension in the Marketplace's **Managed** tab. You can see how the extension labels render in the list and in the details page of the extension.

> Preview extensions already listed in Marketplace
>
>
>
> When you install a local image of an extension already published in the Marketplace, for example with the tag `latest`, your local image is not detected as "unpublished".
>
>
>
> You can re-tag your image in order to have a different image name that's not listed as a published extension.
> Use `docker tag org/published-extension unpublished-extension` and then `docker extension install unpublished-extension`.

![List preview](https://docs.docker.com/extensions/extensions-sdk/extensions/images/list-preview.png)  ![List preview](https://docs.docker.com/extensions/extensions-sdk/extensions/images/list-preview.png)

---

# Build multi

> Step three in creating an extension.

# Build multi-arch extensions

   Table of contents

---

It is highly recommended that, at a minimum, your extension is supported for the following architectures:

- `linux/amd64`
- `linux/arm64`

Docker Desktop retrieves the extension image according to the user’s system architecture. If the extension does not provide an image that matches the user’s system architecture, Docker Desktop is not able to install the extension. As a result, users can’t run the extension in Docker Desktop.

## Build and push for multiple architectures

If you created an extension from the `docker extension init` command, the
`Makefile` at the root of the directory includes a target with name
`push-extension`.

You can run `make push-extension` to build your extension against both
`linux/amd64` and `linux/arm64` platforms, and push them to Docker Hub.

For example:

```console
$ make push-extension
```

Alternatively, if you started from an empty directory, use the command below
to build your extension for multiple architectures:

```console
$ docker buildx build --push --platform=linux/amd64,linux/arm64 --tag=username/my-extension:0.0.1 .
```

You can then check the image manifest to see if the image is available for both
architectures using the
[docker buildx imagetoolscommand](https://docs.docker.com/reference/cli/docker/buildx/imagetools/):

```console
$ docker buildx imagetools inspect username/my-extension:0.0.1
Name:      docker.io/username/my-extension:0.0.1
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:f3b552e65508d9203b46db507bb121f1b644e53a22f851185d8e53d873417c48

Manifests:
  Name:      docker.io/username/my-extension:0.0.1@sha256:71d7ecf3cd12d9a99e73ef448bf63ae12751fe3a436a007cb0969f0dc4184c8c
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/amd64

  Name:      docker.io/username/my-extension:0.0.1@sha256:5ba4ceea65579fdd1181dfa103cc437d8e19d87239683cf5040e633211387ccf
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm64
```

> Tip
>
> If you're having trouble pushing the image, make sure you're signed in to Docker Hub. Otherwise, run `docker login` to authenticate.

For more information, see
[Multi-platform images](https://docs.docker.com/build/building/multi-platform/) page.

## Adding multi-arch binaries

If your extension includes some binaries that deploy to the host, it’s important that they also have the right architecture when building the extension against multiple architectures.

Currently, Docker does not provide a way to explicitly specify multiple binaries for every architecture in the `metadata.json` file. However, you can add architecture-specific binaries depending on the `TARGETARCH` in the extension’s `Dockerfile`.

The following example shows an extension that uses a binary as part of its operations. The extension needs to run both in Docker Desktop for Mac and Windows.

In the `Dockerfile`, download the binary depending on the target architecture:

```Dockerfile
#syntax=docker/dockerfile:1.3-labs

FROM alpine AS dl
WORKDIR /tmp
RUN apk add --no-cache curl tar
ARG TARGETARCH
RUN <<EOT ash
    mkdir -p /out/darwin
    curl -fSsLo /out/darwin/kubectl "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/darwin/${TARGETARCH}/kubectl"
    chmod a+x /out/darwin/kubectl
EOT
RUN <<EOT ash
    if [ "amd64" = "$TARGETARCH" ]; then
        mkdir -p /out/windows
        curl -fSsLo /out/windows/kubectl.exe "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/windows/amd64/kubectl.exe"
    fi
EOT

FROM alpine
LABEL org.opencontainers.image.title="example-extension" \
    org.opencontainers.image.description="My Example Extension" \
    org.opencontainers.image.vendor="Docker Inc." \
    com.docker.desktop.extension.api.version=">= 0.3.3"

COPY --from=dl /out /
```

In the `metadata.json` file, specify the path for every binary on every platform:

```json
{
  "icon": "docker.svg",
  "ui": {
    "dashboard-tab": {
      "title": "Example Extension",
      "src": "index.html",
      "root": "ui"
    }
  },
  "host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/kubectl"
          }
        ],
        "windows": [
          {
            "path": "/windows/kubectl.exe"
          }
        ]
      }
    ]
  }
}
```

As a result, when `TARGETARCH` equals:

- `arm64`, the `kubectl` binary fetched corresponds to the `arm64` architecture, and is copied to `/darwin/kubectl` in the final stage.
- `amd64`, two `kubectl` binaries are fetched. One for Darwin and another for Windows. They are copied to `/darwin/kubectl` and `/windows/kubectl.exe` respectively, in the final stage.

> Note
>
> The binary destination path for Darwin is `darwin/kubectl` in both cases. The only change is the architecture-specific binary that is downloaded.

When the extension is installed, the extension framework copies the binaries from the extension image at `/darwin/kubectl` for Darwin, or `/windows/kubectl.exe` for Windows, to a specific location in the user’s host filesystem.

## Can I develop extensions that run Windows containers?

Although Docker Extensions is supported on Docker Desktop for Windows, Mac, and Linux, the extension framework only supports Linux containers. Therefore, you must target `linux` as the OS when you build your extension image.

---

# Publish in the Marketplace

> Docker extension distribution

# Publish in the Marketplace

   Table of contents

---

## Submit your extension to the Marketplace

Docker Desktop displays published extensions in the Extensions Marketplace on [Docker Desktop](https://open.docker.com/extensions/marketplace) and [Docker Hub](https://hub.docker.com/search?q=&type=extension).
The Extensions Marketplace is a space where developers can discover extensions to improve their developer experience and propose their own extension to be available for all Desktop users.

Whenever you are [ready to publish](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/) your extension in the Marketplace, you can [self-publish your extension](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)

> Note
>
> As the Extension Marketplace continues to add new features for both Extension users and publishers, you are expected
> to maintain your extension over time to ensure it stays available in the Marketplace.

> Important
>
> The Docker manual review process for extensions is paused at the moment. Submit your extension through the [automated submission process](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)

### Before you submit

Before you submit your extension, it must pass the [validation](https://docs.docker.com/extensions/extensions-sdk/extensions/validate/) checks.

It is highly recommended that your extension follows the guidelines outlined in this section before submitting your
extension. If you request a review from the Docker Extensions team and have not followed the guidelines, the review process may take longer.

These guidelines don't replace Docker's terms of service or guarantee approval:

- Review the [design guidelines](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/)
- Ensure the [UI styling](https://docs.docker.com/extensions/extensions-sdk/design/) is in line with Docker Desktop guidelines
- Ensure your extensions support both light and dark mode
- Consider the needs of both new and existing users of your extension
- Test your extension with potential users
- Test your extension for crashes, bugs, and performance issues
- Test your extension on various platforms (Mac, Windows, Linux)
- Read the [Terms of Service](https://www.docker.com/legal/extensions_marketplace_developer_agreement/)

#### Validation process

Submitted extensions go through an automated validation process. If all the validation checks pass successfully, the extension is
published on the Marketplace and accessible to all users within a few hours.
It is the fastest way to get developers the tools they need and to get feedback from them as you work to
evolve/polish your extension.

> Important
>
> Docker Desktop caches the list of extensions available in the Marketplace for 12 hours. If you don't see your
> extension in the Marketplace, you can restart Docker Desktop to force the cache to refresh.
