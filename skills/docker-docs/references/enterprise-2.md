# Configure sign and more

# Configure sign

> Configure sign-in enforcement for Docker Desktop using registry keys, configuration profiles, plist files, or registry.json files

# Configure sign-in enforcement

   Table of contents

---

Subscription: Team  Business For: Administrators

You can enforce sign-in for Docker Desktop using several methods. Choose the method that best fits your organization's infrastructure and security requirements.

## Choose your method

| Method | Platform |
| --- | --- |
| Registry key | Windows only |
| Configuration profiles | macOS only |
| plistfile | macOS only |
| registry.json | All platforms |

> Tip
>
> For macOS, configuration profiles offer the highest security because they're
> protected by Apple's System Integrity Protection (SIP).

## Windows: Registry key method

To configure the registry key method manually:

1. Create the registry key:
  ```console
  $ HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop
  ```
2. Create a multi-string value name `allowedOrgs`.
3. Use your organization names as string data:
  - Use lowercase letters only
  - Add each organization on a separate line
  - Do not use spaces or commas as separators
4. Restart Docker Desktop.
5. Verify the `Sign in required!` prompt appears in Docker Desktop.

> Important
>
> You can add multiple organizations with Docker Desktop version 4.36 and later.
> With version 4.35 and earlier, adding multiple organizations causes sign-in
> enforcement to fail silently.

Deploy the registry key across your organization using Group Policy:

1. Create a registry script with the required key structure.
2. In Group Policy Management, create or edit a GPO.
3. Navigate to **Computer Configuration** > **Preferences** > **Windows Settings** > **Registry**.
4. Right-click **Registry** > **New** > **Registry Item**.
5. Configure the registry item:
  - Action: **Update**
  - Path: `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop`
  - Value name: `allowedOrgs`
  - Value data: Your organization names
6. Link the GPO to the target Organizational Unit.
7. Test on a small group using `gpupdate/force`.
8. Deploy organization-wide after verification.

## macOS: Configuration profiles method (recommended)

Requires: Docker Desktop 4.36 and later

Configuration profiles provide the most secure enforcement method for macOS, as they're protected by Apple's System Integrity Protection.

The payload is a dictionary of key-values. Docker Desktop supports the following keys:

- `allowedOrgs`: Sets a list of organizations in one single string, where each organization is separated by a semi-colon.

In Docker Desktop version 4.48 and later, the following keys are also supported:

- `overrideProxyHTTP`: Sets the URL of the HTTP proxy that must be used for outgoing HTTP requests.
- `overrideProxyHTTPS`: Sets the URL of the HTTP proxy that must be used for outgoing HTTPS requests.
- `overrideProxyExclude`: Bypasses proxy settings for the specified hosts and domains. Uses a comma-separated list.
- `overrideProxyPAC`: Sets the file path where the PAC file is located. It has precedence over the remote PAC file on the selected proxy.
- `overrideProxyEmbeddedPAC`: Sets the content of an in-memory PAC file. It has precedence over `overrideProxyPAC`.

Overriding at least one of the proxy settings via Configuration profiles will automatically lock the settings as they're managed by macOS.

1. Create a file named `docker.mobileconfig` and include the following content:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
     <key>PayloadContent</key>
     <array>
        <dict>
           <key>PayloadType</key>
           <string>com.docker.config</string>
           <key>PayloadVersion</key>
           <integer>1</integer>
           <key>PayloadIdentifier</key>
           <string>com.docker.config</string>
           <key>PayloadUUID</key>
           <string>eed295b0-a650-40b0-9dda-90efb12be3c7</string>
           <key>PayloadDisplayName</key>
           <string>Docker Desktop Configuration</string>
           <key>PayloadDescription</key>
           <string>Configuration profile to manage Docker Desktop settings.</string>
           <key>PayloadOrganization</key>
           <string>Your Company Name</string>
           <key>allowedOrgs</key>
           <string>first_org;second_org</string>
           <key>overrideProxyHTTP</key>
           <string>http://company.proxy:port</string>
           <key>overrideProxyHTTPS</key>
           <string>https://company.proxy:port</string>
        </dict>
     </array>
     <key>PayloadType</key>
     <string>Configuration</string>
     <key>PayloadVersion</key>
     <integer>1</integer>
     <key>PayloadIdentifier</key>
     <string>com.yourcompany.docker.config</string>
     <key>PayloadUUID</key>
     <string>0deedb64-7dc9-46e5-b6bf-69d64a9561ce</string>
     <key>PayloadDisplayName</key>
     <string>Docker Desktop Config Profile</string>
     <key>PayloadDescription</key>
     <string>Config profile to enforce Docker Desktop settings for allowed organizations.</string>
     <key>PayloadOrganization</key>
     <string>Your Company Name</string>
  </dict>
  </plist>
  ```
2. Replace placeholders:
  - Change `com.yourcompany.docker.config` to your company identifier
  - Replace `Your Company Name` with your organization name
  - Replace `PayloadUUID` with a randomly generated UUID
  - Update the `allowedOrgs` value with your organization names (separated by semicolons)
  - Replace `company.proxy:port` with http/https proxy server host(or IP address) and port
3. Deploy the profile using your MDM solution.
4. Verify the profile appears in **System Settings** > **General** > **Device Management** under **Device (Managed)**. Ensure the profile is listed with the correct name and settings.

Some MDM solutions let you specify the payload as a plain dictionary of key-value settings without the full `.mobileconfig` wrapper:

```xml
<dict>
   <key>allowedOrgs</key>
   <string>first_org;second_org</string>
   <key>overrideProxyHTTP</key>
   <string>http://company.proxy:port</string>
   <key>overrideProxyHTTPS</key>
   <string>https://company.proxy:port</string>
