# Google Cloud's approach to changeStay organized with collectionsSave and categorize content based on your preferences. and more

# Google Cloud's approach to changeStay organized with collectionsSave and categorize content based on your preferences.

> Learn how Google Cloud safely and quickly introduces code changes into its products by following a rigorous change management process.

# Google Cloud's approach to changeStay organized with collectionsSave and categorize content based on your preferences.

Billions of users each year interact with Google's products and services. Key
offerings like Search, Gmail, Maps, YouTube, Chrome, and now also
Google Cloud, are so seamlessly integrated into modern life that they help
define the 21st-century experience. This planet-wide impact is the result of the
proven quality of our offerings and the expectation that Google is always
available.

At Google Cloud, we continuously introduce code changes to our products
and services to ensure that we're delivering the best user experience possible,
improving safety and reliability, and adhering to regulatory and compliance
requirements. Any such change, however big or small, can sometimes break things.
To address that risk, we prioritize change safety throughout the entire
lifecycle of a change.

This document explains how Google Cloud teams build on Google's decades of
investment in development excellence to implement reliability best practices and
engineering standards that meet Google Cloud customer expectations for
development velocity and reliability.

## The life of a change at Google Cloud

Google Cloud product teams share much of the management process and
tooling with other engineering teams across Google. We implement a standard
software development approach for change management that prioritizes continuous
integration (CI) and continuous delivery (CD). CI includes frequently proposing,
testing, and submitting changes, often multiple times a day for any given
product or service. CD is an extension of CI in which engineers continuously
prepare release candidates based on the latest stable snapshot of a codebase.

This approach prioritizes creating and rolling out changes in stages to
Google Cloud customers as soon as possible but also as safely as possible.
We consider change safety before we write any code, and we continue to focus on
safety even after we roll out changes in production. There are four general
phases in our change management model: design, development, qualification, and
rollout. These four phases are shown in the following diagram and are discussed
in more detail throughout this document:

