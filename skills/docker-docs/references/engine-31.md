# Antivirus software and Docker and more

# Antivirus software and Docker

> General guidelines for using antivirus software with Docker

# Antivirus software and Docker

---

When antivirus software scans files used by Docker, these files may be locked
in a way that causes Docker commands to hang.

One way to reduce these problems is to add the Docker data directory
(`/var/lib/docker` on Linux, `%ProgramData%\docker` on Windows Server, or `$HOME/Library/Containers/com.docker.docker/` on Mac) to the
antivirus's exclusion list. However, this comes with the trade-off that viruses
or malware in Docker images, writable layers of containers, or volumes are not
detected. If you do choose to exclude Docker's data directory from background
virus scanning, you may want to schedule a recurring task that stops Docker,
scans the data directory, and restarts Docker.

---

# AppArmor security profiles for Docker

> Enabling AppArmor in Docker

# AppArmor security profiles for Docker

   Table of contents

---

AppArmor (Application Armor) is a Linux security module that protects an
operating system and its applications from security threats. To use it, a system
administrator associates an AppArmor security profile with each program. Docker
expects to find an AppArmor policy loaded and enforced.

Docker automatically generates and loads a default profile for containers named
`docker-default`. The Docker binary generates this profile in `tmpfs` and then
loads it into the kernel.

> Note
>
> This profile is used on containers, not on the Docker daemon.

A profile for the Docker Engine daemon exists but it is not currently installed
with the `deb` packages. If you are interested in the source for the daemon
profile, it is located in
[contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor)
in the Docker Engine source repository.

## Understand the policies