</dict>
```

## macOS: plist file method

Use this alternative method for macOS with Docker Desktop version 4.32 and later.

1. Create the file `/Library/Application Support/com.docker.docker/desktop.plist`.
2. Add this content, replacing `myorg1` and `myorg2` with your organization names:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
    <dict>
        <key>allowedOrgs</key>
        <array>
            <string>myorg1</string>
            <string>myorg2</string>
        </array>
    </dict>
  </plist>
  ```
3. Set file permissions to prevent editing by non-administrator users.
4. Restart Docker Desktop.
5. Verify the `Sign in required!` prompt appears in Docker Desktop.

Create and deploy a script for organization-wide distribution:

```bash
#!/bin/bash

# Create directory if it doesn't exist
sudo mkdir -p "/Library/Application Support/com.docker.docker"

# Write the plist file
sudo defaults write "/Library/Application Support/com.docker.docker/desktop.plist" allowedOrgs -array "myorg1" "myorg2"

# Set appropriate permissions
sudo chmod 644 "/Library/Application Support/com.docker.docker/desktop.plist"
sudo chown root:admin "/Library/Application Support/com.docker.docker/desktop.plist"
```

Deploy this script using SSH, remote support tools, or your preferred deployment method.

## All platforms: registry.json method

The registry.json method works across all platforms and offers flexible deployment options.

### File locations

Create the `registry.json` file (UTF-8 without BOM) at the appropriate location:

| Platform | Location |
| --- | --- |
| Windows | /ProgramData/DockerDesktop/registry.json |
| Mac | /Library/Application Support/com.docker.docker/registry.json |
| Linux | /usr/share/docker-desktop/registry/registry.json |

### Basic setup

1. Ensure users are members of your Docker organization.
2. Create the `registry.json` file at the appropriate location for your platform.
3. Add this content, replacing organization names with your own:
  ```json
  {
     "allowedOrgs": ["myorg1", "myorg2"]
  }
  ```
4. Set file permissions to prevent user editing.
5. Restart Docker Desktop.
6. Verify the `Sign in required!` prompt appears in Docker Desktop.

> Tip
>
> If users have issues starting Docker Desktop after enforcing sign-in,
> they may need to update to the latest version.

#### Windows (PowerShell as Administrator)

```shell
Set-Content /ProgramData/DockerDesktop/registry.json '{"allowedOrgs":["myorg1","myorg2"]}'
```

#### macOS

```console
sudo mkdir -p "/Library/Application Support/com.docker.docker"
echo '{"allowedOrgs":["myorg1","myorg2"]}' | sudo tee "/Library/Application Support/com.docker.docker/registry.json"
```

#### Linux

```console
sudo mkdir -p /usr/share/docker-desktop/registry
echo '{"allowedOrgs":["myorg1","myorg2"]}' | sudo tee /usr/share/docker-desktop/registry/registry.json
```

Create the registry.json file during Docker Desktop installation:

#### Windows

```shell
# PowerShell
Start-Process '.\Docker Desktop Installer.exe' -Wait 'install --allowed-org=myorg'

# Command Prompt
"Docker Desktop Installer.exe" install --allowed-org=myorg
```

#### macOS

```console
sudo hdiutil attach Docker.dmg
sudo /Volumes/Docker/Docker.app/Contents/MacOS/install --allowed-org=myorg
sudo hdiutil detach /Volumes/Docker
```

## Method precedence

When multiple configuration methods exist on the same system, Docker Desktop uses this precedence order:

1. Registry key (Windows only)
2. Configuration profiles (macOS only)
3. plist file (macOS only)
4. registry.json file

> Important
>
> Docker Desktop version 4.36 and later supports multiple organizations in a single configuration. Earlier versions (4.35 and below) fail silently when multiple organizations are specified.

## Troubleshoot sign-in enforcement

