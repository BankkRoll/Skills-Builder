# Instana and more

# Instana

## Overview

## How to configure Instana with Cortex

### Prerequisite

### Configure the integration in Cortex

1. 1.
2.
3. -
  -
4.

## How to connect Cortex entities to Instana

### Import services from Instana

### Import Instana services from Discovery audit

## View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Jenkins

- -
-
-

## How to integrate Jenkins with Cortex

### Prerequisites

- -

### Step 1: Install the Cortex Deployer app

-

### Step 2: Add a step to your Jenkins pipeline

#### Jenkins secrets

#### Jenkinsfile

$/$

### Step 3: Configure Jenkins in Cortex to enable Jenkins Workflow blocks

1. -
2.
3. -
  -
  -
  -
4.

## Using the Jenkins integration

### View Jenkins deploys on entity pages in Cortex

-
-
-

### Kick off a Jenkins pipeline in a Cortex Workflow

### See Jenkins data in Eng Intelligence

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Jira

-
-
-

## How to configure Jira with Cortex

-
- -
  -

1. -
2. -
3. -
  - -
  - -
  - -
  -
4.

1. 1.
  2.
2.
3.
4. -
  -
  -
  -
5.

1.
2. -
  -
  -
  -
3.
4.

1. 1.
  2.
2.
3.
4. -
  -
  -
  -
5.
6. -
  -

## Set a default JQL query for your Jira integration

$/$

### Fallback logic for default JQL

1.
2.
3.
4.

### Adding filter logic to the default JQL query in a Scorecard

## How to connect Cortex entities to Jira labels, components, or projects

### Discovery

### Connecting via YAML or the Cortex UI

1.
2. ![In the upper right side of an entity, click "Configure entity."](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-4377b900f82f853bbf04515ee4b722a56ebc35c1%252Fconfigure-entity-team.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=a199c563&sv=2)
3. ![Click Project management, then click Add.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-76d2fab28795fc034d44dcf53012d9c3667f986e%252Fjira-ui.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=272792e7&sv=2)
4. -
  -
  -
5.

FieldDescriptionRequired$/$$/$$/$$/$$/$

### Identity mappings

## Using the Jira integration

#### Entity pages

-
-

-
-
-
-
-
-

#### Initiatives

#### Dev homepage

### Scorecards and CQL

Issues$/$Issues from JQL query$/$

### View integration logs

## Background sync

## FAQs and troubleshooting

1.
2.
3.

$/$

## Still need help?​

-
-

Last updated 2 months ago

Was this helpful?

---

# Kubernetes

-
-
-

## How to configure Kubernetes with Cortex

### Prerequisites

-
- -
  -

#### Security considerations

-
-
-

### Install the Cortex k8s agent in your Kubernetes cluster

1. $/$
2. $/$
3. $/$

## Connecting Cortex entities to Kubernetes

### Discovery

### Methods for mapping Kubernetes resources

MethodUse caseAction$/$$/$Customize annotation mapping

1. -
2.
3.

$/$$/$Customize label-based auto-mapping

1.
2.
3.

-
-

$/$FieldDescriptionRequired$/$$/$$/$$/$

### Import entities from Kubernetes

## Using the Kubernetes integration

### View Kubernetes data on entity pages

![Kubernetes data appears in the Kubernetes block on the entity details page overview.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-56273288eb9014744ce709454293d22462609efe%252Fkubernetes-block.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=659e515a&sv=2)

-
-

![](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-f7626e73dc00033ea5b57b2cd3cddf8ea34bbc8e%252Fkubernetes-sidebar.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=cc5ae8ea&sv=2)

### Eng Intelligence

### Scorecards and CQL

Cluster information$/$$/$Deployment labels$/$$/$$/$K8s resource is set for entity$/$Kubernetes spec YAML$/$$/$Replica information$/$

## Background sync

## FAQs and troubleshooting

#### When I try to import entities, I don't see all the supported workload types (deployments, ArgoCD rollout, StatefulSet, CronJob)

#### Missing namespaces from Kubernetes discovery

