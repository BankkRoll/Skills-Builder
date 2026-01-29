# Live restore and more

# Live restore

> Learn how to keep containers running when the daemon isn't available

# Live restore

   Table of contents

---

By default, when the Docker daemon terminates, it shuts down running containers.
You can configure the daemon so that containers remain running if the daemon
becomes unavailable. This functionality is called *live restore*. The live restore
option helps reduce container downtime due to daemon crashes, planned outages,
or upgrades.

> Note
>
> Live restore isn't supported for Windows containers, but it does work for
> Linux containers running on Docker Desktop for Windows.

## Enable live restore

There are two ways to enable the live restore setting to keep containers alive
when the daemon becomes unavailable. **Only do one of the following**.

- Add the configuration to the daemon configuration file. On Linux, this
  defaults to `/etc/docker/daemon.json`. On Docker Desktop for Mac or Docker
  Desktop for Windows, select the Docker icon from the task bar, then click
  **Settings** -> **Docker Engine**.
  - Use the following JSON to enable `live-restore`.
    ```json
    {
      "live-restore": true
    }
    ```
  - Restart the Docker daemon. On Linux, you can avoid a restart (and avoid any
    downtime for your containers) by reloading the Docker daemon. If you use
    `systemd`, then use the command `systemctl reload docker`. Otherwise, send a
    `SIGHUP` signal to the `dockerd` process.
- If you prefer, you can start the `dockerd` process manually with the
  `--live-restore` flag. This approach isn't recommended because it doesn't
  set up the environment that `systemd` or another process manager would use
  when starting the Docker process. This can cause unexpected behavior.

## Live restore during upgrades

Live restore allows you to keep containers running across Docker daemon updates,
but is only supported when installing patch releases (`YY.MM.x`), not for
major (`YY.MM`) daemon upgrades.

If you skip releases during an upgrade, the daemon may not restore its
connection to the containers. If the daemon can't restore the connection, it
can't manage the running containers and you must stop them manually.

## Live restore upon restart

The live restore option only works to restore containers if the daemon options,
such as bridge IP addresses and graph driver, didn't change. If any of these
daemon-level configuration options have changed, the live restore may not work
and you may need to manually stop the containers.

## Impact of live restore on running containers

If the daemon is down for a long time, running containers may fill up the FIFO
log the daemon normally reads. A full log blocks containers from logging more
data. The default buffer size is 64K. If the buffers fill, you must restart
the Docker daemon to flush them.

On Linux, you can modify the kernel's buffer size by changing
`/proc/sys/fs/pipe-max-size`. You can't modify the buffer size on Docker Desktop for
Mac or Docker Desktop for Windows.

## Live restore and Swarm mode

The live restore option only pertains to standalone containers, and not to Swarm
services. Swarm services are managed by Swarm managers. If Swarm managers are
not available, Swarm services continue to run on worker nodes but can't be
managed until enough Swarm managers are available to maintain a quorum.

---

# Read the daemon logs

> How to read Docker daemon logs and force a stack trace using SIGUSR1 for debugging

# Read the daemon logs

   Table of contents

---

The daemon logs may help you diagnose problems. The logs may be saved in one of
a few locations, depending on the operating system configuration and the logging
subsystem used:

| Operating system | Location |
| --- | --- |
| Linux | Use the commandjournalctl -xu docker.service(or read/var/log/syslogor/var/log/messages, depending on your Linux Distribution) |
| macOS (dockerdlogs) | ~/Library/Containers/com.docker.docker/Data/log/vm/dockerd.log |
| macOS (containerdlogs) | ~/Library/Containers/com.docker.docker/Data/log/vm/containerd.log |
| Windows (WSL2) (dockerdlogs) | %LOCALAPPDATA%\Docker\log\vm\dockerd.log |
| Windows (WSL2) (containerdlogs) | %LOCALAPPDATA%\Docker\log\vm\containerd.log |
| Windows (Windows containers) | Logs are in the Windows Event Log |

To view the `dockerd` logs on macOS, open a terminal Window, and use the `tail`
command with the `-f` flag to "follow" the logs. Logs will be printed until you
terminate the command using `CTRL+c`:

