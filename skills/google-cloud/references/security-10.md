# Data incident response processStay organized with collectionsSave and categorize content based on your preferences.

# Data incident response processStay organized with collectionsSave and categorize content based on your preferences.

# Data incident response processStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

Google's highest priority is to maintain a safe and secure environment for
customer data. To help protect customer data, we run an industry-leading
information security operation that combines stringent processes, an expert
incident response team, and multi-layered information security and privacy
infrastructure. This document explains our principled approach to managing and
responding to data incidents in Google Cloud.

The [Cloud Data Processing Addendum](https://cloud.google.com/terms/data-processing-addendum) defines a
data incident as “a breach of Google’s security leading to the accidental or
unlawful destruction, loss, alteration, unauthorized disclosure of, or access
to, Customer Data on systems managed by or otherwise controlled by Google.”
While we take steps to address foreseeable threats to data and systems, data
incidents don't include unsuccessful attempts or activities that don't
compromise the security of customer data. For example,
unsuccessful login attempts, pings, port scans, denial of service attacks, and
other network attacks on firewalls or networked systems don't qualify as
data incidents.

Incident response is a key aspect of our overall security and privacy program.
We have a rigorous process for managing data incidents. This process specifies
actions, escalations, mitigation, resolution, and notification of any incidents
that impact the confidentiality, integrity, or availability of customer data.

To learn more about how we secure Google Cloud, see the
[Infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design)
and [Google Cloud security](https://cloud.google.com/security).

## Data incident response

Our incident response program is managed by teams of expert incident responders
across many specialized functions to ensure each response is well-tailored to
the challenges presented by each incident. Depending on the nature of the
incident, the professional response team might include experts from the following
teams:

- Incident and escalation management
- Product engineering
- Site reliability engineering
- Cloud security and privacy
- Digital forensics
- Global investigations
- Detection and response
- Security, privacy, and product counsel
- Trust and safety
- Counter-abuse technology
- Cloud Customer Care

Experts from these teams are engaged in a variety of ways. For example, incident
commanders coordinate incident response and, when needed, the digital forensics
team performs forensic investigations and tracks ongoing attacks. Product
engineers work to limit the impact on customers and provide solutions to fix the
affected products. Counsel works with members of the appropriate security and
privacy team to implement Google’s strategy on evidence collection, engage with
law enforcement and government regulators, and advise on legal issues and
requirements. Customer Care responds to customer inquiries and requests
for additional information and assistance.

## Team organization

When we declare an incident, we designate an incident commander who coordinates
incident response and resolution. The incident commander selects specialists
from different teams and forms a response team. The incident commander delegates
the responsibility for managing different aspects of the incident to these
experts and manages the incident from the moment of declaration to closure. The
following diagram depicts an example organization of various roles and their
responsibilities during incident response. Depending on the type of incident,
different roles might be assigned.

![Data incident response team organization](https://cloud.google.com/static/docs/security/incident-response/resources/data-incident-response-org.svg)

## Data incident response process

Every data incident is unique, and the goal of the data incident response
process is to protect customer data, restore normal service as quickly as
possible, and meet both regulatory and contractual compliance requirements. The
following table describes the main steps in the Google incident response
program.

| Incident step | Goal | Description |
| --- | --- | --- |
| Identification | Detection | Automated and manual processes detect potential vulnerabilities and
incidents. |
| Reporting | Automated and manual processes report the issue to the incident
response team. |  |
| Coordination | Triage | The following activities occur:On-call responder evaluates the nature of the incident report.On-call responder assesses severity of the incident.On-call responder assigns incident commander. |
| Response team engagement | The following activities occur:Incident commander completes assessment of known facts.Incident commander designates leads from relevant teams and forms
incident response team.Incident response team evaluates incident and response effort. |  |
| Resolution | Investigation | The following activities occur:Incident response team gathers key facts about the incident.Additional resources are integrated as needed to allow for
expedient resolution. |
| Containment and recovery | Operations lead takes immediate steps to complete the following:Limit ongoing damage.Fix underlying issue.Restore affected systems and services to normal operations. |  |
| Communication | The following activities occur:Key facts are evaluated to determine whether notification is
appropriate.Communications lead develops a communication plan with
appropriate leads. |  |
| Closure | Lessons learned | The following activities occur:Incident response team retrospects on incident and response
effort.Incident command designates owners for long-term improvements. |
| Continuous improvement | Program development | Necessary teams, training, processes, resources, and tools are
maintained. |
| Prevention | Teams improve the incident response program based on lessons
learned. |  |

The following sections describe each step in more detail.

### Identification

Early and accurate identification of incidents is key to effective incident
management. The focus of the identification phase is to monitor security events
to detect and report on potential data incidents.

The incident detection team employs advanced detection tools, signals, and alert
mechanisms that provide early indication of potential incidents. Our sources of
incident detection include the following:

- **Automated network and system logs analysis:** Automated analysis of network
  traffic and system access helps identify suspicious, abusive, or
  unauthorized activity and escalates to security staff.
- **Testing:** The security team actively scans for security threats using
  penetration tests, quality assurance (QA) measures, intrusion detection, and
  software security reviews.
- **Internal code reviews:** Source code review discovers hidden vulnerabilities,
  design flaws, and verifies if key security controls are implemented.
- **Product-specific tooling and processes:** Automated tooling specific to the
  team function is employed wherever possible to enhance our ability to detect
  incidents at product level.
- **Usage anomaly detection:** We use layers of machine learning systems to
  differentiate between safe and anomalous user activity across browsers,
  devices, application logins, and other usage events.
- **Data center and workplace services security alerts:** Security alerts in data
  centers scan for incidents that might affect our infrastructure.
- **Google employees:** A Google employee detects an anomaly and reports it.
- **Google’s vulnerability reward program:**
  Potential technical vulnerabilities in Google-owned browser extensions,
  mobile, and web applications that affect the confidentiality or integrity of
  user data are sometimes reported by external security researchers.

### Coordination

When an incident is reported, the on-call responder reviews and evaluates the
nature of the incident report to determine if it represents a potential data
incident and initiates our incident response process.

After confirmation, the responder assesses the nature of the incident and
implements a coordinated approach to the response. At this stage, the response
includes completing the triage assessment of the incident, adjusting its
severity if required, and activating the required incident response team with
appropriate operational and technical leads who review the facts and identify
key areas that require investigation. We designate a product lead and a legal
lead to make key decisions on how to respond. The responder then assigns the
responsibility for investigation and the facts are assembled. If necessary, an
incident is declared and an incident commander is assigned.

Many aspects of our response depend on the assessment of severity, which is
based on key facts that are gathered and analyzed by the incident response team.
These key facts include the following:

- Potential for harm to customers, third parties, and Google
- Nature of the incident (for example, whether data was potentially destroyed,
  accessed, or altered)
- Type of data that might be affected
- Impact of the incident on our customers’ ability to use the service
- Status of the incident (for example, whether the incident is isolated,
  continuing, or contained)

The incident commander and other leads periodically re-evaluate these factors
throughout the response effort as new information evolves to ensure that our
response is assigned the appropriate resources and urgency. Events that present
the most critical impact are assigned the highest severity. A communications
lead is appointed to develop a communications plan with other leads.

### Resolution

At the resolution stage, the focus is on investigating the root cause, limiting the impact
of the incident, resolving immediate security risks (if any), implementing
necessary fixes as part of remediation, and recovering affected systems, data,
and services.

Affected data is restored to its original state wherever possible. Depending on
what is reasonable and necessary in a particular incident, we might take a
number of different steps to resolve an incident. For instance, there might be a
need for technical or forensic investigation to reconstruct the root cause of an
issue or to identify any impact on customer data. We might attempt to recover
copies of the data from our backup copies if data is improperly altered or
destroyed.

A key aspect of remediation is notifying customers when incidents impact their
data. Key facts are evaluated throughout the incident to determine whether the
incident affected customer data. If notifying customers is appropriate, the
incident commander initiates the notification process. The communications lead
develops a communication plan with input from the product and legal leads,
informs those affected, and supports customer requests after notification with
the help of Customer Care.

We strive to provide prompt, clear, and accurate notifications containing the
known details of the data incident, steps that we have taken to mitigate the
potential risks, and actions that we recommend customers take to address the
incident. We do our best to provide a clear picture of the incident so that
customers can assess and fulfill their own notification obligations.

### Closure

Following the successful remediation and resolution of a data incident, the
incident response team evaluates the lessons learned from the incident. When the
incident raises critical issues, the incident commander might initiate a
post-mortem analysis. During this process, the incident response team reviews
the causes of the incident and our response and identifies key areas for
improvement. In some cases, this might require discussions with different
product, engineering, and operations teams and product enhancement work. If
follow-up work is required, the incident response team develops an action plan
to complete that work and assigns project managers to lead the long-term
effort. The incident is closed after the remediation efforts conclude.

### Continuous improvement

At Google, we strive to learn from every incident and implement
preventative measures to avoid future incidents.

Actionable insights from incident analysis enable us to enhance our tools,
training, processes, overall security and privacy data protection program,
security policies, and response efforts. The key learnings also facilitate
prioritization of engineering efforts and building of better products.

Security and privacy professionals enhance our program by reviewing our security
plans for all networks, systems, and services, and by providing project-specific
consulting services to product and engineering teams. Security and privacy
professionals deploy machine learning, data analysis, and other novel techniques
to monitor for suspicious activity on our networks, address information security
threats, perform routine security evaluations and audits, and engage outside
experts to conduct regular security assessments. Additionally,
[Project Zero](https://googleprojectzero.blogspot.com/p/about-project-zero.html),
aims to prevent targeted attacks by reporting bugs to software vendors and
filing them in an external database.

We conduct regular training and awareness campaigns to drive innovation in
security and data privacy. Dedicated incident response staff are trained in
forensics and in handling evidence, including the use of third-party and
proprietary tools. Testing of incident response processes and procedures is
performed for key areas, such as systems that store sensitive customer
information. These tests take into consideration a variety of scenarios,
including insider threats and software vulnerabilities and help us better
prepare for security and privacy incidents.

Our processes are tested on a regular basis as part of our ISO-27017, ISO-27018,
ISO-27001, PCI-DSS, SOC 2 and FedRAMP programs to provide our customers and
regulators with independent verification of our security, privacy, and
compliance controls. For a list of third-party certifications for Google Cloud,
see the [Compliance resource center](https://cloud.google.com/security/compliance).

## Summary

Protecting data is core to our business. We continually invest in our overall
security program, resources, and expertise, which enables our customers to rely
on us to respond effectively in the event of an incident, protect customer data,
and maintain the high reliability customers expect of a Google service.

Our world-class incident response program delivers these key functions:

- A process built upon industry-leading techniques for resolving incidents and
  refined to operate efficiently at Google’s scale.
- Pioneering monitoring systems, data analytics, and machine learning services
  to proactively detect and contain incidents.
- Dedicated subject matter experts who can respond to any type
  or size of data incident.
- A mature process for promptly notifying affected customers, aligned with
  Google’s commitments in our terms of service and customer agreements.

## What’s next

- To learn more about incident management, read Chapter 17 of
  [Building secure and reliable systems (O'Reilly book)](https://www.oreilly.com/library/view/building-secure-and/9781492083115/).
- To learn more about how to implement security for customer workloads in
  Google Cloud, see the
  [enterprise foundations blueprint](https://cloud.google.com/architecture/security-foundations) and the
  [Google Cloud Well-Architected Framework](https://cloud.google.com/architecture/framework/security).

   Was this helpful?
