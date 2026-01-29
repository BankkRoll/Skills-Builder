# Spend and more

# Spend

> Learn about the updates to the spend-based committed use discounts program.

# Spend-based CUD program improvementsStay organized with collectionsSave and categorize content based on your preferences.

We are improving and expanding the [spend-based committed-use discounts
(CUD)](https://cloud.google.com/docs/cuds-spend-based)
program. A notification in the **Billing Overview** page shows the date
when we will begin the automatic migration from the legacy spend-based CUD model
using credits, to the new spend-based CUD model using discounts, however you can
[act now to opt in early](#how-to-opt-in).

## Key concepts

Your applicable discount rates for existing SKUs won't change as part of this
migration, and your current contractual rates are preserved. If your usage
behavior remains the same, your total costs won't increase.

- **How to verify**: You can
  [verify your specific discounts](https://cloud.google.com/docs/cuds-verify-discounts)
  and preview the new billing format using the Pricing user interface and the
  [BigQuery sample data export](https://cloud.google.com/docs/cuds-multiprice-datamodel#bq-sample-data-export).
- **Data model change**: Discounts are now represented by a new
  [consumption models](#consumption-model-intro)
  field in your billing data rather than a separate credit.
- **Action required**: If you export Cloud Billing data to
  BigQuery, you must update any internal systems (like FinOps
  dashboards) that depend on the data schema to ensure compatibility.

### Purchase commitments

To determine the correct amount of CUDs to purchase, the CUD Recommendations
tool remains the best method.

- **Process change**: The main change in the purchasing flow is that you now
  commit to the equivalent CUD discounted spend, which is your hourly cost
  after buying the commitment, rather than the previous model of committing to
  the on-demand spend amount.
- **System updates**: This new purchasing logic is reflected in the updated
  CUD purchasing user interface and the Marketplace Procurement API.

For more information, see
[Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly).

### List prices

This migration doesn't change the list price for SKU usage.

**Fee SKU change**: You will see new CUD fee SKUs priced at $1. This is a
structural change to the data model. When you use the CUD, an offsetting credit
(`FEE_UTILIZATION_OFFSET`) negates this fee.

For more information, see
[Changes to SKU usage list price compared to Fee SKU list price](#sku-price-changes).

### Expanded SKUs

The program is expanding to cover more products, which may decrease your costs
if you use have eligible spend for these SKUs, but aren't fully utilizing your
commitments.

- **New SKUs added**: This expansion applies to Compute flexible CUDs and
  includes:
  - [Compute-optimized H3 VMs](https://cloud.google.com/compute/docs/compute-optimized-machines#h3_series)
  - [Memory-optimized M1, M2, M3, and M4 VMs](https://cloud.google.com/compute/docs/memory-optimized-machines)
  - [Cloud Run](https://cloud.google.com/run) (request-based billing during billed
    instance time), including Cloud Run functions.
- **Unaffected CUDs**: The scope for other spend-based CUDs is unchanged. No
  resource-based CUDs (for example, specific machine types) are affected by
  this migration.

For more information, see
[New SKUs added](#added-skus).

### Changed savings program credit display

After migrating, you'll notice a significant change in how savings are
displayed in the FinOps dashboard and Cost reports page. If your "Savings
programs" credits appear lower, this is due to a change in presentation, not a
reduction in your actual savings.

- **Old model**: Showed a large gross credit that offset your on-demand costs
  (for example, -$10.00).
- **New model**: Directly shows your actual, net savings (for example,
  -$4.50), which is the difference between the on-demand price and your final,
  discounted cost.

Your final bill and true savings amount remain exactly the same; the new model
makes your net savings more transparent.

For more information, see
[Changes in displaying credits from savings programs](#credits-display-change).

## Changes summary

These changes provide the following benefits:

- **Simplified billing**: Google Cloud uses discounted prices to
  represent savings from spend-based CUDs, making it easier for you to
  calculate the total cost of your CUDs and savings. This moves away from the
  legacy concept of offering credits to offset costs.
- **Greater flexibility**: Expands the scope for some spend-based CUDs. As a
  result, a larger portion of your usage might be eligible for discounts.
  These changes don't increase your total costs.

The changes include:

- **Added consumption models**: A better way to understand and track your
  cloud spending, especially concerning promotional offers and discounts. For
  more information, see [consumption models](#consumption-model-intro).
- **Expanded product coverage for CUDs**. For more information, see [affected
  CUDs](#affected-cuds).
- **Simplified CUD fee SKUs**: New CUD fee SKUs replace existing CUD fee SKUs.
  The price for these new SKUs is $1.  For more information, see [Simplified
  CUD fee SKUs](#new-cud-fee-skus).
- **Billing user interface improvements**: The [Billing section](https://console.cloud.google.com/billing/overview)
  of the Google Cloud console changes to better enable accurate cost management
  and optimization experiences for CUDs. For more information, see [Billing
  user interface improvements](#billing-ui).
- **Updates to the CUD purchasing experience**: Your hourly commitment amount
  is now the discounted price instead of the on-demand price. For more
  information, see [CUD purchasing
  experience](https://cloud.google.com/docs/cuds-spend-based#steps_to_purchase).
- **Updated the Marketplace Procurement API**: The Marketplace Procurement API
  is updated to enable purchasing of CUDs in this new model. For more
  information, see [Updated the Marketplace Procurement
  API](#procurement-api-changes).
- **Expanded Billing data export**: The Billing export data columns change to
  reflect the new pricing metadata and monetization of spend-based CUDs. For
  more information, see [BigQuery sample data export](https://cloud.google.com/docs/cuds-multiprice-datamodel#bq-sample-data-export).
- **Easier tracking for consumption model prices**: A new metadata field,
  consumption model, represents the price of usage for a given SKU. Discounted
  prices at the appropriate consumption model represent the savings from
  spend-based CUDs. This model replaces the use of credits that offset
  your list price usage rates. For more information, see [Easier tracking for
  consumption model prices](#new-model-metadata).
- **New CUD metadata export** to BigQuery. For more
  information, see [CUD metadata export](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/cud-export).

## Opt in early starting July 15, 2025

Starting **July 15, 2025**, you can opt in early to these improvements by using
the [Billing
section](https://console.cloud.google.com/billing/overview)
 of the Google Cloud console. Doing so begins the account migration process.

For more details about the various timelines for this CUD migration, see
[Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline).

## Affected CUDs

The following spend-based CUDs are affected by this change.

- [AlloyDB for PostgreSQL](https://cloud.google.com/alloydb/cud)
- [Backup and DR (for Oracle)](https://cloud.google.com/backup-disaster-recovery/docs/configuration/cud)
- [BigQuery](https://cloud.google.com/bigquery/docs/bigquery-cud)
- [Bigtable](https://cloud.google.com/bigtable/docs/cuds)
- [Cloud Run](https://cloud.google.com/run/cud)
- [Cloud SQL](https://cloud.google.com/sql/cud)
- [Compute flexible CUDs](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview#spend_based)
- [Dataflow](https://cloud.google.com/dataflow/docs/cuds)
- [Firestore](https://cloud.google.com/firestore/docs/cuds)
- [GKE](https://cloud.google.com/kubernetes-engine/cud)
- [Managed Service for Apache Kafka](https://cloud.google.com/managed-service-for-apache-kafka/docs/cuds)
- [Memorystore](https://cloud.google.com/memorystore/docs/redis/cuds)
- [Spanner](https://cloud.google.com/spanner/docs/cuds)

## Unaffected CUDs

The following CUDs won't be affected by this change:

- Backup for GKE
- Backup and DR (for VMware Engine)
- All VMware Engine CUDs
- NetApp Volumes
- All resource-based CUDs

As new CUDs launch, check this section to understand their eligibility for these
changes.

## Action required

We recommend that you review the changes to determine if your usage scenario
requires you to take action. In addition, take the following steps to prepare:

- Explore these [resources to help you adopt these
  improvements](#migration-resources).
- If you [export Cloud Billing data to
  BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery)
  you must update any of your internal systems that depend on the data
  schema. For example, update any FinOps cost management reporting dashboards
  to ensure compatibility with the new schema before the mandatory change.
- See the [sample data export](https://cloud.google.com/docs/cuds-multiprice-datamodel#bq-sample-data-export)
  to preview how your existing data appears under the new data export model.
- If you are a reseller or have a billing account hierarchy, see
  [Resellers](https://cloud.google.com/docs/cuds-new-model-timeline).

## Resources to help adopt these improvements

To help you get ready for the changes, we provide these resources:

- [BigQuery sample data export](https://cloud.google.com/docs/cuds-multiprice-datamodel#bq-sample-data-export): A
  sample dataset that demonstrates how [opting in](https://cloud.google.com/billing/docs/resources/multiprice-cuds#how-to-opt-in)
  changes the appearance of your spend-based CUD data exports in
  BigQuery.
- [CUD KPI example queries](https://cloud.google.com/docs/cuds-multiprice-datamodel#cud-kpis): Example
  queries to use with the BigQuery sample data export to calculate
  important CUD key performance indicators (KPI).
- [List of new SKUs added to CUDs](#added-skus): Details about the new SKUs
  added to the scope of CUDs.
- [List of new CUD fields](https://cloud.google.com/docs/cuds-multiprice-datamodel#cud-product-info):
  Descriptions of new CUDs fields, for example new CUD Fee SKUs IDs, offer
  names, and consumption model IDs.

## Consumption models

The new CUD program introduces the concept of consumption models. In
Cloud Billing, a consumption model represents the price you pay for a
certain amount of SKU usage within a certain context. A SKU can have several
consumption models, but only one applies to any given amount of usage at a
particular time. Each SKU has at least one consumption model, whose description
is `Default`.

Consumption models often represent various kinds of discounted SKU usage,
such as committed use discounts (CUDs). For example, if a one year Flex CUD
covers a particular VM usage, then the consumption model that applies to that
SKU usage has the description `Compute Flexible CUD - 1 Year`.

For spend-based CUDs, consumption models replace the legacy system of using
credits to offset usage costs calculated at list price. The new model also
changes how commitments are purchased:

| Previous Model | Current Model |
| --- | --- |
| Commitments were purchased based onequivalent on-demand
      spend. | Commitments are now purchased based onequivalent CUD
      discounted spend. |
| This represented the list price of the usage your commitment would
      cover. | This represents the actual discounted cost of the usage you commit
      to pay each hour. |

To support consumption models, several fields have been added or updated in
the Cloud Billing data model. For more information, see
[New consumption model metadata](#new-model-metadata).

### New consumption model metadata

For each SKU, a new metadata field, `Consumption Model`, represents the price of
usage for that SKU. This price applies when the system monetizes usage for that
SKU under this particular consumption model. For example, if a 1-Year Flex CUD
covers VM usage, then the consumption model of the usage has a value of `1 Year
Flex CUD`.

For more information, see
[Offers and consumption model IDs](https://cloud.google.com/docs/cuds-multiprice-datamodel#offer-consumption-ids).

## Changes in displaying credits from savings programs

Your final bill and your true savings have not changed, but their presentation
is different in the new model. We've updated how we display credits from
savings programs, such as Committed Use Discounts (CUDs), in your cost
reports. The goal of this change is to provide a more direct and transparent
view of your actual savings.

- **Before migration (old model):** The **Savings programs** column showed
  the *credit* applied to your on-demand costs. This credit was one part of a
  multi-step calculation, and it did not represent your final savings.
- **After migration (new model):** The **Savings programs** column shows
  your **actual savings**. This is the final, bottom-line amount you saved
  compared to what you would have paid at on-demand prices.
  - This column is calculated as follows: Cost at on-demand rates -
    costs at CUD consumption rate + CUD Fees (if applicable).
  - A negative number indicates savings, while a positive number
    indicates the CUDs aren't generating savings (a loss).

### Old model: A credit-based calculation

In the old model, your savings were calculated in multiple steps. We showed the
on-demand price for your usage, charged you a separate commitment fee, and then
applied a credit to offset the on-demand cost. To find your true savings, you had
to perform a manual calculation.

Let us use a consistent example: a CUD that costs **$5.50/hr** to cover
**$10/hr** of on-demand usage.

#### Example A: 100% Utilization (old model)

In this example, you fully used the resources covered by your commitment before
migration (old CUD model).

1. **On-Demand Cost:** Your usage would have cost **$10.00**.
2. **CUD Commitment Fee:** You're charged the commitment fee of **$5.50**.
3. **CUD Credit:** A credit of **$10.00** is applied to cancel out the
  on-demand cost.
4. **Cost Calculation:** $10.00 (On-Demand Cost) + $5.50 (CUD Fee) - $10.00
  (Credit) = **$5.50**.
5. **Savings Programs:** It displayed the gross credit, which was
  **-$10.00**.
6. **How to Find Savings:** You had to manually compare the on-demand cost
  to your final cost: $10.00 - $5.50 = **$4.50 in savings**.

### New model: A direct savings calculation

In the new model, we apply your discounted price directly to any usage covered
by a commitment. The **Savings Programs** column now directly shows you the
difference between the on-demand price and what you actually paid.
Using the same example: a CUD that costs **$5.50/hr** to cover **$10/hr**
of on-demand usage.

#### Example A: 100% Utilization (New model)

In this example, you fully used the resources covered by your commitment after
migration (new CUD model).

1. **Discounted Cost:** Your cost for the resources is directly billed at
  the discounted CUD rate of **$5.50**. There are no separate fees or credits
  on the bill.
2. **Cost Calculation:** Your final cost is just **$5.50**.
3. **Savings Programs:** It now shows your actual, net savings.
  - **Calculation:** On-Demand Cost - Final Cost
  - $10.00 - $5.50 = $4.50
  - The column displays **-$4.50**.

### New savings presentation

The following table shows an example of the new way that savings are presented.
Although the number in the **Savings Program** column has changed from -$10 to
-$4.50 in this example, your final cost of $5.5/hr and your true savings of
$4.5/hr haven't been affected.

| Scenario (100% utilization) | SavingsPrograms column |
| --- | --- |
| Old model | -$10.00 (Gross credit) |
| New model | -$4.50 (Net savings) |

## Unchanged costs and discounts

Your applicable discount rate for SKUs already eligible for spend-based CUDs
remains the same. Your total costs won't increase if your usage behavior remains
the same. However, your bill might decrease if you aren't fully utilizing your
commitments but are using any of the newly added SKUs. Your contractual
discounts are honored for the duration of your contract. The following aren't
affected by this change:

- [Certain spend-based CUDs](#unaffected-cuds)
- Resource-based CUDs

In addition, these changes don't affect previous bills. This change in how
spend-based CUDs are billed only affects *future bills*.

## CUD savings report changes

The change in the billing model doesn't increase your total costs. Your
contractual discounts are honored for the duration of your contract. Your total
costs won't increase. However, you'll notice changes in the way that
Google Cloud represents your CUD savings. You'll also notice changes in the data
structure in the BigQuery export and the presentation of
information in the [Billing
section](https://console.cloud.google.com/billing/overview)
of the Google Cloud console. The goal of the change is to simplify billing, make
CUDs easier to understand, and expand their scope over time.

Additionally, the cost of your commitments won't change. However, you'll
notice that your total commitment amount changes from *commitment amount in
on-demand spend* to *commitment amount in CUD discounted spend* and equals your
hourly commitment costs at the time of conversion.

## Commitment fee SKUs show zero net cost

In the new model, new CUD fee SKUs are priced at $1. However, the billing data
export includes a credit, specifically the `FEE_UTILIZATION_OFFSET` credit,
which is applied to negate this commitment fee cost. This means that if you're
fully utilizing a CUD, the fee sku will have zero net cost.

![View of the fully utilized cud](https://cloud.google.com/static/docs/images/cuds-fully-utilized-view.png)

In the screenshot, the account fully utilized its Flexible CUDs on an hourly
basis for the period of September 1st through September 29th. The associated CUD
fees were completely offset by the `FEE_UTILIZATION_OFFSET` credits, resulting
in a net cost of $0. However, on September 30th, a minor utilization of the
3-year CUD led to an underutilization of their commitments, incurring a charge
of $2.56.

## Changes to SKU usage list price compared to Fee SKU list price

The list price of the SKU usage hasn't changed. However, the commitment
purchasing flow has changed. Instead of basing the commitment on equivalent
on-demand spend, it's now based on equivalent CUD discounted spend, which is
the actual discounted cost that you commit to pay each hour.

The list prices of the Fee SKUs have changed to be $1 because the CUD model has
changed from using credits to using discounts. This means that while total costs
are constant, the data model changes. The net costs are moving from CUD Fee SKUs
to SKUs that use the CUDs at the consumption model prices. To get apples to
apples comparison between the models, make sure you include credits in the total
calculation.

For example: In the old CUD model, you pay $0.7 for a fee SKU that gives $1 in
credits at on-demand rates and you get the discount as a result. In the new CUD
model, you pay at a 1:1 ratio, for example you pay $0.7 to get $0.7 (the new fee
skus are all at $1). The costs are now moved to consumption models, which are
discounted rates (down to $0.7). To perform these calculations, you must also
account for credits.

In the new CUD model, the Cost Management user interface reflects the
spend-based CUD savings calculated using the following formula:

`Cost at on-demand rates - costs at CUD consumption rate + CUD Fees` (if
applicable).

![View of the underutilized cud](https://cloud.google.com/static/docs/images/cuds-underutilized-view.png)

The screenshot shows a Cloud Billing account with spend-based CUDs that are
significantly underutilized, resulting in a charge of $29,114.45, which is the
cost of the unused commitment. When the CUD is utilized, this bar will be
reflected as savings.

## New SKUs added

After you opt in to the new model, SKUs for the following products are added to
the scope of your Compute flexible CUDs, for example:

- [Compute-optimized H3 VMs](https://cloud.google.com/compute/docs/compute-optimized-machines#h3_series)
- [Memory-optimized M1, M2, M3, and M4 VMs](https://cloud.google.com/compute/docs/memory-optimized-machines)
- [Cloud Run](https://cloud.google.com/run) (request-based billing during billed instance time), including Cloud Run functions.

To see the full list of Compute flexible CUDs SKUs covered in the new model,
see
[SKU Groups - Compute Flexible CUD Eligible](https://cloud.google.com/skus/sku-groups/compute-flexible-cud-eligible-skus).
To programmatically get a list of all SKUs belonging to a SKU group, see
[Method: skuGroups.skus.list](https://cloud.google.com/billing/docs/reference/pricing-api/rest/v1beta/skuGroups.skus/list).

## New CUD fee SKUs

The existing CUD fee SKUs are replaced with new SKUs. These SKUs are priced at
$1/hr, unlike the existing SKUs, which are priced at a lower rate to indicate the
CUD benefit. The CUD benefit is now reflected using the Consumption Model prices
described in [New consumption model metadata](#new-model-metadata). This doesn't
affect your costs.

New Offer IDs and Consumption model IDs are shared for all [in-scope
CUDs](https://cloud.google.com/billing/docs/resources/multiprice-cuds#affected-cuds).
You can use the following details to help you map your queries and dashboards.

For more information, see the list of [new CUD fee
SKUs](https://cloud.google.com/docs/cuds-migration#new-sku-ids).

## Billing user interface improvements

To see the list of improvements to the Cloud Billing user interface as part
of the new CUDs program, see [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements).

## CUD purchase flow changes

The user interface that you use to purchase CUDs changes. This change doesn't
impact CUDs that you already purchased. The system converts existing CUDs to the
new model seamlessly. For more information, see [CUD purchasing
experience](https://cloud.google.com/docs/cuds-spend-based#steps_to_purchase).

## Cloud Commerce Consumer Procurement API changes

The [Cloud Commerce Consumer Procurement
API](https://cloud.google.com/marketplace/docs/commitment-api-purchasing)
enables programmatic purchases of spend-based CUDs with Marketplace offers. This
API changes:

- The offer name for existing spend-based CUDs changes.
- The commitment amount for CUDs you purchase changes. See [CUD
  purchase flow changes](#purchase-flow-changes)
  for more details.

You must update any code that automates purchases of spend-based CUDs. Use the
updated offer name and commitment amounts after you transition to the new
billing model.

## Next steps

- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)

## Related topics

- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline)
- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)
- [Sample queries for the new CUDs data model](https://cloud.google.com/docs/cuds-example-queries)
- [Migrated CUD SKUs, offers, and consumption model IDs](https://cloud.google.com/docs/cuds-migration)
- [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements)

   Was this helpful?

---

# Timelines for new CUD model migrationStay organized with collectionsSave and categorize content based on your preferences.

> Learn about the dates related to the new CUDs data model.

# Timelines for new CUD model migrationStay organized with collectionsSave and categorize content based on your preferences.

## Effective dates

The changes take effect on the following dates, depending on which scenario
applies to you.

Customers who opt in early will be unable to purchase new spend-based CUDs for
a few hours during their account migration. Google Cloud displays a
warning about this outage in the
[Billing section](https://console.cloud.google.com/billing/overview)
of the Google Cloud console.

For customers who don't opt in early, the same outage occurs when they are
automatically migrated to the new model. A notification in the **Billing
Overview** page shows the date when we will begin the automatic migration
from the legacy spend-based CUD model using credits, to the new spend-based CUD
model using discounts.

### New customers

If you create a Billing Account on or after **July 15, 2025**, the new billing
model applies to you for spend-based CUDs in the [affected CUDs
list](https://cloud.google.com/docs/cuds-multiprice#affected-cuds).

### Customers with active spend-based CUDs

For Billing accounts with any active spend-based CUDs [in this
list](https://cloud.google.com/docs/cuds-multiprice#affected-cuds) on or after **July 15, 2024**, a
notification in the **Billing Overview** page shows the date when we
will begin the automatic migration from the legacy spend-based CUD model using
credits, to the new spend-based CUD model using discounts. You can opt in
earlier, starting
**July 15, 2025**. In that case, the new model applies when you click opt-in.
Learn more about [how to opt
in](https://cloud.google.com/docs/cuds-multiprice#how-to-opt-in).

### Customers without active spend-based CUDs

For Billing Accounts with no active spend-based CUDs [in this
list](https://cloud.google.com/docs/cuds-multiprice#affected-cuds) since **July 15, 2024**, the new
model applies on **July 15, 2025**, at midnight US and Canadian Pacific Time
(UTC-8).

### Customers with a two-tier billing account hierarchy

- **Customers with billing account hierarchies that don't have active
  spend-based CUDs in theaffected CUDs
  liston or after July 15, 2024**: The
  new model applies on July 15, 2025, at 12 AM US and Canadian Pacific Time
  (UTC-8) to all billing accounts in the hierarchy.
- **Customers with billing account hierarchies that have active spend-based
  CUDs in theaffected CUDs listsince
  July 15, 2024**: A notification in the **Billing Overview** page shows the
  date when we will begin the automatic migration from the legacy
  spend-based CUD model using credits, to the new spend-based CUD model using
  discounts. You can opt in your entire hierarchy (at the parent billing
  account) earlier, starting July 15, 2025. In that case, the new model
  applies when you click opt-in to all billing accounts in the hierarchy.
  Learn more about [how to opt in](https://cloud.google.com/docs/cuds-multiprice#how-to-opt-in).

### Resellers

- **Resellers that don't have active spend-based CUDs on the parent or
  sub-accounts in theaffected CUDs
  liston or after July
  15, 2024**: The new model applies on July 15, 2025, at 12 AM US and Canadian
  Pacific Time (UTC-8). This applies to all billing accounts in the hierarchy.
- **Resellers with active spend-based CUDs on the parent or sub-accounts in
  theaffected CUDs listsince July 15,
  2024**: A notification in the **Billing Overview** page shows the
  date when we will begin the automatic migration from the legacy spend-based CUD
  model using credits, to the new spend-based CUD model using
  discounts.Resellers can opt in their parent billing account earlier,
  starting July 15, 2025. In that case, the new model applies when you click
  opt-in to all billing accounts in the hierarchy that don't have spend-based
  CUDs in the [affected CUDs list](https://cloud.google.com/docs/cuds-multiprice#affected-cuds) since
  July 15, 2024. For the remaining billing accounts, billing account
  administrators can then opt in their billing accounts. Learn more about [how
  to opt in](https://cloud.google.com/docs/cuds-multiprice#how-to-opt-in).

## Determine when other spend-based CUDs change

Timelines for other spend-based CUDs to move to this new model are unavailable.

## Related topics

- [Spend-based CUD program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)
- [Sample queries for the new CUDs data model](https://cloud.google.com/docs/cuds-example-queries)
- [Migrated CUD SKUs, offers, and consumption model IDs](https://cloud.google.com/docs/cuds-migration)
- [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements)

   Was this helpful?
