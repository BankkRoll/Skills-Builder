# Get recommendations for committed use discounts (CUD)Stay organized with collectionsSave and categorize content based on your preferences. and more

# Get recommendations for committed use discounts (CUD)Stay organized with collectionsSave and categorize content based on your preferences.

> Overview of Google Cloud committed use discount recommender.

# Get recommendations for committed use discounts (CUD)Stay organized with collectionsSave and categorize content based on your preferences.

[Committed use discount (CUD)](https://cloud.google.com/docs/cuds)
recommendations help you optimize the resource costs of the projects in your
Cloud Billing account. CUD recommendations are automatically generated using
a formula that analyzes historical and recent usage metrics gathered by
Cloud Billing, and includes usage covered by existing commitments.
You can apply these recommendations to purchase additional commitments and
further optimize your Google Cloud costs.

Recommendations are available for a [subset of resource-based commitments](https://cloud.google.com/docs/cuds-recommender#supported-resource-types-recommendation)
and a [subset of spend-based commitments](https://cloud.google.com/docs/cuds-recommender#supported-spend-types-recommendation)
for [eligible products](https://cloud.google.com/docs/cuds#spend_based_commitments)
, including [Compute flexible commitments](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview#spend_based).

Refer to the guides on this page to learn about the following tasks:

- [Understand commitment recommendations](https://cloud.google.com/docs/cuds-recommender#understanding-recommendations)
- [Set permissions to access recommendations](https://cloud.google.com/docs/cuds-recommender#permissions)
- [View recommendations](https://cloud.google.com/docs/cuds-recommender#viewing-recommendations)
- [Interpret the recommendation summary](https://cloud.google.com/docs/cuds-recommender#understanding-summary-cards)
- [Simulate scenarios for spend-based CUDs savings](https://cloud.google.com/docs/cuds-recommender#simulate-scenarios)
- [Apply recommendations to purchase additional commitments](https://cloud.google.com/docs/cuds-recommender#purchasing-recommendations)
- [Dismiss recommendations](https://cloud.google.com/docs/cuds-recommender#dismissing-recommendations)
- [Configure recommendation settings](https://cloud.google.com/docs/cuds-recommender#configure-recommendation)

For more information about the Recommender service, see the
[Recommender overview](https://cloud.google.com/recommender/docs/overview).

## Understand commitment recommendations

Committed use discount recommendations let you identify spending and usage
patterns in your Google Cloud projects. Your spending patterns generate
recommendations for
[spend-based commitments](https://cloud.google.com/docs/cuds-spend-based),
including
[Compute flexible commitments](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview#spend_based),
and your usage patterns on Compute Engine generate recommendations for
[resource-based commitments](https://cloud.google.com/docs/cuds#resource_based_commitments).
The recommendations for resource-based commitments also account for your use of
[custom machine types on Compute Engine](https://cloud.google.com/compute/docs/instances/creating-instance-with-custom-machine-type).
Purchasing the recommended commitments helps you optimize your
Google Cloud costs.

## Permissions required to view and modify recommendations

Depending on your needs, ask your administrator to assign the following
predefined IAM roles:

- If your Cloud Billing account has
  [discount sharing](https://cloud.google.com/compute/docs/committed-use-discounts/share-resource-cuds-across-projects#turning_on_committed_use_discount_sharing)
  enabled for resource-based commitments, you need one of these roles on the
  Cloud Billing account:
  - To view recommendations only, assign the **Billing Account Viewer**
    (`roles/billing.viewer`) role.
  - To view and modify recommendations, assign the
    **Billing Account Administrator** (`roles/billing.admin`) role.
  [Learn how to assign these roles to manage access to a Cloud Billing account](https://cloud.google.com/billing/docs/how-to/grant-access-to-billing).
- If your Cloud Billing account does *not* have
  [discount sharing](https://cloud.google.com/compute/docs/committed-use-discounts/share-resource-cuds-across-projects#turning_on_committed_use_discount_sharing)
  for resource-based commitments, you need one of these roles on each project
  attached to your Cloud Billing account that has purchased
  committed use discounts:
  - To view recommendations only, assign the **Viewer** (`roles/viewer`) role
    on the projects.
  - To view and modify recommendations, assign the **Owner** (`roles/owner`)
    or **Editor** (`roles/editor`) role on the projects.
  [Learn how to assign these roles to manage access to projects](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

If you are using custom roles, update the custom role to include the following
individual permissions:

### Permissions to simulate scenarios for CUD savings

- To simulate scenarios based on list prices, you need
  `billing.cudrecommendations.generateDefaultPriceSavingRecommendation`
- If you have a custom pricing contract, you need
  `billing.cudrecommendations.generateCustomPriceSavingRecommendation` to
  simulate scenarios based on your custom prices.

### Permissions to view recommendations

To view *spend-based* CUD recommendations:

- `recommender.spendBasedCommitmentRecommendations.get`
- `recommender.spendBasedCommitmentRecommendations.list`
- `recommender.spendBasedCommitmentInsights.get`
- `recommender.spendBasedCommitmentInsights.list`
- `recommender.spendBasedCommitmentRecommenderConfig.get`

To view *resource-based* CUD recommendations:

- `recommender.usageCommitmentRecommendations.get`
- `recommender.commitmentUtilizationInsights.get`
- `recommender.usageCommitmentRecommendations.list`
- `recommender.commitmentUtilizationInsights.list`

### Permissions to modify recommendations

To modify *spend-based* CUD recommendations:

- `recommender.spendBasedCommitmentRecommendations.update`
- `recommender.spendBasedCommitmentInsights.update`
- `recommender.spendBasedCommitmentRecommenderConfig.update`

To modify *resource-based* CUD recommendations:

- `recommender.usageCommitmentRecommendations.update`
- `recommender.commitmentUtilizationInsights.update`

## View recommendations

There are different ways to view your committed use discount recommendations.

To view commitment recommendations that apply to all the usage for your
Cloud Billing account, use the [FinOps hub](https://cloud.google.com/billing/docs/how-to/finops-hub).

To view commitment recommendations for a specific project that
you own, use the **Cost recommendations** page in the
[Recommendations Hub](https://cloud.google.com/recommender/docs/recommendation-hub/identify-configuration-problems)
in the Google Cloud console.

To view the committed use discount recommendations for your
Cloud Billing account, do one of the following:

| View all recommendations for a Cloud Billing account | View recommendations scoped to a specific project |
| --- | --- |
| If you have Cloud Billing account permissions, you can get
        CUD recommendations for all the usage billed to the
        Cloud Billing account, using theFinOps hub.In the Google Cloud console, open the FinOps hub.Go to FinOps hubAt the prompt, choose the Cloud Billing account for which you
          want to view CUD recommendations.If there are CUD recommendations
          available for your Cloud Billing account, they are in theTop recommendationssection.To view detailed information about a recommendation, click the
        recommendation. | If you have permissions for a specific project, get resource-based
        CUD recommendations for the project in theCost recommendationspage in the Active Assist.In the Google Cloud console, open theCost recommendationspage in the Active Assist.Go to Cost recommendationsSelect the project for which you want to view CUD recommendations.To view detailed information about a recommendation, click the
        recommendation. |

## Interpret the recommendation summary

The following is an example of a recommendation summary for a spend-based
CUD recommendation, with the chart that shows how the recommendation is
calculated. At a high level, the recommendation is based on your resource
utilization, how much of your usage you want to cover with CUDs, and your
existing CUDs. The chart shows you the level of utilization at which you'll
save costs by signing up for a commitment.

![Example of a spend-based committed use discount recommendation summary.](https://cloud.google.com/static/billing/docs/images/cud-recommendations-summary.png)

### Estimate your optimal usage

#### Usage insights

For a brief explanation of how your spend-based recommendation was calculated,
see the **Usage insights** section of the recommendation. Usage insights
explains the break-even point for your commitment purchase. For example, your
usage insight will look similar to this, depending on the details of your
CUD recommendation:

"With the recommended CUD coverage of $90.00/hr, savings will remain positive
even if eligible usage drops by 54%."

#### Example of how to calculate your optimal usage

To estimate the resource utilization at which you'll break even on your costs,
subtract the CUD discount percentage from 100. For example, if you get a
recommendation for a 1-year Cloud SQL CUD with a discount of 25%, the
resource utilization at which you'll break-even is `100% - 25% = 75%`.

To understand the estimate, consider Cloud SQL usage of $100 at list
price. If your Cloud SQL instances run at 100% uptime, and you sign up
for a 1-year spend-based CUD at a 25% discount, you'll pay `$100 - (25% of $100)
= $75` for your usage.

If the uptime for your Cloud SQL instances reduces to 80%, your list
price is $80, but with a commitment, you'd pay $75 for your usage, which still
gives you a `($80 - $75) / $80 = 0.0625` or a `6.25%` discount on the list price.

Similarly, at 75% uptime, your costs are the same as if you were paying the list
price, and at less than 75% uptime, you no longer save money by signing up for a
commitment.

For a brief explanation of how your spend-based recommendation was calculated,
see the **Usage insights** section of the recommendation.

## Simulate scenarios for CUDs savings

In the FinOps hub, you can use a *spend-based* or *resource-based* CUD
recommendation as a starting point to simulate various usage scenarios, and
customize the recommendation to purchase a commitment that maximizes your savings.

[Go to FinOps hub](https://console.cloud.google.com/billing/optimize)

### Create a CUD scenario model

1. To start customizing a recommendation in the FinOps hub, click
  the **recommendation** you want to model.
2. On the recommendation's details page, click **Create a scenario**.
3. In the scenario modeling tool, use the options that best reflect your usage.
  Some of the ways you can customize the recommendation are as follows:
  - **Recommendation based on usage history** section: By default, the
    recommendation is based on the last 30 days of usage. To analyze your
    usage over a longer time, change the number of days of history to
    consider.
    To exclude dates where you might have had atypical usage, such as a
    period where you had unusually high demand, enable **Ignore usage
    history from specific days**, and specify a time range.
    The recommendation is recalculated based on the number of days that you
    select and the dates that you exclude.
  - **Eligible usage covered** section: You can model the amount of usage
    covered by a CUD, depending on the CUD type:
    - For spend-based CUDs, you can set a percentage of spend per hour.
    - For resource-based CUDs, you can set a number of resource units
      used.
    To help you model your real-world usage more accurately, this section
    includes a message that shows your actual stable usage for the model's
    date range.
  - **CUD term** section: You can select a 1-year or 3-year term for the CUD
    scenario model. The recommendation is recalculated if you change the
    selected term.

For example, the following screenshot shows a CUD scenario model recommendation
for the purchase of a 3-year Compute flexible commitment, based on the
previous 30 days of usage.

![Example of a committed use discounts scenario.](https://cloud.google.com/static/billing/docs/images/cud-scenario-model.png)

#### Usage insights in the scenario model

In the *CUD scenario model*, the **Usage insights** section provides a brief
explanation of how your spend-based recommendation was calculated. Usage
insights for the scenario include your historical spending patterns for the
recommended amount, and explains the break-even point for your commitment
purchase. For example, your usage insights will look similar to this, depending
on the details of your CUD scenario model:

- "With the CUD scenario model coverage of $0.07/hr, savings will remain
  positive even if eligible usage drops by 47%."

### Share the CUD scenario model

To share the scenario's configuration with others, click
**Copy to clipboard**
to copy a link that you can share. When your recipients open the link, they see
the scenario with the parameters that you chose, and with updated information
about additional usage that occurs before they open the link.

## Apply recommendations to purchase additional commitments

After you've reviewed the recommendation and selected the options that meet
your needs, you can start the purchase process.

### Review and purchase resource-based recommendations

While
[viewing your commitment recommendations](#viewing-recommendations),
open the recommendation's details page, and follow these steps:

1. Click **Review and purchase** at the bottom of the page.
  - For **spend-based commitment** recommendations, review the
    pre-populated fields in the **Purchase a committed use discount**
    form for accuracy.
    If your Cloud Billing account is billed in non-USD currency,
    your cost and savings estimates are displayed in both USD and your
    local currency.
    [Learn more about spend-based commitments, including Compute flexible commitments](https://cloud.google.com/docs/cuds-spend-based)
  - For **resource-based commitment** recommendations, you are redirected
    to the Compute Engine section of the Google Cloud console, where you can
    complete your purchase using the **Purchase a committed use discount**
    form.
    You might be prompted to select a project. This is the project where
    the commitments are purchased. Ensure that the Compute Engine API is
    enabled in the selected project, and that you have sufficient
    permissions on the project to purchase resource-based commitments.
    The fields in the purchase form are pre-populated based on the
    recommendation. Review the fields for accuracy, and update any values
    as needed.
    [Learn more about resource-based commitments for Compute Engine](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts)
2. To complete the purchase process, after reviewing the form, click
  **Purchase**.

## Dismiss recommendations

To no longer see a particular recommendation, you can **dismiss** it. This
prevents all users from seeing the recommendation in Cloud Billing
FinOps hub or Active Assist pages.

To dismiss recommendations for your Cloud Billing account, follow
these steps:

1. In the Google Cloud console, open the **FinOps hub** for
  your Cloud Billing account.
  [Go to FinOps hub](https://console.cloud.google.com/billing/optimize)
2. At the bottom of the **Potential savings/month** section, click
  **View all recommendations**.
3. In the list of recommendations, click
  **Actions**, then select
  **Dismiss**.

## Configure your default CUD recommendation settings

To customize the CUD recommendations that you get,
configure your recommendation settings using the following steps. Your
configuration settings are applied within one business day.

1. Go to the
  [Committed use discounts (CUDs)](https://console.cloud.google.com/billing/reports/commitments)
  page in the Billing section of the Google Cloud console.
2. Select  **Configure recommendations**
3. Enter your preferred coverage threshold as a percentage.
4. Choose your preferred commitment term duration(s).
5. View your recommendations by visiting the
  [Recommendations page](https://console.cloud.google.com/home/recommendations).

## Resource-based CUDs supported by recommendations

Resource-based CUD recommendations are available only for vCPUs and Memory, for
the following machine types and families:

- [Accelerator-optimized A2 series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#a2_vms)
- [Accelerator-optimized A3 Mega series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#a3-mega-vms)
- [Accelerator-optimized A3 series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#a3-high-vms)
- [Accelerator-optimized A3 Ultra series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#a3-ultra-vms)
- [Compute-optimized C2 series](https://cloud.google.com/compute/docs/compute-optimized-machines)
- [Compute-optimized C2D series](https://cloud.google.com/compute/docs/compute-optimized-machines#c2d_series)
- [Compute-optimized H3 series](https://cloud.google.com/compute/docs/compute-optimized-machines#h3_series)
- [Compute-optimized H4D series](https://cloud.google.com/compute/docs/compute-optimized-machines#h4d_series)
- [General-purpose C3 series](https://cloud.google.com/compute/docs/general-purpose-machines#c3_series)
- [General-purpose C3D series](https://cloud.google.com/compute/docs/general-purpose-machines#c3d_series)
- [General-purpose C4 series](https://cloud.google.com/compute/docs/general-purpose-machines#c4_series)
- [General-purpose C4A series](https://cloud.google.com/compute/docs/general-purpose-machines#c4a_series)
- [General-purpose C4D series](https://cloud.google.com/compute/docs/general-purpose-machines#c4d_series)
- [General-purpose E2 series](https://cloud.google.com/compute/docs/general-purpose-machines#e2_machine_types)
- [General-purpose N1 series](https://cloud.google.com/compute/docs/general-purpose-machines#n1_machines)
- [General-purpose N2 series](https://cloud.google.com/compute/docs/general-purpose-machines#n2_series)
- [General-purpose N2D series](https://cloud.google.com/compute/docs/general-purpose-machines#n2d_machines)
- [General-purpose N4 series](https://cloud.google.com/compute/docs/general-purpose-machines#n4_series)
- [General-purpose N4D series](https://cloud.google.com/compute/docs/general-purpose-machines#n4d_series)
- [General-purpose Tau T2D series](https://cloud.google.com/compute/docs/general-purpose-machines#t2d_machines)
- [Graphics-optimized G2 series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#g2-vms)
- [Graphics-optimized G4 series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#g4-series)
- [Memory-optimized M1 series](https://cloud.google.com/compute/docs/memory-optimized-machines#m1_series)
- [Memory-optimized M2 series](https://cloud.google.com/compute/docs/memory-optimized-machines#m2_series)
- [Memory-optimized M3 series](https://cloud.google.com/compute/docs/memory-optimized-machines#m3_series)
- [Memory-optimized M4 series](https://cloud.google.com/compute/docs/memory-optimized-machines#m4_series)
- [Memory-optimized X4 series](https://cloud.google.com/compute/docs/memory-optimized-machines#x4_series)
- [Storage-optimized Z3 series](https://cloud.google.com/compute/docs/storage-optimized-machines#z3_series)

For more information, see [Resource-based commitments](https://cloud.google.com/docs/cuds#resource_based_commitments).

## Spend-based CUDs supported by recommendations

Spend-based CUD recommendations are available only for the following products:

- AlloyDB for PostgreSQL
- Backup and DR Service
- Backup for GKE
- Dataflow Streaming CUD Subscription
- Memorystore
- Spanner
- Cloud SQL
- Compute flexible CUDs
- Google Cloud VMware Engine
- Google Cloud NetApp Volumes

For more information, see [Spend-based commitments](https://cloud.google.com/docs/cuds#spend_based_commitments).

## Related topics

- [Learn more about committed use discounts](https://cloud.google.com/docs/cuds)
- [Analyze the effectiveness of your committed use discounts](https://cloud.google.com/billing/docs/how-to/cud-analysis)
- [View the credits you are receiving in reports](https://cloud.google.com/billing/docs/how-to/reports#credits)
- [Understand your savings with cost breakdown reports](https://cloud.google.com/billing/docs/how-to/cost-breakdown)

   Was this helpful?

---

# Spend

> Overview of Google Cloud spend-based committed use discounts.

# Spend-based committed use discountsStay organized with collectionsSave and categorize content based on your preferences.

Spend-based committed use discounts (CUDs) provide a discount in exchange for
your commitment to spend a minimum amount for a product or service. The discount
applies to the set of [eligible resources](https://cloud.google.com/docs/cuds#spend_based_commitments)
for the service.

[Learn about the products covered by spend-based commitments](https://cloud.google.com/docs/cuds#spend_based_commitments).

You must purchase separate spend-based commitments for each Google Cloud
service that CUDs are available for. The CUDs apply to
eligible usage in any projects that the Cloud Billing account pays for.

## Purchase spend-based commitments

You can purchase spend-based CUDs in the Google Cloud console.
The discounts are applied to eligible usage in the applicable
regions.

After you purchase a commitment, the commitment goes into effect based on which
part of the hour it was purchased. Commitments purchased earlier than 10
minutes before the end of the hour start at the beginning of the next hour.
Otherwise, they start at the beginning of the hour after next. These times
assume your local time zone. For example:

If you buy a commitment before the last 10 minutes of any hour (at :49 or
earlier), your discount starts at the beginning of the next hour. If you buy a
commitment within the last 10 minutes of any hour (at :50 or later), your
discount will skip an hour and start at the beginning of the hour after next.

Using this example, a commitment purchased at 4:51 PM starts at 6:00 PM, and a
commitment purchased at 4:49 PM starts at 5:00 PM.

### Permissions required

To purchase or manage spend-based CUDs for your
Cloud Billing account, you must be a [Billing Account
Administrator](https://cloud.google.com/billing/docs/how-to/billing-access).

### Steps to purchase

To purchase spend-based committed use discounts, complete the following steps:

1. Sign in to the Google Cloud console.
  [Sign in to Google Cloud console](https://console.cloud.google.com/)
2. Open the Google Cloud console **Navigation menu** ,
  and then select **Billing**.
  If you have more than one Cloud Billing account, do one of the
  following:
  - To manage Cloud Billing for the current project, select
    **Go to linked billing account**.
  - To locate a different Cloud Billing account, select
    **Manage billing accounts** and then choose the account that you want to
    manage.
3. You can purchase commitments from the committed use discount [dashboard](https://cloud.google.com/billing/docs/how-to/cud-analysis-spend-based#understanding_dashboard)
  or [analysis
  report](https://cloud.google.com/billing/docs/how-to/cud-analysis-spend-based#understanding_analysis).
  1. To view the dashboard select **Committed use discounts (CUDs)** from the
    **Cloud Billing** menu.
  2. To purchase a commitment select **Purchase**.
4. Select the **Product**.
5. Enter a **name** for your commitment.
6. Choose a **commitment term** of 1 or 3 years, the duration for which you are
  charged for the commitment.
7. Enter your hourly **commitment amount**, in terms of equivalent discount
  spend.
  - This amount represents the equivalent of discount costs that you would
    have incurred with the committed use discount.
  - You can view the **commitment fee**, your recurring charge, in the
    **commitment summary**.
  - You can view the estimated savings when your commitments are fully
    utilized in the **commitment summary**.
8. Read the [Service Specific Terms regarding Committed
  Units](https://cloud.google.com/terms/service-terms)
9. Review everything you entered to verify you're committing to the correct
  amount. If the product requires commitment within a specific region, make
  sure that you have also selected the correct region.
10. To preview your purchase, click the **Purchase** button. This does not
  process the actual purchase, but rather prepares a summary for you to review
  before finalizing.
11. To finalize your purchase, review the commitment summary and click
  **Purchase** again.

Repeat these steps for each service that you want to purchase a commitment for.

## View commitments

You can view the details of your spend-based committed use discounts in the
Google Cloud console commitment dashboard or analysis report, described in
[Analyze the effectiveness of your CUDs](https://cloud.google.com/billing/docs/how-to/analyze-cuds).

For an explanation of the commitment dashboard and analysis report, see
[Understand the CUD analysis report](https://cloud.google.com/billing/docs/how-to/analyze-cuds#understanding_analysis)
and
[Understanding the analysis
report](https://cloud.google.com/billing/docs/how-to/cud-analysis-spend-based#understanding_analysis).

## Cancel commitments

You can't cancel the commitments you've purchased. You must pay the agreed upon
monthly amount for the duration of the commitment. Your commitment and the
resources covered by it aren't affected by future changes to the standard
prices for those resources.

If you accidentally purchased a commitment or made a mistake configuring your
commitment, contact [Cloud Billing
Support](https://cloud.google.com/support/billing)
for help.

## How committed use discounts work

Your spend-based committed use discount is applied to the eligible usage each
hour.

If you use more in the hour than you committed to, the overage is charged at
your regular on-demand rate. If you use less in the hour than you committed to,
you underutilize your commitment and don't realize your full discount.

To understand how your commitment fees and credits are applied to your
Cloud Billing account and projects, see [Attribution of committed use
discount fees and
credits](https://cloud.google.com/docs/cuds-attribution).

## Understanding your bill, invoice, and exported data

To understand spend-based CUDs in your bill, invoice, and
exported data, see [Analyze the effectiveness of your CUDs](https://cloud.google.com/billing/docs/how-to/analyze-cuds).

## Legacy spend-based CUDs

In the legacy spend-based CUDs program, your commitment amount is the on-demand
price instead. For more information about the differences between the legacy and
new spend-based CUDs program, see [Spend-based CUDs program
improvements](https://cloud.google.com/docs/cuds-multiprice).

## APIs and reference

You can purchase commitments for VMware Engine and
Compute Engine flexible commitments by using the Cloud Commerce Consumer
Procurement API. For more information, see [the
documentation](https://cloud.google.com/marketplace/docs/commitment-api-purchasing).

## Get support

If you have questions regarding CUDs on your bill, contact
[Cloud Billing Support](https://cloud.google.com/support/billing) for help.

## Related topics

- [Learn more about committed use discounts](https://cloud.google.com/docs/cuds)
- [Learn how to analyze the effectiveness of your CUDs](https://cloud.google.com/billing/docs/how-to/analyze-cuds)
- [View your Cloud Billing reports and cost trends](https://cloud.google.com/billing/docs/how-to/reports)
- [View the credits you are receiving in reports](https://cloud.google.com/billing/docs/how-to/reports#credits)
- [Understand your savings with cost breakdown reports](https://cloud.google.com/billing/docs/how-to/cost-breakdown)
- [Learn how to export Cloud Billing data to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery)
- [View your cost and payment history](https://cloud.google.com/billing/docs/how-to/view-history)

   Was this helpful?

---

# Verify your discounts after migrationStay organized with collectionsSave and categorize content based on your preferences.

> How to verify your discounts after the new CUD data model migration.

# Verify your discounts after migrationStay organized with collectionsSave and categorize content based on your preferences.

Your discounts won't change after migration, because your current
contractual rates are **guaranteed for the duration of your contract**. As long
as your usage remains the same, your total costs won't increase.
To see how your billing and discounts will look after the migration, you can use
the
[BigQuery Sample Data Export](https://cloud.google.com/docs/cuds-multiprice-datamodel#bq-sample-data-export).
To understand your savings, commitment utilization, and effective savings rate,
you can use the
[Compute flexible CUD example queries](https://docs.cloud.google.com/docs/cuds-verify-discounts?tab=t.urytg1ca4hpw#heading=h.x1ob7sfz57id).
To view your discount percentages before migration (old CUD model) or after
migration (new CUD model), choose one of the following steps.

## View discount percentages before migration (old CUD model)

- To view your effective CUD discount compared to List On-Demand Price,
  see
  [Calculate your overall flexible CUDs savings](https://cloud.google.com/billing/docs/how-to/cud-analysis-flexible#calculating_overall_discount).
- To view your effective CUD discount compared to Contracted On-Demand
  Price: `(0.01 - Flex CUD SKU price) * 100`

## View discount percentages after migration (new CUD model)

After you migrate to the new model, SKUs can have different usage rates based
on the
[consumption model](https://cloud.google.com/docs/cuds-multiprice#consumption-model-intro)
you use them under.

In the following example, we analyze the SKU named `N2 Instance Core running in
Americas` (SKU ID: `BB77-5FDA-69D9`). This SKU has three primary consumption
models:

- **On-Demand**: Standard, pay-as-you-go usage (consumption model
  `7754-699E-0EBF`).
- **1-Year Flexible CUD**: Usage covered by a 1-year commitment
  (consumption model `D97B-0795-975B`).
- **3-Year Flexible CUD**: Usage covered by a 3-year commitment
  (consumption model `70D7-D1AB-12A4`).

Use the Pricing user interface to see details about the pricing for each
model:

1. In the Google Cloud console, go to your Cloud Billing account.
  [Go to your Cloud Billing account](https://console.cloud.google.com/billing)
2. Select **Pricing** from the sidebar.
3. Both the public list price and your contractual prices are displayed.

In this example, we add two columns to show the savings ($/%) compared to the
on-demand consumption model.

| Fields from pricing UI | Added fields to show savings calculations |
| --- | --- |
| SKU ID | Consumption model ID |
| BB77-5FDA-69D9 | 7754-699E-0EBF |
| BB77-5FDA-69D9 | 70D7-D1AB-12A4 |
| BB77-5FDA-69D9 | D97B-0795-975B |

The preceding chart uses five formulas to calculate the dollar savings in the
columns named **Savings from on-demand contract rates** and **Savings from
on-demand list rates**.

The calculations use the formula `New Price - Baseline Price` to show savings
as a negative value. The accompanying percentage is then calculated by dividing
that dollar saving by the baseline price.

### Savings from on-demand list rates (for on-demand usage)

This formula calculates your initial savings from using the discounted
On-demand Contract Price instead of the public On-demand List Price.

**Formula**: `On-demand Contract Price − On-demand List Price` **Example from chart**: `$0.02055 − $0.03161 = −$0.01106`

### Savings from on-demand contract rates (for 3-Year CUD)

This formula calculates the additional savings gained by using a 3-Year
Flexible CUD compared to the already discounted On-demand Contract Price.

**Formula**: `3-Year CUD Contract Price − On-demand Contract Price` **Example from chart**: `$0.01408 − $0.02055 = −$0.00647`

### Savings from on-demand list rates (for 3-Year CUD)

This formula calculates the total savings gained by using a 3-Year Flexible CUD
compared to the public On-demand List Price.

**Formula**: `3-Year CUD Contract Price − On-demand List Price` **Example from chart**: `$0.01408 − $0.03161 = −$0.01753`

### Savings from on-demand contract rates (for 1-Year CUD)

This formula calculates the additional savings gained by using a 1-Year
Flexible CUD compared to the on-demand Contract Price.

**Formula**: `1-Year CUD Contract Price − On-demand Contract Price` **Example from chart**: `$0.01878 − $0.02055 = −$0.00177`

### Savings from on-demand list rates (for 1-Year CUD)

This formula calculates the total savings gained by using a 1-Year Flexible CUD
compared to the public On-demand List Price.

**Formula**: `1-Year CUD Contract Price − On-demand List Price` **Example from chart**: `$0.01878 − $0.03161 = −$0.01283`

## Calculate the effective savings rate (ROI)

To calculate your effective savings rate (ROI), use the
[CUD KPI sample queries](https://cloud.google.com/docs/cuds-multiprice-datamodel#cud-kpis).
Separate sample queries are available specifically for the legacy data model and
the new data model to facilitate comparison.

## Related topics

- [Spend-based CUD program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)
- [Sample queries for the new CUDs data model](https://cloud.google.com/docs/cuds-example-queries)
- [Migrated CUD SKUs, offers, and consumption model IDs](https://cloud.google.com/docs/cuds-migration)
- [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements)

   Was this helpful?