![Diagram showing the steps for the design, development, qualification, and rollout phases.](https://cloud.google.com/static/docs/images/cloud-approach-to-change/change-management-lifecycle.svg)

## Safe by design

We recognize that even small mistakes early in the development process can cause
big problems later on that significantly impact customer experiences. As a
result, we require all major changes to start with an approved design document.
We have a common design document template for engineering teams to propose major
changes. This common design document helps us evaluate major changes across
Google Cloud products consistently. The following diagram shows what our
standard design process for a major change looks like:

![Detailed diagram of the steps involved in the design phase.](https://cloud.google.com/static/docs/images/cloud-approach-to-change/design-phase.svg)

The design phase begins when a software developer proposes a change that
addresses business, technical, cost, and maintenance requirements. After
submitting that change, a comprehensive review and approval process kicks off
with senior experts, including reliability and security experts, and technical
leads. Work to implement the change can proceed only after the engineer who
proposed the design addresses all the feedback from experts and each expert
approves the design. This design and review process reduces the probability that
Google Cloud product teams even start working on changes that could
negatively impact customers in production.

## Safe as developed

Our code development process increases the quality and reliability of our code.
After approval of a proposed change, the development process begins with a
comprehensive onboarding for new engineers, including training, mentorship, and
detailed feedback on proposed code changes. A multi-layered development and
testing approach with manual and automated testing continuously validates code
at every stage of development. Each code change is thoroughly reviewed to
ensure that it meets Google's high standards.

The following diagram provides a workflow that illustrates approximately what
our development process looks like:

![Detailed diagram of the steps involved in the development phase.](https://cloud.google.com/static/docs/images/cloud-approach-to-change/development-phase.svg)

The development phase begins when an engineer starts writing code and
corresponding unit and integration tests. Throughout this phase, the engineer
can run tests they wrote and a suite of presubmit tests to ensure that code
additions and changes are valid. After wrapping up code changes and running
tests, the engineer requests a manual review from someone else who's familiar
with the code. This human review process is often iterative and can result in
additional code revisions. When the author and reviewer come to a consensus,
the author submits the code.

### Coding standards ensure high-quality changes

Google's engineering culture, practices, and tools are designed to ensure that
our code is correct, clear, concise, and efficient. Code development at Google
takes place in our
[monorepo](https://research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/),
the world's largest integrated code repository. The monorepo houses millions of
source files, billions of lines of code, and has a history of hundreds of
millions of commits called changelists. It continues to grow rapidly, with tens
of thousands of new changelists added every workday. Key benefits of the
monorepo are that it facilitates code reuse, makes dependency management easier,
and enforces consistent developer workflows across products and services.

Code reuse is helpful because we already have a good idea about how reused code
performs in production. By leveraging high-quality code that already exists,
changes are inherently more robust and easier to maintain at the required
standard. This practice not only saves time and effort, but also ensures that
the overall health of the codebase remains high, leading to more reliable
products.

Google Cloud services that build on high-quality open source software may
supplement the monorepo with another repository — usually Git — to
use branching to manage the open source software.

#### A note on training

Investment in code quality starts when an engineer joins a team. If the engineer
is new to Google, or is less familiar with the team's infrastructure and
architecture, they go through extensive onboarding. As a part of this
onboarding, they study style guides, best practices and development guides, and
manually perform practical exercises. Additionally, new engineers require an
extra level of approval for each individual changelist submission. Approval for
changes in a given programming language is granted by engineers who have passed
a rigorous set of expectations based on their expertise and have earned
readability in that programming language. Any engineer can earn readability for
a programming language — most teams have multiple approvers for the
programming languages they code in.

### Shift left improves velocity safely

Shift left is a principle that moves testing and validation earlier in the
development process. This principle is based on our observation that costs
dramatically increase the later in the release process that we find and fix a
bug. In an extreme case, consider a bug that a customer finds in production.
This bug could negatively affect the customer's workloads and applications, and
the customer might also need to go through the Cloud Customer Care process before
the relevant engineering team can mitigate the bug. If an engineer assigned to
address the issue is a different person than who originally introduced the
change that contained the bug, the new engineer will need to become familiar
with the code changes, likely increasing the time needed to reproduce and
eventually fix the bug. This whole process requires a great deal of time from
customers and Google Cloud's support, and demands that engineers drop what
they're working on to fix something.

Conversely, consider a bug that an automated test failure catches while an
engineer is working on a change that's in development. When the engineer sees
the test failure, they can immediately fix it. Because of our coding standards,
the engineer wouldn't even be able to submit the change with the test failure.
This early detection means that the engineer can fix the bug with no customer
impact, and that there's no context switching overhead.

The latter scenario is infinitely preferable for everyone involved. As a result,
over the years, Google Cloud has invested heavily into this shift left
principle, moving tests traditionally performed during change qualification and
rollout phases directly into the development loop. Today, all unit tests, all
but the largest integration tests, and extensive static and dynamic analyses are
completed in parallel while an engineer is proposing code changes.

### Automated presubmit tests enforce coding standards

Presubmit tests are checks that run before any changes are submitted in a given
directory. Presubmit tests can be unit and integration tests specific to a
change or general tests (for example, static and dynamic analysis) that run for
any change. Historically, presubmit tests ran as the very last step before
someone submits a change to a codebase. Today, partly because of the shift left
principle and our implementation of CI, we run presubmit tests in a continuous
fashion while an engineer makes code changes in a development environment and
before merging changes into our monorepo. An engineer can also manually run a
presubmit test suite with a single click in the development UI, and every
presubmit test automatically runs for each changelist prior to a human code
review.

The presubmit test suite generally covers unit tests, fuzz tests (fuzzing),
hermetic integration tests, as well as static and dynamic code analysis. For
changes to core libraries or code used widely across Google, developers run a
global presubmit. A global presubmit tests the change against the entire Google
codebase, minimizing the risk that a proposed change negatively impacts other
projects or systems.

#### Unit and integration tests

Thorough testing is integral to the code development process. Everyone
is required to write unit tests for code changes and we continually track code
coverage at a project level to ensure we are validating expected behavior.
Additionally, we require that any critical user journey has integration tests
in which we validate the functionality of all necessary components and
dependencies.

Unit tests and all but the largest integration tests are designed to complete
promptly, and are executed incrementally with high parallelism in a distributed
environment, resulting in rapid and continuous automated development feedback.

#### Fuzzing

Whereas unit and integration tests help us validate expected behavior with
predetermined inputs and outputs, fuzzing is a technique that bombards an
application with random inputs, aiming to expose hidden flaws or weaknesses
that could lead to security vulnerabilities or crashes. Fuzzing allows us to
proactively identify and address potential weaknesses in our software, enhancing
the overall security and reliability of our products before customers interact
with changes. The randomness of this testing is particularly useful because users
sometimes interact with our products in interesting ways that we don't expect,
and fuzzing helps us account for scenarios that we didn't manually consider.

#### Static analysis

Static analysis tools play a critical role in maintaining code quality in our
development workflows. Static analysis has evolved significantly from its early
days of linting with regular expressions to identify problematic C++ code
patterns. Today, static analysis covers all Google Cloud production
languages, and finds erroneous, inefficient, or deprecated code patterns.

With advanced compiler frontends and LLMs, we can automatically propose
improvements while engineers are writing code. Each proposed code change is
vetted with static analyses. As we add new static checks over time, the entire
codebase is constantly scanned for compliance, and fixes are automatically
generated and sent for review.

#### Dynamic analysis

While static analysis focuses on identifying known code patterns that can lead
to problems, dynamic analysis takes a different approach. It involves compiling
and running code to uncover issues that only surface during execution like
memory violations and race conditions. Google has a rich history of utilizing
dynamic analysis, and has even
[shared several of its tools](https://github.com/google/sanitizers)
with the broader developer community, including the following:

- [AddressSanitizer](https://github.com/google/sanitizers/tree/master/hwaddress-sanitizer):
  Detects memory errors like buffer overflows and use-after-free
- ThreadSanitizer ([C++](https://github.com/google/sanitizers/wiki/ThreadSanitizerCppManual),
  [Go](https://github.com/google/sanitizers/wiki/ThreadSanitizerGoManual)):
  Finds data races and other threading bugs
- [MemorySanitizer](https://github.com/google/sanitizers/wiki/MemorySanitizer):
  Uncovers uninitialized memory usage

These tools and others like them are essential for catching complex bugs that
can't be detected through static analysis alone. By using both static and
dynamic analysis, Google strives to ensure that its code is well-structured,
free of known problems, and behaves as expected in real-world scenarios.

### Human code reviews validate changes and test results

When an engineer reaches a critical milestone in their code and wants to
integrate it into the main repository, they initiate a code review by proposing
a changelist. A code review request consists of the following:

- A description that captures the purpose of the changes and any additional
  context
- The actual modified code
- Unit and any integration tests for the modified code
- Automated presubmit test results

It's at this point in the development process that another human steps in. One
or more designated reviewers carefully examine the changelist for correctness
and clarity, using the attached tests and presubmit results as a guide. Each
code directory has a set of designated reviewers responsible for ensuring the
quality of that subset of the codebase, and whose approval is necessary to make
changes within that directory. Reviewers and engineers collaborate to spot and
address any problems that might arise with a proposed code change. When the
changelist meets our standards, a reviewer gives their approval ("LGTM," short
for "looks good to me"). However, if the engineer is still in training for the
programming language used, they need additional approval from an expert who has
earned readability in the programming language.

After a changelist passes tests and automated checks and receives an LGTM, the
engineer who proposed the change is allowed to make only minimal changes to the
code. Any substantial alterations invalidate the approval and require another
round of review. Even small changes are automatically flagged to the original
reviewers. Once the engineer submits the finalized code, it goes through another
full round of presubmit testing before the changelist is merged into the
monorepo. If any tests fail, the submission is rejected, and the developer and
reviewers receive an alert to take corrective action before trying to submit the
changes again.

## Safe release qualification

While presubmit testing is comprehensive, it's not the end of the testing
process at Google. Teams often have additional tests, such as large-scale
integration tests, that aren't feasible to run during the initial code review
(they may take a longer time to run or require high-fidelity testing
environments). Furthermore, teams need to be aware of any failures caused by
factors outside their control, like changes in external dependencies.

That's why Google requires a qualification phase after the development phase.
This qualification phase uses a continuous build and test process, as shown in
the following diagram:

![Detailed diagram of the steps involved in the qualification phase.](https://cloud.google.com/static/docs/images/cloud-approach-to-change/qualification-phase.svg)

This process periodically runs tests for all code affected by direct or indirect
changes since the last run. Any failures are automatically escalated to the
responsible engineering team. In many cases, the system is able to automatically
identify the changelist that caused the breakage, and roll it back. These
large-scale integration tests are executed in a spectrum of staging environments
that go from partially simulated environments to entire physical locations.

Tests have a variety of qualification goals that range from basic reliability
and safety to business logic. These qualification tests include testing the code
for the following:

- The ability to deliver the requisite functionality, which is tested by using
  large-scale integration tests
- The ability to satisfy business requirements, which is tested with synthetic
  representations of customer workloads
- The ability to sustain failures of the underlying infrastructure, which is
  tested by using the injection of failures across the stack
- The ability to sustain serving capacity, which is tested with load testing
  frameworks
- The ability to roll back safely

## Safe rollouts

Even with the strongest development, testing, and qualification processes,
defects sometimes sneak into production environments that negatively impact our
users. In this section, we explain how the Google Cloud rollout process
limits the impact of defective changes and ensures the rapid detection of any
regressions. We apply this approach to all types of changes deployed to
production, including binaries, configurations, schema updates, capacity
changes, and access control lists.

### Change propagation and supervision

We apply a consistent approach to deploying changes across Google Cloud to
minimize negative customer impacts, and isolate issues to individual logical and
physical failure domains. The process builds on our decades-long
[SRE reliability practices](https://sre.google/sre-book/table-of-contents/)
and on our
[planet-scale monitoring system](https://research.google/pubs/monarch-googles-planet-scale-in-memory-time-series-database/)
to detect and mitigate bad changes as quickly as possible. Rapid detection lets
us notify customers faster and take corrective actions to systematically prevent
similar failures from happening again.

Most Google Cloud products are regional or zonal. This means that a
regional product running in Region A is independent of the same product running
in Region B. Similarly, a zonal product running in Zone C within Region A is
independent of the same zonal product running in Zone D within Region A. This
architecture minimizes the risk of an outage that affects other regions or other
zones within a single region. Some services, like IAM or
Google Cloud console, provide a globally consistent layer spanning all
regions, which is why we call them global services. Global services are
replicated across regions, to avoid any single points of failure and to minimize
latency. The shared Google Cloud rollout platform is aware of whether a
service is zonal, regional, or global, and orchestrates production changes
appropriately.

The Google Cloud rollout process splits all replicas of a service deployed
across multiple target locations into waves. Initial waves include a small
number of replicas, with updates proceeding serially. The initial waves balance
shielding most customer workloads with maximizing the exposure to workload
diversity to detect issues as early as possible, and include synthetic workloads
that mimic common customer workload patterns.

If the rollout remains successful as service replicas are updated in target
locations, subsequent rollout waves increase progressively in size and
introduce more parallelism. Even though some parallelism is necessary to account
for the number of Google Cloud locations, we disallow simultaneous updates
to locations that are in different waves. If a wave extends into the night or a
weekend, it can complete its progression, but no new wave can start until the
beginning of business hours for the team managing the rollout.

The following diagram is an example workflow that illustrates the rollout
logic we use across Google Cloud for regional products and services:

![Detailed diagram of the steps involved in the rollout phase.](https://cloud.google.com/static/docs/images/cloud-approach-to-change/rollout-phase.svg)

The Google Cloud rollout process uses the
[Canary Analysis Service (CAS)](https://research.google/pubs/canary-analysis-service/)
to automate A/B testing throughout the duration of a rollout. Some replicas
become canaries (that is, a partial and time-limited deployment of a change in a
service), and the remaining replicas make up the control group that don't
include the change. Each step of the rollout process has a bake time to catch
slow-burning issues before progressing to the next step to ensure that all the
functionalities of a service are well exercised and that potential anomalies are
detected by CAS. The bake time is carefully defined to balance the detection of
slow-burning issues with development velocity. Google Cloud rollouts
typically take one week.

This diagram provides a quick overview of what the CAS workflow looks like:

![Diagram of the steps followed in the CAS workflow.](https://cloud.google.com/static/docs/images/cloud-approach-to-change/cas-workflow.svg)

The workflow starts with the rollout tool deploying the change to the canary
replica. The rollout tool then requests a verdict from CAS. CAS evaluates the
canary replica against the control group and returns a verdict of PASS or FAIL.
If any health signal fails, an alert is generated for the service owners and the
running step of the rollout is paused or rolled back. If the change causes
disruption to external customers, an external incident is declared and affected
customers are notified using the
[Personalized Service Health](https://cloud.google.com/service-health)
service. Incidents also trigger an internal review.
[Google's Postmortem Philosophy](https://sre.google/sre-book/postmortem-culture/)
ensures that the right set of corrective actions is identified and applied to
minimize the likelihood that similar failures happen again.

### Monitoring signals and post-rollout safety

Software defects don't always manifest instantly, and some may require specific
circumstances to trigger. Because of this, we continue to monitor production
systems after a rollout is complete. Over the years, we've noticed that even if
a rollout doesn't trigger any issues right away, a bad rollout is still the most
likely culprit of a production incident. Because of this, our production
playbooks instruct incident responders to correlate recent rollouts with the
observed issues, and to default to rolling back a recent rollout if incident
responders can't rule out recent changes as a root cause of the incident.

Post-rollout monitoring builds on the same set of monitoring signals that we use
for automated A/B analyses during a rollout window. The Google Cloud
monitoring and alerting philosophy combines two types of monitoring:
*introspective* (also known as white-box) and *synthetic* (also known as
black-box). Introspective monitoring uses metrics like CPU utilization, memory
utilization, and other internal service data. Synthetic monitoring looks at
system behavior from a customer's perspective, tracking service error rates and
responses to synthetic traffic from prober services. Synthetic monitoring is
symptoms-oriented and identifies active problems, whereas introspective
monitoring enables us to diagnose confirmed problems, and in some cases identify
imminent issues.

To assist with detection of incidents that affect only some customers, we
cluster customer workloads into cohorts of related workloads. Alerts trigger as
soon as the performance of a cohort deviates from the norm. These alerts allow
us to detect customer-specific regressions even if aggregate performance appears
to be normal.

### Software supply chain protection

Whenever Google Cloud teams introduce changes, we use a security check
called [Binary Authorization for Borg (BAB)](https://cloud.google.com/docs/security/binary-authorization-for-borg)
to protect our software supply chain and Cloud customers against insider risk.
BAB starts at the code review stage and creates an audit trail of code and
configuration deployed to production. To ensure the integrity of production, BAB
only admits changes that meet the following criteria:

- Are tamper-proof and signed
- Come from an identified build party and an identified source location
- Have been reviewed and explicitly approved by a party distinct from the code
  author

If you're interested in applying some of the same concepts in your own software
development lifecycle, we included key concepts of BAB in an open specification
called [Supply-chain Levels for Software Artifacts (SLSA)](https://slsa.dev/).
The SLSA acts as a security framework for developing and running code in
production environments.

## Conclusion

Google Cloud builds on the decades of Google's investment in development
excellence. Code health and production health are cultural tenets instilled in
all engineering teams at Google. Our design review process ensures that
implications on code and production health are considered early on. Our
development process, based on the shift left principle and extensive testing,
ensures that design ideas are implemented safely and correctly. Our
qualification process further expands testing to cover large-scale integrations
and external dependencies. Finally, our rollout platform enables us to
progressively build confidence that a given change actually behaves as expected.
Spanning conception to production, our approach allows us to meet
Google Cloud customer expectations for both development velocity and
reliability.

## Contributors

Authors:

- [Krzysztof Duleba](https://www.linkedin.com/in/kduleba) | Principal Engineer
- [Luca Bigliardi](https://www.linkedin.com/in/shammash/) | Staff Site Reliability Engineer
- [Sridivya Bonam](https://www.linkedin.com/in/sridivya/) | Group Product Manager
- [Brian Ashby](https://www.linkedin.com/in/bpashby/) | Senior Technical Writer

Other contributors:

- [Andrew Fikes](https://www.linkedin.com/in/andrew-fikes) | Engineering Fellow, Reliability
- [Dermot Duffy](https://www.linkedin.com/in/dermot-duffy-12041216/) | Senior Software Engineering Director
- [Sunder Parameswaran](https://www.linkedin.com/in/sunderparam/) | Senior Director, Product Management
- [Raj Bose](https://www.linkedin.com/in/rbose/) | Director, Site Reliability Engineering
- [Alain Azagury](https://www.linkedin.com/in/alain-azagury/) | Senior Staff Software Engineer
- [Emil Tiller](https://www.linkedin.com/in/emil-tiller-baa4452/) | Senior Staff Software Engineer
- [Kumar Dhanagopal](https://www.linkedin.com/in/kumardhanagopal) | Cross-Product Solution Developer

---

# Compute

> Documentation and resources for running your workloads on virtual machines for ML, high-performance computing, and more.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Learn about the six deployment archetypes, including the use cases and design considerations for each deployment archetype.
                        Recommendations to help you plan and provision resources to match the requirements and consumption patterns of your cloud workloads.
                        Recommendations to optimize the performance of workloads in Google Cloud.
                        Study cloud computing, ways to use Google Cloud, and different compute options.
                        Learn about the wide range of options for hosting applications on Google Cloud.

Create a VM.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/products/compute-engine-color.svg)
                                      Configure and deploy scalable, high-performance virtual machine (VM) instances and instance groups.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Get visibility into your project's use of virtual machine (VM) instance resources.

                                      Compute Engine resources are hosted in multiple locations worldwide. These locations are composed of regions and zones.

OS images for virtual machines.

                                      Use operating system (OS) images to create boot disks for your virtual machine (VM) instances.

                                      Learn general operating system (OS) details and feature support for the OS images that are available on Compute Engine.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Bring up your Docker containers on Google Cloud quickly, efficiently, and securely.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Deploy VM images that are optimized for data science and ML tasks.

Expand this section to see relevant products and documentation.

                                      Provide always-encrypted solid-state storage for Compute Engine VMs.

                                      Use durable network storage devices that your virtual machine (VM) instances can access like physical disks in a desktop or a server.

                                      Use scalable, high-performance storage service with a comprehensive suite of data persistence and management capabilities.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Unified platform that helps you accelerate your end-to-end cloud journey from your current on-premises or cloud environments to Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Migrate servers and VMs from on-premises or another cloud to Compute Engine.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Migrate VMs from on-premises or other clouds directly into containers in GKE.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Assess your mainframe workloads and generate codebase documentation with generative AI.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Move your mainframe data to Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Simultaneously run workloads on your mainframe and on Google Cloud, and compare their outputs.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/products/ai-hypercomputer-color.svg)
                                      A supercomputer architecture that employs systems-level codesign to boost efficiency and productivity across AI training, tuning, and serving.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Schedule, queue, and execute batch jobs at scale with a fully managed batch service on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Add GPUs to your workloads for machine learning, scientific computing, and 3D visualization.

                                      Learn the machine families, machine series, and machine types that you can choose from to create a virtual machine (VM) instance.
                                               ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Migrate and run your VMware workloads natively on Google Cloud.

                                      Leverage your SAP data in innovative ways, all while running your SAP applications more reliably, securely, and cost-effectively.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      End-to-end solutions to manage your SAP and Microsoft SQL Server workloads running on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Deploy high performance computing (HPC) environments on Google Cloud.

                                      Learn how to manage the network your VMs belong to.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Set up permissions uses IAM roles to control access to your VMs.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/storage-color.svg)
                                      Store objects with global edge caching.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      VMs on Google Cloud hardened by a set of security controls that help defend against rootkits and bootkits.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/secops-color.svg)
                                      A type of virtual machine that enables enhanced performance and security for high-memory workloads using AMD Secure Encrypted Virtualization (SEV).

---

# Costs and usage management

> Documentation and resources for managing costs and usage across Google Cloud products and services.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Plan with best practices to optimize the cost of workloads.
                        Learn about cost management tools that help you track and understand your Google Cloud spending, pay your bill, and optimize your costs.

                        Get at-a-glance and user-configurable views of your cost history, current cost trends, and forecasted costs with intuitive reports.

                        Get best practices for monitoring, controlling, and optimizing your costs with Google Cloud's cost management tools.
                        Study Google Cloud billing and cost management essentials for those in a Finance and/or IT related role.
                        Study optimization of your cluster's infrastructure to help save costs and create a more efficient architecture for your applications.
                        Study why Google Cloud is the cleanest cloud in the industry by exploring and utilizing sustainability tools.

Track your Google Cloud costs, analyze your billing data, control and optimize your costs, and take advantage of committed use discounts.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Learn about cost management tools that help you track and understand your Google Cloud spending, pay your bill, and optimize your costs.

                                      Committed use discounts (CUDs) provide discounted prices in exchange for your commitment to use a minimum level of resources for a specified term.

                                      This article describes the components of the Google Cloud Free Program.

                                      Monitor and communicate your current savings, explore new recommended opportunities to optimize costs, and plan your optimization goals.

                                      Get answers to questions 'Which Google Cloud services cost the most last month?'

                                      Use the CUD reports to analyze the effectiveness of your discounts.

                                      Use budgets to track your actual Google Cloud costs against your planned costs and receive spending alerts.

                                      Use programmatic budget notifications to automate your cost control response based on the budget notification.

Optimize your Google Cloud resource usage and increase efficiency.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Monitor quota usage, create and modify quota alerts, and request quota adjustments for all of your Google Cloud services.

                                      View and manage the quota restrictions that are applicable to the Google Cloud resources that you use.

                                      Plan using best practices for running cost-optimized applications on GKE to take advantage of the elasticity provided by Google Cloud.

Measure, report, and reduce your Cloud carbon emissions.

                                      Display gross greenhouse gas emissions from electricity associated with the usage of covered Google Cloud services.

                                      Review the calculation methodology that Google Cloud uses to give our customers a report tailored to their specific gross carbon footprint.

                                      Learn how to export your Carbon Footprint data to BigQuery or Sheets in order to perform data analysis and create custom dashboards and reports.
                                                Was this helpful?

---

# Access and resource management

> Documentation and resources for organizing, analyzing, and managing access to your Google Cloud resources and services.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Explore the methods you can use to configure identities for users and workloads on Google Cloud

                        Learn about Google Cloud's Identity and Access Management system, which lets you control who can access your Google Cloud resources.

                        Learn about the resource hierarchy in Google Cloud and how you can use that hierarchy to organize your resources.

                        Configure an initial foundation to support your Google Cloud workloads, including setting up your resource hierarchy and granting initial access.

                        Plan your general practice of IAM.
                        Plan how to develop your approach for identity governance and access management for applications and workloads running on Google Cloud.
                        Study planning, configuring, setting up, and deploying cloud solutions.
                        Study creating and managing Google Cloud resources.

Define who can access resources in your organization.

                                      Identify excess permissions using policy insights.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Simplify, automate, and customize the deployment, management, and security of private certificate authorities (CA).
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Establish fine-grained identity and access management for Google Cloud resources.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Control resources and manage access through policies to proactively improve your security configuration.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Allow organization administrators to define fine-grained, attribute-based access control for projects and resources in Google Cloud.

                                      Plan your design for granting the right individuals access to the right resources for the right reasons.
                                      Study fundamental features of cloud security related to access management and identity.        ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage user identities, devices, and applications from one console.

Manage internal enterprise solutions and Google Cloud APIs.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Discover, govern, use, and monitor Model Context Protocol (MCP) servers and tools.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Control internal enterprise solutions and make them easily discoverable.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      List, enable, and disable APIs and services in your Google Cloud projects, and apply quota restrictions to services.

Optimize your service usage, monitor application and resource health, and identify disruptive events.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      Gain visibility into disruptive events impacting Google Cloud products.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      View centralized operations data and insights about the health of your Google Cloud applications and resources so that you can take action on  issues, patterns, and trends.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Provides usage recommendations and insights for Cloud products and services to optimize usage for performance, security, cost, or manageability.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage Google Cloud resources programmatically.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Use inventory services based on a time series database.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage your Google Cloud resources using a command-line interface from any browser.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage Google Cloud resources, such as Spanner or Cloud Storage, through the Google Kubernetes Engine API.

                                      Centralized and programmatic control over your organization's cloud resources.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Control resources and manage access through policies to proactively improve your security configuration.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      View and manage your Google Cloud resources, grant Identity and Access Management (IAM) roles at the organization level, and manage organization resource billing accounts using the Google Cloud console.

                                      Explore methods to authenticate your applications to access Google APIs and services.

                                      Monitor for credential compromise and take action to keep your data secure and protected from attackers.

                                      Review the secure process that occurs when you delete your customer data stored in Google Cloud.
                                                Was this helpful?