If sign-in enforcement doesn't work:

- Verify file locations and permissions
- Check that organization names use lowercase letters
- Restart Docker Desktop or reboot the system
- Confirm users are members of the specified organizations
- Update Docker Desktop to the latest version

---

# Enforce sign

> Require users to sign in to Docker Desktop to access organization benefits and security features

# Enforce sign-in for Docker Desktop

   Table of contents

---

Subscription: Team  Business For: Administrators

By default, users can access Docker Desktop without signing in to your organization.
When users don't sign in as organization members, they miss out on subscription benefits and can bypass security features configured for your organization.

You can enforce sign-in using several methods, depending on your setup:

- [Registry key method (Windows only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#registry-key-method-windows-only)
- [Configuration profiles method (Mac only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#configuration-profiles-method-mac-only)
- [.plistmethod (Mac only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#plist-method-mac-only)
- [registry.jsonmethod (All)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#registryjson-method-all)

This page provides an overview of how sign-in enforcement works.

## How sign-in enforcement works

When Docker Desktop detects a registry key, `.plist` file, or
`registry.json` file:

- A `Sign in required!` prompt appears, requiring users to sign
  in as organization members to use Docker Desktop.
- If users sign in with accounts that aren't organization members, they're
  automatically signed out and can't use Docker Desktop. They can select **Sign in**
  to try again with a different account.
- When users sign in with organization member accounts, they can use Docker
  Desktop normally.
- When users sign out, the `Sign in required!` prompt reappears and they can
  no longer use Docker Desktop unless they sign back in.

> Note
>
> Enforcing sign-in for Docker Desktop doesn't affect Docker CLI access. CLI access is only restricted for organizations that enforce single sign-on (SSO).

## Enforcing sign-in versus enforcing single sign-on (SSO)

Enforcing Docker Desktop sign-in and
[enforcing SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/#optional-enforce-sso) are different features that serve different purposes:

| Enforcement | Description | Benefits |
| --- | --- | --- |
| Enforce sign-in only | Users must sign in before using Docker Desktop | Ensures users receive the benefits of your subscription and ensures security features are applied. In addition, you gain insights into users’ activity. |
| Enforce single sign-on (SSO) only | If users sign in, they must sign in using SSO | Centralizes authentication and enforces unified policies set by the identity provider. |
| Enforce both | Users must sign in using SSO before using Docker Desktop | Ensures users receive the benefits of your subscription and ensures security features are applied. In addition, you gain insights into users’ activity. It also centralizes authentication and enforces unified policies set by the identity provider. |
| Enforce neither | If users sign in, they can use SSO or their Docker credentials | Lets users access Docker Desktop without barriers, at the cost of reduced security and insights. |

## Next steps

- To set up sign-in enforcement, see
  [Configure sign-in enforcement](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/).
- To configure SSO enforcement, see
  [Enforce SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/).

---

# Air

> Control container network access with air-gapped containers using custom proxy rules and network restrictions

# Air-gapped containers

   Table of contents

---

Requires: Docker Desktop
[4.29.0](https://docs.docker.com/desktop/release-notes/#4290) and later

Air-gapped containers let you restrict container network access by controlling where containers can send and receive data. This feature applies custom proxy rules to container network traffic, helping secure environments where containers shouldn't have unrestricted internet access.

Docker Desktop can configure container network traffic to accept connections, reject connections, or tunnel through HTTP or SOCKS proxies. You control which TCP ports the policy applies to and whether to use a single proxy or per-destination policies via Proxy Auto-Configuration (PAC) files.

This page provides an overview of air-gapped containers and configuration steps.

## Who should use air-gapped containers?

Air-gapped containers help organizations maintain security in restricted environments:

- Secure development environments: Prevent containers from accessing unauthorized external services
- Compliance requirements: Meet regulatory standards that require network isolation
- Data loss prevention: Block containers from uploading sensitive data to external services
- Supply chain security: Control which external resources containers can access during builds
- Corporate network policies: Enforce existing network security policies for containerized applications

## How air-gapped containers work

Air-gapped containers operate by intercepting container network traffic and applying proxy rules:

1. Traffic interception: Docker Desktop intercepts all outgoing network connections from containers
2. Port filtering: Only traffic on specified ports (`transparentPorts`) is subject to proxy rules
3. Rule evaluation: PAC file rules or static proxy settings determine how to handle each connection
4. Connection handling: Traffic is allowed directly, routed through a proxy, or blocked based on the rules

Some important considerations include:

- The existing `proxy` setting continues to apply to Docker Desktop application traffic on the host
- If PAC file download fails, containers block requests to target URLs
- Hostname is available for ports 80 and 443, but only IP addresses for other ports

## Prerequisites

Before configuring air-gapped containers, you must have:

- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) enabled to ensure users authenticate with your organization
- A Docker Business subscription
- Configured
  [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/) to manage organization policies
- Downloaded Docker Desktop 4.29 or later

## Configure air-gapped containers

Add the container proxy to your
[admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/). For example:

```json
{
  "configurationFileVersion": 2,
  "containersProxy": {
    "locked": true,
    "mode": "manual",
    "http": "",
    "https": "",
    "exclude": [],
    "pac": "http://192.168.1.16:62039/proxy.pac",
    "transparentPorts": "*"
  }
}
```

### Configuration parameters

The `containersProxy` setting controls network policies applied to container traffic:

| Parameter | Description | Value |
| --- | --- | --- |
| locked | Prevents developers from overriding settings | true(locked),false(default) |
| mode | Proxy configuration method | system(use system proxy),manual(custom) |
| http | HTTP proxy server | URL (e.g.,"http://proxy.company.com:8080") |
| https | HTTPS proxy server | URL (e.g.,"https://proxy.company.com:8080") |
| exclude | Bypass proxy for these addresses | Array of hostnames/IPs |
| pac | Proxy Auto-Configuration file URL | URL to PAC file |
| transparentPorts | Ports subject to proxy rules | Comma-separated ports or wildcard ("*") |

### Configuration examples

Block all external access:

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "",
  "https": "",
  "exclude": [],
  "transparentPorts": "*"
}
```

Allow specific internal services:

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "",
  "https": "",
  "exclude": ["internal.company.com", "10.0.0.0/8"],
  "transparentPorts": "80,443"
}
```

Route through corporate proxy:

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "http://corporate-proxy.company.com:8080",
  "https": "http://corporate-proxy.company.com:8080",
  "exclude": ["localhost", "*.company.local"],
  "transparentPorts": "*"
}
```

## Proxy Auto-Configuration (PAC) files

PAC files provide fine-grained control over container network access by defining rules for different destinations.

### Basic PAC file structure

```javascript
function FindProxyForURL(url, host) {
	if (localHostOrDomainIs(host, 'internal.corp')) {
		return "PROXY 10.0.0.1:3128";
	}
	if (isInNet(host, "192.168.0.0", "255.255.255.0")) {
	    return "DIRECT";
	}
    return "PROXY reject.docker.internal:1234";
}
```

### General considerations

- `FindProxyForURL` function URL parameter format is http://host_or_ip:port or https://host_or_ip:port
- If you have an internal container trying to access [https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers) the docker proxy service will submit docs.docker.com for the host value and [https://docs.docker.com:443](https://docs.docker.com:443) for the url value to FindProxyForURL, if you are using `shExpMatch` function in your PAC file as follows:
  ```console
  if(shExpMatch(url, "https://docs.docker.com:443/enterprise/security/*")) return "DIRECT";
  ```
  `shExpMatch` function will fail, instead use:
  ```console
  if (host == docs.docker.com && url.indexOf(":443") > 0) return "DIRECT";
  ```

### PAC file return values

| Return value | Action |
| --- | --- |
| PROXY host:port | Route through HTTP proxy at specified host and port |
| SOCKS5 host:port | Route through SOCKS5 proxy at specified host and port |
| DIRECT | Allow direct connection without proxy |
| PROXY reject.docker.internal:any_port | Block the request completely |

### Advanced PAC file example

```javascript
function FindProxyForURL(url, host) {
  // Allow access to Docker Hub for approved base images
  if (dnsDomainIs(host, ".docker.io") || host === "docker.io") {
    return "PROXY corporate-proxy.company.com:8080";
  }

  // Allow internal package repositories
  if (localHostOrDomainIs(host, 'nexus.company.com') ||
      localHostOrDomainIs(host, 'artifactory.company.com')) {
    return "DIRECT";
  }

  // Allow development tools on specific ports
  if (url.indexOf(":3000") > 0 || url.indexOf(":8080") > 0) {
    if (isInNet(host, "10.0.0.0", "255.0.0.0")) {
      return "DIRECT";
    }
  }

  // Block access to developer's localhost
  if (host === "host.docker.internal" || host === "localhost") {
    return "PROXY reject.docker.internal:1234";
  }

  // Block all other external access
  return "PROXY reject.docker.internal:1234";
}
```

## Verify air-gapped container configuration

After applying the configuration, test that container network restrictions work:

Test blocked access:

```console
$ docker run --rm alpine wget -O- https://www.google.com
# Should fail or timeout based on your proxy rules
```

Test allowed access:

```console
$ docker run --rm alpine wget -O- https://internal.company.com
# Should succeed if internal.company.com is in your exclude list or PAC rules
```

Test proxy routing:

```console
$ docker run --rm alpine wget -O- https://docker.io
# Should succeed if routed through approved proxy
```

## Security considerations

- Network policy enforcement: Air-gapped containers work at the Docker Desktop level. Advanced users might bypass restrictions through various means, so consider additional network-level controls for high-security environments.
- Development workflow impact: Overly restrictive policies can break legitimate development workflows. Test thoroughly and provide clear exceptions for necessary services.
- PAC file management: Host PAC files on reliable internal infrastructure. Failed PAC downloads result in blocked container network access.
- Performance considerations: Complex PAC files with many rules may impact container network performance. Keep rules simple and efficient.

---

# Configure Docker socket exceptions and advanced settings

> Configure Docker socket exceptions and advanced settings for Enhanced Container Isolation

# Configure Docker socket exceptions and advanced settings

   Table of contents

---

Subscription: Business For: Administrators

This page shows you how to configure Docker socket exceptions and other advanced settings for Enhanced Container Isolation (ECI). These configurations enable trusted tools like Testcontainers to work with ECI while maintaining security.

## Docker socket mount permissions

By default, Enhanced Container Isolation blocks containers from mounting the Docker socket to prevent malicious access to Docker Engine. However, some tools require Docker socket access.

Common scenarios requiring Docker socket access include:

- Testing frameworks: Testcontainers, which manages test containers
- Build tools: Paketo buildpacks that create ephemeral build containers
- CI/CD tools: Tools that manage containers as part of deployment pipelines
- Development utilities: Docker CLI containers for container management

## Configure socket exceptions

Configure Docker socket exceptions using Settings Management:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Go to **Admin Console** > **Desktop Settings Management**.
3. [Create or edit a setting policy](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/).
4. Find **Enhanced Container Isolation** settings.
5. Configure **Docker socket access control** with your trusted images and
  command restrictions.

Create an
[admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/) and add:

```json
{
  "configurationFileVersion": 2,
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*",
          "docker:cli"
        ],
        "allowDerivedImages": true
      },
      "commandList": {
        "type": "deny",
        "commands": ["push", "build"]
      }
    }
  }
}
```

## Image allowlist configuration

The `imageList` defines which container images can mount the Docker socket.

### Image reference formats

| Format | Description |
| --- | --- |
| <image_name>[:<tag>] | Name of the image, with optional tag. If the tag is omitted, the:latesttag is used. If the tag is the wildcard*, then it means "any tag for that image." |
| <image_name>@<digest> | Name of the image, with a specific repository digest (e.g., as reported bydocker buildx imagetools inspect <image>). This means only the image that matches that name and digest is allowed. |

### Example configurations

Basic allowlist for testing tools:

```json
"imageList": {
  "images": [
    "docker.io/testcontainers/ryuk:*",
    "docker:cli",
    "alpine:latest"
  ]
}
```

Wildcard allowlist (Docker Desktop 4.36 and later):

```json
"imageList": {
  "images": ["*"]
}
```

> Warning
>
> Using `"*"` allows all containers to mount the Docker socket, which reduces security. Only use this when explicitly listing allowed images isn't feasible.

### Security validation

Docker Desktop validates allowed images by:

1. Downloading image digests from registries for allowed images
2. Comparing container image digests against the allowlist when containers start
3. Blocking containers whose digests don't match allowed images

This prevents bypassing restrictions by re-tagging unauthorized images:

```console
$ docker tag malicious-image docker:cli
$ docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
# This fails because the digest doesn't match the real docker:cli image
```

## Derived images support

For tools like Paketo buildpacks that create ephemeral local images, you can
allow images derived from trusted base images.

### Enable derived images

```json
"imageList": {
  "images": [
    "paketobuildpacks/builder:base"
  ],
  "allowDerivedImages": true
}
```

When `allowDerivedImages` is true, local images built from allowed base images (using `FROM` in Dockerfile) also gain Docker socket access.

### Derived images requirements

- Local images only: Derived images must not exist in remote registries
- Base image available: The parent image must be pulled locally first
- Performance impact: Adds up to 1 second to container startup for validation
- Version compatibility: Full wildcard support requires Docker Desktop 4.36+

## Command restrictions

### Deny list (recommended)

Blocks specified commands while allowing all others:

```json
"commandList": {
  "type": "deny",
  "commands": ["push", "build", "image*"]
}
```

### Allow list

Only allows specified commands while blocking all others:

```json
"commandList": {
  "type": "allow",
  "commands": ["ps", "container*", "volume*"]
}
```

### Command wildcards

| Wildcard | Blocks/allows |
| --- | --- |
| "container\*" | All "docker container ..." commands |
| "image\*" | All "docker image ..." commands |
| "volume\*" | All "docker volume ..." commands |
| "network\*" | All "docker network ..." commands |
| "build\*" | All "docker build ..." commands |
| "system\*" | All "docker system ..." commands |

### Command blocking example

When a blocked command is executed:

```console
/ # docker push myimage
Error response from daemon: enhanced container isolation: docker command "/v1.43/images/myimage/push?tag=latest" is blocked; if you wish to allow it, configure the docker socket command list in the Docker Desktop settings.
```

## Common configuration examples

### Testcontainers setup

For Java/Python testing with Testcontainers:

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker.io/testcontainers/ryuk:*",
      "testcontainers/*:*"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["push", "build"]
  }
}
```

### CI/CD pipeline tools

For controlled CI/CD container management:

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:cli",
      "your-registry.com/ci-tools/*:*"
    ]
  },
  "commandList": {
    "type": "allow",
    "commands": ["ps", "container*", "image*"]
  }
}
```

### Development environments

For local development with Docker-in-Docker:

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:dind",
      "docker:cli"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["system*"]
  }
}
```

