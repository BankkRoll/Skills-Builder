# Terraform blueprints and modules for Google CloudStay organized with collectionsSave and categorize content based on your preferences. and more

# Terraform blueprints and modules for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

# Terraform blueprints and modules for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

Blueprints and modules help you automate provisioning and managing
 Google Cloud resources at scale.

A module is a reusable set of Terraform configuration files that creates a
logical abstraction of Terraform resources.

A blueprint is a package of deployable, reusable modules and policy that
implements and documents a specific opinionated solution. Deployable
configuration for all Terraform blueprints are packaged as Terraform modules.

Add a <devsite-select> custom element and give it a unique 'id'.    Select a category Compute Containers Data analytics Databases Developer tools End-to-end Healthcare and life sciences Networking Operations Security and identity Serverless computing Storage Workspace  Select an option

- Select a category
- Compute
- Containers
- Data analytics
- Databases
- Developer tools
- End-to-end
- Healthcare and life sciences
- Networking
- Operations
- Security and identity
- Serverless computing
- Storage
- Workspace

  Add a <devsite-filter> custom element and set its 'select-el-container-id' attribute to the
same value as the 'id' assigned to the <devsite-select> custom element; this is what connects the
dropdown menu to the filter.

| Category | Blueprints and modules | Description |
| --- | --- | --- |
| End-to-end, Data analytics | ai-notebook | Demonstrates how to protect confidential data in Vertex AI Workbench
       notebooks |
| Data analytics, End-to-end | crmint | Deploy the marketing analytics application, CRMint |
| End-to-end, Operations | enterprise-application | Deploy an enterprise developer platform on Google Cloud |
| End-to-end, Operations | example-foundation | Shows how the CFT modules can be composed to build a secure cloud foundation |
| End-to-end | fabric | Provides advanced examples designed for prototyping |
| Developer tools, End-to-end, Security and identity | secure-cicd | Builds a secure CI/CD pipeline on Google Cloud |
| End-to-end, Data analytics | secured-data-warehouse | Deploys a secured BigQuery data warehouse |
| Data analytics, End-to-end, Security and identity | secured-data-warehouse-onprem-ingest | Deploys a secured data warehouse variant for ingesting encrypted data from on-prem sources |
| End-to-end | vertex-mlops | Create a Vertex AI environment needed for MLOps |
| Networking | address | Manages Google Cloud IP addresses |
| Databases | alloy-db | Creates an AlloyDB for PostgreSQL instance |
| Data analytics | analytics-lakehouse | Deploys a Lakehouse Architecture Solution |
| Compute | anthos-vm | Creates VMs on Google Distributed Cloud clusters |
| Developer tools | apphub | Creates and manages App Hub resources |
| Containers, Developer tools | artifact-registry | Create and manage Artifact Registry repositories |
| Developer tools, Operations, Security and identity | bastion-host | Generates a bastion host VM compatible with OS Login and IAP tunneling that can be used to access internal VMs |
| Compute, Operations | backup-dr | Deploy Backup and DR appliances |
| Data analytics | bigquery | Creates opinionated BigQuery datasets and tables |
| Data analytics | bigtable | Create and manage Google Bigtable resources |
| Developer tools, Operations | bootstrap | Bootstraps Terraform usage and related CI/CD in a new Google Cloud organization |
| Compute, Networking | cloud-armor | Deploy Google Cloud Armor security policy |
| Databases | cloud-datastore | Manages Datastore |
| Developer tools | cloud-deploy | Create Cloud Deploy pipelines and targets |
| Networking | cloud-dns | Creates and manages Cloud DNS public or private zones and their records |
| Serverless computing | cloud-functions | Deploys Cloud Run functions (Gen 2) |
| Networking, Security and identity | cloud-ids | Deploys a Cloud IDS instance and associated resources |
| Networking | cloud-nat | Creates and configures Cloud NAT |
| Operations | cloud-operations | Manages Cloud Logging and Cloud Monitoring |
| Networking | cloud-router | Manages a Cloud Router on Google Cloud |
| Serverless computing | cloud-run | Deploys apps to Cloud Run, along with option to map custom domain |
| Databases | cloud-spanner | Deploys Spanner instances |
| Storage | cloud-storage | Creates one or more Cloud Storage buckets and assigns basic permissions on them to arbitrary users |
| Developer tools, Serverless computing | cloud-workflows | Manage Workflows with optional Cloud Scheduler or Eventarc triggers |
| End-to-end, Data analytics, Operations | composer | Manages Cloud Composer v1 and v2 along with option to manage networking |
| Compute, Containers | container-vm | Deploys containers on Compute Engine instances |
| Data analytics | data-fusion | Manages Cloud Data Fusion |
| Data analytics | dataflow | Handles opinionated Dataflow job configuration and deployments |
| Data analytics | datalab | Creates DataLab instances with support for GPU instances |
| Data analytics | dataplex-auto-data-quality | Deploys data quality rules on BigQuery tables across development and production environments using Cloud Build |
| Serverless computing | event-function | Responds to logging events with a Cloud Run functions |
| Developer tools | folders | Creates several Google Cloud folders under the same parent |
| Developer tools | gcloud | Executes Google Cloud CLI commands within Terraform |
| Developer tools | github-actions-runners | Creates self-hosted GitHub Actions Runners on Google Cloud |
| Developer tools | gke-gitlab | Installs GitLab on Kubernetes Engine |
| Workspace | group | Manages Google Groups |
| Operations, Workspace | gsuite-export | Creates a Compute Engine VM instance and sets up a cronjob to export
       Google Workspace Admin SDK data to Cloud Logging on a schedule |