The `docker-default` profile is the default for running containers. It is
moderately protective while providing wide application compatibility. The
profile is generated from the following
[template](https://github.com/moby/profiles/blob/main/apparmor/template.go).

When you run a container, it uses the `docker-default` policy unless you
override it with the `security-opt` option. For example, the following
explicitly specifies the default policy:

```console
$ docker run --rm -it --security-opt apparmor=docker-default hello-world
```

## Load and unload profiles

To load a new profile into AppArmor for use with containers:

```console
$ apparmor_parser -r -W /path/to/your_profile
```

Then, run the custom profile with `--security-opt`:

```console
$ docker run --rm -it --security-opt apparmor=your_profile hello-world
```

To unload a profile from AppArmor:

```console
# unload the profile
$ apparmor_parser -R /path/to/profile
```

### Resources for writing profiles

The syntax for file globbing in AppArmor is a bit different than some other
globbing implementations. It is highly suggested you take a look at some of the
below resources with regard to AppArmor profile syntax.

- [Quick Profile Language](https://gitlab.com/apparmor/apparmor/wikis/QuickProfileLanguage)
- [Globbing Syntax](https://gitlab.com/apparmor/apparmor/wikis/AppArmor_Core_Policy_Reference#AppArmor_globbing_syntax)

## Nginx example profile

In this example, you create a custom AppArmor profile for Nginx. Below is the
custom profile.

```c
#include <tunables/global>

profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,
  network inet icmp,

  deny network raw,

  deny network packet,

  file,
  umount,

  deny /bin/** wl,
  deny /boot/** wl,
  deny /dev/** wl,
  deny /etc/** wl,
  deny /home/** wl,
  deny /lib/** wl,
  deny /lib64/** wl,
  deny /media/** wl,
  deny /mnt/** wl,
  deny /opt/** wl,
  deny /proc/** wl,
  deny /root/** wl,
  deny /sbin/** wl,
  deny /srv/** wl,
  deny /tmp/** wl,
  deny /sys/** wl,
  deny /usr/** wl,

  audit /** w,

  /var/run/nginx.pid w,

  /usr/sbin/nginx ix,

  deny /bin/dash mrwklx,
  deny /bin/sh mrwklx,
  deny /usr/bin/top mrwklx,

  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

1. Save the custom profile to disk in the
  `/etc/apparmor.d/containers/docker-nginx` file.
  The file path in this example is not a requirement. In production, you could
  use another.
2. Load the profile.
  ```console
  $ sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx
  ```
3. Run a container with the profile.
  To run nginx in detached mode:
  ```console
  $ docker run --security-opt "apparmor=docker-nginx" \
       -p 80:80 -d --name apparmor-nginx nginx
  ```
4. Exec into the running container.
  ```console
  $ docker container exec -it apparmor-nginx bash
  ```
5. Try some operations to test the profile.
  ```console
  root@6da5a2a930b9:~# ping 8.8.8.8
  ping: Lacking privilege for raw socket.
  root@6da5a2a930b9:/# top
  bash: /usr/bin/top: Permission denied
  root@6da5a2a930b9:~# touch ~/thing
  touch: cannot touch 'thing': Permission denied
  root@6da5a2a930b9:/# sh
  bash: /bin/sh: Permission denied
  root@6da5a2a930b9:/# dash
  bash: /bin/dash: Permission denied
  ```

You just deployed a container secured with a custom apparmor profile.

## Debug AppArmor

You can use `dmesg` to debug problems and `aa-status` check the loaded profiles.

### Use dmesg

Here are some helpful tips for debugging any problems you might be facing with
regard to AppArmor.

AppArmor sends quite verbose messaging to `dmesg`. Usually an AppArmor line
looks like the following:

```text
[ 5442.864673] audit: type=1400 audit(1453830992.845:37): apparmor="ALLOWED" operation="open" profile="/usr/bin/docker" name="/home/jessie/docker/man/man1/docker-attach.1" pid=10923 comm="docker" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
```

In the above example, you can see `profile=/usr/bin/docker`. This means the
user has the `docker-engine` (Docker Engine daemon) profile loaded.

Look at another log line:

```text
[ 3256.689120] type=1400 audit(1405454041.341:73): apparmor="DENIED" operation="ptrace" profile="docker-default" pid=17651 comm="docker" requested_mask="receive" denied_mask="receive"
```

This time the profile is `docker-default`, which is run on containers by
default unless in `privileged` mode. This line shows that apparmor has denied
`ptrace` in the container. This is exactly as expected.

### Use aa-status

If you need to check which profiles are loaded, you can use `aa-status`. The
output looks like:

```console
$ sudo aa-status
apparmor module is loaded.
14 profiles are loaded.
1 profiles are in enforce mode.
   docker-default
13 profiles are in complain mode.
   /usr/bin/docker
   /usr/bin/docker///bin/cat
   /usr/bin/docker///bin/ps
   /usr/bin/docker///sbin/apparmor_parser
   /usr/bin/docker///sbin/auplink
   /usr/bin/docker///sbin/blkid
   /usr/bin/docker///sbin/iptables
   /usr/bin/docker///sbin/mke2fs
   /usr/bin/docker///sbin/modprobe
   /usr/bin/docker///sbin/tune2fs
   /usr/bin/docker///sbin/xtables-multi
   /usr/bin/docker///sbin/zfs
   /usr/bin/docker///usr/bin/xz
38 processes have profiles defined.
37 processes are in enforce mode.
   docker-default (6044)
   ...
   docker-default (31899)
1 processes are in complain mode.
   /usr/bin/docker (29756)
0 processes are unconfined but have a profile defined.
```

The above output shows that the `docker-default` profile running on various
container PIDs is in `enforce` mode. This means AppArmor is actively blocking
and auditing in `dmesg` anything outside the bounds of the `docker-default`
profile.

The output above also shows the `/usr/bin/docker` (Docker Engine daemon) profile
is running in `complain` mode. This means AppArmor only logs to `dmesg`
activity outside the bounds of the profile. (Except in the case of Ubuntu
Trusty, where some interesting behaviors are enforced.)

## Contribute to Docker's AppArmor code

Advanced users and package managers can find a profile for `/usr/bin/docker`
(Docker Engine daemon) underneath
[contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor)
in the Docker Engine source repository.

The `docker-default` profile for containers lives in
[profiles/apparmor](https://github.com/moby/profiles/blob/main/apparmor).

---

# Verify repository client with certificates

> How to set up and use certificates with a registry to verify access

# Verify repository client with certificates

   Table of contents

---

In [Running Docker with HTTPS](https://docs.docker.com/engine/security/protect-access/), you learned that, by default,
Docker runs via a non-networked Unix socket and TLS must be enabled in order
to have the Docker client and the daemon communicate securely over HTTPS. TLS ensures authenticity of the registry endpoint and that traffic to/from registry is encrypted.

This article demonstrates how to ensure the traffic between the Docker registry
server and the Docker daemon (a client of the registry server) is encrypted and
properly authenticated using certificate-based client-server authentication.

We show you how to install a Certificate Authority (CA) root certificate
for the registry and how to set the client TLS certificate for verification.

## Understand the configuration

A custom certificate is configured by creating a directory under
`/etc/docker/certs.d` using the same name as the registry's hostname, such as
`localhost`. All `*.crt` files are added to this directory as CA roots.

> Note
>
> On Linux any root certificates authorities are merged with the system defaults,
> including the host's root CA set. If you are running Docker on Windows Server,
> or Docker Desktop for Windows with Windows containers, the system default
> certificates are only used when no custom root certificates are configured.

The presence of one or more `<filename>.key/cert` pairs indicates to Docker
that there are custom certificates required for access to the desired
repository.

> Note
>
> If multiple certificates exist, each is tried in alphabetical
> order. If there is a 4xx-level or 5xx-level authentication error, Docker
> continues to try with the next certificate.

The following illustrates a configuration with custom certificates:

```text
/etc/docker/certs.d/        <-- Certificate directory
    └── localhost:5000          <-- Hostname:port
       ├── client.cert          <-- Client certificate
       ├── client.key           <-- Client key
       └── ca.crt               <-- Root CA that signed
                                    the registry certificate, in PEM
```

The preceding example is operating-system specific and is for illustrative
purposes only. You should consult your operating system documentation for
creating an os-provided bundled certificate chain.

## Create the client certificates

Use OpenSSL's `genrsa` and `req` commands to first generate an RSA
key and then use the key to create the certificate.

```console
$ openssl genrsa -out client.key 4096
$ openssl req -new -x509 -text -key client.key -out client.cert
```

> Note
>
> These TLS commands only generate a working set of certificates on Linux.
> The version of OpenSSL in macOS is incompatible with the type of
> certificate Docker requires.

## Troubleshooting tips

The Docker daemon interprets `.crt` files as CA certificates and `.cert` files
as client certificates. If a CA certificate is accidentally given the extension
`.cert` instead of the correct `.crt` extension, the Docker daemon logs the
following error message:

```text
Missing key KEY_NAME for client certificate CERT_NAME. CA certificates should use the extension .crt.
```

If the Docker registry is accessed without a port number, do not add the port to the directory name. The following shows the configuration for a registry on default port 443 which is accessed with `docker login my-https.registry.example.com`:

```text
/etc/docker/certs.d/
    └── my-https.registry.example.com          <-- Hostname without port
       ├── client.cert
       ├── client.key
       └── ca.crt
```

## Related information

- [Use trusted images](https://docs.docker.com/engine/security/trust/)
- [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)

---

# Docker security non

> Review of security vulnerabilities Docker mitigated

# Docker security non-events

---

This page lists security vulnerabilities which Docker mitigated, such that
processes run in Docker containers were never vulnerable to the bug—even before
it was fixed. This assumes containers are run without adding extra capabilities
or not run as `--privileged`.

The list below is not even remotely complete. Rather, it is a sample of the few
bugs we've actually noticed to have attracted security review and publicly
disclosed vulnerabilities. In all likelihood, the bugs that haven't been
reported far outnumber those that have. Luckily, since Docker's approach to
secure by default through apparmor, seccomp, and dropping capabilities, it
likely mitigates unknown bugs just as well as it does known ones.

Bugs mitigated:

- [CVE-2013-1956](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1956),
  [1957](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1957),
  [1958](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1958),
  [1959](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1959),
  [1979](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1979),
  [CVE-2014-4014](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4014),
  [5206](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5206),
  [5207](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5207),
  [7970](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7970),
  [7975](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7975),
  [CVE-2015-2925](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-2925),
  [8543](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-8543),
  [CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134),
  [3135](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3135), etc.:
  The introduction of unprivileged user namespaces lead to a huge increase in the
  attack surface available to unprivileged users by giving such users legitimate
  access to previously root-only system calls like `mount()`. All of these CVEs
  are examples of security vulnerabilities due to introduction of user namespaces.
  Docker can use user namespaces to set up containers, but then disallows the
  process inside the container from creating its own nested namespaces through the
  default seccomp profile, rendering these vulnerabilities unexploitable.
- [CVE-2014-0181](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0181),
  [CVE-2015-3339](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3339):
  These are bugs that require the presence of a setuid binary. Docker disables
  setuid binaries inside containers via the `NO_NEW_PRIVS` process flag and
  other mechanisms.
- [CVE-2014-4699](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4699):
  A bug in `ptrace()` could allow privilege escalation. Docker disables `ptrace()`
  inside the container using apparmor, seccomp and by dropping `CAP_PTRACE`.
  Three times the layers of protection there!
- [CVE-2014-9529](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9529):
  A series of crafted `keyctl()` calls could cause kernel DoS / memory corruption.
  Docker disables `keyctl()` inside containers using seccomp.
- [CVE-2015-3214](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3214),
  [4036](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-4036): These are
  bugs in common virtualization drivers which could allow a guest OS user to
  execute code on the host OS. Exploiting them requires access to virtualization
  devices in the guest. Docker hides direct access to these devices when run
  without `--privileged`. Interestingly, these seem to be cases where containers
  are "more secure" than a VM, going against common wisdom that VMs are
  "more secure" than containers.
- [CVE-2016-0728](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-0728):
  Use-after-free caused by crafted `keyctl()` calls could lead to privilege
  escalation. Docker disables `keyctl()` inside containers using the default
  seccomp profile.
- [CVE-2016-2383](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2383):
  A bug in eBPF -- the special in-kernel DSL used to express things like seccomp
  filters -- allowed arbitrary reads of kernel memory. The `bpf()` system call
  is blocked inside Docker containers using (ironically) seccomp.
- [CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134),
  [4997](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4997),
  [4998](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4998):
  A bug in setsockopt with `IPT_SO_SET_REPLACE`, `ARPT_SO_SET_REPLACE`, and
  `ARPT_SO_SET_REPLACE` causing memory corruption / local privilege escalation.
  These arguments are blocked by `CAP_NET_ADMIN`, which Docker does not allow by
  default.

Bugs not mitigated:

- [CVE-2015-3290](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3290),
  [5157](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5157): Bugs in
  the kernel's non-maskable interrupt handling allowed privilege escalation.
  Can be exploited in Docker containers because the `modify_ldt()` system call is
  not currently blocked using seccomp.
- [CVE-2016-5195](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5195):
  A race condition was found in the way the Linux kernel's memory subsystem
  handled the copy-on-write (COW) breakage of private read-only memory mappings,
  which allowed unprivileged local users to gain write access to read-only memory.
  Also known as "dirty COW."
  *Partial mitigations:* on some operating systems this vulnerability is mitigated
  by the combination of seccomp filtering of `ptrace` and the fact that `/proc/self/mem` is read-only.

---

# Protect the Docker daemon socket

> How to setup and run Docker with SSH or HTTPS

# Protect the Docker daemon socket

   Table of contents

---

By default, Docker runs through a non-networked UNIX socket. It can also
optionally communicate using SSH or a TLS (HTTPS) socket.

## Use SSH to protect the Docker daemon socket

> Note
>
> The given `USERNAME` must have permissions to access the docker socket on the
> remote machine. Refer to [manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
> to learn how to give a non-root user access to the docker socket.

The following example creates a
[docker context](https://docs.docker.com/engine/manage-resources/contexts/)
to connect with a remote `dockerd` daemon on `host1.example.com` using SSH, and
as the `docker-user` user on the remote machine:

```console
$ docker context create \
    --docker host=ssh://docker-user@host1.example.com \
    --description="Remote engine" \
    my-remote-engine

my-remote-engine
Successfully created context "my-remote-engine"
```

After creating the context, use `docker context use` to switch the `docker` CLI
to use it, and to connect to the remote engine:

```console
$ docker context use my-remote-engine
my-remote-engine
Current context is now "my-remote-engine"

$ docker info
<prints output of the remote engine>
```

Use the `default` context to switch back to the default (local) daemon:

```console
$ docker context use default
default
Current context is now "default"
```

Alternatively, use the `DOCKER_HOST` environment variable to temporarily switch
the `docker` CLI to connect to the remote host using SSH. This does not require
creating a context, and can be useful to create an ad-hoc connection with a different
engine:

```console
$ export DOCKER_HOST=ssh://docker-user@host1.example.com
$ docker info
<prints output of the remote engine>
```

### SSH Tips

For the best user experience with SSH, configure `~/.ssh/config` as follows to allow
reusing a SSH connection for multiple invocations of the `docker` CLI:

```text
ControlMaster     auto
ControlPath       ~/.ssh/control-%C
ControlPersist    yes
```

## Use TLS (HTTPS) to protect the Docker daemon socket

If you need Docker to be reachable through HTTP rather than SSH in a safe manner,
you can enable TLS (HTTPS) by specifying the `tlsverify` flag and pointing Docker's
`tlscacert` flag to a trusted CA certificate.

In the daemon mode, it only allows connections from clients
authenticated by a certificate signed by that CA. In the client mode,
it only connects to servers with a certificate signed by that CA.

> Important
>
> Using TLS and managing a CA is an advanced topic. Familiarize yourself
> with OpenSSL, x509, and TLS before using it in production.

### Create a CA, server and client keys with OpenSSL

> Note
>
> Replace all instances of `$HOST` in the following example with the
> DNS name of your Docker daemon's host.

First, on the Docker daemon's host machine, generate CA private and public keys:

```console
$ openssl genrsa -aes256 -out ca-key.pem 4096
Generating RSA private key, 4096 bit long modulus
..............................................................................++
........++
e is 65537 (0x10001)
Enter pass phrase for ca-key.pem:
Verifying - Enter pass phrase for ca-key.pem:

$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
Enter pass phrase for ca-key.pem:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:Queensland
Locality Name (eg, city) []:Brisbane
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Docker Inc
Organizational Unit Name (eg, section) []:Sales
Common Name (e.g. server FQDN or YOUR name) []:$HOST
Email Address []:Sven@home.org.au
```

Now that you have a CA, you can create a server key and certificate
signing request (CSR). Make sure that "Common Name" matches the hostname you use
to connect to Docker:

> Note
>
> Replace all instances of `$HOST` in the following example with the
> DNS name of your Docker daemon's host.

```console
$ openssl genrsa -out server-key.pem 4096
Generating RSA private key, 4096 bit long modulus
.....................................................................++
.................................................................................................++
e is 65537 (0x10001)

$ openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr
```

Next, we're going to sign the public key with our CA:

Since TLS connections can be made through IP address as well as DNS name, the IP addresses
need to be specified when creating the certificate. For example, to allow connections
using `10.10.10.20` and `127.0.0.1`:

```console
$ echo subjectAltName = DNS:$HOST,IP:10.10.10.20,IP:127.0.0.1 >> extfile.cnf
```

Set the Docker daemon key's extended usage attributes to be used only for
server authentication:

```console
$ echo extendedKeyUsage = serverAuth >> extfile.cnf
```

Now, generate the signed certificate:

```console
$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out server-cert.pem -extfile extfile.cnf
Signature ok
subject=/CN=your.host.com
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

[Authorization plugins](https://docs.docker.com/engine/extend/plugins_authorization/) offer more
fine-grained control to supplement authentication from mutual TLS. In addition
to other information described in the above document, authorization plugins
running on a Docker daemon receive the certificate information for connecting
Docker clients.

For client authentication, create a client key and certificate signing
request:

> Note
>
> For simplicity of the next couple of steps, you may perform this
> step on the Docker daemon's host machine as well.

```console
$ openssl genrsa -out key.pem 4096
Generating RSA private key, 4096 bit long modulus
.........................................................++
................++
e is 65537 (0x10001)

$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
```

To make the key suitable for client authentication, create a new extensions
config file:

```console
$ echo extendedKeyUsage = clientAuth > extfile-client.cnf
```

Now, generate the signed certificate:

```console
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out cert.pem -extfile extfile-client.cnf
Signature ok
subject=/CN=client
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

After generating `cert.pem` and `server-cert.pem` you can safely remove the
two certificate signing requests and extensions config files:

```console
$ rm -v client.csr server.csr extfile.cnf extfile-client.cnf
```

With a default `umask` of 022, your secret keys are *world-readable* and
writable for you and your group.

To protect your keys from accidental damage, remove their
write permissions. To make them only readable by you, change file modes as follows:

```console
$ chmod -v 0400 ca-key.pem key.pem server-key.pem
```

Certificates can be world-readable, but you might want to remove write access to
prevent accidental damage:

```console
$ chmod -v 0444 ca.pem server-cert.pem cert.pem
```

Now you can make the Docker daemon only accept connections from clients
providing a certificate trusted by your CA:

```console
$ dockerd \
    --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=server-cert.pem \
    --tlskey=server-key.pem \
    -H=0.0.0.0:2376
```

To connect to Docker and validate its certificate, provide your client keys,
certificates and trusted CA:

> Tip
>
> This step should be run on your Docker client machine. As such, you
> need to copy your CA certificate, your server certificate, and your client
> certificate to that machine.

> Note
>
> Replace all instances of `$HOST` in the following example with the
> DNS name of your Docker daemon's host.

```console
$ docker --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=cert.pem \
    --tlskey=key.pem \
    -H=$HOST:2376 version
```

> Note
>
> Docker over TLS should run on TCP port 2376.

> Warning
>
> As shown in the example above, you don't need to run the `docker` client
> with `sudo` or the `docker` group when you use certificate authentication.
> That means anyone with the keys can give any instructions to your Docker
> daemon, giving them root access to the machine hosting the daemon. Guard
> these keys as you would a root password!

### Secure by default

If you want to secure your Docker client connections by default, you can move
the files to the `.docker` directory in your home directory --- and set the
`DOCKER_HOST` and `DOCKER_TLS_VERIFY` variables as well (instead of passing
`-H=tcp://$HOST:2376` and `--tlsverify` on every call).

```console
$ mkdir -pv ~/.docker
$ cp -v {ca,cert,key}.pem ~/.docker

$ export DOCKER_HOST=tcp://$HOST:2376 DOCKER_TLS_VERIFY=1
```

Docker now connects securely by default:

```
$ docker ps
```

### Other modes

If you don't want to have complete two-way authentication, you can run
Docker in various other modes by mixing the flags.

#### Daemon modes

- `tlsverify`, `tlscacert`, `tlscert`, `tlskey` set: Authenticate clients
- `tls`, `tlscert`, `tlskey`: Do not authenticate clients

#### Client modes

- `tls`: Authenticate server based on public/default CA pool
- `tlsverify`, `tlscacert`: Authenticate server based on given CA
- `tls`, `tlscert`, `tlskey`: Authenticate with client certificate, do not
  authenticate server based on given CA
- `tlsverify`, `tlscacert`, `tlscert`, `tlskey`: Authenticate with client
  certificate and authenticate server based on given CA

If found, the client sends its client certificate, so you just need
to drop your keys into `~/.docker/{ca,cert,key}.pem`. Alternatively,
if you want to store your keys in another location, you can specify that
location using the environment variable `DOCKER_CERT_PATH`.

```console
$ export DOCKER_CERT_PATH=~/.docker/zone1/
$ docker --tlsverify ps
```

#### Connecting to the secure Docker port usingcurl

To use `curl` to make test API requests, you need to use three extra command line
flags:

```console
$ curl https://$HOST:2376/images/json \
  --cert ~/.docker/cert.pem \
  --key ~/.docker/key.pem \
  --cacert ~/.docker/ca.pem
```

## Related information

- [Using certificates for repository client verification](https://docs.docker.com/engine/security/certificates/)
- [Use trusted images](https://docs.docker.com/engine/security/trust/)

---

# Tips

> Tips for the Rootless mode

# Tips

   Table of contents

---

## Advanced usage

### Daemon

The systemd unit file is installed as `~/.config/systemd/user/docker.service`.

Use `systemctl --user` to manage the lifecycle of the daemon:

```console
$ systemctl --user start docker
```

To launch the daemon on system startup, enable the systemd service and lingering:

```console
$ systemctl --user enable docker
$ sudo loginctl enable-linger $(whoami)
```

Starting Rootless Docker as a systemd-wide service (`/etc/systemd/system/docker.service`)
is not supported, even with the `User=` directive.

To run the daemon directly without systemd, you need to run `dockerd-rootless.sh` instead of `dockerd`.

The following environment variables must be set:

- `$HOME`: the home directory
- `$XDG_RUNTIME_DIR`: an ephemeral directory that is only accessible by the expected user, e,g, `~/.docker/run`.
  The directory should be removed on every host shutdown.
  The directory can be on tmpfs, however, should not be under `/tmp`.
  Locating this directory under `/tmp` might be vulnerable to TOCTOU attack.

It's important to note that with directory paths:

- The socket path is set to `$XDG_RUNTIME_DIR/docker.sock` by default.
  `$XDG_RUNTIME_DIR` is typically set to `/run/user/$UID`.
- The data dir is set to `~/.local/share/docker` by default.
  The data dir should not be on NFS.
- The daemon config dir is set to `~/.config/docker` by default.
  This directory is different from `~/.docker` that is used by the client.

### Client

Since Docker Engine v23.0, `dockerd-rootless-setuptool.sh install` automatically configures
the `docker` CLI to use the `rootless` context.

Prior to Docker Engine v23.0, a user had to specify either the socket path or the CLI context explicitly.

To specify the socket path using `$DOCKER_HOST`:

```console
$ export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
$ docker run -d -p 8080:80 nginx
```

To specify the CLI context using `docker context`:

```console
$ docker context use rootless
rootless
Current context is now "rootless"
$ docker run -d -p 8080:80 nginx
```

## Best practices

### Rootless Docker in Docker

To run Rootless Docker inside "rootful" Docker, use the `docker:<version>-dind-rootless`
image instead of `docker:<version>-dind`.

```console
$ docker run -d --name dind-rootless --privileged docker:25.0-dind-rootless
```

The `docker:<version>-dind-rootless` image runs as a non-root user (UID 1000).
However, `--privileged` is required for disabling seccomp, AppArmor, and mount
masks.

### Expose Docker API socket through TCP

To expose the Docker API socket through TCP, you need to launch `dockerd-rootless.sh`
with `DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp"`.

```console
$ DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp" \
  dockerd-rootless.sh \
  -H tcp://0.0.0.0:2376 \
  --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem
```

### Expose Docker API socket through SSH

To expose the Docker API socket through SSH, you need to make sure `$DOCKER_HOST`
is set on the remote host.

```console
$ ssh -l REMOTEUSER REMOTEHOST 'echo $DOCKER_HOST'
unix:///run/user/1001/docker.sock
$ docker -H ssh://REMOTEUSER@REMOTEHOST run ...
```

### Routing ping packets

On some distributions, `ping` does not work by default.

Add `net.ipv4.ping_group_range = 0 2147483647` to `/etc/sysctl.conf` (or
`/etc/sysctl.d`) and run `sudo sysctl --system` to allow using `ping`.

### Exposing privileged ports

To expose privileged ports (< 1024), set `CAP_NET_BIND_SERVICE` on `rootlesskit` binary and restart the daemon.

```console
$ sudo setcap cap_net_bind_service=ep $(which rootlesskit)
$ systemctl --user restart docker
```

Or add `net.ipv4.ip_unprivileged_port_start=0` to `/etc/sysctl.conf` (or
`/etc/sysctl.d`) and run `sudo sysctl --system`.

### Limiting resources

Limiting resources with cgroup-related `docker run` flags such as `--cpus`, `--memory`, `--pids-limit`
is supported only when running with cgroup v2 and systemd.
See
[Changing cgroup version](https://docs.docker.com/engine/containers/runmetrics/) to enable cgroup v2.

If `docker info` shows `none` as `Cgroup Driver`, the conditions are not satisfied.
When these conditions are not satisfied, rootless mode ignores the cgroup-related `docker run` flags.
See [Limiting resources without cgroup](#limiting-resources-without-cgroup) for workarounds.

If `docker info` shows `systemd` as `Cgroup Driver`, the conditions are satisfied.
However, typically, only `memory` and `pids` controllers are delegated to non-root users by default.

```console
$ cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/cgroup.controllers
memory pids
```

To allow delegation of all controllers, you need to change the systemd configuration as follows:

```console
# mkdir -p /etc/systemd/system/user@.service.d
# cat > /etc/systemd/system/user@.service.d/delegate.conf << EOF
[Service]
Delegate=cpu cpuset io memory pids
EOF
# systemctl daemon-reload
```

> Note
>
> Delegating `cpuset` requires systemd 244 or later.

#### Limiting resources without cgroup

Even when cgroup is not available, you can still use the traditional `ulimit` and [cpulimit](https://github.com/opsengine/cpulimit),
though they work in process-granularity rather than in container-granularity,
and can be arbitrarily disabled by the container process.

For example:

- To limit CPU usage to 0.5 cores (similar to `docker run --cpus 0.5`):
  `docker run <IMAGE> cpulimit --limit=50 --include-children <COMMAND>`
- To limit max VSZ to 64MiB (similar to `docker run --memory 64m`):
  `docker run <IMAGE> sh -c "ulimit -v 65536; <COMMAND>"`
- To limit max number of processes to 100 per namespaced UID 2000
  (similar to `docker run --pids-limit=100`):
  `docker run --user 2000 --ulimit nproc=100 <IMAGE> <COMMAND>`