```console
$ tail -f ~/Library/Containers/com.docker.docker/Data/log/vm/dockerd.log
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.497642089Z" level=debug msg="attach: stdout: begin"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.497714291Z" level=debug msg="attach: stderr: begin"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.499798390Z" level=debug msg="Calling POST /v1.41/containers/35fc5ec0ffe1ad492d0a4fbf51fd6286a087b89d4dd66367fa3b7aec70b46a40/wait?condition=removed"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.518403686Z" level=debug msg="Calling GET /v1.41/containers/35fc5ec0ffe1ad492d0a4fbf51fd6286a087b89d4dd66367fa3b7aec70b46a40/json"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.527074928Z" level=debug msg="Calling POST /v1.41/containers/35fc5ec0ffe1ad492d0a4fbf51fd6286a087b89d4dd66367fa3b7aec70b46a40/start"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.528203579Z" level=debug msg="container mounted via layerStore: &{/var/lib/docker/overlay2/6e76ffecede030507fcaa576404e141e5f87fc4d7e1760e9ce5b52acb24
...
^C
```

## Enable debugging

There are two ways to enable debugging. The recommended approach is to set the
`debug` key to `true` in the `daemon.json` file. This method works for every
Docker platform.

1. Edit the `daemon.json` file, which is usually located in `/etc/docker/`. You
  may need to create this file, if it doesn't yet exist. On macOS or Windows,
  don't edit the file directly. Instead, edit the file through the Docker Desktop settings.
2. If the file is empty, add the following:
  ```json
  {
    "debug": true
  }
  ```
  If the file already contains JSON, just add the key `"debug": true`, being
  careful to add a comma to the end of the line if it's not the last line
  before the closing bracket. Also verify that if the `log-level` key is set,
  it's set to either `info` or `debug`. `info` is the default, and possible
  values are `debug`, `info`, `warn`, `error`, `fatal`.
3. Send a `HUP` signal to the daemon to cause it to reload its configuration.
  On Linux hosts, use the following command.
  ```console
  $ sudo kill -SIGHUP $(pidof dockerd)
  ```
  On Windows hosts, restart Docker.

Instead of following this procedure, you can also stop the Docker daemon and
restart it manually with the debug flag `-D`. However, this may result in Docker
restarting with a different environment than the one the hosts' startup scripts
create, and this may make debugging more difficult.

## Force a stack trace to be logged

If the daemon is unresponsive, you can force a full stack trace to be logged by
sending a `SIGUSR1` signal to the daemon.

- **Linux**:
  ```console
  $ sudo kill -SIGUSR1 $(pidof dockerd)
  ```