## Security recommendations

### Image allowlist best practices

- Be restrictive: Only allow images you absolutely trust and need
- Use wildcards carefully: Tag wildcards (`*`) are convenient but less secure than specific tags
- Regular reviews: Periodically review and update your allowlist
- Digest pinning: Use digest references for maximum security in critical environments

### Command restrictions

- Default to deny: Start with a deny list blocking dangerous commands like `push` and `build`
- Principle of least privilege: Only allow commands your tools actually need
- Monitor usage: Track which commands are being blocked to refine your configuration

### Monitoring and maintenance

- Regular validation: Test your configuration after Docker Desktop updates, as image digests may change.
- Handle digest mismatches: If allowed images are unexpectedly blocked:
  ```console
  $ docker image rm <image>
  $ docker pull <image>
  ```

This resolves digest mismatches when upstream images are updated.

## Next steps

- Review
  [Enhanced Container Isolation limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).
- Review
  [Enhanced Container Isolation FAQs](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/faq/).

---

# Enable Enhanced Container Isolation

> Enable Enhanced Container Isolation to secure containers in Docker Desktop

# Enable Enhanced Container Isolation

   Table of contents

---

Subscription: Business For: Administrators

ECI prevents malicious containers from compromising Docker Desktop while maintaining full developer productivity.

