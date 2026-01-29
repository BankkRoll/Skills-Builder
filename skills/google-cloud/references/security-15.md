# How Google protects its production servicesStay organized with collectionsSave and categorize content based on your preferences.

# How Google protects its production servicesStay organized with collectionsSave and categorize content based on your preferences.

> Discover how Google protects production services, workloads, and machines.

# How Google protects its production servicesStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in June 2024, and represents the status quo as
of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

Google runs a global-scale, multi-tenant, and distributed computing
infrastructure to provide products and services to billions of people around the
world. This infrastructure must balance the competing priorities of security,
reliability, resilience, efficiency, development velocity, debuggability, and
more.

This document describes some of the mechanisms that we use to maintain an
industry-leading security posture for services that run in Google's production
environment. These services occupy the full spectrum of security sensitivity,
from development experiments that have no access to any sensitive data to
critical identity infrastructure. These services complete tasks such as
processing user data, managing software rollouts, and provisioning and lifecycle
management for individual physical machines.

This document describes the security controls that help protect the following
three key layers of our infrastructure:

- Production services, which include the most security-critical services
  (also known as *foundational services*)
- Production machines
- Production workloads

We apply these controls so that Google
personnel can only access services, machines, and workloads for legitimate
business purposes (for example, maintenance access), and to defend against
insider risk and personnel account compromise. These controls provide further
defense-in-depth protection that supplements the existing [infrastructure
security
controls](https://cloud.google.com/docs/security/infrastructure/design#keeping_employee_devices_and_credentials_safe)
that help prevent account compromise.

## Continuous improvement

The controls that are described in this paper are used throughout Google's
production environment. Many services, including foundational services, use the
latest levels of controls that we offer. However, due to the scope and
complexity of Google's infrastructure, individual production services often have
unique requirements and might require additional time to implement the latest
recommendations. Through a culture of continuous improvement, Google's
[Site Reliability Engineering (SRE)](https://sre.google/)
and security teams constantly adapt security controls to meet the changing
threat landscape.

## Protecting production services

Google helps protect the integrity of production services so that Google
personnel can only access the services for a legitimate business purpose, like
maintenance. There are two primary ways to gain access to services that run in
the production environment: through administrative access and through the
software supply chain.

The following list describes the controls that help protect each access path.

- **Administrative access controls**: Production services need regular
  maintenance (for example, binary or configuration rollouts). At Google, our
  goal is that such operations are done through automation, safe proxies, or
  audited emergency access, following the
  [Zero Touch Prod](https://www.usenix.org/conference/srecon19emea/presentation/czapinski)
  philosophy. The suite of controls that removes human access to production
  assets is called
  [No Persons (NoPe)](#administrative-access-controls).
  NoPe gives Google the flexibility to deploy access controls that are based
  on the sensitivity of a production service and its readiness to achieve an
  even stronger posture through continuous improvement.
  For example, Google doesn't allow unilateral access to foundational
  services — even emergency access requires approval from other Google
  personnel. An access is *unilateral* if someone can perform the access
  without any approval from another authorized individual.
- **Software supply chain controls**: The majority of production workloads at
  Google, including foundational services, run binaries and job configurations
  that are built verifiably from peer-reviewed code that is located in a
  trusted source. We enforce this process using [Binary Authorization for Borg
  (BAB)](#binary-authorization-borg).

The following diagram shows the controls that help protect a production
service.

![Controls that help protect production services.](https://cloud.google.com/static/docs/security/images/protecting-prod-services.svg)

When we apply the highest levels of NoPe and BAB, we help ensure that no
personnel has unilateral access, even in emergencies, to foundational services,
and that any privileged access they receive has a well-defined scope and
duration. Privileged access is an elevated level of access granted to
personnel to administer critical production services during unique circumstances
that are not addressed by automation. We make an exception to this rule to
ensure that Google has a way to get out of lockout situations.

Many other production services, including products like Filestore or
Cloud SQL and internal infrastructure products like
Borg and
[Spanner](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf),
are configured to use the highest levels of NoPe and BAB, and we are
continuously working towards making it easier for production service owners to
adopt NoPe and BAB over time.

### Administrative access controls

On Borg, members of a production role can read, write, or delete the
data that the production role owns, and they can execute code using the role's
authority. A production role is an identity that can run workloads in Google's
production environment.

Permanent membership in production roles carries the risk of unintended
consequences for production, and the risk that these privileges can be abused.
However, SRE's mission demands that teams be empowered to maintain the services
for which they are responsible, so complete access removal might not be a viable
strategy.

The NoPe suite provides a way to configure access that balances the competing
demands of empowering teams and keeping production systems safe. With NoPe,
Google personnel encounter constraints on the privileges of their accounts when
they try to access production services. NoPe allows for the following
constraints:

- **Access requests require an approver and a justification**: a control that
  is called *multi-party authorization (MPA)* helps ensure
  that Google personnel can't gain access to production services without a
  business justification and an approval from another individual who is
  authorized to verify the access request.
- **No direct access to production service roles**: personnel can only access
  production services through [safe proxies for NoPe](#safe-proxies-nope).
  Safe proxies are designed so that only a well-defined set of commands can be
  executed. Any commands that Google Security and SRE organizations consider
  risky (for example, turning down a service or accessing or deleting data)
  also require MPA.
- **No permanent production role membership**: a control called
  [access on demand (AoD)](#access-on-demand)
  requires personnel to request temporary membership, rather than
  allowing personnel accounts to always have access privileges. This control
  helps ensure elevated powers are only granted temporarily and for specific
  reasons.
- **Monitoring of personnel access requests to production services**: Google
  requires a periodic audit of access patterns to production roles that run a
  production service. The goal of the audit is to eliminate the need for such
  requests in the future, through continuous improvement of administrative
  APIs. Access to production services should be reserved only for emergency
  response situations. For foundational services, the number of situations
  where access is granted is so low that a security team performs an audit of
  each granted access to confirm its validity.

The following sections discuss each control in detail.

#### Multi-party authorization for NoPe

MPA requires another authorized Google personnel to approve a request for
access.

For requests to access sufficiently sensitive services, MPA also requires that
personnel provide a business justification that references an ongoing
production emergency with each request.

Both of these conditions are barriers against access abuse.

#### Safe proxies for NoPe

Safe proxies are tools that expose a predefined set of commands that the safe
proxy can execute on a caller's behalf. Safe proxies implement fine-grained,
rule-based authorization policies to provide constraints on access to production
services. These policies can, for example, require approval from another
authorized individual to execute commands that could adversely affect security
or reliability (for example, commands that delete files). Policies can also let
certain safe commands (for example, commands that list resource utilization)
execute without requiring approval. This flexibility is critical to minimizing
operational toil.

In cases of access abuse, accounts are still constrained to the operations that
the safe proxy allows. The account can only execute safe commands
unilaterally, while privileged operations require approval from another
authorized individual. All operations leave a clear audit trail.

For more information on safe proxies, see the
[SREcon presentation](https://www.usenix.org/conference/srecon19emea/presentation/czapinski)
on *zero touch prod*. Zero touch prod is a set of principles and tools that
enforce that every change in production is performed by automation (no people
involved), pre-validated by software, or made using an audited emergency-capable
mechanism.

#### Access on demand

Access on demand (AoD) lets Google reduce personnel privileges by replacing
permanent membership with eligible membership.

Eligible members of a role don't have access to its privileges. Instead, if an
eligible role member requires access, they can request temporary membership,
known as an *AoD grant*. If approved by another authorized individual, an AoD
grant makes the requestor a member of the role for a limited amount of time,
typically less than a day.

The eligible membership model lets personnel request only the subset of access
that they need for the duration that they need. Conceptually, you can think of
AoD as a time-bound production `sudo`, similar to the `sudo -u` command in Unix,
which lets you execute some commands with the elevated permissions that are
associated with a specified user. However, unlike Unix `sudo`, receiving an AoD
grant requires a business justification and MPA, and leaves an audit trail. AoD
grants are also time limited.

Securing the sensitive privileges behind eligible memberships means that even in
unlikely cases of access abuse, accounts can only access those privileges when
there is an active grant. The adoption of [safe proxies](#safe-proxies-nope)
largely eliminates the need for such grants.

#### Access request monitoring

Although many areas of Google production use NoPe as an access reduction
practice, AoD grants are exceedingly rare for our most sensitive production
roles and are reserved only for emergency response. Furthermore, each event
triggers a manual, after-the-fact audit. The goal of the audit is to drive down
the frequency of AoD grants in the future (for example, by using these events to
motivate improvements to Administrative APIs).

Google continuously monitors AoD grants, and actions taken while holding those
grants, across the company. We use the real-time monitoring data to detect
potential compromises and identify areas for further access reduction. If an
incident occurs, the audit trail supports rapid response.

### Binary authorization for Borg

Just as NoPe helps protect privileged access paths, Binary Authorization for
Borg (BAB) helps protect the Google software supply chain. BAB helps ensure
that production software and job configurations are reviewed and approved before
they are deployed, particularly when they can access sensitive data. Originally
devised for Google's production infrastructure, the key concepts of BAB are now
included in an open specification that is called
*Supply Chain Levels for Software Artifacts (SLSA)*.

BAB helps ensure that personnel cannot modify source code, run binaries, or
configure jobs without peer review, and that any binary artifact or software
configuration is built verifiably from checked-in, peer-reviewed source code.

For more information, see
[Binary authorization for Borg](https://cloud.google.com/docs/security/binary-authorization-for-borg).

## Protecting production machines

In addition to hardening privileged access paths and maintaining integrity of
the software supply chain, Google protects the machines that production services
run on. In particular, we implement the following:

- **Shell access controls**: Most Google personnel don't have shell
  access (for example, through SSH) to production machines or to workloads
  running on
  [Borg](https://research.google/pubs/pub43438/),
  Google's cluster management system. Instead, individuals must use safe
  proxies that require another authorized person to review and approve each
  command before the command is executed.
  Only a few teams who work on low-level infrastructure retain
  non-unilateral shell access so that they can debug the most complex issues
  where safe proxies are not practical to use. An access is *non-unilateral*
  if it requires authorization from one, or more, additional authorized
  personnel. Google makes
  [one exception](#ssh-in-lockout)
  where unilateral shell access is allowed: to ensure that Google has a way
  to get out of lockout situations.
- **Physical access controls**: Machines need regular physical
  maintenance to keep them running well. To help ensure that data center
  technicians only access physical machines in the context of a valid
  business reason, Google uses
  [physical-to-logical controls](#physical-access-controls).
- **Firmware and system software controls**: Google implements a measured
  boot security flow that is based on a hardware root of trust. Hardware
  root of trust helps
  [ensure the integrity](#firmware-software-controls)
  of each machine's boot firmware and system software.

The following diagram shows the controls that help protect a machine in a data
center.

![Controls that help protect production machines.](https://cloud.google.com/static/docs/security/images/protecting-prod-machines.svg)

### Shell access controls

SSH is an open-source administrative tool that is popular for allowing broad
access to Linux-based servers. Without controls on SSH access, accounts with the
right credentials can obtain a shell that lets them execute arbitrary code in a
hard-to-audit fashion.

With shell access to a production service, the account could, for example,
change the behavior of a running task, exfiltrate credentials, or use
credentials to achieve a persistent foothold in the environment.

To mitigate this risk, we use the following set of controls that replaces SSH
access to production machines with safe, alternative methods:

- **Narrow APIs**: for teams with well-defined workflows that previously
  required SSH, we replace SSH with
  [narrowly defined, auditable APIs](#narrow-apis).
- **Safe proxies for SSH**: for teams that require more flexible access,
  [safe proxies](#safe-proxies-ssh)
  allow commands to be individually authorized and audited.
- **MPA**: when SREs need emergency SSH access to a machine, Google
  requires a business justification and an authorized individual to approve
  the access. Complete shell session transcripts are logged.
- **Lockout scenarios**: the only exception when unilateral SSH access is
  allowed. Complete shell session transcripts are logged.

These controls balance the need for legitimate shell access against the risk
associated with overly broad shell access.

#### Background: SSH at Google

In the past, Google used SSH to administer its machines. The development of Borg
made it possible for most Google personnel to stop requiring direct access to
the Linux machines that run their binaries, but shell access persisted for
several reasons:

- Personnel sometimes require direct access to a machine for debugging
  purposes.
- SSH access is a valuable teaching tool to understand the various layers
  of abstraction.
- In unanticipated disaster recovery scenarios, higher-level tooling might
  not be available.

To balance between these reasons and the security risk that they incurred,
Google pursued a series of milestones to incrementally eliminate SSH risk and
then usage.

##### Centralized monitoring and access control milestone

Google invested in a central SSH monitoring and authorization system known
as
*host identity-based monitoring authorization (HIBA)*.
HIBA provides visibility into any SSH usage and enables enforcement of strict
authorization policies. SSH attempts are logged, not just by the target machine,
but also by the centralized
[BeyondCorp proxy](https://research.google/pubs/beyondcorp-the-access-proxy/).
Commands executed by the shell are logged and fed into malicious behavior
detection pipelines. However, detection is inherently reactive and vulnerable to
evasion and
[obfuscation](https://attack.mitre.org/techniques/T1027/010/).

##### Eliminating unilateral access milestone

For most personnel, Google has removed shell access (for example, through SSH)
to production machines or to workloads running on Borg. However, it remains
accessible on test machines (for example, machines that are used to qualify new
hardware or new low-level software but not run production services) for the
development teams.

#### Narrow APIs

Some Google teams that historically relied on SSH to run a limited number of
precisely defined commands (for example, in a playbook), or to obtain data whose
structure is predictable, now use narrowly-defined APIs that serve the specific
use case and provide structured data.

Narrow APIs have a small number of methods aligned with common user journeys
and abstract away low-level access details. In consequence, they are Google's
preferred solution because they provide best safety and auditability. By
building them on Google's remote procedure call (RPC) infrastructure, we benefit
from decades of investment in security and auditing.

#### Safe proxies for SSH

Some Google teams can't determine the commands that they might need ahead of
time. In this case, Google uses a command-running daemon that only accepts
arbitrary command execution requests from a trusted proxy that is run by a
security team. This technology is similar to the technology used in
[safe proxies for NoPe](#safe-proxies-nope).

Safe proxies for SSH are responsible for fine-grained authorization of command
execution and for auditing. Authorization is based on the command's argument and
environment, rate-limiting parameters, business justifications, and MPA. This
authorization process enables arbitrarily precise restrictions on what commands
can run following team playbooks and best practices. In unexpected failure
conditions that aren't captured in existing playbooks, personnel can still run
the necessary debugging commands after another authorized individual has
approved them.

#### MPA for SSH

The remaining few teams that work on low-level infrastructure retain a
non-unilateral form of shell access to debug the most complex issues.

#### SSH in lockout scenarios

Google makes an exception where unilateral shell access is allowed: to ensure
that Google can remediate lockout situations. The SSH keys that are used for
this purpose are generated with a distinct auditable process and stored offline
on tamper-resistant hardware. When these keys are used, complete shell session
transcripts are logged.

### Physical access controls

Google data centers are a complex environment of servers, networking devices,
and control systems that require a wide range of roles and skills to manage,
maintain, and operate.

Google implements
[six layers of physical controls](https://www.youtube.com/watch?v=kd33UVZhnAA)
and many logical controls on the machines themselves to help protect workloads
in the data center. We also defend a space between the machines, which we call
the *physical-to-logical* space.

Physical-to-logical controls provide additional layers of defense through
controls that are called *machine hardening*, *task-based access control*, and
*system self-defense*. Physical-to-logical controls defend against an adversary
seeking to exploit physical access to a machine and escalate to a logical attack
on the machine's workloads.

For more information, see
[How Google protects the physical-to-logical space in a data center](https://cloud.google.com/docs/security/physical-to-logical-space).

### Firmware and system software controls

The security posture of a data center machine is established at boot time. The
machine's boot process configures the machine's hardware and initializes its
operating system, while keeping the machine safe to run in Google's production
environment.

At each step in the boot process, Google implements industry-leading controls
to help enforce the boot state that we expect and to help keep customer data
safe. These controls help ensure that our machines boot into their intended
software, allowing us to remove vulnerabilities that could compromise the
initial security posture of the machine.

For more information, see
[How Google enforces boot integrity on production machines](https://cloud.google.com/docs/security/boot-integrity).

## Protecting workloads

In keeping with our [zero-trust philosophy](https://cloud.google.com/learn/what-is-zero-trust), Google
has also introduced controls that help defend against lateral movement threats
between workloads with different security requirements. Google infrastructure
uses a workload hierarchy that is called *workload security rings
(WSR)*.
WSR helps ensure that critical workloads aren't scheduled on the same machines
as less secure workloads, while avoiding negative impact on resource
utilization. WSR groups workloads into [four sensitivity
classes](#workload-rings) — foundational, sensitive, hardened, and unhardened —
and attempts to schedule them in different machine pools.

The following diagram shows how WSR groups and schedules workloads across
foundational, production, and development machines.

![WSR groups and schedules for workload protection.](https://cloud.google.com/static/docs/security/images/protecting-workloads.svg)

WSR provide an additional layer of defense against
local privilege escalation using kernel vulnerability attacks or CPU
side-channel attacks. WSR helps ensure that only workloads with similar security
requirements are co-scheduled on the same machines. To implement WSR, we do the
following:

- Classify workloads according to their security requirements. Each class
  is known as a *workload ring*.
- Distribute physical machines across several machine pools that are
  isolated from each other. In other words, we eliminate lateral movement
  paths between pools.
- Apply scheduling constraints to prevent workloads with different security
  requirements from running on the same machine. These scheduling constraints
  mitigate the risk of compromise through local privilege escalation.

For example, WSR requires that foundational workloads run on dedicated machines
and are never co-scheduled with non-foundational workloads. This constraint
provides strong isolation from less secure workloads.

### Methods for isolating workloads

Modern system software is complex, and security researchers periodically
discover local privilege escalation vulnerabilities, such as kernel zero-day
exploits or new CPU side-channel attacks. WSR, first
[introduced](https://www.usenix.org/publications/loginonline/workload-security-rings)
in USENIX `;login:`, lets Google reduce the risk that is associated with
workload colocation while maintaining high resource utilization.

By default, Borg uses OS-level process boundaries to isolate containers. These
processes offer a weaker isolation boundary than virtual machines that use
hardware-based virtualization. Such weaker isolation is typically a good
trade-off between efficiency and security for multi-tenant environments that run
trusted workloads. A *trusted workload* is a workload where the binary and
configuration were verifiably built from peer-reviewed code of attested
provenance. Trusted workloads don't process arbitrary untrusted data.
Examples of processing untrusted data include hosting third-party code or
encoding videos.

Google achieves trust in our binaries by using
[BAB](#binary-authorization-borg).
However, BAB isn't sufficient to ensure the integrity of workloads that process
untrusted data. In addition to BAB, such workloads must also run inside a
*sandbox*. A sandbox is a constrained environment, like
[gVisor](https://gvisor.dev/),
that lets a binary run safely. Both BAB and sandboxes have limitations.

BAB is a strong control for mature products, but it might reduce velocity during
early stages of new systems development and when running experiments with no
sensitive data (for example, optimizing the encoding of data that is already
public). This limitation means that some workloads must always run without BAB.
Such workloads are inherently at a higher risk of local privilege escalation
(for example, by exploiting a kernel vulnerability to gain local root on a
machine).

Sandboxing untrusted workloads also mitigates security risk, but comes at the
price of increased compute and memory use. Efficiency can drop by a double-digit
percentage, depending on the workload and the type of sandbox. For an example of
the performance impacts on a sandboxed workload, see the detailed benchmarks in
the
[gVisor Performance Guide](https://gvisor.dev/docs/architecture_guide/performance/).
WSR lets us address the efficiency limitations that result from isolating
workloads.

### Workload rings

Google defines four classes of workloads according to their security
requirements: foundational, sensitive, hardened, and unhardened. The following
table describes them in more detail.

| Workload ring | Description |
| --- | --- |
| Foundational | Workloads that are critical to Google's security, like identity
and access management services. Foundational workloads have the
highest security requirements, and routinely trade efficiency for
increased security and reliability. |
| Sensitive | Workloads that can cause wide-spread outages or that have access
to sensitive product-specific data, like user or customer data. |
| Hardened | Support workloads that are not security-critical, but have
adopted BAB or are sandboxed, so that they pose little risk to
neighboring workloads. |
| Unhardened | All other workloads, including those running untrusted
code. |

At Google, we classify critical workloads that support specific products as
sensitive, while foundational workloads are workloads that could impact all
products.

Unlike foundational and sensitive, we can classify any workload as hardened
based exclusively on its adopted controls and the type of input that it
processes. With hardened workloads, we are primarily concerned about their
impact on other workloads, so hardening solutions can include sandboxing.

### Machine pools

To avoid co-scheduling sensitive services with workloads that are less trusted
(for example, ones that process untrusted data without a sandbox), we must run
them on isolated pools of machines. Machine isolation makes it easier to
understand the security invariants, but each additional machine pool introduces
tradeoffs in resource utilization and maintainability.

Machine isolation results in lower physical resource utilization, because
ensuring that machine pools are fully utilized becomes harder as we add more
pools. The efficiency cost might become significant when there are several
large, isolated machine pools.

As the resource footprint of workloads fluctuates in each pool, strict
isolation adds management overhead to periodically rebalance and repurpose
machines between pools. Such rebalancing requires draining all workloads from a
machine, rebooting the machine, and performing our most heavy-weight machine sanitization
process that helps ensure
[firmware authenticity and integrity](https://cloud.google.com/docs/security/remote-attestation).

These considerations mean that Google's implementation of machine isolation
must provide ways to optimize utilization of physical resources while also
defending foundational and sensitive workloads against adversaries.

In Kubernetes, this approach is known as
*node isolation*.
Kubernetes nodes can map to physical or virtual machines. In this paper, we're
focusing on physical machines. Also, Google Cloud products like Compute Engine
[offer sole tenancy](https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes)
to provide physical machine isolation.

### Workload scheduling constraints

Google provisions machines into three types of isolated pools: foundational
machines, production machines, and development machines. Google operates several
isolated pools that host foundational and sensitive workloads, but this document
presents each as one pool for simplicity.

To offer the most effective protection, we deploy the following scheduling
constraints for WSR:

- Foundational workloads can only run on foundational machines.
- Sensitive workloads can only run on production machines.
- Unhardened workloads can only run on development machines.
- Hardened workloads can run on production or development machines, with
  preference for production machines.

The following diagram shows the scheduling constraints.

![Scheduling constraints for WSR.](https://cloud.google.com/static/docs/security/images/scheduling-constraints.svg)

In this diagram, isolation boundaries separate different classes of workloads
both between and within machine pools. Foundational workloads are the sole
tenants of dedicated foundational machines. Binary authorization or sandboxing
for workloads running on production machines help prevent local privilege
escalation attacks. On development machines, there's a residual risk that an
unhardened workload could compromise another workload, but the compromise is
limited to the development machines because hardened workloads cannot create new
jobs.

Hardened workloads are scheduled on production machines or development machines
based on availability. Allowing scheduling in multiple pools might seem
counterintuitive, but it's essential to alleviate the utilization drop caused by
the scheduling constraints. Hardened workloads fill gaps that are introduced by
isolating sensitive and unhardened jobs. In addition, the larger that the
hardened resource footprint is, the more fluctuations in resource usage of the
other two classes can be accommodated without the need for expensive machine
moves between rings.

The following diagram shows the scheduling constraints that are imposed on
different classes of workloads. A hardened workload can be located on either a
production machine or a development machine.

![Scheduling constraints for workload classes.](https://cloud.google.com/static/docs/security/images/split-scheduling.svg)

By isolating foundational workloads on several foundational pools, Google
trades resource efficiency for higher security. Fortunately, foundational
workloads tend to have a relatively small resource footprint, and small isolated
pools of dedicated machines have negligible impact on overall utilization.
However, even with extensive automation in place, maintaining multiple machine
pools is not without a cost, so we are constantly evolving our machine designs
for improved isolation.

WSR provides a strong guarantee that non-foundational workloads are never
allowed to run on foundational machines. Foundational machines are protected
against lateral movement, as only foundational workloads can ever run on those
machines.

## Summary of controls

Google uses a number of controls throughout its infrastructure to help protect
production services, production machines, and workloads. The controls include
the following:

- Administrative access controls and BAB for production services
- Shell access controls, physical access controls, and firmware and system
  software controls for production machines
- WSR for different classes of workloads

Together, these controls enforce constraints that help protect Google's users
and customers—and their data. The following diagram illustrates how the
controls work together to support Google's security posture.

![Protecting production services solution.](https://cloud.google.com/static/docs/security/images/protecting-solution.svg)

## What's next

- For more information about security controls on Google infrastructure,
  read
  [Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).
- To learn about Google security culture, read
  [Building secure and reliable systems (O'Reilly book)](https://www.oreilly.com/library/view/building-secure-and/9781492083115/).
- To learn more about zero-touch prod, see the
  [SREcon presentation](https://www.usenix.org/conference/srecon19emea/presentation/czapinski).
