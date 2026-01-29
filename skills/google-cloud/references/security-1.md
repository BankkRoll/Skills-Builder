# BeyondProdStay organized with collectionsSave and categorize content based on your preferences.

# BeyondProdStay organized with collectionsSave and categorize content based on your preferences.

# BeyondProdStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

This document describes how Google implements security in our infrastructure
using a cloud-native architecture called *BeyondProd*.
BeyondProd refers to services and controls in our infrastructure
that work together to help protect workloads. Workloads are the unique tasks
that an application completes. BeyondProd helps protect the
microservices that we run in our environment, including how we change code and
how we access user data.

This document is part of a series of technical papers that describe the
technologies, such as
[Chrome Enterprise Premium](https://cloud.google.com/beyondcorp),
 that we have
developed to help defend Google platforms from sophisticated threats. Chrome Enterprise Premium
implements a zero-trust architecture that is designed to provide secure access
to Google platforms and the services running on it. Like Chrome Enterprise Premium,
BeyondProd does not rely on traditional network perimeter
protections such as firewalls. Instead, BeyondProd helps create
trust between microservices using characteristics such as code provenance,
service identities, and trusted hardware. This trust extends to software that
runs in Google Cloud and software that is deployed and accessed by Google Cloud
customers.

This document describes the benefits of BeyondProd, its services
and processes, and how we migrated to this architecture. For an overview of our
infrastructure security, see the
[Google infrastructure security design overview](https://cloud.google.com/security/infrastructure/design).

## Introduction

Modern security architectures have moved away from a traditional
perimeter-based security model where a firewall protects the perimeter and any
users or services within the perimeter are considered trusted.

Today, users are mobile and commonly operate outside an organization's
traditional security perimeter such as from their homes, a coffee shop, or an
airplane. Using Chrome Enterprise Premium, we grant access to company resources using multiple
factors, including the identity of the user, the identity of the device that is
being used to access the resource, the health of the device, trust signals such
as user behavior, and access control lists.

BeyondProd addresses the same concern for production services as
Chrome Enterprise Premium does for users. In a cloud-native architecture, we can't simply rely
on a firewall to protect the production network. Microservices move and are
deployed in different environments, across heterogeneous hosts, and operate at
various levels of trust and sensitivity. Where Chrome Enterprise Premium states that *user*
trust should be dependent on characteristics like the context-aware state of
devices and not the ability to connect to the corporate network,
BeyondProd states that *service trust* should depend on
characteristics like code provenance, trusted hardware, and service identity,
rather than the location in the production network, such as IP address or
hostname.

## Containerized infrastructure

Our infrastructure deploys workloads as individual microservices in containers.
Microservices separate the individual tasks that an application needs to perform
into different services. Each service can be developed and managed
independently with their own API, rollout, scaling, and quota management.
Microservices are independent, modular, dynamic, and ephemeral. They can be
distributed across many hosts, clusters, or even clouds. In a microservice
architecture, a workload may be one or multiple microservices.

A containerized infrastructure means that each microservice is deployed as its
own set of moveable and scheduleable containers. To manage these containers
internally, we developed a
[container orchestration system](https://queue.acm.org/detail.cfm?id=2898444)
called
[Borg](https://research.google.com/pubs/pub43438.html),

which deploys several billion containers a week. Borg is Google's unified
container management system, and the inspiration for
[Kubernetes](http://kubernetes.io/).

Containers make workloads easier and more efficient to schedule across machines.
Packaging microservices in containers enable workloads to be split into smaller,
more manageable units for maintenance and discovery. This architecture scales
workloads as needed: if there is high demand for a particular workload, there
may be multiple machines running copies of the same container to handle the
required scale of the workload.

At Google, security plays a critical role in every evolution in our
architecture. Our goal with this microservice architecture and development
process is to address security issues as early in the development and deployment
lifecycle as possible (when addressing issues is less costly) and to do so in a
way that is standardized and consistent. The end result is that developers spend
less time on security while still achieving more secure outcomes.

## BeyondProd benefits

BeyondProd provides many automation and security benefits to
Google infrastructure. The benefits include the following:

- **Network edge protection:** Workloads are isolated from network
  attacks and unauthorized traffic from the internet. Although a perimeter
  approach is not a new concept, it remains a security best practice for
  cloud architectures. A perimeter approach helps protect as much
  infrastructure as possible against unauthorized traffic and potential
  attacks from the internet, such as volume-based DoS attacks.
- **No inherent mutual trust between services:** Only authenticated,
  trusted, and specifically authorized callers or services can access any
  other service. This stops attackers from using untrusted code to access a
  service. If a service is compromised, this benefit helps prevent the
  attacker from performing actions that allow them to expand their reach.
  This mutual distrust, combined with granular access control, helps to limit
  the blast radius of a compromise.
- **Trusted machines that run code with known provenance:** Service
  identities are constrained to use only authorized code and configurations,
  and run only in authorized, verified environments.
- **Consistent policy enforcement across services:** Consistent policy
  enforcement helps ensure that access decisions are dependable across
  services. For example, you can create a policy enforcement that verifies
  requests for access to user data. To access the service, an authorized end
  user must present a validated request, and an administrator must provide
  a business justification.
- **Simple, automated, and standardized change rollout:** Infrastructure
  changes can be easily reviewed for their impact on security, and security
  patches can be rolled out with little impact on production.
- **Isolation between workloads that share an operating system:** If a
  service is compromised, it can't affect the security of another workload
  running on the same host. This isolation helps to limit the blast radius of a compromise.
- **Trusted hardware and attestation:** A hardware root of trust helps
  ensure that only known and authorized code (from firmware to user mode) is
  running on the host before any workloads are scheduled to run on it.

These benefits mean that containers and the microservices that run inside our
cloud architecture can be deployed, communicate with each other, and run next to
each other without weakening the security of our infrastructure. In addition,
individual microservice developers aren't burdened with the security and
implementation details of the underlying infrastructure.

## BeyondProd security services

We designed and developed several BeyondProd security services
to create the benefits discussed in
[BeyondProd benefits](#beyondprod-benefits).
The following sections describe these security services.

### Google Front End for network edge protection

[Google Front End (GFE)](https://cloud.google.com/docs/security/infrastructure/design#google_front_end_service)

provides network edge protection. GFE terminates the connection from the end
user and provides a central point for enforcing TLS best practices.

Even though our emphasis is no longer on perimeter-based security, the GFE is
still an important part of our strategy for protecting internal services against
DoS attacks. GFE is the first point of entry for a user connecting to Google
infrastructure. After a user connects to our infrastructure, GFE is also
responsible for load balancing and rerouting traffic between regions as needed.
GFE is the edge proxy that routes traffic to the right microservice.

Customer VMs on Google Cloud do not register with GFE. Instead, they
register with the Cloud Front End, which is a special configuration of GFE that
uses the Compute Engine networking stack. Cloud Front End lets customer VMs
access a Google service directly using their public or private IP address.
(Private IP addresses are only available when
[Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)
is enabled.)

### Application Layer Transport Security for trust between services

[Application Layer Transport Security (ALTS)](https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security)

helps ensure that there is no inherent mutual trust between services. ALTS is
used for remote procedure call (RPC) authentication,

integrity, traffic encryption, and service identities. ALTS is a mutual
authentication and transport encryption system for services in Google
infrastructure. In general, identities are bound to services instead of to a
specific server name or host. This binding helps seamless microservice
replication, load balancing, and rescheduling across hosts.

Each machine has an ALTS credential that is provisioned using the
[host integrity system](#host-integrity),
and can only be decrypted if the host integrity system has verified that secure
boot was successful. Most Google services run as microservices on top of Borg,
and these microservices each have their own ALTS identity. Borg Prime,

Borg's centralized controller, grants these ALTS microservice credentials to
workloads based on the microservice's identity. The machine-level ALTS
credentials form the secure channel for provisioning microservice credentials,
so that only machines that have successfully passed host integrity's verified
boot can host microservice workloads. For more information about ALTS
credentials, see
[Workload certificates](https://cloud.google.com/docs/security/encryption-in-transit/application-layer-transport-security#workload_certificates).

### Binary Authorization for Borg for code provenance

[Binary Authorization for Borg (BAB)](https://cloud.google.com/docs/security/binary-authorization-for-borg)

provides code provenance verification. BAB is a deploy-time enforcement check
that helps ensure that code meets internal security requirements before the code
is deployed. For example, the BAB enforcement check includes ensuring that
changes are reviewed by a second engineer before code is submitted to our source
code repository, and binaries are verifiably built on dedicated infrastructure.
In our infrastructure, BAB restricts the deployment of unauthorized
microservices.

### Host integrity for machine trust

Host integrity

verifies the integrity of the host system software through a secure boot process
and is backed by a hardware root of trust security chip (called
[Titan](https://research.google/pubs/pub46352/))
where supported. Host integrity checks include verifying digital signatures on
the BIOS, baseboard management controller (BMC),

bootloader, and OS kernel. Where supported, host integrity checks can include
user-mode code and peripheral firmware (such as NICs). In addition to digital
signature verification, host integrity helps ensure that each host is running
the intended version of these software components.

### Service access management and end-user context tickets for policy enforcement

[Service access](https://cloud.google.com/security/infrastructure/design#inter-service_access_management) management

and
[end-user context tickets](https://cloud.google.com/docs/security/infrastructure/design#access-management-of-end-user-data-in-google-workspace)

help provide consistent policy enforcement across services.

Service access management limits how data is accessed between services. When an
RPC is sent from one service to another, service access management defines the
authorization and auditing policies that services require to access the receiving
service's data. This limits how data is accessed, grants the minimal level of
access needed, and specifies how that access can be audited. In Google
infrastructure, service access management limits one microservice's access to
another microservice's data, and allows for global analyses of access controls.

End-user context tickets are issued by an end-user authentication service, and
provide services with a user identity that is separate from their service
identity. These tickets are integrity-protected, centrally-issued, forwardable
credentials that attest to the identity of an end user who made a request of the
service. These tickets reduce the need for trust between services, as peer
identities using ALTS can be insufficient to grant access, when such access
decisions are typically also based on the end user's identity.

### Borg tooling for automatic rollout of changes and scalability

Borg
tooling for blue-green deployments provides simple, automated, and standardized
change rollout.

A
[blue-green deployment](https://en.wikipedia.org/wiki/Blue-green_deployment)
is a way to roll out a change to a workload without affecting incoming traffic,
so that end users don't experience any downtime in accessing the application.

A Borg job

is a single instance of a microservice, running some part of an application.
Jobs are scaled to handle load, with new jobs deployed when the load increases,
and existing jobs terminated when the load diminishes.

Borg tooling is responsible for migrating running workloads when we perform
maintenance tasks. When a new Borg job is deployed, a load balancer gradually
moves traffic from an existing job to the new one. This allows a microservice to
be updated with no downtime and without the user noticing.

We also use this tool to apply service upgrades when we add new features, and to
apply critical security updates with no downtime.
For changes that affect our infrastructure, we use
[live migration](https://cloud.google.com/compute/docs/instances/live-migration)
of customer VMs to help ensure workloads are not impacted.

For more information, see [Binary Authorization for Borg](https://cloud.google.com/docs/security/binary-authorization-for-borg).

### gVisor kernel for workload isolation

The
[gVisor kernel](https://gvisor.dev/)

allows for isolation between workloads that share an operating system. gVisor
uses a user space kernel to intercept and handle syscalls, reducing the
interaction with the host and the potential attack surface. This kernel provides
most of the functionality required to run an application, and limits the host
kernel surface that is accessible to the application. gVisor is one of several
tools that we use to isolate internal workloads and Google Cloud customer
workloads that run on the same host. For more information about other sandboxing
tools, see
[Code Sandboxing](https://developers.google.com/code-sandboxing).

## Protecting user data with BeyondProd

This section describes how BeyondProd services work together to
help protect user data in our infrastructure. The sections below describe two
examples:

- Accessing user data requests from their creation to delivery at their
  destination.
- A code change from development to production.

Not all the technologies that are listed are used in all parts of our
infrastructure; it depends on the services and workloads.

### Accessing user data

The diagram below shows the process that our infrastructure uses to verify that
a user is permitted to access user data.

![Google's cloud-native security controls accessing user data.](https://cloud.google.com/static/docs/security/beyondprod/images/beyondprod-accessing-data.svg)

The steps to access user accounts are as follows:

1. A user sends a request to GFE.
2. GFE terminates the TLS connection and forwards the request to the
  appropriate service's frontend using ALTS.
3. The application frontend authenticates the user's request using a
  central end-user authentication (EUA) service and, if successful, receives
  a short-lived, cryptographic end-user context ticket.
4. The application frontend makes an RPC over ALTS to a storage backend
  service, forwarding the ticket in the backend request.
5. The backend service uses service access management to ensure the
  following criteria is true:
  - The frontend is authenticated using a valid, unrevoked
    certificate. This check implies it is running on a trusted host and BAB
    checks have succeeded.
  - The frontend service's ALTS identity is authorized to make
    requests to the backend service and present an EUC ticket.
  - The end-user context ticket is valid.
  - The user in the EUC ticket is authorized to access the requested data.

If any of these checks fail, the request is denied.

If these checks pass, then the data is returned to the authorized
application frontend, and served to the authorized user.

In many cases, there is a chain of backend calls and every intermediary service
does a service access check on inbound RPCs, and the ticket is forwarded on
outbound RPCs.

For more information about how traffic is routed inside our infrastructure, see
[How traffic gets routed](https://cloud.google.com/security/encryption-in-transit#how_traffic_gets_routed).

### Making a code change

The diagram below shows how a code change is deployed.

![How code changes are made.](https://cloud.google.com/static/docs/security/beyondprod/images/beyondprod-making-code-change.svg)

The steps to make a code change are as follows:

1. A developer makes a change to a microservice protected by BAB. The
  change is submitted to our central code repository,
  which enforces code review.
  After approval, the change is submitted to the central, trusted build
  system
  which produces a package with a signed verifiable build manifest
  certificate.
2. At deployment time, BAB verifies this process was followed by validating
  the signed certificate from the build pipeline.
3. Borg handles all workload updates using a reliability model that ensures
  minimal interruption to services, whether it's a routine rollout or an
  emergency security patch.
4. GFE moves traffic over to the new deployment using load-balancing to
  help ensure continuity of operations.

For more information about this process, see
[Our development and production process](https://cloud.google.com/docs/security/binary-authorization-for-borg#our_development_and_production_process).

All workloads require isolation. If the workload is less trusted because the
source code originates from outside of Google, the workload is deployed with
stronger layers of isolation, such as being deployed into a gVisor-protected
environment. This isolation helps to contain an adversary who manages to
compromise an application.

## Cloud-native security implications

The following sections provide a comparison between aspects of traditional
infrastructure security and their counterpoints in a cloud native
architecture.

### Application architecture

A more traditional security model, focused on perimeter-based security, can't
protect a cloud-native architecture by itself. Traditionally, monolithic
applications used a three-tier architecture and were deployed to private
corporate data centers which had enough capacity to handle peak load for
critical events. Applications with specific hardware or network requirements
were purposefully deployed onto specific machines which typically maintain fixed
IP addresses. Rollouts were infrequent, large, and hard to coordinate as the
resulting changes simultaneously affected many parts of the application. This led
to very long-lived applications that are updated less frequently and where
security patches are typically less frequently applied.

However, in a cloud-native model, applications must be portable between
different environments, because they can run in public clouds, private data
centers, or third-party hosted services. Therefore, instead of a monolithic
application, a containerized application that is split into microservices
becomes ideal for cloud environments. Containers decouple the binaries that your
application needs from the underlying host operating system, and make
applications more portable. Our containers are immutable, meaning that they
don't change after they're deployed. Instead, they're rebuilt and redeployed
frequently.

With containers being restarted, stopped, or rescheduled often, there is more
frequent reuse and sharing of hardware and networking. With a common
standardized build and distribution process, the development process is more
consistent and uniform between teams, even though teams independently manage the
development of their microservices. As a result, security considerations (such
as security reviews, code scanning, and vulnerability management), can be
addressed early in development cycles.

### Service mesh

By building shared and securely designed infrastructure that all developers
use, the burden on developers to know and implement common security requirements
is minimized. Security functionality should require little to no integration
into each application, and is instead provided as a fabric enveloping and
connecting all microservices. This is commonly called a *service mesh*. This
also means that security can be managed and implemented separately from regular
development or deployment activities.

A service mesh is a shared fabric at the infrastructure layer that envelops and
connects all microservices. A service mesh allows for service-to-service
communication, which can control traffic, apply policies, and provide
centralized monitoring for service calls.

### Zero-trust security

In a traditional security model that uses private data centers, an
organization's applications depend on a firewall to help protect workloads from
external network-based threats.

With a zero-trust security model, authorization decisions don't depend on firewalls. Instead, other
controls, like workload identity, authentication, and authorization, help
protect microservices by ensuring internal or external connections are validated
before they can transact. When you remove your dependence on firewalls or
network-based controls, you can implement microservice-level segmentation, with
no inherent trust between services. With microservice-level segmentation,
traffic can have varying levels of trust with different controls and you are no
longer only comparing internal to external traffic.

### Shared security requirements that are integrated into service stacks

In a traditional security model, individual applications are responsible for
meeting their own security requirements independently of other services. Such
requirements include identity management, TLS termination, and data access
management. This can lead to inconsistent implementations or unaddressed
security issues as these issues have to be fixed in many places, which makes
fixes harder to apply.

In a cloud-native architecture, components are much more frequently re-used
between services. Choke points allow for policies to be consistently enforced
across services. Different policies can be enforced using different security
services. Rather than requiring every application to implement critical security
services separately, you can split out the various policies into separate
microservices. For example, you can create one policy to ensure authorized
access to user data, and create another policy to ensure the use of up-to-date
TLS cipher suites.

### Standardized processes with more frequent rollouts

In a traditional security model, there are limited shared services, and code is
often duplicated and coupled with local development. Limited sharing makes it
more difficult to determine the impact of a change and how the change could
affect many parts of an application. As a result, rollouts are infrequent and
difficult to coordinate. To make a change, developers might have to update each
component directly (for example, opening SSH connections to each virtual machine
to update a configuration). Overall, this can lead to extremely long-lived
applications.

From a security perspective, as code is often duplicated, it is more difficult
to review, and even more challenging to ensure that when a vulnerability is
fixed, it is fixed everywhere.

In a cloud-native architecture, rollouts are frequent and standardized. This
process enables security to *shift left* in the software development lifecycle.
Shifting left refers to moving steps earlier in the software development
lifecycle, which may include steps like code, build, test, validate, and deploy.
 Shifting left enables simpler and more consistent enforcement of security,
including regular application of security patches.

## Making the change to BeyondProd

Google's transition to BeyondProd required changes in two main
areas: in our infrastructure and in our development process. We tackled these
changes simultaneously, but you can address them independently if you want to
set up something similar in your environment.

### Changing our infrastructure

Our goal is to automate security across our entire infrastructure because we
believe security should scale in the same way that services scale. Services must
be secure by default and insecure only after an explicit decision was made to accept the risks. Direct human intervention to our
infrastructure should be by exception, not routine, and the interventions should
be auditable when they occur. We can then authenticate a service based on the
code and configuration that is deployed for the service, instead of based on the
people who deployed the service.

We started by building a strong foundation of service identity, authentication,
and authorization.  A microservice uses a service identity

to authenticate itself to other services running in the infrastructure. Having
a foundation of trusted service identities enabled us to implement higher-level
security capabilities dependent on validating these service identities, such as
service access management and end-user context tickets. To make this transition
simple for both new and existing services, ALTS was first provided as a library
with a single helper daemon. This daemon ran on the host called by every
service, and evolved over time into a library that uses service credentials. The
ALTS library was integrated seamlessly into the core RPC library. This
integration made it easier to gain wide adoption, without significant burden on
individual development teams. ALTS rollout was a prerequisite to rolling out
service access management and end-user context tickets.

### Changing our development processes

It was critical for Google to establish a robust build and code review process
to ensure the integrity of services that are running. We created a central build
process where we could begin enforcing requirements such as a two-person code
review and automated testing at build and deployment time. (See
[Binary Authorization for Borg](https://cloud.google.com/security/binary-authorization-for-borg)
for more details on deployment.)

After we had the basics in place, we started to address the need to run
external, untrusted code in our environments. To achieve this goal, we started
sandboxing, first with
[ptrace](https://en.wikipedia.org/wiki/Ptrace),
then later using gVisor. Similarly, blue-green deployments provided significant
benefits in terms of security (for example, patching) and reliability.

We quickly discovered that it was easier if a service started out by logging
policy violations rather than blocking violations. The benefit of this approach
was two-fold:

- It gave the service owners a chance to test the change and gauge the
  impact (if any) that moving to a cloud-native environment would have on
  their service.
- It enabled us to fix any bugs and identify any additional functionality
  that we might need to provide to service teams.

For example, when a service is onboarded to BAB, the service owners enable
audit-only mode. This helps them identify code or workflows that don't meet
their requirements. After they address the issues flagged by audit-only mode,
the service owners switch to enforcement mode. In gVisor, we did this by first
sandboxing workloads, even with compatibility gaps in the sandboxing
capabilities, and then addressing these gaps systematically to improve the
sandbox.

## What's next

- For an overview of our infrastructure security, see the
  [Google infrastructure security design overview](https://cloud.google.com/security/infrastructure/design).
- Read about
  [Binary Authorization for Borg](https://cloud.google.com/docs/security/binary-authorization-for-borg),
  which we use to help protect our deployments.
- To learn more about how we protect our infrastructure, read
  [Building secure and reliable systems (O'Reilly book)](https://www.oreilly.com/library/view/building-secure-and/9781492083115/)
- To adopt a secure CI/CD pipeline, see
  [Supply chain Levels for Software Artifacts (SLSA)](https://slsa.dev/).
- For general information on Google Cloud security, including
  security best practices, see the
  [Security section of the Google Cloud website](https://cloud.google.com/security).
- For information on Google Cloud compliance and compliance
  certifications, see the
  [Compliance section of the Google Cloud website](https://cloud.google.com/security/compliance).

   Was this helpful?