This page shows you how to turn on Enhanced Container Isolation (ECI) and verify it's working correctly.

## Prerequisites

Before you begin, you must have:

- A Docker Business subscription
- Docker Desktop 4.13 or later
- [Enforced sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) (for administrators managing organization-wide settings only)

## Enable Enhanced Container Isolation

### For developers

Turn on ECI in your Docker Desktop settings:

1. Sign in to your organization in Docker Desktop. Your organization must have
  a Docker Business subscription.
2. Stop and remove all existing containers:
  ```console
  $ docker stop $(docker ps -q)
  $ docker rm $(docker ps -aq)
  ```
3. In Docker Desktop, go to **Settings** > **General**.
4. Select the **Use Enhanced Container Isolation** checkbox.
5. Select **Apply and restart**.

> Important
>
> ECI doesn't protect containers created before turning on the feature. Remove existing containers before turning on ECI.

### For administrators

Configure Enhanced Container Isolation organization-wide using Settings Management:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Go to **Admin Console** > **Desktop Settings Management**.
3. [Create or edit a setting policy](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/).
4. Set **Enhanced Container Isolation** to **Always enabled**.

1. Create an
  [admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/) and add:
  ```json
  {
    "configurationFileVersion": 2,
    "enhancedContainerIsolation": {
      "value": true,
      "locked": true
    }
  }
  ```