$/$$/$

#### Helm chart and deprecated Kubernetes Docker registry

1. $/$
2.

#### Failing ArgoCD rollouts error in the k8s agent

$/$

#### Can I deploy on prem if I don’t use Kubernetes?

## Still need help?​

-
-

Last updated 23 days ago

Was this helpful?

---

# LaunchDarkly

-
-
- -

## How to configure LaunchDarkly with Cortex

### Prerequisites

- -
-

### Configure the integration in Cortex

1. -
2.
3. -
  -
  -
4.

#### Configure the integration for multiple LaunchDarkly accounts​

## How to connect Cortex entities to LaunchDarkly

### Discovery

### Editing the entity descriptor

$/$

## Using the LaunchDarkly integration

### Scorecards and CQL

Check if LaunchDarkly project is set$/$Feature flags$/$

### View integration logs

## FAQs and troubleshooting

#### How often does the integration poll for new flags?

## Still need help?​

-
-

Last updated 21 days ago

Was this helpful?

---

# Lightstep

### Overview

### How to configure Lightstep with Cortex

#### Prerequisite

#### Configure the integration in Cortex

1. -
2.
3. - -
  - -
  -
4.

### Linking SLOs in Cortex

$/$FieldDescription

## Using the Lightstep integration

### Entity pages

### Scorecards and CQL

SLOs$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Mend

## Overview

-
-

## How to configure Mend with Cortex

1. -
2.
3. -
4.

1. 1.
  2.
2.
3. -
  - -
  - -
  - -
    -
    -
  -
4.

### Advanced configuration

## How to connect Cortex entities to Mend

#### Discovery

#### Editing the entity descriptor

$/$

## Using the Mend integration

### Entity pages

### Scorecards and CQL

Check if Mend project is set$/$Vulnerabilities$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Microsoft Teams

- -
-
-

## How to configure Microsoft Teams with Cortex

### Step 1: Configure the integration in Cortex

1. 1.
2.
3.
4.

PermissionRequirementsDescription

### Step 2: Install the Cortex app for Teams through Microsoft AppSource

1.
2.

### Step 3: Configure a setup policy for Cortex in Teams

1.
2.
3. -
  -
4.

### Limitations

## How to connect Cortex entities to Microsoft Teams

### Editing the entity descriptor

$/$FieldDescriptionRequired

## Using the Microsoft Teams integration

### Viewing Microsoft Teams information across Cortex

- ![The MS Teams channels appear in the upper right side of an entity details page.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-c61978a640726b1da660b5bd9b4c5be95a013f36%252Fmsteams-entity.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=34c04fc4&sv=2)
-

### Managing Microsoft Teams notifications

![A notification in MS Teams includes actionable information.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-95784fecd6fa3df45dcec47ab0ac6c252096ae87%252Fmsteams-notification.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=1998a4d6&sv=2)

#### Team, user, and entity MS Teams notifications

-
-
-

### Scorecards and CQL

Check if Microsoft Teams channel is set$/$Number of Microsoft Teams channels

-
-

$/$Total number of members across Microsoft Teams channels registered for the entity

-
-
-

$/$

### View integration logs

## Privacy Policy

## Still need help?​

-
-

Last updated 1 month ago

Was this helpful?

---

# New Relic

-
-
-
-

## How to configure New Relic with Cortex

### Prerequisite

- -

### Configure the integration in Cortex

1. 1.
2.
3. -
  -
  -
  -
4.

#### Cross-account access

### Configure the integration for multiple New Relic accounts​

## How to connect Cortex entities to New Relic

#### Auto discovery

- -
- -

### Import entities from New Relic

### Editing the entity descriptor

$/$FieldDescriptionRequired$/$FieldDescriptionRequired$/$FieldDescriptionRequired$/$FieldDescriptionRequired$/$FieldDescriptionRequired

## Using the New Relic integration

### View New Relic data on entity pages

-
-
-
-
-
-
-
-

### Relationship graphs

### Scorecards and CQL

Application summary

-
-
-
-
-
-
-
-
-
-
-
-

