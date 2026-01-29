# Recover your Docker account and more

# Recover your Docker account

> Recover your Docker account and manage two-factor authentication recovery codes

# Recover your Docker account

   Table of contents

---

This page explains how to recover your Docker account and manage recovery codes for two-factor authentication.

## Generate a new recovery code

If you lost your two-factor authentication recovery code but still have access to your Docker Hub account, you can generate a new recovery code.

1. Sign in to your [Docker account](https://app.docker.com/login) with your username and password.
2. Select your avatar and from the drop-down menu, select **Account settings**.
3. Select **2FA**.
4. Enter your password, then select **Confirm**.
5. Select **Generate new code**.

This generates a new code. Select the visibility icon to view the code. Save your recovery code and store it somewhere safe.

## Recover your account without access

If you lost access to both your two-factor authentication application and your recovery code:

1. Sign in to your [Docker account](https://app.docker.com/login) with your username and password.
2. Select **I've lost my authentication device** and **I've lost my recovery code**.
3. Complete the [Contact Support form](https://hub.docker.com/support/contact/?category=2fa-lockout).

You must enter the primary email address associated with your Docker ID in the Contact Support form for recovery instructions.

---

# Enable two

> Enable or disable two-factor authentication on your Docker account for enhanced security and account protection

# Enable two-factor authentication for your Docker account

   Table of contents

---

Two-factor authentication (2FA) adds an essential security layer to your Docker account by requiring a unique security code in addition to your password when signing in. This prevents unauthorized access even if your password is compromised.

When you turn on two-factor authentication, Docker provides a unique recovery code specific to your account. Store this code securely as it lets you recover your account if you lose access to your authenticator app.

## Key benefits

Two-factor authentication significantly improves your account security:

- Protection against password breaches: Even if your password is stolen or leaked, attackers can't access your account without your second factor.
- Secure CLI access: Required for Docker CLI authentication when 2FA is turned on, ensuring automated tools use personal access tokens instead of passwords.
- Compliance requirements: Many organizations require 2FA for accessing development and production resources.
- Peace of mind: Know that your Docker repositories, images, and account settings are protected by industry-standard security practices.

## Prerequisites

Before turning on two-factor authentication, you need:

- A smartphone or device with a Time-based One-time password (TOTP) authenticator app installed
- Access to your Docker account password

## Enable two-factor authentication

To turn on 2FA for your Docker account:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar and then from the drop-down menu, select **Account settings**.
3. Select **2FA**.
4. Enter your account password, then select **Confirm**.
5. Save your recovery code and store it somewhere safe. You can use your recovery code to recover your account in the event you lose access to your authenticator app.
6. Use a TOTP mobile app to scan the QR code or enter the text code.
7. Once you've linked your authenticator app, enter the six-digit code in the text-field.
8. Select **Enable 2FA**.

Two-factor authentication is now active on your account. You'll need to enter a security code from your authenticator app each time you sign in.

## Disable two-factor authentication

> Warning
>
> Disabling two-factor authentication results in decreased security for your Docker account.

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar and then from the drop-down menu, select **Account settings**.
3. Select **2FA**.
4. Enter your password, then select **Confirm**.
5. Select **Disable 2FA**.

---

# Personal access tokens

> Create and manage personal Docker access tokens for secure CLI authentication and automation

# Personal access tokens

   Table of contents

---

Personal access tokens (PATs) provide a secure alternative to passwords for Docker CLI authentication. Use PATs to authenticate automated systems, CI/CD pipelines, and development tools without exposing your Docker Hub password.

## Key benefits

PATs offer significant security advantages over password authentication:

- Enhanced security: Investigate token usage, disable suspicious tokens, and prevent administrative actions that could compromise your account if your system is compromised.
- Better automation: Issue multiple tokens for different integrations, each with specific permissions, and revoke them independently when no longer needed.
- Two-factor authentication compatibility: Required when you have two-factor authentication turned on, providing secure CLI access without bypassing 2FA protection.
- Usage tracking: Monitor when and how tokens are used to identify potential security issues or unused automation.

## Who should use personal access tokens?

Use PATs for these common scenarios:

- Development workflows: Authenticate Docker CLI during local development
- CI/CD pipelines: Automate image builds and deployments in continuous integration systems
- Automation scripts: Push and pull images in automated deployment or backup scripts
- Development tools: Integrate Docker Hub access with IDEs, container management tools, or monitoring systems
- Two-factor authentication: Required for CLI access when 2FA is turned on

> Note
>
> For organization-wide automation, consider
> [organization access tokens](https://docs.docker.com/enterprise/security/access-tokens/) which aren't tied to individual user accounts.

## Create a personal access token

> Important
>
> Treat access tokens like passwords and keep them secure. Store tokens in credential managers and never commit them to source code repositories.

To create a personal access token:

1. Sign in to [Docker Home](https://app.docker.com/).
2. Select your avatar in the top-right corner and from the drop-down menu select **Account settings**.
3. Select **Personal access tokens**.
4. Select **Generate new token**.
5. Configure your token:
  - **Description:** Use a descriptive name that indicates the token's purpose
  - **Expiration date:** Set an expiration date based on your security policies
  - **Access permissions:** **Read**, **Write**, or **Delete**.
6. Select **Generate**. Copy the token that appears on the screen and save it. You won't be able to retrieve the token once you exit the screen.

## Use personal access tokens

Sign in to the Docker CLI using your personal access token:

```console
$ docker login --username YOUR_USERNAME
Password: [paste your PAT here]
```

When prompted for a password, enter your personal access token instead of your Docker Hub password.

## Modify personal access tokens

> Note
>
> You can't edit the expiration date on an existing personal access token. You must create a new PAT if you need to set a new expiration date.

You can rename, activate, deactivate, or delete a token as needed. You can manage your tokens in your account settings.

1. Sign in to [Docker Home](https://app.docker.com/login).
2. Select your avatar in the top-right corner and from the drop-down menu select **Account settings**.
3. Select **Personal access tokens**.
  - This page shows an overview of all your tokens, and lists if the token was generated manually or if it was
    [auto-generated](#auto-generated-tokens). You can also view the scope of the
    tokens, which tokens are activate and inactive, when they were created, when
    they were last used, and their expiration date.
4. Select the actions menu on the far right of a token row, then select **Deactivate** or **Activate**, **Edit**, or **Delete** to modify the token.
5. After editing the token, select **Save token**.

## Auto-generated tokens

Docker Desktop automatically creates authentication tokens when you sign in, with these characteristics:

- Automatic creation: Generated when you sign in to Docker Desktop
- Full permissions: Include Read, Write, and Delete access
- Session-based: Automatically removed when Docker Desktop session expires
- Account limits: Up to 5 auto-generated tokens per account
- Automatic cleanup: Older tokens are deleted when new ones are created

You can manually delete auto-generated tokens if needed, but they'll be recreated when you use Docker Desktop.

## Fair use policy

When using personal access tokens, be aware that excessive token creation may result in throttling or additional charges. Docker reserves the right to impose restrictions on accounts with excessive PAT usage to ensure fair resource allocation and maintain service quality.

Best practices for fair use include:

- Reuse tokens across similar use cases instead of creating many single-purpose tokens
- Delete unused tokens regularly
- Use
  [organization access tokens](https://docs.docker.com/enterprise/security/access-tokens/) for organization-wide automation
- Monitor token usage to identify optimization opportunities

---

# Container security FAQs

> Frequently asked questions about Docker container security and isolation

# Container security FAQs

   Table of contents

---

## How are containers isolated from the host in Docker Desktop?

Docker Desktop runs all containers inside a customized Linux virtual machine (except for native Windows containers). This adds strong isolation between containers and the host machine, even when containers run as root.

Important considerations include:

- Containers have access to host files configured for file sharing via Docker Desktop settings
- Containers run as root with limited capabilities inside the Docker Desktop VM by default
- Privileged containers (`--privileged`, `--pid=host`, `--cap-add`) run with elevated privileges inside the VM, giving them access to VM internals and Docker Engine

With Enhanced Container Isolation turned on, each container runs in a dedicated Linux user namespace inside the Docker Desktop VM. Even privileged containers only have privileges within their container boundary, not the VM. ECI uses advanced techniques to prevent containers from breaching the Docker Desktop VM and Docker Engine.

## Which portions of the host filesystem can containers access?

Containers can only access host files that are:

1. Shared using Docker Desktop settings
2. Explicitly bind-mounted into the container (e.g., `docker run -v /path/to/host/file:/mnt`)

## Can containers running as root access admin-owned files on the host?

No. Host file sharing uses a user-space file server (running in `com.docker.backend` as the Docker Desktop user), so containers can only access files that the Docker Desktop user already has permission to access.

---

# General security FAQs

> Frequently asked questions about Docker security, authentication, and organization management

# General security FAQs

   Table of contents

---

## How do I report a vulnerability?

If you've discovered a security vulnerability in Docker, report it responsibly to [security@docker.com](mailto:security@docker.com) so Docker can quickly address it.

## Does Docker lockout users after failed sign-ins?

Docker Hub locks out users after 10 failed sign-in attempts within 5 minutes. The lockout duration is 5 minutes. This policy applies to Docker Hub, Docker Desktop, and Docker Scout authentication.

## Do you support physical multi-factor authentication (MFA) with YubiKeys?

You can configure physical multi-factor authentication (MFA) through SSO using your identity provider (IdP). Check with your IdP if they support physical MFA devices like YubiKeys.

## How are sessions managed and do they expire?

Docker uses tokens to manage user sessions with different expiration periods:

- Docker Desktop: Signs you out after 90 days, or 30 days of inactivity
- Docker Hub and Docker Home: Sign you out after 24 hours

Docker also supports your IdP's default session timeout through SAML attributes. For more information, see
[SSO attributes](https://docs.docker.com/enterprise/security/provisioning/#sso-attributes).

## How does Docker distinguish between employee users and contractor users?

Organizations use verified domains to distinguish user types. Team members with email domains other than verified domains appear as "Guest" users in the organization.

## How long are activity logs available?

Docker activity logs are available for 90 days. You're responsible for exporting logs or setting up drivers to send logs to your internal systems for longer retention.

## Can I export a list of users with their roles and privileges?

Yes, use the [Export Members](https://docs.docker.com/admin/organization/members/#export-members) feature to export a CSV file containing your organization's users with role and team information.

## How does Docker Desktop handle authentication information?

Docker Desktop uses the host operating system's secure key management to store authentication tokens:

- macOS: [Keychain](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web)
- Windows: [Security and Identity API via Wincred](https://learn.microsoft.com/en-us/windows/win32/api/wincred/)
- Linux: [Pass](https://www.passwordstore.org/).

## How do I remove users who aren't part of my IdP when using SSO without SCIM?

If SCIM isn't turned on, you must manually remove users from the organization. SCIM can automate user removal, but only for users added after SCIM is turned on. Users added before SCIM was turned on must be removed manually.

For more information, see
[Manage organization members](https://docs.docker.com/admin/organization/members/).

## What metadata does Scout collect from container images?

For information about metadata stored by Docker Scout, see
[Data handling](https://docs.docker.com/scout/deep-dive/data-handling/).

## How are Marketplace extensions vetted for security?

Security vetting for extensions is on the roadmap but isn't currently implemented. Extensions aren't covered as part of Docker's Third-Party Risk Management Program.

## Can I prevent users from pushing images to Docker Hub private repositories?

No direct setting exists to disable private repositories. However,
[Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) lets administrators control which registries developers can access through Docker Desktop via the Admin Console.

---

# Network and VM FAQs

> Frequently asked questions about Docker Desktop networking and virtualization security

# Network and VM FAQs

   Table of contents

---

## How can I limit container internet access?

Docker Desktop doesn't have a built-in mechanism for this, but you can use process-level firewalls on the host. Apply rules to the `com.docker.vpnkit` user-space process to control where it can connect (DNS allowlists, packet filters) and which ports/protocols it can use.

For enterprise environments, consider
[Air-gapped containers](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers/) which provide network access controls for containers.

## Can I apply firewall rules to container network traffic?

Yes. Docker Desktop uses a user-space process (`com.docker.vpnkit`) for network connectivity, which inherits constraints like firewall rules, VPN settings, and HTTP proxy properties from the user that launched it.

## Does Docker Desktop for Windows with Hyper-V allow users to create other VMs?

No. The `DockerDesktopVM` name is hard-coded in the service, so you cannot use Docker Desktop to create or manipulate other virtual machines.

## How does Docker Desktop achieve network isolation with Hyper-V and WSL 2?

Docker Desktop uses the same VM processes for both WSL 2 (in the `docker-desktop` distribution) and Hyper-V (in `DockerDesktopVM`). Host/VM communication uses `AF_VSOCK` hypervisor sockets (shared memory) rather than network switches or interfaces. All host networking is performed using standard TCP/IP sockets from the `com.docker.vpnkit.exe` and `com.docker.backend.exe` processes.

For more information, see [How Docker Desktop networking works under the hood](https://www.docker.com/blog/how-docker-desktop-networking-works-under-the-hood/).

---

# Docker security announcements

> Docker security announcements

# Docker security announcements

   Table of contents

---

## Docker Desktop 4.54.0 security update: CVE-2025-13743

A vulnerability in Docker Desktop was fixed on December 4 in the
[4.54.0](https://docs.docker.com/desktop/release-notes/#4540) release:

- Fixed [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743) where Docker Desktop diagnostics bundles were found to include expired Hub PATs in log output due to error object serialization.

## Docker Desktop 4.49.0 security update: CVE-2025-9164

A vulnerability in Docker Desktop for Windows was fixed on October 23 in the
[4.49.0](https://docs.docker.com/desktop/release-notes/#4490) release:

- Fixed [CVE-2025-9164](https://www.cve.org/cverecord?id=CVE-2025-9164) where the Docker Desktop for Windows installer was vulnerable to DLL hijacking due to insecure DLL search order. The installer searches for required DLLs in the user's Downloads folder before checking system directories, allowing local privilege escalation through malicious DLL placement.

## Docker Desktop 4.47.0 security update: CVE-2025-10657

A vulnerability in Docker Desktop was fixed on September 25 in the
[4.47.0](https://docs.docker.com/desktop/release-notes/#4470) release:

- Fixed [CVE-2025-10657](https://www.cve.org/CVERecord?id=CVE-2025-10657) where the Enhanced Container Isolation [Docker Socket command restrictions](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/#command-restrictions) feature was not working properly in Docker Desktop 4.46.0 only (the configuration for it was being ignored).

## Docker Desktop 4.44.3 security update: CVE-2025-9074

*Last updated August 20, 2025*

A vulnerability in Docker Desktop was fixed on August 20 in the
[4.44.3](https://docs.docker.com/desktop/release-notes/#4443) release:

- Fixed [CVE-2025-9074](https://www.cve.org/CVERecord?id=CVE-2025-9074) where a malicious container running on Docker Desktop could access the Docker Engine and launch additional containers without requiring the Docker socket to be mounted. This could allow unauthorized access to user files on the host system. Enhanced Container Isolation (ECI) does not mitigate this vulnerability.

## Docker Desktop 4.44.0 security update: CVE-2025-23266

*Last updated July 31, 2025*

We are aware of [CVE-2025-23266](https://nvd.nist.gov/vuln/detail/CVE-2025-23266), a critical vulnerability affecting the NVIDIA Container Toolkit in CDI mode up to version 1.17.7. Docker Desktop includes version 1.17.8, which is not impacted. However, older versions of Docker Desktop that bundled earlier toolkit versions may be affected if CDI mode was manually enabled. Upgrade to Docker Desktop 4.44 or later to ensure you're using the patched version.

## Docker Desktop 4.43.0 security update: CVE-2025-6587

*Last updated July 03, 2025*

A vulnerability in Docker Desktop was fixed on July 03 in the
[4.43.0](https://docs.docker.com/desktop/release-notes/#4430) release:

- Fixed [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587) where sensitive system environment variables were included in Docker Desktop diagnostic logs, allowing for potential secret exposure.

## Docker Desktop 4.41.0 Security Update: CVE-2025-3224, CVE-2025-4095, and CVE-2025-3911

*Last updated May 15, 2025*

Three vulnerabilities in Docker Desktop were fixed on April 28 in the
[4.41.0](https://docs.docker.com/desktop/release-notes/#4410) release.

- Fixed [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224) allowing an attacker with access to a user machine to perform an elevation of privilege when Docker Desktop updates.
- Fixed [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095) where Registry Access Management (RAM) policies were not enforced when using a MacOS configuration profile, allowing users to pull images from unapproved registries.
- Fixed [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911) allowing an attacker with read access to a user's machine to obtain sensitive information from Docker Desktop log files, including environment variables configured for running containers.

We strongly encourage you to update to Docker Desktop
[4.41.0](https://docs.docker.com/desktop/release-notes/#4410).

## Docker Desktop 4.34.2 Security Update: CVE-2024-8695 and CVE-2024-8696

*Last updated September 13, 2024*

Two remote code execution (RCE) vulnerabilities in Docker Desktop related to Docker Extensions were reported by [Cure53](https://cure53.de/) and were fixed on September 12 in the
[4.34.2](https://docs.docker.com/desktop/release-notes/#4342) release.

- [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695): A remote code execution (RCE) vulnerability via crafted extension description/changelog could be abused by a malicious extension in Docker Desktop before 4.34.2. [Critical]
- [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696): A remote code execution (RCE) vulnerability via crafted extension publisher-url/additional-urls could be abused by a malicious extension in Docker Desktop before 4.34.2. [High]

No existing extensions exploiting the vulnerabilities were found in the Extensions Marketplace. The Docker Team will be closely monitoring and diligently reviewing any requests for publishing new extensions.

We strongly encourage you to update to Docker Desktop
[4.34.2](https://docs.docker.com/desktop/release-notes/#4342). If you are unable to update promptly, you can
[disable Docker Extensions](https://docs.docker.com/extensions/settings-feedback/#turn-on-or-turn-off-extensions) as a workaround.

## Deprecation of password logins on CLI when SSO enforced

*Last updated July, 2024*

When
[SSO enforcement](https://docs.docker.com/enterprise/security/single-sign-on/connect/) was first introduced, Docker provided a grace period to continue to let passwords be used on the Docker CLI when authenticating to Docker Hub. This was allowed so organizations could more easily use SSO enforcement. It is recommended that administrators configuring SSO encourage users using the CLI
[to switch over to Personal Access Tokens](https://docs.docker.com/enterprise/security/single-sign-on/#prerequisites) in anticipation of this grace period ending.

On September 16, 2024 the grace period will end and passwords will no longer be able to authenticate to Docker Hub via the Docker CLI when SSO is enforced. Affected users are required to switch over to using PATs to continue signing in.

At Docker, we want the experience to be the most secure for our developers and organizations and this deprecation is an essential step in that direction.

## SOC 2 Type 2 attestation and ISO 27001 certification

*Last updated June, 2024*

Docker is pleased to announce that we have received our SOC 2 Type 2 attestation and ISO 27001 certification with no exceptions or major non-conformities.

Security is a fundamental pillar to Docker’s operations, which is embedded into our overall mission and company strategy. Docker’s products are core to our user community and our SOC 2 Type 2 attestation and ISO 27001 certification demonstrate Docker’s ongoing commitment to security to our user base.

For more information, see the [Blog announcement](https://www.docker.com/blog/docker-announces-soc-2-type-2-attestation-iso-27001-certification/).

## Docker Security Advisory: Multiple Vulnerabilities in runc, BuildKit, and Moby

*Last updated February 2, 2024*

We at Docker prioritize the security and integrity of our software and the trust of our users. Security researchers at Snyk Labs identified and reported four security vulnerabilities in the container ecosystem. One of the vulnerabilities, [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626), concerns the runc container runtime, and the other three affect BuildKit ([CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651), [CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652), and [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)). We want to assure our community that our team, in collaboration with the reporters and open source maintainers, has been diligently working on coordinating and implementing necessary remediations.

We are committed to maintaining the highest security standards. We have published patched versions of runc, BuildKit, and Moby on January 31 and released an update for Docker Desktop on February 1 to address these vulnerabilities. Additionally, our latest BuildKit and Moby releases included fixes for [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650) and [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557), discovered respectively by an independent researcher and through Docker’s internal research initiatives.

|  | Versions Impacted |
| --- | --- |
| runc | <= 1.1.11 |
| BuildKit | <= 0.12.4 |
| Moby (Docker Engine) | <= 25.0.1 and <= 24.0.8 |
| Docker Desktop | <= 4.27.0 |

### What should I do if I’m on an affected version?

If you are using affected versions of runc, BuildKit, Moby, or Docker Desktop, make sure to update to the latest versions, linked in the following table:

|  | Patched Versions |
| --- | --- |
| runc | >=1.1.12 |
| BuildKit | >=0.12.5 |
| Moby (Docker Engine) | >=25.0.2and >=24.0.9 |
| Docker Desktop | >=4.27.1 |

If you are unable to update to an unaffected version promptly, follow these best practices to mitigate risk:

- Only use trusted Docker images (such as [Docker Official Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images)).
- Don’t build Docker images from untrusted sources or untrusted Dockerfiles.
- If you are a Docker Business customer using Docker Desktop and unable to update to v4.27.1, make sure to enable
  [Hardened Docker Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/) features such as:
  - [Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/), which mitigates the impact of CVE-2024-21626 in the case of running containers from malicious images.
  - [Image Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/), and
    [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/), which give organizations control over which images and repositories their users can access.
- For CVE-2024-23650, CVE-2024-23651, CVE-2024-23652, and CVE-2024-23653, avoid using BuildKit frontend from an untrusted source. A frontend image is usually specified as the #syntax line on your Dockerfile, or with `--frontend` flag when using the `buildctl build` command.
- To mitigate CVE-2024-24557, make sure to either use BuildKit or disable caching when building images. From the CLI this can be done via the `DOCKER_BUILDKIT=1` environment variable (default for Moby >= v23.0 if the buildx plugin is installed) or the `--no-cache flag`. If you are using the HTTP API directly or through a client, the same can be done by setting `nocache` to `true` or `version` to `2` for the [/build API endpoint](https://docs.docker.com/reference/api/engine/version/v1.44/#tag/Image/operation/ImageBuild).

### Technical details and impact

#### CVE-2024-21626 (High)

In runc v1.1.11 and earlier, due to certain leaked file descriptors, an attacker can gain access to the host filesystem by causing a newly-spawned container process (from `runc exec`) to have a working directory in the host filesystem namespace, or by tricking a user to run a malicious image and allow a container process to gain access to the host filesystem through `runc run`. The attacks can also be adapted to overwrite semi-arbitrary host binaries, allowing for complete container escapes. Note that when using higher-level runtimes (such as Docker or Kubernetes), this vulnerability can be exploited by running a malicious container image without additional configuration or by passing specific workdir options when starting a container. The vulnerability can also be exploited from within Dockerfiles in the case of Docker.

*The issue has been fixed in runc v1.1.12.*

#### CVE-2024-23651 (High)

In BuildKit <= v0.12.4, two malicious build steps running in parallel sharing the same cache mounts with subpaths could cause a race condition, leading to files from the host system being accessible to the build container. This will only occur if a user is trying to build a Dockerfile of a malicious project.

*The issue has been fixed in BuildKit v0.12.5.*

#### CVE-2024-23652 (High)

In BuildKit <= v0.12.4, a malicious BuildKit frontend or Dockerfile using `RUN --mount` could trick the feature that removes empty files created for the mountpoints into removing a file outside the container from the host system. This will only occur if a user is using a malicious Dockerfile.

*The issue has been fixed in BuildKit v0.12.5.*

#### CVE-2024-23653 (High)

In addition to running containers as build steps, BuildKit also provides APIs for running interactive containers based on built images. In BuildKit <= v0.12.4, it is possible to use these APIs to ask BuildKit to run a container with elevated privileges. Normally, running such containers is only allowed if special `security.insecure` entitlement is enabled both by buildkitd configuration and allowed by the user initializing the build request.

*The issue has been fixed in BuildKit v0.12.5.*

#### CVE-2024-23650 (Medium)

In BuildKit <= v0.12.4, a malicious BuildKit client or frontend could craft a request that could lead to BuildKit daemon crashing with a panic.

*The issue has been fixed in BuildKit v0.12.5.*

#### CVE-2024-24557 (Medium)

In Moby <= v25.0.1 and <= v24.0.8, the classic builder cache system is prone to cache poisoning if the image is built FROM scratch. Also, changes to some instructions (most important being `HEALTHCHECK` and `ONBUILD`) would not cause a cache miss. An attacker with knowledge of the Dockerfile someone is using could poison their cache by making them pull a specially crafted image that would be considered a valid cache candidate for some build steps.

*The issue has been fixed in Moby >= v25.0.2 and >= v24.0.9.*

### How are Docker products affected?

#### Docker Desktop

Docker Desktop v4.27.0 and earlier are affected. Docker Desktop v4.27.1 was released on February 1 and includes runc, BuildKit, and dockerd binaries patches. In addition to updating to this new version, we encourage all Docker users to diligently use Docker images and Dockerfiles and ensure you only use trusted content in your builds.

As always, you should check Docker Desktop system requirements for your operating system (
[Windows](https://docs.docker.com/desktop/setup/install/windows-install/#system-requirements),
[Linux](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements),
[Mac](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements)) before updating to ensure full compatibility.

#### Docker Build Cloud

Any new Docker Build Cloud builder instances will be provisioned with the latest Docker Engine and BuildKit versions and will, therefore, be unaffected by these CVEs. Updates have also been rolled out to existing Docker Build Cloud builders.

*No other Docker products are affected by these vulnerabilities.*

### Advisory links

- Runc
  - [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
- BuildKit
  - [CVE-2024-23650](https://github.com/moby/buildkit/security/advisories/GHSA-9p26-698r-w4hx)
  - [CVE-2024-23651](https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv)
  - [CVE-2024-23652](https://github.com/moby/buildkit/security/advisories/GHSA-4v98-7qmw-rqr8)
  - [CVE-2024-23653](https://github.com/moby/buildkit/security/advisories/GHSA-wr6v-9f75-vh2g)
- Moby
  - [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

## Text4Shell CVE-2022-42889

*Last updated October 2022*

[CVE-2022-42889](https://nvd.nist.gov/vuln/detail/CVE-2022-42889) has been discovered in the popular Apache Commons Text library. Versions of this library up to but not including 1.10.0 are affected by this vulnerability.

We strongly encourage you to update to the latest version of [Apache Commons Text](https://commons.apache.org/proper/commons-text/download_text.cgi).

### Scan images on Docker Hub

Docker Hub security scans triggered after 1200 UTC 21 October 2021 are now
correctly identifying the Text4Shell CVE. Scans before this date do not
currently reflect the status of this vulnerability. Therefore, we recommend that
you trigger scans by pushing new images to Docker Hub to view the status of
the Text4Shell CVE in the vulnerability report. For detailed instructions, see [Scan images on Docker Hub](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/).

### Docker Official Images impacted by CVE-2022-42889

A number of [Docker Official Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images) contain the vulnerable versions of
Apache Commons Text. The following lists Docker Official Images that
may contain the vulnerable versions of Apache Commons Text:

- [bonita](https://hub.docker.com/_/bonita)
- [Couchbase](https://hub.docker.com/_/couchbase)
- [Geonetwork](https://hub.docker.com/_/geonetwork)
- [neo4j](https://hub.docker.com/_/neo4j)
- [sliverpeas](https://hub.docker.com/_/sliverpeas)
- [solr](https://hub.docker.com/_/solr)
- [xwiki](https://hub.docker.com/_/xwiki)

We have updated
Apache Commons Text in these images to the latest version. Some of these images may not be
vulnerable for other reasons. We recommend that you also review the guidelines published on the upstream websites.

## Log4j 2 CVE-2021-44228

*Last updated December 2021*

The [Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) vulnerability in Log4j 2, a very common Java logging library, allows remote code execution, often from a context that is easily available to an attacker. For example, it was found in Minecraft servers which allowed the commands to be typed into chat logs as these were then sent to the logger. This makes it a very serious vulnerability, as the logging library is used so widely and it may be simple to exploit. Many open source maintainers are working hard with fixes and updates to the software ecosystem.

The vulnerable versions of Log4j 2 are versions 2.0 to version 2.14.1 inclusive. The first fixed version is 2.15.0. We strongly encourage you to update to the [latest version](https://logging.apache.org/log4j/2.x/download.html) if you can. If you are using a version before 2.0, you are also not vulnerable.

You may not be vulnerable if you are using these versions, as your configuration
may already mitigate this, or the things you
log may not include any user input. This may be difficult to validate however
without understanding all the code paths that may log in detail, and where they
may get input from. So you probably will want to upgrade all code using
vulnerable versions.

> CVE-2021-45046
>
>
>
> As an update to
> [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), the fix made in version 2.15.0 was
> incomplete. Additional issues have been identified and are tracked with
> [CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046) and
> [CVE-2021-45105](https://nvd.nist.gov/vuln/detail/CVE-2021-45105).
> For a more complete fix to this vulnerability, we recommended that you update to 2.17.0 where possible.

### Scan images on Docker Hub

Docker Hub security scans triggered after 1700 UTC 13 December 2021 are now
correctly identifying the Log4j 2 CVEs. Scans before this date do not
currently reflect the status of this vulnerability. Therefore, we recommend that
you trigger scans by pushing new images to Docker Hub to view the status of
Log4j 2 CVE in the vulnerability report. For detailed instructions, see [Scan images on Docker Hub](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/).

## Docker Official Images impacted by Log4j 2 CVE

*Last updated December 2021*

A number of [Docker Official Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images) contain the vulnerable versions of
Log4j 2 CVE-2021-44228. The following table lists Docker Official Images that
may contained the vulnerable versions of Log4j 2. We updated Log4j 2 in these images to the latest version. Some of these images may not be
vulnerable for other reasons. We recommend that you also review the guidelines published on the upstream websites.

| Repository | Patched version | Additional documentation |
| --- | --- | --- |
| couchbase | 7.0.3 | Couchbase blog |
| Elasticsearch | 6.8.22, 7.16.2 | Elasticsearch announcement |
| Flink | 1.11.6, 1.12.7, 1.13.5, 1.14.2 | Flink advice on Log4j CVE |
| Geonetwork | 3.10.10 | Geonetwork GitHub discussion |
| lightstreamer | Awaiting info | Awaiting info |
| logstash | 6.8.22, 7.16.2 | Elasticsearch announcement |
| neo4j | 4.4.2 | Neo4j announcement |
| solr | 8.11.1 | Solr security news |
| sonarqube | 8.9.5, 9.2.2 | SonarQube announcement |
| storm | Awaiting info | Awaiting info |

> Note
>
> Although [xwiki](https://hub.docker.com/_/xwiki) images may be detected as vulnerable
> by some scanners, the authors believe the images are not vulnerable by Log4j 2
> CVE as the API jars do not contain the vulnerability.
> The [Nuxeo](https://hub.docker.com/_/nuxeo)
> image is deprecated and will not be updated.