2. Configure the following as needed:
  - `"value": true`: Turns on ECI by default (required)
  - `"locked": true`: Prevents developers from turning off ECI
  - `"locked": false`: Allows developers to control the setting

### Apply the configuration

For ECI settings to take effect:

- New installations: Users launch Docker Desktop and sign in
- Existing installations: Users must fully quit Docker Desktop and relaunch

> Important
>
> Restarting from the Docker Desktop menu isn't sufficient. Users must completely quit and reopen Docker Desktop.

You can also configure
[Docker socket mount permissions](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/) for trusted images that need Docker API access.

## Verify Enhanced Container Isolation is active

After turning on ECI, verify it's working correctly using these methods.

### Check user namespace mapping

Run a container and examine the user namespace mapping:

```console
$ docker run --rm alpine cat /proc/self/uid_map
```

With ECI turned on:

```text
0     100000      65536
```

This shows the container's root user (0) maps to an unprivileged user (100000) in the Docker Desktop VM, with a range of 64K user IDs. Each container gets an exclusive user ID range for isolation.

With ECI turned off:

```text
0          0 4294967295
```

This shows the container root user (0) maps directly to the VM root user (0), providing less isolation.

### Check container runtime

Verify the container runtime being used:

```console
$ docker inspect --format='{{.HostConfig.Runtime}}' <container_name>
```

