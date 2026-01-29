# Encryption in transit for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

# Encryption in transit for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

# Encryption in transit for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in April 2025, and represents the status quo as
of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers*.

At Google, our security controls help protect your data—whether it is
traveling over the internet, moving within Google's infrastructure, or stored on
our servers. Central to Google's security strategy are authentication,
integrity, and encryption, for both data at rest and data in transit. This paper
describes how we designed
Google Cloud to encrypt data in transit from the internet and data in
transit within Google's networks. This document doesn't apply to data in transit
over interconnects between customer data center networks and Google's data
center networks.

Encryption in transit uses various technologies to help protect data, including
transport layer security (TLS), BoringSSL, application layer transport security
(ALTS), and the [PSP security
protocol](https://cloud.google.com/blog/products/identity-security/announcing-psp-security-protocol-is-now-open-source).
In addition to the default protection that Google provides, you can further
protect data by adding encryption options such as IPsec, managed TLS
certificates, and Cloud Service Mesh.

This document is aimed at CISOs and security operations teams using or
considering Google Cloud. This document assumes a basic understanding of
[encryption](https://en.wikipedia.org/wiki/Encryption) and [cryptographic
primitives](https://en.wikipedia.org/wiki/Cryptographic_primitive).

## Authentication,integrity,and encryption

Google employs the following security measures to help ensure the authenticity,
integrity, and privacy of data in transit:

- **Authentication** verifies the identity of a peer (either a human or a
  process) in a connection.
- **Integrity** prevents data that you send from being altered while in transit
  between the source and the destination.
- **Encryption** uses cryptography to make your data unreadable while in transit
  and keep it confidential.

Encryption in transit helps protect your data if communications are intercepted
while data moves between the end user and Google Cloud or between two
services. Encryption in transit authenticates the endpoints and encrypts the
data before transmission. On arrival, the receiver decrypts the data and
verifies that it was not modified during transit.

Encryption is one component of a broader security strategy. Encryption in
transit defends your data against potential attackers and removes the need for
Google, Google Cloud customers, or end users to trust the lower layers of
the network.

### How traffic gets routed

This section describes how requests get from an end user to the appropriate
Google Cloud service or customer application, and how traffic is routed
between services.

A *Google Cloud service* is a modular cloud service that we offer to our
customers. These services include compute, data storage, data analytics, and
machine learning. For example, Cloud Storage is a Google Cloud service.

A *customer application* is an application hosted on Google Cloud that
you, as a Google customer, can build and deploy using Google Cloud
services. Customer applications or partner solutions that are hosted on
Google Cloud are not considered Google Cloud services. For example,
an application you build using Cloud Run, Google Kubernetes Engine, or a VM
in Compute Engine is a customer application.

The following diagram shows traffic paths from the end user to Google, paths
within Google's network, and the security for each connection. The following
 traffic paths are shown:

- End user on the internet to a Google Cloud service (labeled A in the
  diagram)
- End user on the internet to a customer application that is hosted on
  Google Cloud (labeled B in the diagram)
- Virtual machine to virtual machine (labeled C in the diagram)
- Virtual machine to Google Front End (GFE) (labeled D in the diagram)
- GFE to Google APIs and services (labeled E in the diagram)
- Google Cloud service to Google Cloud service (labeled F in the
  diagram)

![Traffic paths for Google.](https://cloud.google.com/static/docs/security/images/encryption-in-transit-overview.svg)

## Encryption in transit between the end user and Google

The following sections provide more detail about the end-user routing requests
that are shown in the preceding diagram.

### End user to a Google Cloud service

Google Cloud services such as Cloud Storage or
Compute Engine are cloud services that we offer to customers and run in
our [production
environment](https://cloud.google.com/docs/security/production-services-protection).
Google Cloud services accept requests from around the world using a
globally distributed system called [Google Front End
(GFE)](https://cloud.google.com/docs/security/infrastructure/design#google-frontend-service).
GFE terminates traffic for incoming HTTP(S), TCP, and TLS connections; provides
DDoS attack countermeasures; and routes and load balances traffic to the
Google Cloud services themselves. GFE points of presence exist around the
globe with paths that are advertised using unicast or
[Anycast](https://tools.ietf.org/html/rfc1546).

GFE routes traffic from an end user over Google's network to a
Google Cloud service, and from an end user to a customer application that
is hosted on Google Cloud and uses
[Cloud Load Balancing](https://cloud.google.com/load-balancing/docs/load-balancing-overview).

Requests that clients send to a Google Cloud service over HTTPS, HTTP/2,
or HTTP/3 are secured with TLS. TLS in the GFE is implemented with
[BoringSSL](https://boringssl.googlesource.com/boringssl), a Google-maintained,
open-source implementation of the TLS protocol. BoringCrypto, the core of
BoringSSL, is validated to [FIPS 140-3 level
1](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4735).

The GFE negotiates industry-standard cryptographic parameters with the client,
including forward-secure key negotiation. For older, less capable clients, the
GFE chooses the strongest legacy cryptographic primitives that the client
offers.

### End user to a customer application hosted on Google Cloud

You can route end user traffic from the internet to your customer applications
that are hosted on Google Cloud using a direct connection or through a
load balancer. When the traffic is routed directly, the traffic is routed to the
external IP address of the VM server that hosts the application.

You can use TLS with the external Application Load Balancer or the
external proxy Network Load Balancer to connect to
your application running on Google Cloud. When you use a Layer 7 load
balancer, the connection between the end user and the load balancer is encrypted
using TLS by default (provided that the end user's client application supports
TLS). GFE terminates the TLS connections from your end users using TLS
certificates that are self-managed or Google-managed. For more information about
customizing your certificate, see [SSL certificates
overview](https://cloud.google.com/compute/docs/load-balancing/http/ssl-certificates).
To enable encryption between the load balancer and the VM that hosts the
customer application, see [Encryption from the load balancer to the
backends](https://cloud.google.com/load-balancing/docs/ssl-certificates/encryption-to-the-backends).

To configure mutual TLS (mTLS), see [Mutual TLS
overview](https://cloud.google.com/load-balancing/docs/mtls). For workloads on
GKE and Compute Engine, consider
[Cloud Service Mesh](https://cloud.google.com/service-mesh/docs/security/security-overview)
so that you can use mTLS for mutual authentication (client and server) and
encrypt communications in transit using certificates that you manage.

For [Firebase
Hosting](https://firebase.google.com/docs/hosting/custom-domain) and
[Cloud Run custom
domains](https://cloud.google.com/run/docs/mapping-custom-domains), consider our
free and automated TLS certificates. With Cloud Run custom domains, you
can also [provide your own SSL
certificates](https://cloud.google.com/load-balancing/docs/https/setup-global-ext-https-serverless)
and use an HTTP strict transport security (HSTS) header.

## Encryption in transit within Google networks

Google Cloud encrypts customer data in transit within Google's
networks, unless described otherwise in this section.

Specialized ultra-high performance interconnects that connect TPUs or GPUs
within Google's AI supercomputers are separate from the networks described in
this document. In Google Cloud, these ultra-high performance interconnects
are ICI for TPUs and NVLink for GPUs. For more information, see [TPU
architecture](https://cloud.google.com/tpu/docs/system-architecture-tpu-vm) and
[GPU machine types](https://cloud.google.com/compute/docs/gpus).

Traffic over connections to VMs using external IP addresses leaves Google's
networks. You are responsible for configuring your own encryption for those
connections.

### Google Cloud virtual network authentication and encryption

Google Cloud's virtual network encrypts, integrity-protects, and
authenticates traffic between VMs.

Encryption of private IP traffic within the same VPC or across peered VPC
networks within Google Cloud's virtual network is performed at the network
layer.

Each pair of communicating hosts establishes a session key using a control
channel that is protected by
[ALTS](#service-to-service-authentication)
for authenticated, integrity-protected, and encrypted communications. The
session key is used to encrypt VM-to-VM communication between those hosts,
and session keys are rotated periodically.

VM-to-VM connections within VPC networks and peered VPC networks inside of
Google's production network are integrity-protected and encrypted. These
connections include connections between customer VMs and between customer and
Google-managed VMs such as Cloud SQL. The diagram in [How traffic gets
routed](#how-traffic) shows this interaction (labeled connection C). Note that
because Google activates automatic encryption based on the use of internal IP
addresses, connections between VMs using external IP addresses aren't
automatically encrypted.

Google Cloud's virtual network authenticates all
traffic between VMs. This authentication, achieved using security tokens,
prevents a compromised host from spoofing packets on the network.

Security tokens are encapsulated in a tunnel header which contains
authentication information about the sender and receiver. The control plane on
the sending host sets the token, and the receiving host validates the token.
Security tokens are pre-generated for every flow, and consist of a token
(containing the sender's information) and the host secret.

### Connectivity to Google APIs and services

Traffic handling differs depending on where the Google Cloud service is
hosted.

Most Google APIs and services are hosted on GFEs. VM to GFE
traffic uses external IP addresses to reach Google Cloud services, but you
can configure [private
access](https://cloud.google.com/vpc/docs/private-access-options) to avoid using
external IP addresses. The connection from the GFE to the service is
authenticated and encrypted.

Some services, such as [Cloud SQL](https://cloud.google.com/sql/docs/mysql/introduction), are
hosted on Google-managed VM instances. If customer VMs access the services
hosted on Google-managed VM instances using external IP addresses, traffic
remains in Google's production network but isn't automatically encrypted because
of the use of the external IP addresses. For more information, see
[Google Cloud virtual network authentication and
encryption](#gcp-virtual).

When a user sends a request to a Google Cloud service, we secure the data
in transit (providing authentication, integrity, and encryption) using HTTPS
with a certificate from a web (public) certificate authority. Any data the user
sends to the GFE is encrypted in transit with TLS or QUIC. GFE negotiates a
particular encryption protocol with the client depending on what the client can
support. GFE negotiates more modern encryption protocols when possible.

### Service-to-service authentication, integrity, and encryption

Google's infrastructure uses ALTS for the authentication, integrity, and
encryption of connections from the GFE to a Google Cloud service, and from
one Google Cloud service to another Google Cloud service.

ALTS uses [service-based
identities](https://cloud.google.com/docs/security/binary-authorization-for-borg#step_4_service-based_identity)
for authentication. Services running in Google's production environment are
issued credentials asserting their service-based identities. When making or
receiving RPCs from other services, a service uses its credentials to
authenticate. ALTS verifies that these credentials are issued by Google's
internal CA. Google's internal CA is unrelated and independent of the
[Certificate Authority Service](https://cloud.google.com/security/products/certificate-authority-service).

ALTS uses encryption and cryptographic integrity protection for traffic that
carries Google Cloud data from the GFE to a service and between services
that are running in Google's production environment.

ALTS is also used to encapsulate other Layer 7 protocols, such as HTTP, in RPC
mechanisms for traffic between GFEs and Google Cloud services. This protection
helps isolate the application layer and removes any dependency on the network
path's security.

## Encryption in transit methods

The following sections describe some of the technologies that Google uses to
encrypt data in transit.

### Network encryption using PSP

PSP is a transport-independent protocol that enables per-connection security and
supports offloading of encryption to smart network-interface card (SmartNIC)
hardware. Whenever SmartNICs are available, ALTS uses PSP to encrypt data in
transit across our network.

PSP is designed to meet the requirements of large-scale data-center traffic.
Google infrastructure uses PSP to encrypt traffic within and between our data
centers. PSP also supports non-TCP protocols such as UDP and uses a unique
encryption key for each connection.

### Application layer transport security

ALTS is a mutual authentication and encryption system developed by Google. ALTS
provides authentication, confidentiality, and integrity for data-in-transit
between services running in Google's production environment. ALTS consists of
the following protocols:

- **Handshake protocol:** The client initiates a combined elliptic curve and
  quantum-safe key exchange. At the end of the handshake, involved services
  authenticate each other's identities by exchanging and verifying signed
  certificates and compute a shared traffic key. Among the algorithms that are
  supported for deriving the shared traffic key is the NIST post-quantum
  algorithm [ML-KEM (FIPS 203)](https://csrc.nist.gov/pubs/fips/203/final). For
  more information, see [Post-quantum
  cryptography](https://cloud.google.com/security/resources/post-quantum-cryptography).
- **Record protocol:** Service-to-service data is encrypted in transit using
  the shared traffic key. By default, ALTS uses AES-128-GCM encryption for all
  traffic. Data in transit within Google's lowest-level storage system uses
  AES-256 encryption, and ALTS provides AES message authentication. Encryption
  in ALTS is provided by BoringSSL or PSP. This encryption is validated at
  FIPS 140-2 level 1 or FIPS 140-3 level 1.

The root signing keys for ALTS certificates are stored in Google's internal
CA.

## What's next

- For more information about our data center security, see [data center
  security](https://www.google.com/about/datacenters/data-security/).
- For information on security configuration options for interconnects between
  Google Cloud and customer data center networks, see [Choosing a Network Connectivity product
  (IPSec)](https://cloud.google.com/network-connectivity/docs/how-to/choose-product) and [MACsec for
  Cloud Interconnect
  overview](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/macsec-overview).
- For information on Google Cloud compliance and compliance
  certifications, see the [compliance resource
  center](https://cloud.google.com/compliance), which includes our [SOC
  3 audit report](https://www.google.com/work/soc3.html).
- For best practices on how to secure your data in transit, see the [Enterprise
  foundations
  blueprint](https://cloud.google.com/architecture/security-foundations/networking),
  [Google Cloud Architecture Framework: Security, privacy, and
  compliance](https://cloud.google.com/architecture/framework/security), and
  [Decide how to meet regulatory requirements for encryption in
  transit](https://cloud.google.com/architecture/landing-zones/decide-security#encrypt-transit).

   Was this helpful?