$/$New Relic application is set$/$Raw NRQL query$/$$/$SLOs

-
-
-
-
-
-
-
-
-

-
-

-
-

$/$$/$Accessing OpenTelemetry data with CQL and NRQL$/$

### View integration logs

## Still need help?​

-
-

Last updated 1 month ago

Was this helpful?

---

# Okta

## Overview

## How to configure Okta with Cortex

### Prerequisites

- - -
    -
    -
- -

### Configure the integration in Cortex

1. -
2.
3. -
  -
  -
4.

## How to connect Cortex entities to Okta

### Import teams from Okta

### Editing the entity descriptor

$/$

## Using the Okta integration

### Scorecards and CQL

All ownership details$/$All owner details$/$Team details$/$

### View integration logs

## Background sync

## Troubleshooting and FAQ

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Opsgenie

- -
  -
-
-

## How to configure Opsgenie with Cortex

### Prerequisite

-
-

### Configure the integration in Cortex

1. -
2. -
  -
  -
3.

## How to connect Cortex entities to Opsgenie

### Discovery

### Entity descriptor

$/$FieldDescriptionRequired$/$FieldDescriptionRequired

#### Ownership

$/$FieldDescriptionRequired

#### Identity mappings

## Using the Opsgenie integration

### Viewing on-call information for an entity

![On-call information appears on the right side of an entity details page.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-f03475e71133c9b3b9aa06d674c5dd5afe904f25%252Fon-call-block.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=13d5530a&sv=2)

### Viewing recent Opsgenie events

### Viewing on-call information on the dev homepage

### Scorecards and CQL

Check if on-call is set$/$Number of alerts$/$$/$Number of escalations$/$On-call metadata

-
-
-

$/$$/$All ownership details$/$All owner details$/$Team details$/$

### View integration logs

## Background sync

-
-

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# PagerDuty

- -
  -
-
- -
-
-
-
-

### How to configure PagerDuty with Cortex

### Prerequisites

- - -
    -
  - -
    -
    -
    -
    -

### Configure the integration in Cortex

1. -
2.
3. - -
4.

## Enabling the On-call Assistant

## How to connect Cortex entities to PagerDuty

### Discovery

### Considerations for registering PagerDuty entities

-
-
-
-

#### View on-call data only

### Editing the entity descriptor

FieldDescriptionRequired

#### Define a PagerDuty service

$/$

#### Define a schedule

$/$

#### Define an escalation policy

$/$

### Identity mappings

## Using the PagerDuty integration

#### Entity pages

#### Engineering homepage

#### Eng Intelligence

#### Retrieve on-call information in Slack

#### Scorecards and CQL

Check if on-call is set$/$Forbidden contact methods

-
-
-
-
-

$/$$/$$/$Incident response analysis

-
-
-
-
-
-
-
-
-
-
-
-
-
-
-

$/$$/$$/$Incidents

-
-
-
-
-
-
-

$/$$/$$/$Number of escalations$/$On-call metadata$/$$/$

### Trigger an incident

1.
2.
3. -
  -
  -
4. -

### View integration logs

## Background sync

-
-
-

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Prometheus

## Overview

-
-

## How to configure Prometheus with Cortex

### Prerequisite

1. -
2.
3. -
  -
  -
  - -
4.

## Connecting Cortex entities to Prometheus

### Linking SLOs in Cortex

$/$FieldDescription

### How Cortex calculates Prometheus SLOs

$/$

## Using the Prometheus integration

### View Prometheus data in entity pages

### Scorecards and CQL

SLOs$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 2 months ago

Was this helpful?

---

# Rollbar

-
-

## How to configure Rollbar with Cortex

### Prerequisites

- -
  -

### Configure the integration in Cortex

1. 1.
2.
3. -
  - -
4.

## How to connect Cortex entities to Rollbar projects

### Discovery

### Editing the entity descriptor

$/$FieldDescriptionRequired

## Using the Rollbar integration

### Viewing Rollbar errors on an entity

### Scorecards and CQL