With ECI turned on, it turns `sysbox-runc`. With ECI turned off, it returns
`runc`.

### Test security restrictions

Verify that ECI security restrictions are active.

Test namespace sharing:

```console
$ docker run -it --rm --pid=host alpine
```

With ECI turned on, this command fails with an error about Sysbox containers
not being able to share namespaces with the host.

Test Docker socket access:

```console
$ docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock alpine
```

With ECI turned on, this command fails unless you've configured Docker socket exceptions for trusted images.

## What users see with enforced ECI

When administrators enforce Enhanced Container Isolation through
Settings Management:

- The **Use Enhanced Container Isolation** setting appears turned on in
  Docker Desktop settings.
- If set to `"locked": true`, the setting is locked and greyed out.
- All new containers automatically use Linux user namespaces.
- Existing development workflows continue to work without modification.
- Users see `sysbox-runc` as the container runtime in `docker inspect` output.

## Next steps

- Review
  [Configure Docker socket exceptions and advanced settings](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/).
- Review
  [Enhanced Container Isolation limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

---

# Enhanced Container Isolation FAQs

> Frequently asked questions about Enhanced Container Isolation

# Enhanced Container Isolation FAQs

   Table of contents

---

Subscription: Business For: Administrators

This page answers common questions about Enhanced Container Isolation (ECI) that aren't covered in the main documentation.

## Do I need to change the way I use Docker when ECI is switched on?

No. ECI works automatically in the background by creating more secure containers. You can continue using all your existing Docker commands, workflows, and development tools without any changes.

## Do all container workloads work well with ECI?

Most container workloads run without issues when ECI is turned on. However, some advanced workloads that require specific kernel-level access may not work. For details about which workloads are affected, see
[ECI limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

## Why not just restrict usage of the--privilegedflag?

Privileged containers serve legitimate purposes like Docker-in-Docker, Kubernetes-in-Docker, and accessing hardware devices. ECI provides a better solution by allowing these advanced workloads to run securely while preventing them from compromising the Docker Desktop VM.

## Does ECI affect container performance?

ECI has minimal impact on container performance. The only exception is containers that perform many `mount` and `umount` system calls, as these are inspected by the Sysbox runtime for security. Most development workloads see no noticeable performance difference.

## Can I override the container runtime with ECI turned on?

No. When ECI is turned on, all containers use the Sysbox runtime regardless of any `--runtime` flags:

```console
$ docker run --runtime=runc alpine echo "test"
# This still uses sysbox-runc, not runc
```

The `--runtime` flag is ignored to prevent users from bypassing ECI security by running containers as true root in the Docker Desktop VM.

## Does ECI protect containers created before turning it on?

No. ECI only protects containers created after it's turned on. Remove existing containers before turning on ECI:

```console
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -aq)
```

For more details, see
[Enable Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/enable-eci/).

## Which containers does ECI protect?

ECI protection varies by container type and Docker Desktop version:

### Always protected

- Containers created with `docker run` and `docker create`
- Containers using the `docker-container` build driver

### Version dependent

- Docker Build: Protected in Docker Desktop 4.30+ (except WSL 2)
- Kubernetes: Protected in Docker Desktop 4.38+ when using the kind provisioner

### Not protected

- Docker Extensions
- Docker Debug containers
- Kubernetes with Kubeadm provisioner

For complete details, see
[ECI limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

## Can I mount the Docker socket with ECI turned on?

By default, no. ECI blocks Docker socket bind mounts for security. However, you can configure exceptions for trusted images like Testcontainers.

For configuration details, see
[Configure Docker socket exceptions](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/).

## What bind mounts does ECI restrict?

ECI restricts bind mounts of Docker Desktop VM directories but allows host directory mounts configured in Docker Desktop Settings.

---

# Enhanced Container Isolation limitations

> Known limitations and platform-specific considerations for Enhanced Container Isolation

# Enhanced Container Isolation limitations

   Table of contents

---

Subscription: Business For: Administrators

Enhanced Container Isolation has some platform-specific limitations and feature constraints. Understanding these limitations helps you plan your security strategy and set appropriate expectations.

## WSL 2 security considerations

> Note
>
> Docker Desktop requires WSL 2 version 2.1.5 or later. Check your version with `wsl --version` and update with `wsl --update` if needed.

Enhanced Container Isolation provides different security levels depending on your Windows backend configuration.

The following table compares ECI on WSL 2 and ECI on Hyper-V:

| Security feature | ECI on WSL | ECI on Hyper-V | Comment |
| --- | --- | --- | --- |
| Strongly secure containers | Yes | Yes | Makes it harder for malicious container workloads to breach the Docker Desktop Linux VM and host. |
| Docker Desktop Linux VM protected from user access | No | Yes | On WSL, users can access Docker Engine directly or bypass Docker Desktop security settings. |
| Docker Desktop Linux VM has a dedicated kernel | No | Yes | On WSL, Docker Desktop can't guarantee the integrity of kernel level configs. |

WSL 2 security gaps include:

- Direct VM access: Users can bypass Docker Desktop security by accessing the VM directly: `wsl -d docker-desktop`. This gives users root access to modify Docker Engine settings and bypass
  Settings Management configurations.
- Shared kernel vulnerability: All WSL 2 distributions share the same Linux kernel instance. Other WSL distributions can modify kernel settings that affect Docker Desktop's security.

### Recommendation

Use Hyper-V backend for maximum security. WSL 2 offers better performance and resource
utilization, but provides reduced security isolation.

## Windows containers not supported

ECI only works with Linux containers (Docker Desktop's default mode). Native Windows
containers mode isn't supported.

## Docker Build protection varies

Docker Build protection depends on the driver and Docker Desktop version:

| Build drive | Protection | Version requirements |
| --- | --- | --- |
| docker(default) | Protected | Docker Desktop 4.30 and later (except WSL 2) |
| docker(legacy) | Not protected | Docker Desktop versions before 4.30 |
| docker-container | Always protected | All Docker Desktop versions |

The following Docker Build features don't work with ECI:

- `docker build --network=host`
- Docker Buildx entitlements: `network.host`, `security.insecure`

### Recommendation

Use `docker-container` build driver for builds requiring these features:

```console
$ docker buildx create --driver docker-container --use
$ docker buildx build --network=host .
```

## Docker Desktop Kubernetes not protected

The integrated Kubernetes feature doesn't benefit from ECI protection. Malicious or privileged pods can compromise the Docker Desktop VM and bypass security controls.

### Recommendation

Use Kubernetes in Docker (KinD) for ECI-protected Kubernetes:

```console
$ kind create cluster
```

With ECI turned on, each Kubernetes node runs in an ECI-protected container, providing stronger isolation from the Docker Desktop VM.

## Unprotected container types

These container types currently don't benefit from ECI protection:

- Docker Extensions: Extension containers run without ECI protection
- Docker Debug: Docker Debug containers bypass ECI restrictions
- Kubernetes pods: When using Docker Desktop's integrated Kubernetes

### Recommendation

Only use extensions from trusted sources and avoid Docker Debug in security-sensitive environments.

## Global command restrictions

Command lists apply to all containers allowed to mount the Docker socket. You can't configure different command restrictions per container image.

## Local-only images not supported

You can't allow arbitrary local-only images (images not in a registry) to mount the Docker socket, unless they're:

- Derived from an allowed base image (with `allowDerivedImages: true`)
- Using the wildcard allowlist (`"*"`, Docker Desktop 4.36 and later)

## Unsupported Docker commands

These Docker commands aren't yet supported in command list restrictions:

- `compose`: Docker Compose commands
- `dev`: Development environment commands
- `extension`: Docker Extensions management
- `feedback`: Docker feedback submission
- `init`: Docker initialization commands
- `manifest`: Image manifest management
- `plugin`: Plugin management
- `sbom`: Software Bill of Materials
- `scout`: Docker Scout commands
- `trust`: Image trust management

## Performance considerations

### Derived images impact

Enabling `allowDerivedImages: true` adds approximately 1 second to container startup time for image validation.

### Registry dependencies

- Docker Desktop periodically fetches image digests from registries for validation
- Initial container starts require registry access to validate allowed images
- Network connectivity issues may cause delays in container startup

### Image digest validation

When allowed images are updated in registries, local containers may be unexpectedly blocked until you refresh the local image:

```console
$ docker image rm <image>
$ docker pull <image>
```

## Version compatibility

ECI features have been introduced across different Docker Desktop versions:

- Docker Desktop 4.36 and later: Wildcard allowlist support (`"*"`) and improved derived images handling
- Docker Desktop 4.34 and later: Derived images support (`allowDerivedImages`)
- Docker Desktop 4.30 and later: Docker Build protection with default driver (except WSL 2)
- Docker Desktop 4.13 and later: Core ECI functionality

For the latest feature availability, use the most recent Docker Desktop version.

## Production compatibility

### Container behavior differences

Most containers run identically with and without ECI. However, some advanced workloads may behave differently:

- Containers requiring kernel module loading
- Workloads modifying global kernel settings (BPF, sysctl)
- Applications expecting specific privilege escalation behavior
- Tools requiring direct hardware device access

Test advanced workloads with ECI in development environments before production deployment to ensure compatibility.

### Runtime considerations

Containers using the Sysbox runtime (with ECI) may have subtle differences compared to standard OCI runc runtime in production. These differences typically only affect privileged or system-level operations.