| Healthcare and life sciences | healthcare | Handles opinionated Google Cloud Healthcare datasets and stores |
| Security and identity | iam | Manages multiple IAM roles for resources on Google Cloud |
| Developer tools | jenkins | Creates a Compute Engine instance running Jenkins |
| Security and identity | kms | Allows managing a keyring, zero or more keys in the keyring, and IAM role bindings on individual keys |
| Compute, Containers | kubernetes-engine | Configures opinionated GKE clusters |
| Networking | lb | Creates a regional TCP proxy load balancer for Compute Engine by using target pools and forwarding rules |
| Networking | lb-http | Creates a global HTTP load balancer for Compute Engine by using forwarding rules |
| Networking | lb-internal | Creates an internal load balancer for Compute Engine by using forwarding rules |
| Networking | load-balanced-vms | Creates a managed instance group with a load balancer |
| Data analytics | log-analysis | Stores and analyzes log data |
| Operations | log-export | Creates log exports at the project, folder, or organization level |
| Operations | media-cdn-vod | Deploys Media CDN video-on-demand |
| Databases | memorystore | Creates a fully functional Google Memorystore (redis) instance |
| Compute, Networking | netapp-volumes | Deploy Google Cloud NetApp Volumes |
| Networking | network | Sets up a new VPC network on Google Cloud |
| Networking | network-forensics | Deploys Zeek on Google Cloud |
| Security and identity | org-policy | Manages Google Cloud organization policies |
| Networking | out-of-band-security-3P | Creates a 3P out-of-band security appliance deployment |
| Security and identity | pam | Deploy Privileged Access Manager |
| Operations | project-factory | Creates an opinionated Google Cloud project by using Shared VPC, IAM, and Google Cloud APIs |
| Data analytics | Pub/Sub | Creates Pub/Sub topic and subscriptions associated with the topic |
| Compute | sap | Deploys SAP products |
| Serverless computing | scheduled-function | Sets up a scheduled job to trigger events and run functions |
| Security and identity | secret-manager | Creates one or more Google Secret Manager secrets and manages basic permissions for them |
| Networking, Security and identity | secure-web-proxy | Create and manage Secure Web Proxy on Google Cloud for secured egress web traffic |
| Security and identity | service-accounts | Creates one or more service accounts and grants them basic roles |
| Operations | slo | Creates SLOs on Google Cloud from custom Stackdriver metrics capability to export SLOs to Google Cloud services and other systems |
| Databases | sql-db | Creates a Cloud SQL database instance |
| Compute | startup-scripts | Provides a library of useful startup scripts to embed in VMs |
| Operations, Security and identity | tags | Create and manage Google Cloud Tags |
| Developer tools, Operations, Security and identity | tf-cloud-agents | Creates self-hosted Terraform Cloud Agent on Google Cloud |
| Databases, Serverless computing | three-tier-web-app | Deploys a three-tier web application using Cloud Run and Cloud SQL |
| Operations | utils | Gets the short names for a given Google Cloud region |
| Developer tools, Operations, Security and identity | vault | Deploys Vault on Compute Engine |
| Compute | vertex-ai | Deploy Vertex AI resources |
| Compute | vm | Provisions VMs in Google Cloud |
| Networking | vpc-service-controls | Handles opinionated VPC Service Controls and Access Context Manager configuration and deployments |
| Networking | vpn | Sets up a Cloud VPN gateway |
| Operations | waap | Deploys the WAAP solution on Google Cloud |

     Was this helpful?

