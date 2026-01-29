# Configure Settings Management with a JSON file

# Configure Settings Management with a JSON file

> Configure and enforce Docker Desktop settings using an admin-settings.json file

# Configure Settings Management with a JSON file

   Table of contents

---

Subscription: Business For: Administrators

Settings Management lets you configure and enforce Docker Desktop settings across your organization using an `admin-settings.json` file. This standardizes Docker Desktop environments and ensures consistent configurations for all users.

## Prerequisites

Before you begin, make sure you have:

- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) for
  your organization
- A Docker Business subscription

Docker Desktop only applies settings from the `admin-settings.json` file when both authentication and Docker Business license checks succeed.

> Important
>
> Users must be signed in and part of a Docker Business organization. If either condition isn't met, the settings file is ignored.

## Step one: Create the settings file

You can create the `admin-settings.json` file in two ways:

- Use the `--admin-settings` installer flag to auto-generate the file:
  - [macOS](https://docs.docker.com/desktop/setup/install/mac-install/#install-from-the-command-line) installation guide
  - [Windows](https://docs.docker.com/desktop/setup/install/windows-install/#install-from-the-command-line) installation guide
- Create it manually (UTF-8 without BOM) and place it in the following locations:
  - Mac: `/Library/Application\ Support/com.docker.docker/admin-settings.json`
  - Windows: `C:\ProgramData\DockerDesktop\admin-settings.json`
  - Linux: `/usr/share/docker-desktop/admin-settings.json`

> Important
>
> Place the file in a protected directory to prevent unauthorized changes. Use Mobile Device Management (MDM) tools like Jamf to distribute the file at scale across your organization.

## Step two: Configure settings

> Tip
>
> For a complete list of available settings, their supported platforms, and which configuration methods they work with, see the [Settings reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/).

The `admin-settings.json` file uses structured keys to define configurable settings and whether values are enforced.

Each setting supports a `locked` field that controls user permissions:

- When `locked` is set to `true`, users can't change that value in Docker Desktop, the CLI, or config files.
- When `locked` is set to `false`, the value acts like a default suggestion and users
  can still update it.

Settings where `locked` is set to `false` are ignored on existing installs if
a user has already customized that value in `settings-store.json`,
`settings.json`, or `daemon.json`.

### Grouped settings

Docker Desktop groups some settings together with a single toggle that controls
the entire section. These include:

- Enhanced Container Isolation (ECI): Uses a main toggle (`enhancedContainerIsolation`) that enables/disables the entire feature, with sub-settings for specific configurations
- Kubernetes: Uses a main toggle (`kubernetes.enabled`) with sub-settings for cluster configuration
- Docker Scout: Groups settings under the `scout` object

When configuring grouped settings:

1. Set the main toggle to enable the feature
2. Configure sub-settings within that group
3. When you lock the main toggle, users cannot modify any settings in that group

Example for `enhancedContainerIsolation`:

```json
"enhancedContainerIsolation": {
  "locked": true,  // This locks the entire ECI section
  "value": true,   // This enables ECI
  "dockerSocketMount": {  // These are sub-settings
    "imageList": {
      "images": ["docker.io/testcontainers/ryuk:*"]
    }
  }
}
```

### Exampleadmin-settings.jsonfile

The following sample is an `admin-settings.json` file with common enterprise settings configured. You can use this example as a template with the [admin-settings.jsonconfigurations](#admin-settingsjson-configurations):

```json
{
  "configurationFileVersion": 2,
  "exposeDockerAPIOnTCP2375": {
    "locked": true,
    "value": false
  },
  "proxy": {
    "locked": true,
    "mode": "system",
    "http": "",
    "https": "",
    "exclude": [],
    "windowsDockerdPort": 65000,
    "enableKerberosNtlm": false,
    "pac": "",
    "embeddedPac": ""
  },
  "containersProxy": {
    "locked": true,
    "mode": "manual",
    "http": "",
    "https": "",
    "exclude": [],
    "pac":"",
    "embeddedPac": "",
    "transparentPorts": ""
  },
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*"
        ]
      },
      "commandList": {
        "type": "deny",
        "commands": ["push"]
      }
    }
  },
  "linuxVM": {
    "wslEngineEnabled": {
      "locked": false,
      "value": false
    },
    "dockerDaemonOptions": {
      "locked": false,
      "value":"{\"debug\": false}"
    },
    "vpnkitCIDR": {
      "locked": false,
      "value":"192.168.65.0/24"
    }
  },
  "kubernetes": {
     "locked": false,
     "enabled": false,
     "showSystemContainers": false,
     "imagesRepository": ""
  },
  "windowsContainers": {
    "dockerDaemonOptions": {
      "locked": false,
      "value":"{\"debug\": false}"
    }
  },
  "disableUpdate": {
    "locked": false,
    "value": false
  },
  "analyticsEnabled": {
    "locked": false,
    "value": true
  },
  "extensionsEnabled": {
    "locked": true,
    "value": false
  },
  "scout": {
    "locked": false,
    "sbomIndexing": true,
    "useBackgroundIndexing": true
  },
  "allowBetaFeatures": {
    "locked": false,
    "value": false
  },
  "blockDockerLoad": {
    "locked": false,
    "value": true
  },
  "filesharingAllowedDirectories": [
    {
      "path": "$HOME",
      "sharedByDefault": true
    },
    {
      "path":"$TMP",
      "sharedByDefault": false
    }
  ],
  "useVirtualizationFrameworkVirtioFS": {
    "locked": true,
    "value": true
  },
  "useVirtualizationFrameworkRosetta": {
    "locked": true,
    "value": true
  },
  "useGrpcfuse": {
    "locked": true,
    "value": true
  },
  "displayedOnboarding": {
    "locked": true,
    "value": true
  },
  "desktopTerminalEnabled": {
    "locked": false,
    "value": false
  },
  "enableInference": {
    "locked": false,
    "value": true
  },
  "enableInferenceTCP": {
    "locked": false,
    "value": true
  },
  "enableInferenceTCPPort": {
    "locked": true,
    "value": 12434
  },
  "enableInferenceCORS": {
    "locked": true,
    "value": ""
  },
  "enableInferenceGPUVariant": {
    "locked": true,
    "value": true
  },
  "portBindingBehavior": {
    "locked": true,
    "value": "default-port-binding"
  }
}
```

## Step three: Apply the settings

Settings take effect after Docker Desktop restarts and the user signs in.

For new installations:

1. Launch Docker Desktop.
2. Sign in with your Docker account.

For existing installations:

1. Quit Docker Desktop completely.
2. Relaunch Docker Desktop.

> Important
>
> You must fully quit and reopen Docker Desktop. Restarting from the menu isn't sufficient.

## admin-settings.jsonconfigurations

The following tables describe all available settings in the `admin-settings.json` file.

> Note
>
> Some settings are platform-specific or require minimum Docker Desktop versions. Check the Version column for requirements.

### General settings

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| configurationFileVersion |  | Specifies the version of the configuration file format. |  |
| analyticsEnabled |  | Ifvalueis set to false, Docker Desktop doesn't send usage statistics to Docker. |  |
| disableUpdate |  | Ifvalueis set to true, checking for and notifications about Docker Desktop updates is disabled. |  |
| blockDockerLoad |  | Ifvalueis set totrue, users are no longer able to rundocker loadand receive an error if they try to. |  |
| displayedOnboarding |  | Ifvalueis set totrue, the onboarding survey will not be displayed to new users. Settingvaluetofalsehas no effect. | Docker Desktop version 4.30 and later |
| desktopTerminalEnabled |  | Ifvalueis set tofalse, developers cannot use the Docker terminal to interact with the host machine and execute commands directly from Docker Desktop. |  |
| exposeDockerAPIOnTCP2375 | Windows only | Exposes the Docker API on a specified port. Ifvalueis set to true, the Docker API is exposed on port 2375. Note: This is unauthenticated and should only be enabled if protected by suitable firewall rules. |  |
| silentModulesUpdate |  | Ifvalueis set totrue, Docker Desktop automatically updates components that don't require a restart. For example, the Docker CLI or Docker Scout components. | Docker Desktop version 4.46 and later. |

### Extensions

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| extensionsEnabled |  | Ifvalueis set to false, Docker Extensions are disabled. |  |
| onlyMarketplaceExtensions |  | Ifvalueis set to true, developers are blocked from installing other extensions via the command line. |  |
| extensionsPrivateMarketplace |  | Ifvalueis set to true, activates the private marketplace is enabled which ensures Docker Desktop connects to content defined and controlled by the administrator instead of the public Docker marketplace. |  |
| extensionsPrivateMarketplaceAdminContactURL |  | Defines a contact link for developers to request new extensions in the private marketplace. |  |

### File sharing and emulation

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| filesharingAllowedDirectories |  | Specify which paths your developers can add file shares to. Also accepts$HOME,$TMP, or$TEMPaspathvariables. When a path is added, its subdirectories are allowed. IfsharedByDefaultis set totrue, that path will be added upon factory reset or when Docker Desktop first starts. |  |
| useVirtualizationFrameworkVirtioFS | macOS only | Ifvalueis set totrue, VirtioFS is set as the file sharing mechanism. Note: If bothuseVirtualizationFrameworkVirtioFSanduseGrpcfusehavevalueset totrue, VirtioFS takes precedence. Likewise, if bothuseVirtualizationFrameworkVirtioFSanduseGrpcfusehavevalueset tofalse, osxfs is set as the file sharing mechanism. |  |
| useGrpcfuse | macOS only | Ifvalueis set totrue, gRPC Fuse is set as the file sharing mechanism. |  |
| useVirtualizationFrameworkRosetta | macOS only | Ifvalueis set totrue, Docker Desktop turns on Rosetta to accelerate x86_64/amd64 binary emulation on Apple Silicon. Note: This also automatically enablesUse Virtualization framework. | Docker Desktop version 4.29 and later. |

### Docker Scout

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| scout |  | SettinguseBackgroundIndexingtofalsedisables automatic indexing of images loaded to the image store. SettingsbomIndexingtofalseprevents users from being able to index image by inspecting them in Docker Desktop or usingdocker scoutCLI commands. |  |

### Proxy settings

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| proxy |  | Ifmodeis set tosysteminstead ofmanual, Docker Desktop gets the proxy values from the system and ignores and values set forhttp,httpsandexclude. Changemodetomanualto manually configure proxy servers. If the proxy port is custom, specify it in thehttporhttpsproperty, for example"https": "http://myotherproxy.com:4321". Theexcludeproperty specifies a comma-separated list of hosts and domains to bypass the proxy. |  |
| windowsDockerdPort | Windows only | Exposes Docker Desktop's internal proxy locally on this port for the Windows Docker daemon to connect to. If it is set to 0, a random free port is chosen. If the value is greater than 0, use that exact value for the port. The default value is -1 which disables the option. |  |
| enableKerberosNtlm |  | When set totrue, Kerberos and NTLM authentication is enabled. Default isfalse. For more information, see the settings documentation. | Docker Desktop version 4.32 and later. |
| pac |  | Specifies a PAC file URL. For example,"pac": "http://proxy/proxy.pac". |  |
| embeddedPac |  | Specifies an embedded PAC (Proxy Auto-Config) script. For example,"embeddedPac": "function FindProxyForURL(url, host) { return \"DIRECT\"; }". This setting takes precedence over HTTP, HTTPS, Proxy bypass and PAC server URL. | Docker Desktop version 4.46 and later. |

### Container proxy

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| containersProxy |  | Creates air-gapped containers. For more information seeAir-Gapped Containers. | Docker Desktop version 4.29 and later. |
| pac |  | Specifies a PAC file URL. For example,"pac": "http://containerproxy/proxy.pac". |  |
| embeddedPac |  | Specifies an embedded PAC (Proxy Auto-Config) script. For example,"embeddedPac": "function FindProxyForURL(url, host) { return \"PROXY 192.168.92.1:2003\"; }". This setting takes precedence over HTTP, HTTPS, Proxy bypass and PAC server URL. | Docker Desktop version 4.46 and later. |

### Linux VM settings

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| linuxVM |  | Parameters and settings related to Linux VM options - grouped together here for convenience. |  |
| wslEngineEnabled | Windows only | Ifvalueis set to true, Docker Desktop uses the WSL 2 based engine. This overrides anything that may have been set at installation using the--backend=<backend name>flag. |  |
| dockerDaemonOptions |  | Ifvalueis set to true, it overrides the options in the Docker Engine config file. See theDocker Engine reference. Note that for added security, a few of the config attributes may be overridden when Enhanced Container Isolation is enabled. |  |
| vpnkitCIDR |  | Overrides the network range used for vpnkit DHCP/DNS for*.docker.internal |  |

### Windows containers

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| windowsContainers |  | Parameters and settings related towindowsContainersoptions - grouped together here for convenience. |  |
| dockerDaemonOptions |  | Overrides the options in the Linux daemon config file. See theDocker Engine reference. |  |

> Note
>
> This setting is not available to configure via the Docker Admin Console.

### Kubernetes settings

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| kubernetes |  | Ifenabledis set to true, a Kubernetes single-node cluster is started when Docker Desktop starts. IfshowSystemContainersis set to true, Kubernetes containers are displayed in the Docker Desktop Dashboard and when you rundocker ps. TheimagesRepositorysetting lets you specify which repository Docker Desktop pulls control-plane Kubernetes images from. |  |

> Note
>
> When using `imagesRepository` with Enhanced Container Isolation (ECI), add these images to the [ECI Docker socket mount image list](#enhanced-container-isolation):
>
>
>
> `[imagesRepository]/desktop-cloud-provider-kind:` `[imagesRepository]/desktop-containerd-registry-mirror:`
>
>
>
> These containers mount the Docker socket, so you must add them to the ECI images list. Otherwise, ECI blocks the mount and Kubernetes won't start.

### Networking settings

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| defaultNetworkingMode | Windows and Mac only | Defines the default IP protocol for new Docker networks:dual-stack(IPv4 + IPv6, default),ipv4only, oripv6only. | Docker Desktop version 4.43 and later. |
| dnsInhibition | Windows and Mac only | Controls DNS record filtering returned to containers. Options:auto(recommended),ipv4,ipv6,none | Docker Desktop version 4.43 and later. |
| portBindingBehavior | Linux-based containers only | Defines port binding restrictions and default behavior, allowing admins to control how a user exposes ports from their containers. Options:default-port-binding,default-local-port-binding,local-only-port-binding | Docker Desktop version 4.52 and later. |

For more information, see
[Networking](https://docs.docker.com/desktop/features/networking/#networking-mode-and-dns-behaviour-for-mac-and-windows).

### AI settings

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| enableInference |  | SettingenableInferencetotrueenablesDocker Model Runner. |  |
| enableInferenceTCP |  | Enable host-side TCP support. This setting requires the Docker Model Runner setting to be enabled first. |  |
| enableInferenceTCPPort |  | Specifies the exposed TCP port. This setting requires the Docker Model Runner and Enable host-side TCP support settings to be enabled first. |  |
| enableInferenceCORS |  | Specifies the allowed CORS origins. Empty string to deny all,*to accept all, or a list of comma-separated values. This setting requires the Docker Model Runner and Enable host-side TCP support settings to be enabled first. |  |
| enableInferenceGPUVariant | Windows only | SettingenableInferenceGPUVarianttotrueenables GPU-backed inference. The additional components required for this don't come by default with Docker Desktop, therefore they will be downloaded to~/.docker/bin/inference. |  |

### Beta features

> Important
>
> For Docker Desktop versions 4.41 and earlier, some of these settings lived under the **Experimental features** tab on the **Features in development** page.

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| allowBetaFeatures |  | Ifvalueis set totrue, beta features are enabled. |  |
| enableDockerAI |  | IfallowBetaFeaturesis true, settingenableDockerAItotrueenablesDocker AI (Ask Gordon)by default. You can independently control this setting from theallowBetaFeaturessetting. |  |
| enableDockerMCPToolkit |  | IfallowBetaFeaturesis true, settingenableDockerMCPToolkittotrueenables theMCP Toolkit featureby default. You can independently control this setting from theallowBetaFeaturessetting. |  |
| allowExperimentalFeatures |  | Ifvalueis set totrue, experimental features are enabled. | Docker Desktop version 4.41 and earlier |

### Enhanced Container Isolation

| Parameter | OS | Description | Version |
| --- | --- | --- | --- |
| enhancedContainerIsolation |  | Ifvalueis set to true, Docker Desktop runs all containers as unprivileged, via the Linux user-namespace, prevents them from modifying sensitive configurations inside the Docker Desktop VM, and uses other advanced techniques to isolate them. For more information, seeEnhanced Container Isolation. |  |
| dockerSocketMount |  | By default, enhanced container isolation blocks bind-mounting the Docker Engine socket into containers (e.g.,docker run -v /var/run/docker.sock:/var/run/docker.sock ...). This lets you relax this in a controlled way. SeeECI Configurationfor more info. |  |
| imageList |  | Indicates which container images are allowed to bind-mount the Docker Engine socket. |  |
| commandList |  | Restricts the commands that containers can issue via the bind-mounted Docker Engine socket. |  |