- **Windows Server**:
  Download [docker-signal](https://github.com/moby/docker-signal).
  Get the process ID of dockerd `Get-Process dockerd`.
  Run the executable with the flag `--pid=<PID of daemon>`.

This forces a stack trace to be logged but doesn't stop the daemon. Daemon logs
show the stack trace or the path to a file containing the stack trace if it was
logged to a file.

The daemon continues operating after handling the `SIGUSR1` signal and dumping
the stack traces to the log. The stack traces can be used to determine the state
of all goroutines and threads within the daemon.

## View stack traces

The Docker daemon log can be viewed by using one of the following methods:

- By running `journalctl -u docker.service` on Linux systems using `systemctl`
- `/var/log/messages`, `/var/log/daemon.log`, or `/var/log/docker.log` on older
  Linux systems

> Note
>
> It isn't possible to manually generate a stack trace on Docker Desktop for
> Mac or Docker Desktop for Windows. However, you can click the Docker taskbar
> icon and choose **Troubleshoot** to send information to Docker if you run into
> issues.

Look in the Docker logs for a message like the following:

```text
...goroutine stacks written to /var/run/docker/goroutine-stacks-2017-06-02T193336z.log
```

The locations where Docker saves these stack traces and dumps depends on your
operating system and configuration. You can sometimes get useful diagnostic
information straight from the stack traces and dumps. Otherwise, you can provide
this information to Docker for help diagnosing the problem.

---

# Collect Docker metrics with Prometheus

> Collecting Docker metrics with Prometheus

# Collect Docker metrics with Prometheus

   Table of contents

---

[Prometheus](https://prometheus.io/) is an open-source systems monitoring and
alerting toolkit. You can configure Docker as a Prometheus target.

> Warning
>
> The available metrics and the names of those metrics are in active
> development and may change at any time.

Currently, you can only monitor Docker itself. You can't currently monitor your
application using the Docker target.

## Example

The following example shows you how to configure your Docker daemon, set up
Prometheus to run as a container on your local machine, and monitor your Docker
instance using Prometheus.

### Configure the daemon

To configure the Docker daemon as a Prometheus target, you need to specify the
`metrics-address` in the `daemon.json` configuration file. This daemon expects
the file to be located at one of the following locations by default. If the
file doesn't exist, create it.

- **Linux**: `/etc/docker/daemon.json`
- **Windows Server**: `C:\ProgramData\docker\config\daemon.json`
- **Docker Desktop**: Open the Docker Desktop settings and select **Docker Engine** to edit the file.

Add the following configuration:

```json
{
  "metrics-addr": "127.0.0.1:9323"
}
```

Save the file, or in the case of Docker Desktop for Mac or Docker Desktop for
Windows, save the configuration. Restart Docker.

Docker now exposes Prometheus-compatible metrics on port 9323 via the loopback
interface. You can configure it to use the wildcard address `0.0.0.0` instead,
but this will expose the Prometheus port to the wider network. Consider your
threat model carefully when deciding which option best suits your environment.

### Create a Prometheus configuration

Copy the following configuration file and save it to a location of your choice,
for example `/tmp/prometheus.yml`. This is a stock Prometheus configuration file,
except for the addition of the Docker job definition at the bottom of the file.

```yml
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: "codelab-monitor"

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first.rules"
  # - "second.rules"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: prometheus

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]

  - job_name: docker
      # metrics_path defaults to '/metrics'
      # scheme defaults to 'http'.

    static_configs:
      - targets: ["host.docker.internal:9323"]
```

### Run Prometheus in a container

Next, start a Prometheus container using this configuration.

```console
$ docker run --name my-prometheus \
    --mount type=bind,source=/tmp/prometheus.yml,destination=/etc/prometheus/prometheus.yml \
    -p 9090:9090 \
    --add-host host.docker.internal=host-gateway \
    prom/prometheus
```

If you're using Docker Desktop, the `--add-host` flag is optional. This flag
makes sure that the host's internal IP gets exposed to the Prometheus
container. Docker Desktop does this by default. The host IP is exposed as the
`host.docker.internal` hostname. This matches the configuration defined in
`prometheus.yml` in the previous step.

### Open the Prometheus Dashboard

Verify that the Docker target is listed at `http://localhost:9090/targets/`.

![Prometheus targets page](https://docs.docker.com/engine/daemon/images/prometheus-targets.webp)  ![Prometheus targets page](https://docs.docker.com/engine/daemon/images/prometheus-targets.webp)

> Note
>
> You can't access the endpoint URLs on this page directly if you use Docker
> Desktop.

### Use Prometheus

Create a graph. Select the **Graphs** link in the Prometheus UI. Choose a metric
from the combo box to the right of the **Execute** button, and click
**Execute**. The screenshot below shows the graph for
`engine_daemon_network_actions_seconds_count`.

![Idle Prometheus report](https://docs.docker.com/engine/daemon/images/prometheus-graph_idle.webp)  ![Idle Prometheus report](https://docs.docker.com/engine/daemon/images/prometheus-graph_idle.webp)

The graph shows a pretty idle Docker instance, unless you're already running
active workloads on your system.

To make the graph more interesting, run a container that uses some network
actions by starting downloading some packages using a package manager:

```console
$ docker run --rm alpine apk add git make musl-dev go
```

Wait a few seconds (the default scrape interval is 15 seconds) and reload your
graph. You should see an uptick in the graph, showing the increased network
traffic caused by the container you just ran.

![Prometheus report showing traffic](https://docs.docker.com/engine/daemon/images/prometheus-graph_load.webp)  ![Prometheus report showing traffic](https://docs.docker.com/engine/daemon/images/prometheus-graph_load.webp)

## Next steps

The example provided here shows how to run Prometheus as a container on your
local system. In practice, you'll probably be running Prometheus on another
system or as a cloud service somewhere. You can set up the Docker daemon as a
Prometheus target in such contexts too. Configure the `metrics-addr` of the
daemon and add the address of the daemon as a scrape endpoint in your
Prometheus configuration.

```yaml
- job_name: docker
  static_configs:
    - targets: ["docker.daemon.example:PORT"]
```

For more information about Prometheus, refer to the
[Prometheus documentation](https://prometheus.io/docs/introduction/overview/)

---

# Daemon proxy configuration

> Learn how to configure the Docker daemon to use an HTTP proxy

# Daemon proxy configuration

   Table of contents

---

If your organization uses a proxy server to connect to the internet, you may
need to configure the Docker daemon to use the proxy server. The daemon uses
a proxy server to access images stored on Docker Hub and other registries,
and to reach other nodes in a Docker swarm.

This page describes how to configure a proxy for the Docker daemon. For
instructions on configuring proxy settings for the Docker CLI, see
[Configure
Docker CLI to use a proxy server](https://docs.docker.com/engine/cli/proxy/).

> Important
>
> Proxy configurations specified in the `daemon.json` are ignored by Docker
> Desktop. If you use Docker Desktop, you can configure proxies using the
> [Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

There are two ways you can configure these settings:

- [Configuring the daemon](#daemon-configuration) through a configuration file or CLI flags
- Setting [environment variables](#environment-variables) on the system

Configuring the daemon directly takes precedence over environment variables.

## Daemon configuration

You may configure proxy behavior for the daemon in the `daemon.json` file,
or using CLI flags for the `--http-proxy` or `--https-proxy` flags for the
`dockerd` command. Configuration using `daemon.json` is recommended.

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "https://proxy.example.com:3129",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }
}
```

After changing the configuration file, restart the daemon for the proxy configuration to take effect:

```console
$ sudo systemctl restart docker
```

## Environment variables

The Docker daemon checks the following environment variables in its start-up
environment to configure HTTP or HTTPS proxy behavior:

- `HTTP_PROXY`
- `http_proxy`
- `HTTPS_PROXY`
- `https_proxy`
- `NO_PROXY`
- `no_proxy`

### systemd unit file

If you're running the Docker daemon as a systemd service, you can create a
systemd drop-in file that sets the variables for the `docker` service.

> **Note for rootless mode**
>
>
>
> The location of systemd configuration files are different when running Docker
> in
> [rootless mode](https://docs.docker.com/engine/security/rootless/). When running in
> rootless mode, Docker is started as a user-mode systemd service, and uses
> files stored in each users' home directory in
> `~/.config/systemd/<user>/docker.service.d/`. In addition, `systemctl` must
> be executed without `sudo` and with the `--user` flag. Select the "Rootless
> mode" tab if you are running Docker in rootless mode.

1. Create a systemd drop-in directory for the `docker` service:
  ```console
  $ sudo mkdir -p /etc/systemd/system/docker.service.d
  ```
2. Create a file named `/etc/systemd/system/docker.service.d/http-proxy.conf`
  that adds the `HTTP_PROXY` environment variable:
  ```systemd
  [Service]
  Environment="HTTP_PROXY=http://proxy.example.com:3128"
  ```
  If you are behind an HTTPS proxy server, set the `HTTPS_PROXY` environment
  variable:
  ```systemd
  [Service]
  Environment="HTTPS_PROXY=https://proxy.example.com:3129"
  ```
  Multiple environment variables can be set; to set both a non-HTTPS and a
  HTTPs proxy;
  ```systemd
  [Service]
  Environment="HTTP_PROXY=http://proxy.example.com:3128"
  Environment="HTTPS_PROXY=https://proxy.example.com:3129"
  ```
  > Note
  >
  > Special characters in the proxy value, such as `#?!()[]{}`, must be double
  > escaped using `%%`. For example:
  >
  >
  >
  > ```systemd
  > [Service]
  > Environment="HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/"
  > ```
3. If you have internal Docker registries that you need to contact without
  proxying, you can specify them via the `NO_PROXY` environment variable.
  The `NO_PROXY` variable specifies a string that contains comma-separated
  values for hosts that should be excluded from proxying. These are the options
  you can specify to exclude hosts:
  - IP address prefix (`1.2.3.4`)
  - Domain name, or a special DNS label (`*`)
  - A domain name matches that name and all subdomains. A domain name with a
    leading "." matches subdomains only. For example, given the domains
    `foo.example.com` and `example.com`:
    - `example.com` matches `example.com` and `foo.example.com`, and
    - `.example.com` matches only `foo.example.com`
  - A single asterisk (`*`) indicates that no proxying should be done
  - Literal port numbers are accepted by IP address prefixes (`1.2.3.4:80`) and
    domain names (`foo.example.com:80`)
  Example:
  ```systemd
  [Service]
  Environment="HTTP_PROXY=http://proxy.example.com:3128"
  Environment="HTTPS_PROXY=https://proxy.example.com:3129"
  Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
  ```
4. Flush changes and restart Docker
  ```console
  $ sudo systemctl daemon-reload
  $ sudo systemctl restart docker
  ```
5. Verify that the configuration has been loaded and matches the changes you
  made, for example:
  ```console
  $ sudo systemctl show --property=Environment docker
  Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=https://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
  ```

1. Create a systemd drop-in directory for the `docker` service:
  ```console
  $ mkdir -p ~/.config/systemd/user/docker.service.d
  ```
2. Create a file named `~/.config/systemd/user/docker.service.d/http-proxy.conf`
  that adds the `HTTP_PROXY` environment variable:
  ```systemd
  [Service]
  Environment="HTTP_PROXY=http://proxy.example.com:3128"
  ```
  If you are behind an HTTPS proxy server, set the `HTTPS_PROXY` environment
  variable:
  ```systemd
  [Service]
  Environment="HTTPS_PROXY=https://proxy.example.com:3129"
  ```
  Multiple environment variables can be set; to set both a non-HTTPS and a
  HTTPs proxy;
  ```systemd
  [Service]
  Environment="HTTP_PROXY=http://proxy.example.com:3128"
  Environment="HTTPS_PROXY=https://proxy.example.com:3129"
  ```
  > Note
  >
  > Special characters in the proxy value, such as `#?!()[]{}`, must be double
  > escaped using `%%`. For example:
  >
  >
  >
  > ```systemd
  > [Service]
  > Environment="HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/"
  > ```
3. If you have internal Docker registries that you need to contact without
  proxying, you can specify them via the `NO_PROXY` environment variable.
  The `NO_PROXY` variable specifies a string that contains comma-separated
  values for hosts that should be excluded from proxying. These are the options
  you can specify to exclude hosts:
  - IP address prefix (`1.2.3.4`)
  - Domain name, or a special DNS label (`*`)
  - A domain name matches that name and all subdomains. A domain name with a
    leading "." matches subdomains only. For example, given the domains
    `foo.example.com` and `example.com`:
    - `example.com` matches `example.com` and `foo.example.com`, and
    - `.example.com` matches only `foo.example.com`
  - A single asterisk (`*`) indicates that no proxying should be done
  - Literal port numbers are accepted by IP address prefixes (`1.2.3.4:80`) and
    domain names (`foo.example.com:80`)
  Example:
  ```systemd
  [Service]
  Environment="HTTP_PROXY=http://proxy.example.com:3128"
  Environment="HTTPS_PROXY=https://proxy.example.com:3129"
  Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
  ```
4. Flush changes and restart Docker
  ```console
  $ systemctl --user daemon-reload
  $ systemctl --user restart docker
  ```
5. Verify that the configuration has been loaded and matches the changes you
  made, for example:
  ```console
  $ systemctl --user show --property=Environment docker
  Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=https://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
  ```

---

# Configure remote access for Docker daemon

> Configuring remote access allows Docker to accept requests from remote hosts by configuring it to listen on an IP address and port as well as the Unix socket

# Configure remote access for Docker daemon

   Table of contents

---

By default, the Docker daemon listens for connections on a Unix socket to accept
requests from local clients. You can configure Docker to accept requests
from remote clients by configuring it to listen on an IP address and port as well
as the Unix socket.

> Warning
>
> Configuring Docker to accept connections from remote clients can leave you
> vulnerable to unauthorized access to the host and other attacks.
>
>
>
> It's critically important that you understand the security implications of opening Docker to the network.
> If steps aren't taken to secure the connection, it's possible for remote non-root users to gain root access on the host.
>
>
>
> Remote access without TLS is **not recommended**, and will require explicit opt-in in a future release.
> For more information on how to use TLS certificates to secure this connection, see
> [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/).

## Enable remote access

You can enable remote access to the daemon either using a `docker.service` systemd unit file for Linux distributions using systemd.
Or you can use the `daemon.json` file, if your distribution doesn't use systemd.

Configuring Docker to listen for connections using both the systemd unit file
and the `daemon.json` file causes a conflict that prevents Docker from starting.

### Configuring remote access with systemd unit file

1. Use the command `sudo systemctl edit docker.service` to open an override file
  for `docker.service` in a text editor.
2. Add or modify the following lines, substituting your own values.
  ```systemd
  [Service]
  ExecStart=
  ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:2375
  ```
3. Save the file.
4. Reload the `systemctl` configuration.
  ```console
  $ sudo systemctl daemon-reload
  ```
5. Restart Docker.
  ```console
  $ sudo systemctl restart docker.service
  ```
6. Verify that the change has gone through.
  ```console
  $ sudo netstat -lntp | grep dockerd
  tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
  ```

### Configuring remote access withdaemon.json

1. Set the `hosts` array in the `/etc/docker/daemon.json` to connect to the Unix
  socket and an IP address, as follows:
  ```json
  {
    "hosts": ["unix:///var/run/docker.sock", "tcp://127.0.0.1:2375"]
  }
  ```
2. Restart Docker.
3. Verify that the change has gone through.
  ```console
  $ sudo netstat -lntp | grep dockerd
  tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
  ```

### Allow access to the remote API through a firewall

If you run a firewall on the same host as you run Docker, and you want to access
the Docker Remote API from another remote host, you must configure your firewall
to allow incoming connections on the Docker port. The default port is `2376` if
you're using TLS encrypted transport, or `2375` otherwise.

Two common firewall daemons are:

- [Uncomplicated Firewall (ufw)](https://help.ubuntu.com/community/UFW), often
  used for Ubuntu systems.
- [firewalld](https://firewalld.org), often used for RPM-based systems.

Consult the documentation for your OS and firewall. The following information
might help you get started. The settings used in this instruction are
permissive, and you may want to use a different configuration that locks your
system down more.

- For ufw, set `DEFAULT_FORWARD_POLICY="ACCEPT"` in your configuration.
- For firewalld, add rules similar to the following to your policy. One for
  incoming requests, and one for outgoing requests.
  ```xml
  <direct>
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -i zt0 -j ACCEPT </rule> ]
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -o zt0 -j ACCEPT </rule> ]
  </direct>
  ```
  Make sure that the interface names and chain names are correct.

## Additional information

For more detailed information on configuration options for remote access to the daemon, refer to the
[dockerd CLI reference](https://docs.docker.com/reference/cli/dockerd/#bind-docker-to-another-hostport-or-a-unix-socket).

---

# Start the daemon

> Starting the Docker daemon manually

# Start the daemon

   Table of contents

---

This page shows how to start the daemon, either manually or using OS utilities.

## Start the daemon using operating system utilities

On a typical installation the Docker daemon is started by a system utility, not
manually by a user. This makes it easier to automatically start Docker when the
machine reboots.

The command to start Docker depends on your operating system. Check the correct
page under
[Install Docker](https://docs.docker.com/engine/install/).

### Start with systemd

On some operating systems, like Ubuntu and Debian, the Docker daemon service
starts automatically. Use the following command to start it manually:

```console
$ sudo systemctl start docker
```

If you want Docker to start at boot, see
[Configure Docker to start on boot](https://docs.docker.com/engine/install/linux-postinstall/#configure-docker-to-start-on-boot-with-systemd).

## Start the daemon manually

If you don't want to use a system utility to manage the Docker daemon, or just
want to test things out, you can manually run it using the `dockerd` command.
You may need to use `sudo`, depending on your operating system configuration.

When you start Docker this way, it runs in the foreground and sends its logs
directly to your terminal.

```console
$ dockerd

INFO[0000] +job init_networkdriver()
INFO[0000] +job serveapi(unix:///var/run/docker.sock)
INFO[0000] Listening for HTTP on unix (/var/run/docker.sock)
```

To stop Docker when you have started it manually, issue a `Ctrl+C` in your
terminal.
