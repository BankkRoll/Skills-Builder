# Explore the Containers view in Docker Desktop and more

# Explore the Containers view in Docker Desktop

> Understand what you can do with the Containers view on Docker Dashboard

# Explore the Containers view in Docker Desktop

   Table of contents

---

The **Containers** view lists all running and stopped containers and applications. It provides a clean interface to manage the lifecycle of your containers, interact with running applications, and inspect Docker objects—including Docker Compose apps.

## Container actions

Use the **Search** field to find a specific container by name.

From the **Containers** view you can:

- Start, stop, pause, resume, or restart containers
- View image packages and CVEs
- Delete containers
- Open the application in VS code
- Open the port exposed by the container in a browser
- Copy the `docker run` command for reuse or modification
- Use [Docker Debug](#execdebug)

## Resource usage

From the **Containers** view you can monitor your containers' CPU and memory usage over time. This can help you understand if something is wrong with your containers or if you need to allocate additional resources.

When you [inspect a container](#inspect-a-container), the **Stats** tab displays further information about a container's resource utilization. You can see how much CPU, memory, network and disk space your container is using over time.

## Inspect a container

You can obtain detailed information about the container when you select it.

From here, you can use the quick action buttons to perform various actions such as pause, resume, start or stop, or explore the **Logs**, **Inspect**, **Bind mounts**, **Debug**, **Files**, and **Stats** tabs.

### Logs

Select **Logs** to view output from the container in real time. While viewing logs, you can:

- Use `Cmd + f`/`Ctrl + f` to open the search bar and find specific entries.
  Search matches are highlighted in yellow.
- Press `Enter` or `Shift + Enter` to jump to the next or previous search match
  respectively.
- Use the **Copy** icon in the top right-hand corner to copy all the logs to
  your clipboard.
- Show timestamps
- Use the **Clear terminal** icon in the top right-hand corner to clear the
  logs terminal.
- Select and view external links that may be in your logs.

You can refine your view by:

- Filtering logs for specific containers, if you're running a multi-container application.
- Using regular expressions or exact match search terms

### Inspect

Select **Inspect** to view low-level information about the container. It displays the local path, version number of the image, SHA-256, port mapping, and other details.

### Exec/Debug

If you have not enabled Docker Debug in settings, the **Exec** tab displays. It lets you quickly run commands within your running container.

Using the **Exec** tab is the same as running one of the following commands:

- `docker exec -it <container-id> /bin/sh`
- `docker exec -it <container-id> cmd.exe` when accessing Windows containers

For more details, see the
[docker execCLI reference](https://docs.docker.com/reference/cli/docker/exec/).

If you have enabled Docker Debug in settings, or toggled on **Debug mode** to the right of the tab options, the **Debug** tab displays.

Debug mode has several advantages, such as:

- A customizable toolbox. The toolbox comes with many standard Linux tools
  pre-installed, such as `vim`, `nano`, `htop`, and `curl`. For more details, see the
  [docker debugCLI reference](https://docs.docker.com/reference/cli/docker/debug/).
- The ability to access containers that don't have a shell, for example, slim or
  distroless containers.

To use debug mode:

- Hover over your running container and under the **Actions** column, select the **Show container actions**
  menu. From the drop-down menu, select **Use Docker Debug**.
- Or, select the container and then select the **Debug** tab.

To use debug mode by default, navigate to
the **General** tab in **Settings** and select the **Enable Docker Debug by
default** option.

### Files

Select **Files** to explore the filesystem of running or stopped containers. You
can also:

- See which files have been recently added, modified, or deleted
- Edit a file straight from the built-in editor
- Drag and drop files and folders between the host and the container
- Delete unnecessary files when you right-click on a file
- Download files and folders from the container straight to the host

## Additional resources

- [What is a container](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [Run multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/)

---

# Explore the Images view in Docker Desktop

> Understand what you can do with the Images view on Docker Dashboard

# Explore the Images view in Docker Desktop

   Table of contents

---

The **Images** view displays a list of your Docker images and allows you to run an image as a container, pull the latest version of an image from Docker Hub, and inspect images. It also displays a summary of image vulnerabilities. In addition, the **Images** view contains clean-up options to remove unwanted images from the disk to reclaim space. If you are logged in, you can also see the images you and your organization have shared on Docker Hub. For more information, see [Explore your images](https://docs.docker.com/desktop/use-desktop/images/).

The **Images** view lets you manage Docker images without having to use the CLI. By default, it displays a list of all Docker images on your local disk.

You can also view Hub images once you have signed in to Docker Hub. This allows you to collaborate with your team and manage your images directly through Docker Desktop.

The **Images** view lets you perform core operations such as running an image as a container, pulling the latest version of an image from Docker Hub, pushing the image to Docker Hub, and inspecting images.

It also displays metadata about the image such as the:

- Tag
- Image ID
- Date created
- Size of the image.

An **In Use** tag displays next to images used by running and stopped containers. You can choose what information you want displayed by selecting the **More options** menu to the right of the search bar, and then use the toggle switches according to your preferences.

The **Images on disk** status bar displays the number of images and the total disk space used by the images and when this information was last refreshed.

## Manage your images

Use the **Search** field to search for any specific image.

You can sort images by:

- In use
- Unused
- Dangling

## Run an image as a container

From the **Images view**, hover over an image and select **Run**.

When prompted you can either:

- Select the **Optional settings** drop-down to specify a name, port, volumes, environment variables and select **Run**
- Select **Run** without specifying any optional settings.

## Inspect an image

To inspect an image, select the image row. Inspecting an image displays detailed information about the image such as the:

- Image history
- Image ID
- Date the image was created
- Size of the image
- Layers making up the image
- Base images used
- Vulnerabilities found
- Packages inside the image

[Docker Scout](https://docs.docker.com/scout/) powers this vulnerability information.
For more information about this view, see
[Image details view](https://docs.docker.com/scout/explore/image-details-view/)

## Pull the latest image from Docker Hub

Select the image from the list, select the **More options** button and select **Pull**.

> Note
>
> The repository must exist on Docker Hub in order to pull the latest version of an image. You must be signed in to pull private images.

## Push an image to Docker Hub

Select the image from the list, select the **More options** button and select **Push to Hub**.

> Note
>
> You can only push an image to Docker Hub if the image belongs to your Docker ID or your organization. That is, the image must contain the correct username/organization in its tag to be able to push it to Docker Hub.

## Remove an image

> Note
>
> To remove an image used by a running or a stopped container, you must first remove the associated container.

An unused image is an image which is not used by any running or stopped containers. An image becomes dangling when you build a new version of the image with the same tag.

To remove individual images, select the bin icon.

## Docker Hub repositories

The **Images** view also allows you to manage and interact with images in Docker Hub repositories.
By default, when you go to **Images** in Docker Desktop, you see a list of images that exist in your local image store.
The **Local** and **Docker Hub repositories** tabs near the top toggles between viewing images in your local image store,
and images in remote Docker Hub repositories that you have access to.

Switching to the **Docker Hub repositories** tab prompts you to sign in to your Docker Hub account, if you're not already signed in.
When signed in, it shows you a list of images in Docker Hub organizations and repositories that you have access to.

Select an organization from the drop-down to view a list of repositories for that organization.

If you have enabled [Docker Scout](https://docs.docker.com/scout/) on the repositories,
image analysis results (and
[health scores](https://docs.docker.com/scout/policy/scores/) if
your Docker organization is eligible) appear next to the image tags.

Hovering over an image tag reveals two options:

- **Pull**: Pull the latest version of the image from Docker Hub.
- **View in Hub**: Open the Docker Hub page and display detailed information about the image.

## Additional resources

- [What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)

---

# Explore the Kubernetes view

> See how you can deploy to Kubernetes on Docker Desktop

# Explore the Kubernetes view

   Table of contents

---

Docker Desktop includes a standalone Kubernetes server and client, as well as Docker CLI integration, enabling local Kubernetes development and testing directly on your machine.

The Kubernetes server runs as a single or multi-node cluster, within Docker containers. This lightweight setup helps you explore Kubernetes features, test workloads, and work with container orchestration in parallel with other Docker features.

## Enable Kubernetes

With Docker Desktop version 4.51 and later, you can manage Kubernetes directly from the **Kubernetes** view in the Docker Desktop Dashboard.

1. Open the Docker Desktop Dashboard and select the **Kubernetes** view.
2. Select **Create cluster**.
3. Choose your cluster type:
  - **Kubeadm** creates a single-node cluster and the version is set by Docker Desktop.
  - **kind** creates a multi-node cluster and you can set the version and number of nodes.
    For more detailed information on each cluster type, see [Cluster provisioining method](#cluster-provisioning-method).
4. Optional: Select **Show system containers (advanced)** to view internal containers when using Docker commands.
5. Select **Create**.

This sets up the images required to run the Kubernetes server as containers, and installs the `kubectl` command-line tool on your system at `/usr/local/bin/kubectl` (Mac) or `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe` (Windows). If you installed `kubectl` using Homebrew, or by some other method, and experience conflicts, remove `/usr/local/bin/kubectl`.

> Note
>
> Docker Desktop for Linux does not include `kubectl` by default. You can install it separately by following the [Kubernetes installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/). Ensure the `kubectl` binary is installed at `/usr/local/bin/kubectl`.

The following actions are also triggered in the Docker Desktop backend and VM:

- Generation of certificates and cluster configuration
- Download and installation of Kubernetes internal components
- Cluster bootup
- Installation of additional controllers for networking and storage

When Kubernetes is enabled, its status is displayed in the Docker Desktop Dashboard footer and the Docker menu.

You can check which version of Kubernetes you're on with:

```console
$ kubectl version
```

### Cluster provisioning method

Docker Desktop Kubernetes can be provisioned with either the `kubeadm` or `kind`
provisioners.

`kubeadm` is the older provisioner. It supports a single-node cluster, you can't select the kubernetes
version, it's slower to provision than `kind`, and it's not supported by
[Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) (ECI),
meaning that if ECI is enabled the cluster works but it's not protected by ECI.

`kind` is the newer provisioner. It supports multi-node clusters (for
a more realistic Kubernetes setup), you can choose the Kubernetes version, it's
faster to provision than `kubeadm`, and it's supported by ECI - when ECI is
enabled, the Kubernetes cluster runs in unprivileged Docker containers, thus
making it more secure.

| Feature | kubeadm | kind |
| --- | --- | --- |
| Multi-node cluster support | No | Yes |
| Kubernetes version selector | No | Yes |
| Speed to provision | ~1 min | ~30 seconds |
| Supported by ECI | No | Yes |
| Works with containerd image store | Yes | Yes |
| Works with Docker image store | Yes | No |

## Dashboard view

When a Kubernetes cluster is enabled, the **Kubernetes** view displays a live dashboard view showing:

- A namespace selector at the top
- A real-time list of resources - pods, services, deployments - in the selected namespace
- Automatic updates when resources are created, deleted, or modified

## Verify installation

Confirm that your cluster is running:

```console
$ kubectl get nodes
NAME                 STATUS    ROLES            AGE       VERSION
docker-desktop       Ready     control-plane    3h        v1.29.1
```

If kubectl is pointing to another environment, switch to the Docker Desktop context:

```console
$ kubectl config use-context docker-desktop
```

> Tip
>
> If no contexts appear, try:
>
>
>
> - Running the command in the Command Prompt or PowerShell.
> - Setting the `KUBECONFIG` environment variable to point to your `.kube/config` file.

For more information about `kubectl`, see the
[kubectldocumentation](https://kubernetes.io/docs/reference/kubectl/overview/).

## Edit or stop your cluster

When Kubernetes is enabled:

- Select **Edit cluster** to modify configuration. For example, switch between **kubeadm** and **kind**, or change the number of nodes.
- Select **Stop** to disable the cluster. Progress is displayed, and the **Kubernetes** view returns to the **Create cluster** screen. This stops and removes Kubernetes containers, and also removes the `/usr/local/bin/kubectl` command.

## Upgrade your cluster

Kubernetes clusters are not automatically upgraded with Docker Desktop updates. To upgrade the cluster, you must manually select **Reset cluster** in the **Kubernetes** settings.

## Configuring a custom image registry for Kubernetes control plane images

Docker Desktop uses containers to run the Kubernetes control plane. By default, Docker Desktop pulls
the associated container images from Docker Hub. The images pulled depend on the [cluster provisioning mode](#cluster-provisioning-method).

For example, in `kind` mode it requires the following images:

```console
docker.io/kindest/node:<tag>
docker.io/envoyproxy/envoy:<tag>
docker.io/docker/desktop-cloud-provider-kind:<tag>
docker.io/docker/desktop-containerd-registry-mirror:<tag>
```

In `kubeadm` mode it requires the following images:

```console
docker.io/registry.k8s.io/kube-controller-manager:<tag>
docker.io/registry.k8s.io/kube-apiserver:<tag>
docker.io/registry.k8s.io/kube-scheduler:<tag>
docker.io/registry.k8s.io/kube-proxy
docker.io/registry.k8s.io/etcd:<tag>
docker.io/registry.k8s.io/pause:<tag>
docker.io/registry.k8s.io/coredns/coredns:<tag>
docker.io/docker/desktop-storage-provisioner:<tag>
docker.io/docker/desktop-vpnkit-controller:<tag>
docker.io/docker/desktop-kubernetes:<tag>
```

The image tags are automatically selected by Docker Desktop based on several
factors, including the version of Kubernetes being used. The tags vary for each image and may change between Docker Desktop releases. To stay informed, monitor the Docker Desktop release notes.

To accommodate scenarios where access to Docker Hub is not allowed, admins can
configure Docker Desktop to pull the above listed images from a different registry (e.g., a mirror)
using the
[KubernetesImagesRepository](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/#kubernetes) setting as follows.

An image name can be broken into `[registry[:port]/][namespace/]repository[:tag]` components.
The `KubernetesImagesRepository` setting allows users to override the `[registry[:port]/][namespace]`
portion of the image's name.

For example, if Docker Desktop Kubernetes is configured in `kind` mode and
`KubernetesImagesRepository` is set to `my-registry:5000/kind-images`, then
Docker Desktop will pull the images from:

```console
my-registry:5000/kind-images/node:<tag>
my-registry:5000/kind-images/envoy:<tag>
my-registry:5000/kind-images/desktop-cloud-provider-kind:<tag>
my-registry:5000/kind-images/desktop-containerd-registry-mirror:<tag>
```

These images should be cloned/mirrored from their respective images in Docker Hub. The tags must
also match what Docker Desktop expects.

The recommended approach to set this up is the following:

1. Start Kubernetes using the desired cluster provisioning method: `kubeadm` or `kind`.
2. Once Kubernetes has started, use `docker ps` to view the container images used by Docker Desktop for the Kubernetes control plane.
3. Clone or mirror those images (with matching tags) to your custom registry.
4. Stop the Kubernetes cluster.
5. Configure the `KubernetesImagesRepository` setting to point to your custom registry.
6. Restart Docker Desktop.
7. Verify that the Kubernetes cluster is using the custom registry images using the `docker ps` command.

> Note
>
> The `KubernetesImagesRepository` setting only applies to control plane images used by Docker Desktop
> to set up the Kubernetes cluster. It has no effect on other Kubernetes pods.

> Note
>
> In Docker Desktop versions 4.43 or earlier, when using `KubernetesImagesRepository` and
> [Enhanced Container Isolation (ECI)](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/)
> is enabled, add the following images to the
> [ECI Docker socket mount image list](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/#enhanced-container-isolation):
>
>
>
> `[imagesRepository]/desktop-cloud-provider-kind:` `[imagesRepository]/desktop-containerd-registry-mirror:`
>
>
>
> These containers mount the Docker socket, so you must add the images to the ECI images list. If not,
> ECI will block the mount and Kubernetes won't start.

## Troubleshooting

- If Kubernetes fails to start, make sure Docker Desktop is running with enough allocated resources. Check **Settings** > **Resources**.
- If the `kubectl` commands return errors, confirm the context is set to `docker-desktop`
  ```console
  $ kubectl config use-context docker-desktop
  ```
  You can then try checking the logs of the Kubernetes system containers if you have enabled that setting.
- If you're experiencing cluster issues after updating, reset your Kubernetes cluster. Resetting a Kubernetes cluster can help resolve issues by essentially reverting the cluster to a clean state, and clearing out misconfigurations, corrupted data, or stuck resources that may be causing problems. If the issue still persists, you may need to clean and purge data, and then restart Docker Desktop.

---

# Pause Docker Desktop

> understand what pausing Docker Desktop Dashboard means

# Pause Docker Desktop

---

Pausing Docker Desktop temporarily suspends the Linux VM running Docker Engine. This saves the current state of all containers in memory and freezes all running processes, significantly reducing CPU and memory usage which is helpful for conserving battery on laptops.

To pause Docker Desktop, select the **Pause** icon to the left of the footer in the Docker Dashboard. To manually resume Docker Desktop, select the **Resume** option in the Docker menu, or run any Docker CLI command.

When you manually pause Docker Desktop, a paused status displays on the Docker menu and on the Docker Desktop Dashboard. You can still access the **Settings** and the **Troubleshoot** menu.

> Tip
>
> The Resource Saver feature is enabled by default and provides better CPU and memory savings than the manual Pause feature. See [Resource Saver mode](https://docs.docker.com/desktop/use-desktop/resource-saver/) for more info.

---

# Docker Desktop's Resource Saver mode

> Understand what Docker Desktop Resource Saver mode is and how to configure it

# Docker Desktop's Resource Saver mode

   Table of contents

---

Resource Saver mode significantly reduces Docker
Desktop's CPU and memory utilization on the host by 2 GBs or more, by
automatically stopping the Docker Desktop Linux VM when no containers are
running for a period of time. The default time is set to 5 minutes, but this can be adjusted to suit your needs.

With Resource Saver mode, Docker Desktop uses minimal system resources when it's idle, thereby
allowing you to save battery life on your laptop and improve your multi-tasking
experience.

## Configure Resource Saver

Resource Saver is enabled by default but can be disabled by navigating to the **Resources** tab, in **Settings**. You can also configure the idle
timer as shown below.

![Resource Saver Settings](https://docs.docker.com/desktop/images/resource-saver-settings.webp)  ![Resource Saver Settings](https://docs.docker.com/desktop/images/resource-saver-settings.webp)

If the values available aren't sufficient for your
needs, you can reconfigure it to any value, as long as the value is larger than 30 seconds, by
changing `autoPauseTimeoutSeconds` in the Docker Desktop `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier):

- Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
- Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
- Linux: `~/.docker/desktop/settings-store.json`

There's no need to restart Docker Desktop after reconfiguring.

When Docker Desktop enters Resource Saver mode:

- A moon icon displays on the
  Docker Desktop status bar as well as on the Docker icon in
  the system tray.
- Docker commands that don't run containers, for example listing container images or volumes, don't necessarily trigger an exit from Resource Saver mode as Docker Desktop can serve such commands without unnecessarily waking up the Linux VM.

> Note
>
> Docker Desktop exits the Resource Saver mode automatically when it needs to.
> Commands that cause an exit from Resource Saver take a little longer to execute
> (about 3 to 10 seconds) as Docker Desktop restarts the Linux VM.
> It's generally faster on Mac and Linux, and slower on Windows with Hyper-V.
> Once the Linux VM is restarted, subsequent container runs occur immediately as usual.

## Resource Saver mode versus Pause

Resource Saver has higher precedence than the older [Pause](https://docs.docker.com/desktop/use-desktop/pause/) feature,
meaning that while Docker Desktop is in Resource Saver mode, manually pausing
Docker Desktop is not possible (nor does it make sense since Resource Saver
actually stops the Docker Desktop Linux VM). In general, we recommend keeping
Resource Saver enabled as opposed to disabling it and using the manual Pause
feature, as it results in much better CPU and memory savings.

## Resource Saver mode on Windows

Resource Saver works a bit differently on Windows with WSL. Instead of
stopping the WSL VM, it only pauses the Docker Engine inside the
`docker-desktop` WSL distribution. That's because in WSL there's a single Linux VM
shared by all WSL distributions, so Docker Desktop can't stop the Linux VM (i.e.,
the WSL Linux VM is not owned by Docker Desktop). As a result, Resource Saver
reduces CPU utilization on WSL, but it does not reduce Docker's memory
utilization.

To reduce memory utilization on WSL, we instead recommend that
users enable WSL's `autoMemoryReclaim` feature as described in the
[Docker Desktop WSL docs](https://docs.docker.com/desktop/features/wsl/). Finally, since Docker Desktop does not
stop the Linux VM on WSL, exit from Resource Saver mode is immediate (there's
no exit delay).

---

# Explore the Volumes view in Docker Desktop

> Understand what you can do with the Volumes view on Docker Dashboard

# Explore the Volumes view in Docker Desktop

   Table of contents

---

The **Volumes** view in Docker Desktop lets you create, inspect, delete, clone, empty, export, and import
[Docker volumes](https://docs.docker.com/engine/storage/volumes/). You can also browse files and folders in volumes and see which containers are using them.

## View your volumes

You can view the following information about your volumes:

- Name: The name of the volume.
- Status: Whether the volume is in-use by a container or not.
- Created: How long ago the volume was created.
- Size: The size of the volume.
- Scheduled exports: Whether a scheduled export is active or not.

By default, the **Volumes** view displays a list of all the volumes.

You can filter and sort volumes as well as modify which columns are displayed by
doing the following:

- Filter volumes by name: Use the **Search** field.
- Filter volumes by status: To the right of the search bar, filter volumes by
  **In use** or **Unused**.
- Sort volumes: Select a column name to sort the volumes.
- Customize columns: To the right of the search bar, choose what volume
  information to display.

## Create a volume

You use the following steps to create an empty volume. Alternatively, if you
[start a container with a volume](https://docs.docker.com/engine/storage/volumes/#start-a-container-with-a-volume)
that doesn't yet exist, Docker creates the volume for you.

To create a volume:

1. In the **Volumes** view, select the **Create** button.
2. In the **New Volume** modal, specify a volume name, and then select
  **Create**.

To use the volume with a container, see
[Use volumes](https://docs.docker.com/engine/storage/volumes/#start-a-container-with-a-volume).

## Inspect a volume

To explore the details of a specific volume, select a volume from the list. This
opens the detailed view.

The **Container in-use** tab displays the name of the container using the
volume, the image name, the port number used by the container, and the target. A
target is a path inside a container that gives access to the files in the
volume.

The **Stored data** tab displays the files and folders in the volume and the
file size. To save a file or a folder, right-click on the file or folder to
display the options menu, select **Save as...**, and then specify a location to
download the file.

To delete a file or a folder from the volume, right-click on the file or folder
to display the options menu, select **Delete**, and then select **Delete** again
to confirm.

The **Exports** tab lets you [export the volume](#export-a-volume).

## Clone a volume

Cloning a volume creates a new volume with a copy of all of the data from the
cloned volume. When cloning a volume used by one or more running containers, the
containers are temporarily stopped while Docker clones the data, and then
restarted when the cloning process is completed.

To clone a volume:

1. Sign in to Docker Desktop. You must be signed in to clone a volume.
2. In the **Volumes** view, select the **Clone** icon in the **Actions** column
  for the volume you want to clone.
3. In the **Clone a volume** modal, specify a **Volume name**, and then select
  **Clone**.

## Delete one or more volumes

Deleting a volume deletes the volume and all its data. When a container is using
a volume, you can't delete the volume, even if the container is stopped.
You must first stop and remove any containers
using the volume before you can delete the volume.

To delete a volume:

1. In the **Volumes** view, select **Delete** icon in the **Actions** column for
  the volume you want to delete.
2. In the **Delete volume?** modal, select **Delete forever**.

To delete multiple volumes:

1. In the **Volumes** view, select the checkbox next to all the volumes you want
  to delete.
2. Select **Delete**.
3. In the **Delete volumes?** modal, select **Delete forever**.

## Empty a volume

Emptying a volume deletes all a volume's data, but doesn't delete the volume.
When emptying a volume used by one or more running containers, the containers
are temporarily stopped while Docker empties the data, and then restarted when
the emptying process is completed.

To empty a volume:

1. Sign in to Docker Desktop. You must be signed in to empty a volume.
2. In the **Volumes** view, select the volume you want to empty.
3. Next to **Import**, select the **More volume actions** icon, and then select **Empty volume**.
4. In the **Empty a volume?** modal, select **Empty**.

## Export a volume

You can export the content of a volume to a local file, a local image, and to an
image in Docker Hub, or to a supported cloud provider. When exporting content
from a volume used by one or more running containers, the containers are
temporarily stopped while Docker exports the content, and then restarted when
the export process is completed.

You can either [export a volume now](#export-a-volume-now) or [schedule a recurring export](#schedule-a-volume-export).

### Export a volume now

1. Sign in to Docker Desktop. You must be signed in to export a volume.
2. In the **Volumes** view, select the volume you want to export.
3. Select the **Exports** tab.
4. Select **Quick export**.
5. Select whether to export the volume to **Local or Hub storage** or **External
  cloud storage**, then specify the following additional details depending on
  your selection.
  - **Local file**: Specify a file name and select a folder.
  - **Local image**: Select a local image to export the content to. Any
    existing data in the image will be replaced by the exported content.
  - **New image**: Specify a name for the new image.
  - **Registry**: Specify a Docker Hub repository.
  You must have a [Docker Business subscription](https://www.docker.com/pricing/) to export to an external cloud provider.
  Select your cloud provider and then specify the URL to upload to the storage.
  Refer to the following documentation for your cloud provider to learn how to
  obtain a URL.
  - Amazon Web Services: [Create a presigned URL of Amazon S3 using an AWS SDK](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
  - Microsoft Azure: [Generate a SAS token and URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
  - Google Cloud: [Create a signed URL to upload an object](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)
6. Select **Save**.

### Schedule a volume export

1. Sign in to Docker Desktop. You must be signed in and have a paid [Docker subscription](https://www.docker.com/pricing/) to schedule a volume export.
2. In the **Volumes** view, select the volume you want to export.
3. Select the **Exports** tab.
4. Select **Schedule export**.
5. In **Recurrence**, select how often the export occurs, and then specify the
  following additional details based on your selection.
  - **Daily**: Specify the time that the backup occurs each day.
  - **Weekly**: Specify one or more days, and the time that the backup occurs
    each week.
  - **Monthly**: Specify which day of the month and the time that the backup
    occurs each month.
6. Select whether to export the volume to **Local or Hub storage** or **External
  cloud storage**, then specify the following additional details depending on
  your selection.
  - **Local file**: Specify a file name and select a folder.
  - **Local image**: Select a local image to export the content to. Any
    existing data in the image will be replaced by the exported content.
  - **New image**: Specify a name for the new image.
  - **Registry**: Specify a Docker Hub repository.
  You must have a [Docker Business subscription](https://www.docker.com/pricing/) to export to an external cloud provider.
  Select your cloud provider and then specify the URL to upload to the storage.
  Refer to the following documentation for your cloud provider to learn how to
  obtain a URL.
  - Amazon Web Services: [Create a presigned URL of Amazon S3 using an AWS SDK](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
  - Microsoft Azure: [Generate a SAS token and URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
  - Google Cloud: [Create a signed URL to upload an object](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)
7. Select **Save**.

## Import a volume

You can import a local file, a local image, or an image from Docker Hub. Any
existing data in the volume is replaced by the imported content. When importing
content to a volume used by one or more running containers, the containers are
temporarily stopped while Docker imports the content, and then restarted when
the import process is completed.

To import a volume:

1. Sign in to Docker Desktop. You must be signed in to import a volume.
2. Optionally, [create](#create-a-volume) a new volume to import the content
  into.
3. Select the volume you want to import content in to.
4. Select **Import**.
5. Select where the content is coming from and then specify the following
  additional details depending on your selection:
  - **Local file**: Select the file that contains the content.
  - **Local image**: Select the local image that contains the content.
  - **Registry**: Specify the image from Docker Hub that contains the content.
6. Select **Import**.

## Additional resources

- [Persisting container data](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/)
- [Use volumes](https://docs.docker.com/engine/storage/volumes/)

---

# Explore Docker Desktop

> Learn how to use the Docker Desktop Dashboard within Docker Desktop, including Quick search, the Docker menu, and more

# Explore Docker Desktop

   Table of contents

---

When you open Docker Desktop, the Docker Desktop Dashboard displays.

![Docker Desktop Dashboard on Containers view](https://docs.docker.com/desktop/images/dashboard.webp)  ![Docker Desktop Dashboard on Containers view](https://docs.docker.com/desktop/images/dashboard.webp)

It provides a centralized interface to manage your [containers](https://docs.docker.com/desktop/use-desktop/container/), [images](https://docs.docker.com/desktop/use-desktop/images/), [volumes](https://docs.docker.com/desktop/use-desktop/volumes/), [builds](https://docs.docker.com/desktop/use-desktop/builds/), and [Kubernetes resources](https://docs.docker.com/desktop/use-desktop/kubernetes/).

In addition, the Docker Desktop Dashboard lets you:

- Use
  [Ask Gordon](https://docs.docker.com/ai/gordon/), a personal AI assistant embedded in Docker Desktop and the Docker CLI. It's designed to streamline your workflow and help you make the most of the Docker ecosystem.
- Navigate to the **Settings** menu to configure your Docker Desktop settings. Select the **Settings** icon in the Dashboard header.
- Access the **Troubleshoot** menu to debug and perform restart operations. Select the **Troubleshoot** icon in the Dashboard header.
- Be notified of new releases, installation progress updates, and more in the **Notifications center**. Select the bell icon in the bottom-right corner of the Docker Desktop Dashboard to access the notification center.
- Access the **Learning center** from the Dashboard header. It helps you get started with quick in-app walkthroughs and provides other resources for learning about Docker.
  For a more detailed guide about getting started, see
  [Get started](https://docs.docker.com/get-started/introduction/).
- Access
  [Docker Hub](https://docs.docker.com/docker-hub/) to search, browse, pull, run, or view details
  of images.
- Get to the [Docker Scout](https://docs.docker.com/scout/) dashboard.
- Navigate to
  [Docker Extensions](https://docs.docker.com/extensions/).

## Docker terminal

From the Docker Dashboard footer, you can use the integrated terminal directly within Docker Desktop.

The integrated terminal:

- Persists your session if you navigate to another
  part of the Docker Desktop Dashboard and then return.
- Supports copy, paste, search, and clearing your session.

#### Open the integrated terminal

To open the integrated terminal, either:

- Hover over your running container and under the **Actions** column, select the **Show container actions**
  menu. From the drop-down menu, select **Open in terminal**.
- Or, select the **Terminal** icon located in the bottom-right corner, next to the version number.

To use your external terminal, navigate to the **General** tab in **Settings**
and select the **System default** option under **Choose your terminal**.

## Quick search

Use Quick Search, which is located in the Docker Dashboard header, to search for:

- Any container or Compose application on your local system. You can see an overview of associated environment variables or perform quick actions, such as start, stop, or delete.
- Public Docker Hub images, local images, and images from remote repositories (private repositories from organizations you're a part of in Hub). Depending on the type of image you select, you can either pull the image by tag, view documentation, go to Docker Hub for more details, or run a new container using the image.
- Extensions. From here, you can learn more about the extension and install it with a single click. Or, if you already have an extension installed, you can open it straight from the search results.
- Any volume. From here you can view the associated container.
- Docs. Find help from Docker's official documentation straight from Docker Desktop.

## The Docker menu

Docker Desktop also includes a tray icon, referred to as the Docker menu
![whale menu](https://docs.docker.com/assets/images/whale-x.svg)
for quick access.

Select the
![whale menu](https://docs.docker.com/assets/images/whale-x.svg)
icon in your taskbar to open options such as:

- **Dashboard**. This takes you to the Docker Desktop Dashboard.
- **Sign in/Sign up**
- **Settings**
- **Check for updates**
- **Troubleshoot**
- **Give feedback**
- **Switch to Windows containers** (if you're on Windows)
- **About Docker Desktop**. Contains information on the versions you are running, and links to the Subscription Service Agreement for example.
- **Docker Hub**
- **Documentation**
- **Extensions**
- **Kubernetes**
- **Restart**
- **Quit Docker Desktop**
