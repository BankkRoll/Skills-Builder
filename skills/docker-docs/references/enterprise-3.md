# Enhanced Container Isolation and more

# Enhanced Container Isolation

> Enhanced Container Isolation provides additional security for Docker Desktop by preventing malicious containers from compromising the host

# Enhanced Container Isolation

   Table of contents

---

Subscription: Business For: Administrators

Enhanced Container Isolation (ECI) prevents malicious containers from compromising Docker Desktop or the host system. It applies advanced security techniques automatically while maintaining full developer productivity and workflow compatibility.

ECI strengthens container isolation and locks in security configurations created by administrators, such as
[Registry Access Management policies](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) and [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/) controls.

> Note
>
> ECI works alongside other Docker security features like reduced Linux capabilities, seccomp, and AppArmor.

## Who should use Enhanced Container Isolation?

Enhanced Container Isolation is designed for:

- Organizations that want to prevent container-based attacks and reduce security vulnerabilities in developer environments
- Security teams that need stronger container isolation without impacting developer workflows
- Enterprises that require additional protection when running untrusted or third-party container images

## How Enhanced Container Isolation works

Docker implements ECI using the [Sysbox container runtime](https://github.com/nestybox/sysbox), a
security-enhanced fork of the standard OCI runc runtime. When ECI is turned on, containers created through `docker run` or `docker create` automatically use Sysbox instead of runc without requiring any changes to developer workflows.

Even containers using the `--privileged` flag run securely with Enhanced Container Isolation, preventing them from breaching the Docker Desktop virtual machine or other containers.

> Note
>
> When ECI is turned on, the Docker CLI `--runtime` flag is ignored.
> Docker's default runtime remains runc, but all user containers
> implicitly launch with Sysbox.

## Key security features

### Linux user namespace isolation

With Enhanced Container Isolation, all containers leverage Linux user namespaces for stronger isolation. Container root users map to unprivileged users in the Docker Desktop VM:

```console
$ docker run -it --rm --name=first alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

This output shows that container root (0) maps to unprivileged user 100000 in the VM, with a range of 64K user IDs. Each container gets exclusive mappings:

```console
$ docker run -it --rm --name=second alpine
/ # cat /proc/self/uid_map
         0     165536      65536
```

Without Enhanced Container Isolation, containers run as true root:

```console
$ docker run -it --rm alpine
/ # cat /proc/self/uid_map
         0       0     4294967295
```

By using Linux user namespaces, ECI ensures container processes never run with valid user IDs in the Linux VM, constraining their capabilities to resources within the container only.

### Secured privileged containers

Privileged containers (`docker run --privileged`) normally pose significant security risks because they provide unrestricted access to the Linux kernel. Without ECI, privileged containers can:

- Run as true root with all capabilities
- Bypass seccomp and AppArmor restrictions
- Access all hardware devices
- Modify global kernel settings

Organizations securing developer environments face challenges with privileged containers because they can gain control of the Docker Desktop VM and alter security settings like registry access management and network proxies.

Enhanced Container Isolation transforms privileged containers by ensuring they can only access resources within their container boundary. For example, privileged containers can't access Docker Desktop's network configuration:

```console
$ docker run --privileged djs55/bpftool map show
Error: can't get next map: Operation not permitted
```

Without ECI, privileged containers can easily access and modify these settings:

```console
$ docker run --privileged djs55/bpftool map show
17: ringbuf  name blocked_packets  flags 0x0
        key 0B  value 0B  max_entries 16777216  memlock 0B
18: hash  name allowed_map  flags 0x0
        key 4B  value 4B  max_entries 10000  memlock 81920B
```

Advanced container workloads like Docker-in-Docker and Kubernetes-in-Docker still work with ECI but run much more securely.

> Note
>
> ECI doesn't prevent users from running privileged containers, but makes them secure by containing their access. Privileged workloads that modify global kernel settings (loading kernel modules, changing Berkeley Packet Filter settings) receive "permission denied" errors.

### Namespace isolation enforcement

Enhanced Container Isolation prevents containers from sharing Linux namespaces with the Docker Desktop VM, maintaining isolation boundaries:

**PID namespace sharing blocked:**

```console
$ docker run -it --rm --pid=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share namespaces [pid] with the host (because they use the linux user-namespace for isolation): unknown.
```

**Network namespace sharing blocked:**

```console
$ docker run -it --rm --network=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share a network namespace with the host (because they use the linux user-namespace for isolation): unknown.
```

**User namespace override ignored:**

```console
$ docker run -it --rm --userns=host alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

Docker build operations using `--network-host` and Docker buildx entitlements (`network.host`,
`security.insecure`) are also blocked.

### Protected bind mounts

Enhanced Container Isolation maintains support for standard file sharing while preventing access to sensitive VM directories:

Host directory mounts continue to work:

```console
$ docker run -it --rm -v $HOME:/mnt alpine
/ # ls /mnt
# Successfully lists home directory contents
```

VM configuration mounts are blocked:

```console
$ docker run -it --rm -v /etc/docker/daemon.json:/mnt/daemon.json alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: can't mount /etc/docker/daemon.json because it's configured as a restricted host mount: unknown
```

This prevents containers from reading or modifying Docker Engine configurations, registry access management settings, proxy configurations, and other security-related VM files.

> Note
>
> By default, ECI blocks bind mounting the Docker Engine socket (/var/run/docker.sock) as this would grant containers control over Docker Engine. Administrators can create exceptions for trusted container images.

### Advanced system call protection

Enhanced Container Isolation intercepts sensitive system calls to prevent containers from using legitimate capabilities maliciously:

```console
$ docker run -it --rm --cap-add SYS_ADMIN -v $HOME:/mnt:ro alpine
/ # mount -o remount,rw /mnt /mnt
mount: permission denied (are you root?)
```

Even with `CAP_SYS_ADMIN` capability, containers can't change read-only bind mounts to read-write, ensuring they can't breach container boundaries.

Containers can still create internal mounts within their filesystem:

```console
/ # mkdir /root/tmpfs
/ # mount -t tmpfs tmpfs /root/tmpfs
/ # mount -o remount,ro /root/tmpfs /root/tmpfs
/ # findmnt | grep tmpfs
├─/root/tmpfs    tmpfs      tmpfs    ro,relatime,uid=100000,gid=100000
```

ECI performs system call filtering efficiently by intercepting only control-path system calls (rarely used) while leaving data-path system calls unaffected, maintaining container performance.

### Automatic filesystem user ID mapping

Enhanced Container Isolation solves file sharing challenges between containers with different user ID ranges through automatic filesystem mapping.

Each container gets exclusive user ID mappings, but Sysbox uses filesystem user ID remapping via Linux kernel ID-mapped mounts (added in 2021) or alternative shiftsfs module. This maps filesystem accesses from containers' real user IDs to standard ranges, enabling:

- Volume sharing across containers with different user ID ranges
- Consistent file ownership regardless of container user ID mappings
- Transparent file access without user intervention

### Information hiding through filesystem emulation

ECI emulates portions of `/proc` and `/sys` filesystems within containers to hide sensitive host information and provide per-container views of kernel resources:

```console
$ docker run -it --rm alpine
/ # cat /proc/uptime
5.86 5.86
```

This shows container uptime instead of Docker Desktop VM uptime, preventing system information from leaking into containers.

Several `/proc/sys` resources that aren't namespaced by the Linux kernel are emulated per-container, with Sysbox coordinating values when programming kernel settings. This enables container workloads that normally require privileged access to run securely.

## Performance and compatibility

Enhanced Container Isolation maintains optimized performance and full compatibility:

- No performance impact: System call filtering targets only control-path calls, leaving data-path operations unaffected
- Full workflow compatibility: Existing development processes, tools, and container images work unchanged
- Advanced workload support: Docker-in-Docker, Kubernetes-in-Docker, and other complex scenarios work securely
- Automatic management: User ID mappings, filesystem access, and security policies are handled automatically
- Standard image support: No special container images or modifications required

> Important
>
> ECI protection varies by Docker Desktop version and doesn't yet protect extension containers. Docker builds and Kubernetes in Docker Desktop have varying protection levels depending on the version. For details, see
> [Enhanced Container Isolation limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

---

# Image Access Management

> Control which Docker Hub images developers can access with Image Access Management for enhanced supply chain security

# Image Access Management

   Table of contents

---

Subscription: Business For: Administrators

Image Access Management lets administrators control which types of images developers can pull from Docker Hub. This prevents developers from accidentally using untrusted community images that could pose security risks to your organization.

With Image Access Management, you can restrict access to:

- Docker Official Images: Curated images maintained by Docker
- Docker Verified Publisher Images: Images from trusted commercial publishers
- Organization images: Your organization's private repositories
- Community images: Public images from individual developers

You can also use a repository allow list to approve specific repositories that bypass all other access controls.

## Who should use Image Access Management?

Image Access Management helps prevent supply chain attacks by ensuring developers only use trusted container images. For example, a developer building a new application might accidentally use a malicious community image as a component. Image Access Management prevents this by restricting access to only approved image types.

Common security scenarios include:

- Prevent use of unmaintained or malicious community images
- Ensure developers use only vetted, official base images
- Control access to commercial third-party images
- Maintain consistent security standards across development teams

Use the repository allow list when you need to:

- Grant access to specific vetted community images
- Allow essential third-party tools that don't fall under official categories
- Provide exceptions to general image access policies for specific business requirements

## Prerequisites

Before configuring Image Access Management, you must:

- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) to ensure users authenticate with your organization
- Use
  [personal access tokens (PATs)](https://docs.docker.com/security/access-tokens/) for authentication (Organization access tokens aren't supported)
- Have a Docker Business subscription

> Important
>
> Image Access Management only takes effect when users are signed in to Docker Desktop with organization credentials.

## Configure image access

To configure Image Access Management:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **Image access**.
3. Use the **toggle** to enable image access.
4. Select which image types to allow:
  - **Organization images**: Images from your organization (always allowed by default). These can be public or private images created by members within your organization.
  - **Community images**: Images contributed by various users that may pose security risks. This category includes Docker-Sponsored Open Source images and is turned off by default.
  - **Docker Verified Publisher Images**: Images from Docker partners in the Verified Publisher program, qualified for secure supply chains.
  - **Docker Official Images**: Curated Docker repositories that provide OS repositories, best practices for Dockerfiles, drop-in solutions, and timely security updates.
  - **Repository allow list**: A list of specific repositories that should be
    allowed. Configure in the next step.
5. Optionally, when **Repository allow list** is enabled in the previous step,
  you can add or remove specific repositories in the allow list:
  - To add repositories, in the **Repository allow list** section, select
    **Add repositories to allow list** and follow the on-screen instructions.
  - To remove a repository, in the **Repository allow list** section, select
    the trashcan icon next to it.
  Repositories in the allow list are accessible to all organization members regardless of the image type restrictions configured in the previous steps.

Once restrictions are applied, organization members can view the permissions page in read-only format.

> Note
>
> Image Access Management is turned off by default. Organization owners have access to all images regardless of policy settings.

## Verify access restrictions

After configuring Image Access Management, test that restrictions work correctly.

When developers pull allowed image types:

```console
$ docker pull nginx  # Docker Official Image
# Pull succeeds if Docker Official Images are allowed
```

When developers pull blocked image types:

```console
$ docker pull someuser/custom-image  # Community image
Error response from daemon: image access denied: community images not allowed
```

Image access restrictions apply to all Docker Hub operations including pulls, builds using `FROM` instructions, and Docker Compose services.

## Security implementation

Start with the most restrictive policy and gradually expand based on legitimate business needs:

1. Start with: Docker Official Images and Organization images
2. Add if needed: Docker Verified Publisher Images for commercial tools
3. Carefully evaluate: Community images only for specific, vetted use cases
4. Use the repository allow list sparingly: Only add repositories that have been thoroughly vetted and approved through your organization's security review process

Other security recommendations include:

- Monitor usage patterns: Review which images developers are attempting to pull, identify legitimate requests for additional image types, regularly audit approved image categories for continued relevance, and use Docker Desktop analytics to monitor usage patterns.
- Regularly review the repository allow list: Periodically audit the repositories in your allow list to ensure they remain necessary and trustworthy, and remove any that are no longer needed or maintained.
- Layer security controls: Image Access Management works best with Registry Access Management to control which registries developers can access, Enhanced Container Isolation to secure containers at runtime, and Settings Management to control Docker Desktop configuration.

## Scope and bypass considerations

- Image Access Management only controls access to Docker Hub images. Images from other registries aren't affected by these policies. Use
  [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) to control access to other registries.
- Users can potentially bypass Image Access Management by signing out of Docker Desktop (unless sign-in is enforced), using images from other registries that aren't restricted, or using registry mirrors or proxies. Enforce sign-in and combine with Registry Access Management for comprehensive control.
- Image restrictions apply to Dockerfile `FROM` instructions, Docker Compose services using restricted images will fail, multi-stage builds may be affected if intermediate images are restricted, and CI/CD pipelines using diverse image types may be impacted.

---

# Registry Access Management

> Control access to approved container registries with Registry Access Management for secure Docker Desktop usage

# Registry Access Management

   Table of contents

---

Subscription: Business For: Administrators

Registry Access Management (RAM) lets administrators control which container registries developers can access through Docker Desktop. This DNS-level filtering ensures developers only pull and push images from approved registries, improving supply chain security.

RAM works with all registry types including cloud services, on-premises registries, and registry mirrors. You can allow any hostname or domain, but must include redirect domains (like `s3.amazonaws.com` for some registries) in your allowlist.

## Supported registries

Registry Access Management works with any container registry, including:

- Docker Hub (allowed by default)
- Cloud registries: Amazon ECR, Google Container Registry, Azure Container Registry
- Git-based registries: GitHub Container Registry, GitLab Container Registry
- On-premises solutions: Nexus, Artifactory, Harbor
- Registry mirrors: Including Docker Hub mirrors

## Prerequisites

Before configuring Registry Access Management, you must:

- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) to ensure users authenticate with your organization
- Use
  [personal access tokens (PATs)](https://docs.docker.com/security/access-tokens/) for authentication (Organization access tokens aren't supported)
- Have a Docker Business subscription

> Important
>
> Registry Access Management only takes effect when users are signed in to Docker Desktop with organization credentials.

## Configure registry permissions

To configure registry permissions:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **Registry access**.
3. Use the **toggle** to enable registry access. By default, Docker Hub is enabled
  in the registry list.
4. To add additional registries, select **Add registry** and provide
  a **Registry address** and **Registry nickname**.
5. Select **Create**. You can add up to 100 registries.
6. Verify your registry appears in the registry list and select **Save changes**.

Changes can take up to 24 hours to take effect. To apply them sooner,
have developers sign out and back in to Docker Desktop.

> Important
>
> Starting with Docker Desktop 4.36, if a developer belongs to multiple organizations with different RAM policies, only the policy for the first organization in the configuration file is enforced.

> Tip
>
> RAM restrictions also apply to Dockerfile `ADD` instructions that fetch content via URL. Include trusted registry domains in your allowlist when using `ADD` with URLs.
>
> RAM is designed for container registries, not general-purpose URLs like package mirrors or storage services. Adding too many domains may cause errors or hit system limits.

## Verify restrictions are working

After users sign in to Docker Desktop with their organization credentials, Registry Access Management takes effect immediately.

When users try to pull from a blocked registry:

```console
$ docker pull blocked-registry.com/image:tag
Error response from daemon: registry access to blocked-registry.com is not allowed
```

Allowed registry access works normally:

```console
$ docker pull allowed-registry.com/image:tag
# Pull succeeds
```

Registry restrictions apply to all Docker operations including pulls, pushes,
and builds that reference external registries.

## Registry limits and platform constraints

Registry Access Management has these limits and platform-specific behaviors:

- Maximum allowlist size: 100 registries or domains per organization
- DNS-based filtering: Restrictions work at the hostname level, not IP addresses
- Redirect domains required: Must include all domains a registry redirects to (CDN endpoints, storage services)
- Windows containers: Windows image operations aren't restricted by default. Turn on **Use proxy for Windows Docker daemon** in Docker Desktop settings to apply restrictions
- WSL 2 requirements: Requires Linux kernel 5.4 or later, restrictions apply to all WSL 2 distributions

## Build and deployment restrictions

These scenarios are not restricted by Registry Access Management:

- Docker buildx with Kubernetes driver
- Docker buildx with custom docker-container driver
- Some Docker Debug and Kubernetes image pulls (even if Docker Hub is blocked)
- Images previously cached by registry mirrors may still be blocked if the source registry is restricted

## Security bypass considerations

Users can potentially bypass Registry Access Management through:

- Local proxies or DNS manipulation
- Signing out of Docker Desktop (unless sign-in is enforced)
- Network-level modifications outside Docker Desktop's control

To maximize security effectiveness:

- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) to prevent bypass through sign-out
- Implement additional network-level controls for complete protection
- Use Registry Access Management as part of a broader security strategy

## Registry allowlist best practices

- Include all registry domains: Some registries redirect to multiple
  domains. For AWS ECR, include:
  ```text
  your-account.dkr.ecr.us-west-2.amazonaws.com
  amazonaws.com
  s3.amazonaws.com
  ```
- Practice regular allowlist maintenance:
  - Remove unused registries periodically
  - Add newly approved registries as needed
  - Update domain names that may have changed
  - Monitor registry usage through Docker Desktop analytics
- Test configuration changes:
  - Verify registry access after making allowlist updates
  - Check that all necessary redirect domains are included
  - Ensure development workflows aren't disrupted
  - Combine with
    [Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) for comprehensive protection

---

# Desktop settings reporting

> Track and monitor user compliance with Docker Desktop settings policies using the reporting dashboard

# Desktop settings reporting

   Table of contents

---

Subscription: Business Availability: Early Access
Requires: Docker Desktop 4.40 and later For: Administrators

Desktop settings reporting tracks user compliance with Docker Desktop settings policies. Use this feature to monitor policy application across your organization and identify users who need assistance with compliance.

## Prerequisites

Before you can use Docker Desktop settings reporting, make sure you have:

- [Docker Desktop 4.37.1 or later](https://docs.docker.com/desktop/release-notes/) installed across your organization
- [A verified domain](https://docs.docker.com/enterprise/security/single-sign-on/configure/#step-one-add-and-verify-your-domain)
- [Enforced sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) for your organization
- A Docker Business subscription
- At least one settings policy configured

> Warning
>
> Users on Docker Desktop versions older than 4.40 may appear non-compliant because older versions can't report compliance status. For accurate reporting, update users to Docker Desktop version 4.40 or later.

## Access the reporting dashboard

To view compliance reporting:

1. Sign in to [Docker Home](https://app.docker.com) and select
  your organization.
2. Select **Admin Console**, then **Desktop settings reporting**.

The reporting dashboard provides these tools:

- A search field to find users by username or email address
- Filter options to show users assigned to specific policies
- Toggles to hide or un-hide compliant users
- Compliance status indicators
- CSV export option to download compliance data

## User compliance statuses

Docker Desktop evaluates three types of status to determine overall compliance:

### Compliance status

This is the primary status shown in the dashboard:

| Compliance status | What it means |
| --- | --- |
| Compliant | The user fetched and applied the latest assigned policy. |
| Non-compliant | The user fetched the correct policy, but hasn't applied it. |
| Outdated | The user fetched a previous version of the policy. |
| No policy assigned | The user does not have any policy assigned to them. |
| Uncontrolled domain | The user's email domain is not verified. |

### Domain status

Shows how the user's email domain relates to your organization:

| Domain status | What it means |
| --- | --- |
| Verified | The user’s email domain is verified. |
| Guest user | The user's email domain is not verified. |
| Domainless | Your organization has no verified domains, and the user's domain is unknown. |

### Settings status

Indicates the user's policy assignment:

| Settings status | What it means |
| --- | --- |
| Global policy | The user is assigned your organization's default policy. |
| User policy | The user is assigned a specific custom policy. |
| No policy assigned | The user is not assigned to any policy. |

## Monitor compliance

From the **Desktop settings reporting** dashboard, you can:

- Review organization-wide compliance at a glance
- Turn on **Hide compliant users** to focus on issues
- Filter by specific policies to check targeted compliance
- Export compliance data
- Select any user's name for detailed status and resolution steps

When you select a user's name, you'll see their detailed compliance information including current status, domain verification, assigned policy, last policy fetch time, and Docker Desktop version.

## Resolve compliance issues

You can select a non-compliant user's name in the dashboard for recommended status resolution steps. The following sections are general resolution steps for non-compliant statuses:

### Non-compliant or outdated users

- Ask the user to fully quit and relaunch Docker Desktop
- Verify the user is signed in to Docker Desktop
- Confirm the user has Docker Desktop 4.40 or later

### Uncontrolled domain users

- Verify the user's email domain in your organization settings
- If the domain should be controlled, add and verify it, then wait for verification
- If the user is a guest and shouldn't be controlled, no action is needed

### No policy assigned users

- Assign the user to an existing policy
- Create a new user-specific policy for them
- Verify they're included in your organization's default policy scope

After users take corrective action, refresh the reporting dashboard to verify status changes.

## Policy update timing

Docker Desktop checks for policy updates:

- At startup
- Every 60 minutes while Docker Desktop is running
- When users restart Docker Desktop

Changes to policies in the Admin Console are available immediately, but users must restart Docker Desktop to apply them.

---

# Configure Settings Management with the Admin Console

> Configure and enforce Docker Desktop settings across your organization using the Docker Admin Console

# Configure Settings Management with the Admin Console

   Table of contents

---

Subscription: Business For: Administrators

Use the Docker Admin Console to create and manage settings policies for Docker Desktop across your organization. Settings policies let you standardize configurations, enforce security requirements, and maintain consistent Docker Desktop environments.

## Prerequisites

Before you begin, make sure you have:

- [Docker Desktop 4.37.1 or later](https://docs.docker.com/desktop/release-notes/) installed
- [A verified domain](https://docs.docker.com/enterprise/security/single-sign-on/configure/#step-one-add-and-verify-your-domain)
- [Enforced sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) for your organization
- A Docker Business subscription

> Important
>
> You must add users to your verified domain for settings to take effect.

## Create a settings policy

To create a new settings policy:

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization.
2. Select **Admin Console**, then **Desktop Settings Management**.
3. Select **Create a settings policy**.
4. Provide a name and optional description.
  > Tip
  >
  > You can upload an existing `admin-settings.json` file to pre-fill the form.
  > Admin Console policies override local `admin-settings.json` files.
5. Choose who the policy applies to:
  - All users
  - Specific users
    > Note
    >
    > User-specific policies override global default policies. Test your policy with a small group before applying it organization-wide.
6. Configure each setting using a state:
  - **User-defined**: Users can change the setting.
  - **Always enabled**: Setting is on and locked.
  - **Enabled**: Setting is on but can be changed.
  - **Always disabled**: Setting is off and locked.
  - **Disabled**: Setting is off but can be changed.
    > Tip
    >
    > For a complete list of configurable settings, supported platforms, and configuration methods, see the [Settings reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/).
7. Select **Create** to save your policy.

## Apply the policy

Settings policies take effect after Docker Desktop restarts and users sign in.

For new installations:

1. Launch Docker Desktop.
2. Sign in with your Docker account.

For existing installations:

1. Quit Docker Desktop completely.
2. Relaunch Docker Desktop.

> Important
>
> Users must fully quit and reopen Docker Desktop. Restarting from the Docker Desktop menu isn't sufficient.

Docker Desktop checks for policy updates when it launches and every 60 minutes while running.

## Verify applied settings

After you apply policies:

- Docker Desktop displays most settings as greyed out
- Some settings, particularly Enhanced Container Isolation configurations,
  may not appear in the GUI
- You can verify all applied settings by checking the
  [settings-store.jsonfile](https://docs.docker.com/desktop/settings-and-maintenance/settings/) on your system

## Manage existing policies

From the **Desktop Settings Management** page in the Admin Console, use the **Actions** menu to:

- Edit or delete an existing settings policy
- Export a settings policy as an `admin-settings.json` file
- Promote a user-specific policy to be the new global default

## Roll back policies

To roll back a settings policy:

- Complete rollback: Delete the entire policy.
- Partial rollback: Set specific settings to **User-defined**.

When you roll back settings, users regain control over those settings configurations.