Check if Rollbar project is set$/$$/$RQL query$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Rootly

-
- -
-

## How to configure Rootly with Cortex​

### Prerequisites​

-

### Configure the integration in Cortex​

1. -
2.
3. -
  -
4.

## Viewing incidents in Cortex​

1.
2.
3.

## How to connect Cortex entities to Rootly​

### Discovery​

#### Editing the entity descriptor

FieldDescriptionRequired

#### Service ID

$/$

#### Service slug

$/$

## Using the Rootly integration

### Trigger an incident​

1.
2.
3. -
  -
  -
  -
  -
4. -

### Scorecards and CQL​

Check if Rootly service is set$/$Incidents

-
-
-
-
-
-
-
-

$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Semgrep

-
-

## How to configure Semgrep with Cortex

### Prerequisites

-

### Configure the integration in Cortex

1. -
2.
3. -
  -
  -
  -
4.

## How to connect Cortex entities to Semgrep

### Match entity names to Semgrep projects

### Editing the entity descriptor

$/$

## Using the Semgrep integration

### Viewing Semgrep information in Cortex

- ![See Semgrep data on an entity's overview.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-e46d8071830d28166bca2d0e39a057d9f5708b78%252Fsemgrep-entity-overview.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=5ddbdd19&sv=2)
- -
  ![On an entity, click Code & security > Semgrep to view vulnerability details from Semgrep.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-0497bec10b502cf23b0eded8c570a8fc6e2dad53%252Fsemgrep-entity-details.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=a3bdefc8&sv=2)

### Scorecards and CQL

Check if Semgrep project is set$/$List vulnerabilities$/$Get scan results for an entity$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Sentry

-
-
-

## How to configure Sentry with Cortex

### Prerequisites

- -

### Configure the integration in Cortex

1. -
2.
3. -
  - -
  -
4.

## How to connect Cortex entities to Sentry projects

### Discovery

### Editing the entity descriptor

$/$FieldDescriptionRequired

## Using the Sentry integration

### Viewing Sentry errors on an entity

### Using the Cortex Slack Bot with Sentry

### Scorecards and CQL

Check if Sentry project is set$/$Number of events$/$Number of issues$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 3 months ago

Was this helpful?

---

# ServiceNow

-
-
-
-
-

## How to configure ServiceNow with Cortex

### Prerequisites

### Step 1: Configure the integration in Cortex

1. -
2.
3. - -
  -
4.

### Step 2: Configure table mappings

1.
2. -
  -
  -
  -
  -
  -
  -
3.

## How to connect Cortex entities to ServiceNow

### Import entities from ServiceNow

-
-
- -
  -

### Enable automated import of domains for ServiceNow

1.
2.

#### Manually sync domains

1.
2.

### Editing the entity descriptor

$/$

#### Configuring your ServiceNow teams as owners

$/$

## Using the ServiceNow integration

### Scorecards and CQL

All ownership details$/$All owner details$/$Team details$/$

### View integration logs

### Workflows

### ServiceNow Incidents plugin

![](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-a5dbe65a9b7946303ba6e0bc752bc9d4a9e90dac%252Fservicenow-plugin.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=f489ff15&sv=2)

### Background sync

## Still need help?​

-
-

Last updated 2 months ago

Was this helpful?

---

# Slack

- -
-
-
-
-

## How to configure Slack with Cortex

### Prerequisites

-
-
-

### Step 1: Configure the integration in Cortex

1. -
2.
3.
4. -
5. ![In the Slack permission page, click Allow.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-6bcbe645a01cbd2bead0fcad227a46d9d6e6b522%252Fslack-permission.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=374e1a9a&sv=2)

### Step 2: Configure Slack app settings

-
- -
- -

![You can configure additional settings for Slack after setting up the integration.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-ce9358dec0ac8002efdd24a3ae2d15a6b7a55336%252Fslack-settings.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=443ad5c0&sv=2)

## Using the Slack integration

### Viewing Slack information across Cortex

- ![Slack channels appear in the top of an entity details page.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-76249cb87c7298b7a4b05bdf6e088d6fdb0217c4%252Fslack-on-entity.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=35b11a87&sv=2)
-

### Managing Slack notifications

#### Team, user, and entity Slack notifications

-
-
-

### Using the Cortex Slack bot

#### Cortex Bot notifications

#### Add the Cortex Slack Bot to a private channel

1.
2.
3. ![When Slack prompts you to add the Cortex bot, click "Add them."](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-2ebce75cea6f5d2ad6dd96bafa901d4b12a782e7%252Fslackbot-private-channel.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=e01c333c&sv=2)

#### Cortex Bot Commands

#### Using AI assistant in Slack

-
-

### View integration logs

## How to connect Cortex entities to Slack channels

$/$FieldDescriptionRequired$/$FieldDescriptionRequired$/$

1.
2. ![In the upper right side of an entity, click "Configure entity."](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-4377b900f82f853bbf04515ee4b722a56ebc35c1%252Fconfigure-entity-team.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=a199c563&sv=2)
3. ![Click the Slack Channels tab, then click +Add.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-262f59265979e661079ee08be186603eb7dbef97%252Fadd-slack-channel.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=b549fbc3&sv=2)
4. -
  -
  -
5.

### Identity mappings

## Scorecards and CQL

Check if Slack channel is set$/$Number of Slack channels$/$Total number of members across Slack channel$/$

## Background sync

## FAQs and troubleshooting

#### Can users access information via the Slack Bot if they haven't logged in to our Cortex instance?

#### Can I disable some of the notifications I receive in Slack?

#### Is the Slack integration required to add Slack channels to a team?

#### Why isn't my Slack channel showing up after I've added it to an entity's YAML configuration?

## Privacy policy

## Still need help?​

-
-

Last updated 3 months ago

Was this helpful?

---

# Snyk

- -
-

## How to configure Snyk with Cortex

### Prerequisites

- -
  -
  -
  -

### Configure the integration in Cortex

1. -
2.
3. -
  -
4.

## How to connect Cortex entities to Snyk projects

### Discovery

### Editing the entity descriptor

$/$FieldDescriptionRequired

## Using the Snyk integration

### Viewing Snyk vulnerabilities on an entity

#### Entity page overview

#### Entity code & security sidebar

-
-
-
-
-

### Scorecards and CQL

Check if Snyk project is set$/$Number of Snyk issues

-
-
- -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  - -
    -
    -
    -
    -
    -

$/$$/$$/$

### View integration logs

## Background sync

## Still need help?​

-
-

Last updated 1 month ago

Was this helpful?

---

# SonarQube

-
-

## How to configure SonarQube with Cortex

### Self-hosted prerequisites

### Configure the integration

-
-

1. -
2.
3. -
  -
  - -
4.

#### Integrate via custom webhook

## How to connect Cortex entities to SonarQube projects

### Discovery

### Connect entities via YAML or the Cortex UI

1.
2. ![In the upper right side of an entity, click "Configure entity."](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-4377b900f82f853bbf04515ee4b722a56ebc35c1%252Fconfigure-entity-team.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=a199c563&sv=2)
3. ![Click Code quality, then enter your SonarQube project details.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-4dd3736340b118bf8cf120f511d9017c4b936ad2%252Fsonarqube-ui.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=f6914e64&sv=2)
4. -
  -
5.

$/$FieldDescriptionRequired

## Using the SonarQube integration

### View SonarQube data on entity pages

- -
  -
  -
  -
  -
  -
  -
  -
  -
-
-

### Scorecards and CQL

Analysis freshness$/$Metric

-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-

$/$$/$$/$$/$$/$Project existence$/$Issues$/$$/$$/$

### View integration logs

## FAQs and troubleshooting

#### Does Cortex support SonarCloud?

#### I’m seeing “Socket timed out when trying to connect to SonarQube” for all of my entities in Scorecards.

#### I’m using Gradle and I’ve verified that my project is in SonarQube, but Cortex is still showing me an error.

#### My project is in Sonar and Cortex is able to talk to SonarQube, but my score isn’t showing up.

1.
2.
3.

$/$

#### What if I want to send custom data, but I don't have control over the integration touchpoint?

#### Why might I see the SonarQube connection errorComponent key not found?​

#### Why might I see the errorSonarqube: Fail to request urlon my integration page or avalidity check failederror while creating a Workflow?​

## Still need help?​

-
-

Last updated 1 month ago

Was this helpful?

---

# Splunk Observability Cloud (SignalFx)

-
-

## How to configure Splunk Observability Cloud with Cortex

### Prerequisites

-

### Configure the integration in Cortex

1. 1.
2.
3. - -
  -
4.

## How to connect Cortex entities to Splunk Observability SLOs

### Editing the entity descriptor

$/$FieldDescriptionRequired

## Using the Splunk Observability integration

### Viewing SLO information on an entity

- ![View SLOs in the entity sidebar under Monitoring > Data overview.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-9acda56f365ccf261d909e0af790b538cada3d82%252Fsplunk-entity-details.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=4fa64ab&sv=2)
- ![View a graph of SLO performance.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-f7400b9337475f4af241ac00840b8678d284e66c%252Fsplunk-slo-graph.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=2bdd5f0&sv=2)

### Scorecards and CQL

SLOs$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Splunk On

- -
  -
-

## How to configure Splunk On-Call with Cortex

### Prerequisites

- -
- -

### Configure the integration in Cortex

1. 1.
2.
3. -
  -
  - -
  -
4.

## How to connect Cortex entities to Splunk On-Call

### Editing the entity descriptor

$/$$/$FieldDescriptionRequired

## Using the Splunk On-Call integration

#### Entity pages

### Scorecards and CQL

Check if on-call is set$/$Number of escalations$/$On-call metadata$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Sumo Logic

## Overview

## How to configure Sumo Logic with Cortex

### Prerequisites

-
-

### Configure the integration in Cortex

1. -
2.
3. -
  -
  -
4.

### Linking SLOs in Cortex

$/$

## Using the Sumo Logic integration

#### Entity pages

### Scorecards and CQL

SLOs$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Veracode

-
-

## How to configure Veracode with Cortex

### Prerequisite

- - -
    -
    -
    -
  - -
    -
- -
  -
  -

### Configure the integration in Cortex

1. 1.
2.
3. -
  -
  -
4.

### Advanced configuration

## How to connect Cortex entities to Veracode

### Editing the entity descriptor

$/$

## Using the Veracode integration

### View Veracode data on entity pages

### Scorecards and CQL

Check if Veracode application is set$/$Findings$/$$/$$/$

### View integration logs

## Background sync

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Custom webhook integrations

-
-
-

## How to create a custom webhook integration in Cortex

### Step 1: Configure the custom integration in Cortex

1.
2. ![Click +Add custom integration.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-497af29348536c125bdd1b0d8493f5db58e4be43%252Fcustom-integration.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=732a604f&sv=2)
3. -
  - -
    -
  - -
    -
4.
5.

### Step 2: Send data to the webhook

1.

$/$

1. -

### Changing the mappings for entities

$/$

## View custom integration data in Cortex

![The "Custom data and metrics" page in an entity's sidebar displays data from webhook integrations.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-d9126438a43b6d2b596885d3627d0889c9c8181d%252Fcustom-webhook.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=d5b9a00e&sv=2)

## Example: GitHub webhook

1. -
  -
2.
3. -
  -
4. - ![The repository name appears in the "Recent deliveries" tab for the webhook in GitHub.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-e3e73e09cc4a9f9607d93fd0287baa16ab6df4d1%252Fgithub-webhook-payload.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=244a9162&sv=2)
5. -
6. - ![The custom webhook data appears next to the key on the entity page.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-c863e87724293309994474824775466702d344ae%252Fexample-webhook.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=bd866f3c&sv=2)

Last updated 4 months ago

Was this helpful?

---

# Wiz

-
- -
-

## How to configure Wiz with Cortex

### Prerequisites

-
-
- -

### Configure the integration in Cortex

1. 1.
2.
3. -
  -
  -
4.

## How to connect Cortex entities to Wiz

### Match entity names to Wiz projects

#### Considerations for mapping Wiz projects to entities

Wiz project mapping best practices

- -
-

- -
-
- -

-
- -
-

### Editing the entity descriptor

$/$

## Using the Wiz integration

### View Wiz information on entity pages

![View Wiz issues on the entity details page under Code & security.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-4349daa269f4bfd114283696fd17e2a1ece67d31%252Fwiz-issues-entity.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=7ca9a8ea&sv=2)

### Scorecards and CQL

Check if Wiz project is set$/$Wiz issues$/$$/$$/$

### View integration logs

## Still need help?​

-
-

Last updated 2 months ago

Was this helpful?

---

# Workday

## How to configure Workday with Cortex

### Step 1: Generate an ownership report in Workday

-
-

-
-
-
-
-
-
-
-
-
-

-
-
-
-
-
-
-
- -

### Step 2: Configure the integration in Cortex

1. -
2.
3. -
  -
  - -
4.

### Step 3: Configure the report mappings

1. - -
    -
    -
    -
    - -
    - -
  - - -
    - -
      -
    - - -
        -
        -
        -
2.

#### Configure the hierarchy fields for auto-importing Workday teams

-
-
-
- -

## How to connect Cortex entities to Workday

### Discovery

### Automatic import of teams

1.
2.
3.

#### Manually trigger team import

1.
2.
3.

### Entity descriptor

$/$FieldDescriptionRequired

## Using the Workday integration

#### Entity pages

### Scorecards and CQL

All ownership details$/$All owner details$/$Team details$/$

### View integration logs

## Background sync

## Limitations

## Still need help?​

-
-

Last updated 2 months ago

Was this helpful?

---

# xMatters

- -
  -
-
-

## How to configure xMatters with Cortex

### Configure the integration in Cortex

1. 1.
2.
3. -
  - -
4.

## Trigger an incident

1.
2.
3. -
  -
  -
4. -

## How to connect Cortex entities to xMatters

### Discovery

### Editing the entity descriptor

$/$FieldDescriptionRequired

## Using the xMatters integration

#### Entity pages

### Scorecards and CQL

Check if on-call is set$/$Number of escalations$/$On-call metadata$/$

### View integration logs

## Still need help?​

-
-

Last updated 4 months ago

Was this helpful?

---

# Integrations

![](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-451d9f50cac91b38aca3899530a1d4d01f49dba2%252Fnew-integration-page.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=80cf9bab&sv=2)

## Third-party integrations

### Essentials

Version control

-
-
-
-

Team/Ownership

-
-
-
-
-
-
-
-
-
-

On-call

-
-
-
-

Project management

-
-
-
-
-

Communication

-
-

Code quality

-
-

### Extended

CI/CD

-
-
-
-
-
-

Cloud

-
-
-
-

Error tracking

-
-
-

Feature flags

-

Incidents

-
-
-
-

Observability

-
-
-
-
-
-
-
-
-
-

Security

-
-
-
-
-
-
-
-
-

ITSM

-

### Internally hosted integrations

### Custom webhook integration

### SSO integrations for Cortex workspace access

SSO

-
-
-
-

## Integration rate limiting

## Troubleshooting with integration logs

![Click the Logs tab on an integration to view integration logs and errors.](https://docs.cortex.io/~gitbook/image?url=https%3A%2F%2F826863033-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJW7pYRxS4dHS3Hv6wxve%252Fuploads%252Fgit-blob-9c0bf87a084b87a1b5d6c8f5ace39c90c17ce703%252Fgithub-logs-tab.jpg%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=dd1a09dc&sv=2)

Last updated 1 month ago

Was this helpful?

---

# Overview: Ingesting data into Cortex

### How Cortex handles data modeling

-
-
-

## Connect your data

- -
- -
- -

## Cortex data concepts reference table

ConceptDefinition

Last updated 3 months ago

Was this helpful?