---

# Quickstart: Create a VM instance using TerraformStay organized with collectionsSave and categorize content based on your preferences.

> Learn how to use Terraform to create a Compute Engine VM.

# Quickstart: Create a VM instance using TerraformStay organized with collectionsSave and categorize content based on your preferences.

In this quickstart, you learn how to use Terraform to create a Compute Engine
Virtual Machine (VM) instance and connect to that VM instance.

Hashicorp Terraform is an Infrastructure as code (IaC) tool that lets you
provision and manage cloud infrastructure. *Terraform provider for
Google Cloud* (*Google Cloud provider*) lets you provision and
manage Google Cloud infrastructure.

## Before you begin

1. To use an online terminal with the gcloud CLI and Terraform
  already set up, activate Cloud Shell:
  At the bottom of this page, a Cloud Shell session starts and
  displays a command-line prompt. It can take a few seconds for the session to
  initialize.
2. [Create or select a Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  - **Select a project**: Selecting a project doesn't require a specific
          IAM role—you can select any project that you've been
          granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
          (`roles/resourcemanager.projectCreator`), which contains the
          `resourcemanager.projects.create` permission. [Learn how to grant
          roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  - Create a Google Cloud project:
    ```
    gcloud projects create PROJECT_ID
    ```
    Replace `PROJECT_ID` with a name for the Google Cloud project you are creating.
  - Select the Google Cloud project that you created:
    ```
    gcloud config set project PROJECT_ID
    ```
    Replace `PROJECT_ID` with your Google Cloud project name.
3. [Verify that billing is enabled for your Google Cloud project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
4. Enable the Compute Engine API:
  To enable APIs, you need the Service Usage Admin IAM
        role (`roles/serviceusage.serviceUsageAdmin`), which contains the
        `serviceusage.services.enable` permission. [Learn how to grant
        roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  ```
  gcloud services enable compute.googleapis.com
  ```
5. Grant roles to your user account. Run the following command once for each of the following
            IAM roles:
            `roles/compute.instanceAdmin.v1`
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
  ```
  Replace the following:
  - `PROJECT_ID`: Your project ID.
  - `USER_IDENTIFIER`: The identifier for your user
                account. For examples, see
                [Represent workforce pool users in IAM policies](https://cloud.google.com/iam/docs/workforce-identity-federation#representing-workforce-users).
  - `ROLE`: The IAM role that you grant to your user account.

## Prepare the environment

1. Clone the GitHub repository containing Terraform samples:
  ```
  git clone https://github.com/terraform-google-modules/terraform-docs-samples.git --single-branch
  ```
2. Go to the directory that contains the quickstart sample:
  ```
  cd terraform-docs-samples/compute/quickstart/create_vm
  ```

## Review the Terraform files

Review the `main.tf` file. This file defines the Google Cloud
resources that you want to create.

```
cat main.tf
```

The output is similar to the following

```
resource "google_compute_instance" "default" {
  name         = "my-vm"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-minimal-2210-kinetic-amd64-v20230126"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
```

This file describes the
[google_compute_instanceresource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance), which is the Terraform resource for the
Compute Engine VM instance. `google_compute_instance` is configured to
have the following properties:

- `name` is set to `my-vm`.
- `machine_type` is set to `n1-standard-1`.
- `zone` is set to `us-central1-a`.
- `boot_disk` sets the boot disk for the instance.
- `network_interface` is set to use the default network in your
  Google Cloud project.

## Create the Compute Engine VM instance

1. In Cloud Shell, run the following command to verify that Terraform
  is available:
  ```
  terraform
  ```
  The output should be similar to the following:
  ```
  Usage: terraform [global options] <subcommand> [args]
  The available commands for execution are listed below.
  The primary workflow commands are given first, followed by
  less common or more advanced commands.
  Main commands:
    init          Prepare your working directory for other commands
    validate      Check whether the configuration is valid
    plan          Show changes required by the current configuration
    apply         Create or update infrastructure
    destroy       Destroy previously-created infrastructure
  ```
2. Initialize Terraform by running the following command. This command prepares
  your workspace so Terraform can apply your configuration.
  ```
  terraform init
  ```
  The output should be similar to the following:
  ```
  Initializing the backend...
  Initializing provider plugins...
  - Finding latest version of hashicorp/google...
  - Installing hashicorp/google v5.35.0...
  - Installed hashicorp/google v5.35.0 (signed by HashiCorp)
  Terraform has created a lock file .terraform.lock.hcl to record the provider
  selections it made above. Include this file in your version control repository
  so that Terraform can guarantee to make the same selections by default when
  you run "terraform init" in the future.
  Terraform has been successfully initialized!
  ```
3. Validate the Terraform configuration by running the following command.
  This command takes the following actions:
  - Verifies that the syntax of `main.tf` is correct.
  - Shows a preview of the resources that will be created.
  ```
  terraform plan
  ```
  The output should be similar to the following:
  ```
  Plan: 1 to add, 0 to change, 0 to destroy.
  Note: You didn't use the -out option to save this plan, so Terraform can't
  guarantee to take exactly these actions if you run "terraform apply" now.
  ```
4. Apply the configuration to provision resources described in the `main.tf`
  file:
  ```
  terraform apply
  ```
  When prompted, enter `yes`.
  Terraform calls Google Cloud APIs to create the VM instance defined in
  the `main.tf` file.
  The output should be similar to the following:
  ```
  Apply complete! Resources: 1 added, 0 changed, 0 destroyed
  ```

## Connect to the VM instance

Connect to the VM instance you just created by running the following command:

```
gcloud compute ssh --zone=us-central1-a my-vm
```

## Clean up

To avoid incurring charges to your Google Cloud account for
          the resources used on this page, delete the Google Cloud project with the
          resources.

In Cloud Shell, run the following command to delete the Terraform
resources:

```
terraform destroy
```

When prompted, enter `yes`.

The output should be similar to the following:

```
Destroy complete! Resources: 1 destroyed.
```

## What's next

- Learn how to [deploy a basic Flask web server using Terraform](https://cloud.google.com/docs/terraform/deploy-flask-web-server).
- Learn how to [store Terraform state in a Cloud Storage bucket](https://cloud.google.com/docs/terraform/resource-management/store-state).

         Was this helpful?

---

# Deploy a basic Flask web server by using TerraformStay organized with collectionsSave and categorize content based on your preferences.

# Deploy a basic Flask web server by using TerraformStay organized with collectionsSave and categorize content based on your preferences.

In this tutorial, you learn how to get started with Terraform by using Terraform
to create a basic web server on Compute Engine.

In this tutorial, you do the following:

- Use Terraform to create a VM in Google Cloud.
- Start a basic Python Flask server.

## Costs

In this document, you use the following billable components of Google Cloud:

[Compute Engine](https://cloud.google.com/compute/all-pricing)

To generate a cost estimate based on your projected usage,
      use the [pricing calculator](https://cloud.google.com/products/calculator).

      New Google Cloud users might be eligible for a [free trial](https://cloud.google.com/free).

When you finish the tasks that are described in this document, you can avoid
   continued billing by deleting the resources that you created. For more information, see
[Clean up](#clean-up).

## Before you begin

Prepare to start the tutorial.

### Select or create a project

1. In the Google Cloud console, go to the project selector page.
  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
2. Select or create a Google Cloud project.
  - **Select a project**: Selecting a project doesn't require a specific
          IAM role—you can select any project that you've been
          granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
          (`roles/resourcemanager.projectCreator`), which contains the
          `resourcemanager.projects.create` permission. [Learn how to grant
          roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

### Set up permissions

Make sure that you have the necessary [Compute Engine permissions](https://cloud.google.com/compute/docs/access/iam) on your user account:

- `compute.instances.*`
- `compute.firewalls.*`

[Go to the IAM page](https://console.cloud.google.com/iam-admin/iam)

[Learn more](https://cloud.google.com/iam/docs) about roles and permissions.

### Enable the API

Enable the Compute Engine API.

To enable APIs, you need the Service Usage Admin IAM
          role (`roles/serviceusage.serviceUsageAdmin`), which
          contains the `serviceusage.services.enable` permission. [Learn how to grant
          roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

[Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=compute.googleapis.com)

### Start Cloud Shell

[Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) is a
Compute Engine virtual machine.

The service credentials associated with this virtual machine are automatic, so
there is no need to set up or download a service account key.

Terraform is integrated with Cloud Shell, and Cloud Shell automatically
authenticates Terraform, letting you get started with less setup.

## Create the Compute Engine VM

First, you define the VM's settings in a Terraform configuration file. Then, you
run Terraform commands to create the VM in your project.

### Create the directory

Create a new directory. In your new directory, create a
`main.tf` file for the Terraform configuration. The contents of this file
describe all of the Google Cloud resources to be created in the project.

In Cloud Shell:

```
mkdir tf-tutorial && cd tf-tutorial
```

```
nano main.tf
```

### Create the Virtual Private Cloud network and subnet

In this section, you create a Virtual Private Cloud (VPC) network and subnet for the VM's
network interface.

Add the following Terraform resources to the `main.tf` file that you created:

- [google_compute_network](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_network)
- [google_compute_subnetwork](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_subnetwork)

```
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-west1"
  network       = google_compute_network.vpc_network.id
}
```

### Create the Compute Engine VM resource

In this section, you create a single Compute Engine instance running
Debian. In this tutorial, you use the smallest
[machine type](https://cloud.google.com/compute/docs/machine-types) that's available. Later, you can
upgrade to a larger machine type.

Add the following [google_compute_instance](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance) Terraform resource to the `main.tf` file that you created.

```
# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = "flask-vm"
  machine_type = "f1-micro"
  zone         = "us-west1-a"
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  # Install Flask
  metadata_startup_script = "sudo apt-get update; sudo apt-get install -yq build-essential python3-pip rsync; pip install flask"

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}
```

The sample code sets the Google Cloud zone to `us-west1-a`. You can change
this to a different [zone](https://cloud.google.com/compute/docs/regions-zones#available).

### Initialize Terraform

At this point, you can run `terraform init` to add the necessary plugins and
build the `.terraform` directory.

```
terraform init
```

Output:

```
Initializing the backend...

Initializing provider plugins...
...

Terraform has been successfully initialized!
```

### Validate the Terraform configuration

Optionally, you can validate the Terraform code that you've built so far. Run
`terraform plan`, which does the following:

- Verifies that the syntax of `main.tf` is correct
- Shows a preview of the resources that will be created

```
terraform plan
```

Output:

```
...

Plan: 1 to add, 0 to change, 0 to destroy.

Note: You didn't use the -out option to save this plan, so Terraform can't
guarantee to take exactly these actions if you run "terraform apply" now.
```

### Apply the configuration

To create the VM, run `terraform apply`.

```
terraform apply
```

When prompted, enter `yes`.

Terraform calls Google Cloud APIs to set up the new VM. Check the
[VM instances page](https://console.cloud.google.com/compute/instances) to
see the new VM.

## Run a web server on Google Cloud

Your next steps are getting a web application created, deploying it to the
VM, and creating a firewall rule to allow client requests to the web
application.

### Add a custom SSH firewall rule

The `default-allow-ssh` firewall rule in the `default` network lets you use
SSH to connect to the VM. If you'd rather use your own custom firewall
rule, you can add the following resource at the end of your `main.tf` file:

```
resource "google_compute_firewall" "ssh" {
  name = "allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.vpc_network.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}
```

Run `terraform apply` to create the firewall rule.

### Connect to the VM with SSH

Validate that everything is set up correctly at this point by connecting to the
VM with SSH.

1. Go to the [VM Instances page](https://console.cloud.google.com/compute/instances).
2. Find the VM with the name `flask-vm`.
3. In **Connect** column, click **SSH**.
  An SSH-in-browser terminal window opens for the running VM.

For more information, see [Connecting to
VMs](https://cloud.google.com/compute/docs/instances/connecting-to-instance).

### Build the Flask app

You build a [Python Flask app](http://flask.pocoo.org/) for this tutorial so
that you can have a single file describing your web server and test endpoints.

1. In the SSH-in-browser terminal, create a file called `app.py`.
  ```
  nano app.py
  ```
2. Add the following to the `app.py` file:
  ```
  from flask import Flask
  app = Flask(__name__)
  @app.route('/')
  def hello_cloud():
    return 'Hello Cloud!'
  app.run(host='0.0.0.0')
  ```
3. Run `app.py`:
  ```
  python3 app.py
  ```
  Flask serves traffic on `localhost:5000` by default.
4. Open a second SSH connection:
  1. Go to the [VM Instances page](https://console.cloud.google.com/compute/instances).
  2. Find the VM named `flask-vm` and click **SSH**.
5. In the second SSH connection, run `curl` to confirm that the greeting that
  you configured in `app.py` is returned.
  ```
  curl http://0.0.0.0:5000
  ```
  The output from this command is `Hello Cloud`.

### Open port 5000 on the VM

To connect to the web server from your local computer, the VM must have
port 5000 open. Google Cloud lets you open ports to traffic by using
firewall rules.

Add the following [google_compute_firewall](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_firewall) Terraform resource at the end of your `main.tf` file.

```
resource "google_compute_firewall" "flask" {
  name    = "flask-app-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }
  source_ranges = ["0.0.0.0/0"]
}
```

In Cloud Shell, run `terraform apply` to create the firewall rule.

### Add an output variable for the web server URL

1. At the end of `main.tf`, add [a Terraform output
  variable](https://www.terraform.io/language/values/outputs)
  to output the web server URL:
  ```
  // A variable for extracting the external IP address of the VM
  output "Web-server-URL" {
   value = join("",["http://",google_compute_instance.default.network_interface.0.access_config.0.nat_ip,":5000"])
  }
  ```
2. Run `terraform apply`.
  ```
  terraform apply
  ```
  When prompted, enter `yes`. Terraform prints the VM's external IP
  address and port 5000 to the screen, as follows:
  ```
  Web-server-URL = "http://IP_ADDRESS:5000"
  ```
  At any time, you can run `terraform output` to return this
  output:
  ```
  terraform output
  ```
3. Click the URL from the previous step, and see the "Hello Cloud!" message.
  This means that your server is running.

## Troubleshooting

- If a required API isn't enabled, Terraform returns an error. The error message
  includes a link to enable the API. After enabling the API, you can rerun
  `terraform apply`.
- If you can't connect to your VM through SSH:
  - Make sure to add the [SSH firewall rule](#ssh-firewall-rule).
  - Make sure that your VM includes the `tags = ["ssh"]` argument.

## Clean up

After completing the tutorial, you can delete everything that you
created so that you don't incur any further costs.

Terraform lets you remove all the resources defined in the configuration file by
running the `terraform destroy` command:

```
terraform destroy
```

Enter `yes` to allow Terraform to delete your resources.

## What's next

- Learn how to [export your Google Cloud resources into Terraform
  format](https://cloud.google.com/docs/terraform/resource-management/export).

---

# Quickstart: Create a VM instance using TerraformStay organized with collectionsSave and categorize content based on your preferences.

> Learn how to use Terraform to create a Compute Engine VM.

# Quickstart: Create a VM instance using TerraformStay organized with collectionsSave and categorize content based on your preferences.

In this quickstart, you learn how to use Terraform to create a Compute Engine
Virtual Machine (VM) instance and connect to that VM instance.

Hashicorp Terraform is an Infrastructure as code (IaC) tool that lets you
provision and manage cloud infrastructure. *Terraform provider for
Google Cloud* (*Google Cloud provider*) lets you provision and
manage Google Cloud infrastructure.

## Before you begin

1. To use an online terminal with the gcloud CLI and Terraform
  already set up, activate Cloud Shell:
  At the bottom of this page, a Cloud Shell session starts and
  displays a command-line prompt. It can take a few seconds for the session to
  initialize.
2. [Create or select a Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  - **Select a project**: Selecting a project doesn't require a specific
          IAM role—you can select any project that you've been
          granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
          (`roles/resourcemanager.projectCreator`), which contains the
          `resourcemanager.projects.create` permission. [Learn how to grant
          roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  - Create a Google Cloud project:
    ```
    gcloud projects create PROJECT_ID
    ```
    Replace `PROJECT_ID` with a name for the Google Cloud project you are creating.
  - Select the Google Cloud project that you created:
    ```
    gcloud config set project PROJECT_ID
    ```
    Replace `PROJECT_ID` with your Google Cloud project name.
3. [Verify that billing is enabled for your Google Cloud project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
4. Enable the Compute Engine API:
  To enable APIs, you need the Service Usage Admin IAM
        role (`roles/serviceusage.serviceUsageAdmin`), which contains the
        `serviceusage.services.enable` permission. [Learn how to grant
        roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  ```
  gcloud services enable compute.googleapis.com
  ```
5. Grant roles to your user account. Run the following command once for each of the following
            IAM roles:
            `roles/compute.instanceAdmin.v1`
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
  ```
  Replace the following:
  - `PROJECT_ID`: Your project ID.
  - `USER_IDENTIFIER`: The identifier for your user
                account. For examples, see
                [Represent workforce pool users in IAM policies](https://cloud.google.com/iam/docs/workforce-identity-federation#representing-workforce-users).
  - `ROLE`: The IAM role that you grant to your user account.

## Prepare the environment

1. Clone the GitHub repository containing Terraform samples:
  ```
  git clone https://github.com/terraform-google-modules/terraform-docs-samples.git --single-branch
  ```
2. Go to the directory that contains the quickstart sample:
  ```
  cd terraform-docs-samples/compute/quickstart/create_vm
  ```

## Review the Terraform files

Review the `main.tf` file. This file defines the Google Cloud
resources that you want to create.

```
cat main.tf
```

The output is similar to the following

```
resource "google_compute_instance" "default" {
  name         = "my-vm"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-minimal-2210-kinetic-amd64-v20230126"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
```

This file describes the
[google_compute_instanceresource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance), which is the Terraform resource for the
Compute Engine VM instance. `google_compute_instance` is configured to
have the following properties:

- `name` is set to `my-vm`.
- `machine_type` is set to `n1-standard-1`.
- `zone` is set to `us-central1-a`.
- `boot_disk` sets the boot disk for the instance.
- `network_interface` is set to use the default network in your
  Google Cloud project.

## Create the Compute Engine VM instance

1. In Cloud Shell, run the following command to verify that Terraform
  is available:
  ```
  terraform
  ```
  The output should be similar to the following:
  ```
  Usage: terraform [global options] <subcommand> [args]
  The available commands for execution are listed below.
  The primary workflow commands are given first, followed by
  less common or more advanced commands.
  Main commands:
    init          Prepare your working directory for other commands
    validate      Check whether the configuration is valid
    plan          Show changes required by the current configuration
    apply         Create or update infrastructure
    destroy       Destroy previously-created infrastructure
  ```
2. Initialize Terraform by running the following command. This command prepares
  your workspace so Terraform can apply your configuration.
  ```
  terraform init
  ```
  The output should be similar to the following:
  ```
  Initializing the backend...
  Initializing provider plugins...
  - Finding latest version of hashicorp/google...
  - Installing hashicorp/google v5.35.0...
  - Installed hashicorp/google v5.35.0 (signed by HashiCorp)
  Terraform has created a lock file .terraform.lock.hcl to record the provider
  selections it made above. Include this file in your version control repository
  so that Terraform can guarantee to make the same selections by default when
  you run "terraform init" in the future.
  Terraform has been successfully initialized!
  ```
3. Validate the Terraform configuration by running the following command.
  This command takes the following actions:
  - Verifies that the syntax of `main.tf` is correct.
  - Shows a preview of the resources that will be created.
  ```
  terraform plan
  ```
  The output should be similar to the following:
  ```
  Plan: 1 to add, 0 to change, 0 to destroy.
  Note: You didn't use the -out option to save this plan, so Terraform can't
  guarantee to take exactly these actions if you run "terraform apply" now.
  ```
4. Apply the configuration to provision resources described in the `main.tf`
  file:
  ```
  terraform apply
  ```
  When prompted, enter `yes`.
  Terraform calls Google Cloud APIs to create the VM instance defined in
  the `main.tf` file.
  The output should be similar to the following:
  ```
  Apply complete! Resources: 1 added, 0 changed, 0 destroyed
  ```

## Connect to the VM instance

Connect to the VM instance you just created by running the following command:

```
gcloud compute ssh --zone=us-central1-a my-vm
```

## Clean up

To avoid incurring charges to your Google Cloud account for
          the resources used on this page, delete the Google Cloud project with the
          resources.

In Cloud Shell, run the following command to delete the Terraform
resources:

```
terraform destroy
```

When prompted, enter `yes`.

The output should be similar to the following:

```
Destroy complete! Resources: 1 destroyed.
```

## What's next

- Learn how to [deploy a basic Flask web server using Terraform](https://cloud.google.com/docs/terraform/deploy-flask-web-server).
- Learn how to [store Terraform state in a Cloud Storage bucket](https://cloud.google.com/docs/terraform/resource-management/store-state).

         Was this helpful?

---

# Get support for Terraform issuesStay organized with collectionsSave and categorize content based on your preferences.

# Get support for Terraform issuesStay organized with collectionsSave and categorize content based on your preferences.

The Terraform provider for Google Cloud is jointly developed by
HashiCorp and Google. The core Terraform CLI is developed by HashiCorp.

## Get a Google support package

Google Cloud offers different support packages to meet different needs, such as 24-7
coverage, phone support, and access to a technical support manager. For more
information, see [Cloud Customer Care](https://cloud.google.com/support).

Support for the Terraform provider for Google Cloud is offered under the
Premium support package, which lets you take advantage of the corresponding
[features and services](https://cloud.google.com/support#premium-support). The core Terraform CLI is
supported by HashiCorp.

If you're not sure whether you have a paid technical support package, check your
Cloud Support console:

[Go to Support](https://console.cloud.google.com/support)

## Open an issue on GitHub

On [GitHub](https://github.com/terraform-providers/terraform-provider-google/issues),
you can open the following types of issues:

- Provider-related issues
- Module and sample-related issues in the following GitHub repository
  collections:
  - [Terraform modules for Google Cloud](https://github.com/terraform-google-modules)
  - [Google Community](https://github.com/googlecloudplatform)

## Check the Hashicorp community portal and get troubleshooting advice

For questions about Terraform in general and common patterns, check the
[HashiCorp community portal](https://discuss.hashicorp.com/c/terraform-core).

For general troubleshooting advice, see Terraform’s
[debugging documentation](https://www.terraform.io/docs/internals/debugging.html).

For Google-specific questions, see [the Google section of the Hashicorp Discuss portal](https://discuss.hashicorp.com/c/terraform-providers/tf-google/32).

## Ask a question on Stack Overflow

Ask a question about Terraform for Google Cloud on
[Stack Overflow](http://stackoverflow.com/questions/tagged/terraform-provider-gcp).
Use the tag `terraform-provider-gcp` for questions about
Terraform for Google Cloud.

## Find troubleshooting tips forgcloud beta terraform vet

Learn how to [troubleshoot gcloud beta terraform vet](https://cloud.google.com/docs/terraform/policy_validation/troubleshooting).

## Discuss Terraform for Google Cloud

Visit the Google Cloud
[Slack community](https://googlecloud-community.slack.com/) to discuss
the Terraform Google Provider and other Google Cloud products. If you
haven't already joined,
[use this form to sign up](https://join.slack.com/t/googlecloud-community/shared_invite/zt-3icuwfdvq-eq_58LqmOoCNc16mpZcaNA).

For Terraform for Google Cloud, join the
[#terraform](https://googlecloud-community.slack.com/messages/C1VNJ4EG7/)
channel.

## File bugs or feature requests

From the [Terraform for Google Cloud documentation](https://cloud.google.com/docs/terraform),
click **Send feedback** near the top right of the page or at the bottom of the
page. This opens a feedback form.
