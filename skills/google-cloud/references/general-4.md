# Attribution of committed use discount fees and creditsStay organized with collectionsSave and categorize content based on your preferences. and more

# Attribution of committed use discount fees and creditsStay organized with collectionsSave and categorize content based on your preferences.

> Overview of Google Cloud committed use discount attribution.

# Attribution of committed use discount fees and creditsStay organized with collectionsSave and categorize content based on your preferences.

[Committed use discounts](https://cloud.google.com/docs/cuds)
(CUDs) provide a discount in exchange for your commitment to
[spend a minimum amount](https://cloud.google.com/docs/cuds#spend_based_commitments)
or
[use a minimum level of resources](https://cloud.google.com/docs/cuds#resource_based_commitments)
for a product for a specified term.

Attribution refers to how resource benefits shared at the
Cloud Billing account level are divided among
[account-level resources](https://cloud.google.com/billing/docs/concepts#gcp_resource_hierarchy_overview),
such as projects.
Attribution for a subscription, such as your committed use discount
subscription, determines how fees and credits are applied to your
Cloud Billing account and spread across the account's projects that are
eligible to consume them. This is reflected in how the fees and credits appear
in Cloud Billing cost management interfaces, such as the
[usage cost export](#view-attribution-in-exported-data)
or the [Google Cloud console](#view-attribution-in-reports).

## Types of commitment attribution

Attribution impacts how your committed use discount fees and credits
are applied to the projects in your Cloud Billing account, which
is reflected in the cost management interfaces. The following are ways in
which they can be applied.

### Unattributed

When *unattributed*, the subscription fees and credits are applied to your
Cloud Billing account's projects, as they consume eligible usage.
Any subscription fees that are not attributed to a project are charged at the
Cloud Billing account level.

This type of attribution can affect the predictability of a project's adjusted
costs after applying the commitment fees and credits because of the timing or
order of consumption relative to other eligible projects.

### Proportional attribution

*Proportional attribution* applies the credits and, where appropriate, the
subscription fees from your *spend-based* and *resource-based* committed use
discounts to the projects in your Cloud Billing account, directly
in proportion to the amount of total eligible usage consumed by each project.

For example, if project A consumed $75 worth of usage and project B consumed
$25, project A would be covered by up to 75% of available credit and
project B would be covered by up to 25%.

Any subscription fees that are not attributed to a project are charged
at the Cloud Billing account level.

Proportional attribution helps you understand the actual cost of a given project
that is consuming the discount by clearly disclosing the following:

- The project's portion of the total commitment fee
- The project's SKU-based usage cost
- The project's CUD credit

For your *resource-based* committed use discounts to use proportional
attribution,
[Compute Engine discount sharing](#compute-discount-sharing)
must be enabled.

### Prioritized attribution

*Prioritized attribution* applies the credits and, where appropriate, the
subscription fees from your *resource-based committed use discounts* to the
projects in your Cloud Billing account based on the
distribution you specify. The total amount of the allotments cannot exceed the
commitment amount purchased. Any remaining unprioritized commitment credits
and fees are then applied proportionally across all projects.

You can *allocate all of your purchased commitments* across projects you
specify. For example, if you purchased 60 GB of commitments, you can
prioritize project A to receive 40 GB of the allotment and project B
to receive 20 GB of the allotment. In this case, projects A and B fully
reserve the 60 GB of eligible committed usage. Then if project A and B have
fully utilized 60 GB of commitment, the other projects in your
Cloud Billing account don't receive an allocation of the credits and
fees, even if they have eligible usage. But if project A and B have not fully
utilized the 60 GB of commitment, other projects will receive the remaining
committed usage credits, if they have eligible usage.

You can also *allocate a portion of your purchased commitments* to certain
projects, allowing the remainder to be applied proportionately to the eligible
usage in all projects. For example, if you purchased 60 GB of
commitments, you can prioritize project A to receive 30 GB of the allotment
and allow the remaining 30 GB to be applied proportionately to the eligible
usage in your other projects.

You can *select multiple projects for a single prioritized allotment*. In that
case, the allotment is shared proportionately between the projects based on
their eligible usage.

If you don't utilize all of your purchased commitments for the period, the
fees are still charged to the prioritized projects. For example, if project A
is allotted 30 GB of usage but only uses 10 GB, the project still
receives the fee for the full allotment of 30 GB.

You cannot prioritize more commitment resources than what you have purchased.

Prioritized attribution helps you control how your commitments impact
each of your projects and their actual cost by clearly disclosing the
following:

- The project's exact portion of the total commitment fee
- The project's SKU-based usage cost
- The project's CUD credit

#### Enable Compute Engine discount sharing

To use prioritized attribution for your resource-based commitments, you
*must enable* [Compute Engine discount sharing](#compute-discount-sharing). This lets you
specify how the credits and fees are prioritized for the projects in your
Cloud Billing account.

If you have *not enabled* Compute Engine discount sharing, you might want to
select and configure prioritized attribution for your resource-based commitments
*before* you enable discount sharing. By doing this, you maintain the current
attribution model (unattributed) for your credits and fees up until the
moment you select prioritized attribution. In this situation, if you enable
discount sharing before selecting and configuring prioritized attribution there
will be a period of time where your commitment credits and fees are shared
across your Cloud Billing account's projects according to the tenets
of discount sharing. This could result in the appearance of erratic behavior in
your reports as they move from unattributed to discount sharing to prioritized
attribution.

### Compute Engine discount sharing

*Discount sharing* is only available for Compute Engine resource-based
committed use discounts purchased at the project level. When *discount sharing*
is enabled, the benefit of the commitment is shared at the Cloud Billing
account level based on the resource consumption. This allows all projects
with eligible resource usage to consume that commitment's credits and fees.
These are not tied to the amount spent, but rather to the amount of the resource
used.

See [Understanding discount sharing](https://cloud.google.com/billing/docs/how-to/analyze-cuds#discount_sharing)
to learn more or how to
[turn on committed use discount sharing](https://cloud.google.com/compute/docs/committed-use-discounts/share-resource-cuds-across-projects#turning_on_committed_use_discount_sharing).

## Choose proportional attribution for spend-based commitments

To keep your project costs predictable, starting from August 2021, the
following automatically use *proportional attribution* when
you purchase spend-based commitments:

- You have an existing Cloud Billing account that has no
  spend-based commitments.
- You create a new Cloud Billing account and purchase spend-based
  commitments.

If your Cloud Billing account existed and you purchased spend-based
commitments before or during August 2021, you can
[request to switch your account to proportional attribution](#select-proportional-attribution-spend-based).

#### Select proportional attribution

If you purchased spend-based commitments before or during August 2021, they
might be [unattributed](#type-billing-unattributed).
You can request that your billing account switches to proportional attribution,
which converts your existing spend-based commitments. To do so, submit the
requested information in
[the proportional attribution opt-in form](https://forms.gle/UEsTuotQsHj5d8qj6).

If you're uncertain whether or not your spend-based commitments purchased
before or during August 2021 are using proportional attribution, submit the
requested information in
[the proportional attribution opt-in form](https://forms.gle/UEsTuotQsHj5d8qj6)
to verify it is enabled.

## Choose attribution for resource-based commitments

To keep your project costs predictable for resource-based commitments, you
can select *prioritized attribution* or *proportional attribution*.
Attribution works in conjunction with
[Compute Engine discount sharing](#compute-discount-sharing).
To use attribution, you *must* also
[enable CUD sharing](https://cloud.google.com/compute/docs/committed-use-discounts/share-resource-cuds-across-projects#turning_on_committed_use_discount_sharing)
for your Cloud Billing account. Any attribution preferences that you
configure are applied only after you enable CUD sharing.

You can update prioritized attribution anytime during the commitment's
lifetime. The attribution starts applying to usage starting
12 AM US and Canadian Pacific Time (UTC-8, or UTC-7 during daylight saving time)
on the following day. The updated attribution setting is only applied moving
forward.

To choose the attribution for your resource-based commitment, perform the
following steps:

1. Sign in to your Cloud Billing account in the Google Cloud console.
  [Sign in to your Cloud Billing account](https://console.cloud.google.com/billing/overview)
2. At the prompt, **choose the Cloud Billing account**
  for which you'd like to configure attribution. The Billing *Overview* page
  opens for the selected billing account.
3. From the Billing navigation menu, select **Committed use discounts** to
  view the committed use discounts dashboard.
4. From the committed use discounts dashboard, locate the *resource-based*
  commitment for which you want to configure attribution.
5. Click the **View Analysis** action menu
  for the *resource-based* commitment, then click **Configure Attribution**
  to view the commitment summary.
6. Choose between
  [prioritized attribution](#select-prioritized-attribution-resource-based)
  or
  [proportional attribution](#select-proportional-attribution-resource-based).
7. [Enable CUD discount sharing](https://cloud.google.com/compute/docs/committed-use-discounts/share-resource-cuds-across-projects#turning_on_committed_use_discount_sharing),
  if you haven't already done so.

### Select prioritized attribution

From the **Configure Attribution** page for your resource-based commitments,
you can select *prioritized attribution* with the following steps:

1. From the commitment summary, select **Prioritized** to view your active
  commitments.
2. Click  **Add Allotment**.
3. Click **Targets 1**
  to select from your available projects to receive an allotment.
  You can select multiple projects for a single allotment. In that case, the
  allotment is shared proportionately between the projects based on their
  eligible usage.
4. In the **Allotment 1** field, enter the amount to be prioritized for the
  selected targets.
  To add additional allotments, click  **Add Allotment**.
5. Click **Save** to apply your changes.
6. If you haven't already, when you are ready for your attribution
  configuration to take effect,
  [turn on Compute Engine discount sharing](https://cloud.google.com/compute/docs/committed-use-discounts/share-resource-cuds-across-projects#turning_on_committed_use_discount_sharing).
  If you have *not enabled* Compute Engine discount sharing, you might want
  to select and
  [configure prioritized attributionbeforeyou enable discount sharing](#enable-discount-sharing).
  [Compute Engine discount sharing](#compute-discount-sharing) *must be enabled for your resource-based commitments* to use your
  attribution preferences.

To switch to *proportional attribution* after selecting *prioritized
attribution* for your resource-based commitments, follow the instructions at
[select proportional attribution](#select-proportional-attribution-resource-based).

The following image is an example of configuring *prioritized attribution* for
a resource-based commitment on the **configure attribution** page.

![Example of configuring prioritized attribution for a resource-based commitment.](https://cloud.google.com/static/billing/docs/images/cud-attribution-prioritized-resource-based.png)

### Select proportional attribution

From the **Configure Attribution** page for your resource-based commitments,
you can select *proportional attribution* with the following steps:

1. From the commitment summary, select **Proportional (default)**.
2. Click **Save** to apply your changes.

To switch to *prioritized attribution* after selecting *proportional
attribution* for your resource-based commitments, follow the instructions at
[select prioritized attribution](#select-prioritized-attribution-resource-based).

## View attribution in your reports

You can view the allocation of your committed use discount fees and charges for
unattributed, proportional, and prioritized attribution in your billing reports.

When you navigate to the reports page, group by **Project**, and filter by
**SKU**, each project displays the subscription fees specifically attributed
to it. Any remaining subscription fees that are not associated with a project
are unattributed and assigned to **Charges not specific to a project**.

To view the Cloud Billing reports for your Cloud Billing
account:

1. Sign in to your Cloud Billing account in the Google Cloud console.
  [Sign in to your Cloud Billing account](https://console.cloud.google.com/billing/overview)
2. At the prompt, **choose the Cloud Billing account**
  for which you'd like to view reports. The Billing *Overview* page
  opens for the selected billing account.
3. In the Billing navigation menu, select **Reports**.

For more information on viewing your billing reports, see
[View your billing reports and cost trends](https://cloud.google.com/billing/docs/how-to/reports).

## View attribution in your exported data

You can view the allocation of your committed use discount fees and charges for
unattributed, proportional, and prioritized attribution in the
Cloud Billing BigQuery usage cost export.

When viewing your exported data in BigQuery, each project
consuming credit has a line item corresponding to its portion of the
subscription fee, alongside a line item that represents the usage and credit
consumed for that project.

If there is any unconsumed credit, where you didn't consume as much as you
committed to, then the remaining subscription fees are assigned to
**Costs not specific to a project** and not attributed to any projects.
The total charges for the SKU remain the same, divided between fees that
are assigned proportionally to related projects and unattributed fees that
are assigned to **Costs not specific to a project**.

For more information about exporting your cost data to BigQuery,
see [Export Cloud Billing data to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery).

## Related topics

- [Learn about spend-based CUDs program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Learn more about committed use discounts](https://cloud.google.com/docs/cuds)
- [Analyze the effectiveness of your committed use discounts](https://cloud.google.com/billing/docs/how-to/cud-analysis)
- [View your Cloud Billing reports and cost trends](https://cloud.google.com/billing/docs/how-to/reports)
- [View the credits you are receiving in reports](https://cloud.google.com/billing/docs/how-to/reports#credits)
- [Understand your savings with cost breakdown reports](https://cloud.google.com/billing/docs/how-to/cost-breakdown)
- [Export Cloud Billing data to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery)
- [View your cost and payment history](https://cloud.google.com/billing/docs/how-to/view-history)

---

# Billing user interface improvementsStay organized with collectionsSave and categorize content based on your preferences.

> Learn about the Billing user interface improvements as part of the new CUDs program.

# Billing user interface improvementsStay organized with collectionsSave and categorize content based on your preferences.

In the Google Cloud console, the Cloud Billing user interface has the following
updates to support the new CUDs program:

- **Cost breakdown report**: The Cost breakdown
  chart now visually represents the net impact of your spend-based CUDs
  discount, showing savings in green or any underutilized commitment waste
  in orange.
- **Savings filter**: In **Reports** and the **Cost table**
  report, the **Credits** filter is now named **Savings** and has been
  restructured with clearer subcategories for easier analysis. The Cost table
  report incorporates additional columns reflecting these distinct savings
  categories.
- **Improved CUD analysis tool**: A new
  and improved analysis page for CUDs is available, offering more powerful
  filtering, data aggregation, and utilization tracking. For the new
  spend-based CUD model, the analysis tool now provides insights into
  utilization patterns visualized as equivalent on-demand spend (for savings
  and usage analysis). The new tool offers new filters by multiple dimensions
  and aggregates machine commitments. It also has a new graph to track
  utilization percentages over time.
- **CUD dashboard display names**: All spend-based CUDs
  now follow a consistent `[Product] CUD` naming pattern in the dashboard for
  better clarity.
- **Budgets**: Budgets track your net cost after savings
  are applied. You must review your existing budget alert thresholds, as your
  tracked costs might be lower, depending on the filters that you have
  configured. The total costs tracked by these budgets can decrease as the
  uncredited costs now include savings when the new model applies.
- **Pricing table**: The pricing table has new
  fields to support [consumption models](https://cloud.google.com/docs/cuds-multiprice#consumption-model-intro).
- **CUD metadata exports to BigQuery**: Added
  new billing data exports for pricing and CUD metadata to BigQuery.

## View your savings

On the Billing account **Overview** page, the Savings calculation includes
all eligible discounts and credits. The *View details* link now takes you
to the **Cost breakdown** report, shown as #1 in the following image.

![Example of the billing account overview page](https://cloud.google.com/static/docs/images/cuds-savings.png)

### Filter your savings

In **Reports**, the **Credits** filter is now named **Savings**, and the
subcategories have been restructured as *Savings programs* and *Other savings*
for easier analysis. The filters let you see your costs before and after
various discounts are applied. By toggling these options, you can analyze how
much money you are saving with each type of discount, shown as #2 in the
following image.

![Example of the savings filter in cost Reports](https://cloud.google.com/static/docs/images/cuds-savings-filter.png)

In Reports, the savings filter displays only the specific credit types that
you incurred in your Google Cloud costs. If a particular type of credit
doesn't apply to your Cloud Billing account, you won't see that
credit option in the list.

The *Savings programs* subcategory includes the Committed Use Discount (CUD)
options:

- **Spend-based CUD discounts**: Discounts earned with the new pricing
  model, showing you the cost savings you have from your commitments.
- **Legacy spend-based CUD credits**: Spend-based committed use discounts
  (CUDs) credits for SKUs that are not part of the new pricing model, or
  for CUDs credits earned before the new pricing model went into effect.
- **Resource-based CUD credits**: Credits on Compute Engine resource costs
  when you commit to using eligible resources during a specified term.

The *Other savings* subcategory includes Free tier credits, Promotional
credits, and other discounts and credits such as the following:

- **Sustained Use Discounts (SUDs)**: Discounts automatically earned when
  you run eligible Compute Engine resources throughout the billing
  month.
- **Spending-based discounts**: Discounts applied after a contractual
  spending threshold is reached, typically earning progressively larger
  discounts based on your total spend over a defined period.
- **Subscription credits** These credits are typically applied to Base +
  Overage subscriptions, also known as Non-Unified Commitment Service
  (Non-UCS) subscriptions.

See Cloud Billing Reports to
[learn more about savings](https://cloud.google.com/billing/docs/how-to/reports#credits).

## New columns and filters in the Cost table report

In the Cost table report, new columns and filters show you how the consumption
model affects your costs and let you filter the savings data for more
flexibility, shown as #3 and #4 respectively in the following image.

![View of the savings filter](https://cloud.google.com/static/docs/images/cuds-consumption-model-filters.png)

## Use labels and group data in the Cost table report

In the Cost table report, you can use the **Table configuration** settings to
organize, aggregate, and add business context to your tabular view of your
costs for a given invoice or statement. These settings let you select a label
to categorize your data, use labels as a grouping dimension, and select a
grouping option, shown as #5 in the following image.

![Table configuration settings in the cost
 table report.](https://cloud.google.com/static/docs/images/cuds-label-and-group-data.png)

The table configuration dialog has the following options:

- **Label data**: This lets you select one of your custom label keys. It
  adds a new column to the table, showing the specific label value for each
  cost item. This is the best way to overlay your own business context
  (like teams, environments, or cost centers) onto your report.
- **Group by**: The grouping options control how the rows in the table are
  aggregated and nested. You can view a flat list, or you can create a
  hierarchical, nested view of your costs. The Group by options include:
  - **No grouping**: Shows each cost item as a separate, individual row.
  - **Project > Service > SKU > Consumption model**: Creates a nested
    hierarchy starting with the project at the highest level, allowing you
    to see costs roll up from the most granular level (the consumption
    model) to the highest level.
  - **Service > SKU > Consumption model**: Creates a nested hierarchy
    starting with the service at the highest level.
  - **Custom grouping**: Select grouping dimensions to break out totals of the
    different types of savings or credits that apply.

[Learn more about the Cost table report](https://cloud.google.com/billing/docs/how-to/cost-table).

## Analyze your savings with the Cost Breakdown report

For the report date range, the Cost breakdown report shows your base usage
cost and how that cost is affected by any credits, adjustments, and taxes, to
arrive at your total cost. The waterfall chart displays charges in orange,
savings in green, and subtotals and totals in blue. For services covered by the
new spend-based CUDs, the *Spend-based CUD discounts* bar shows the net impact
of your spend-based commitments, shown as #6 in the following image.

![The cost breakdown report.](https://cloud.google.com/static/docs/images/cuds-cost-breakdown.png)

The Cost breakdown report includes a savings bar for each *applicable* type
of credit. If a particular type of credit doesn't apply to your
Cloud Billing account, you won't see that savings type in the chart.
In the example image, the Cost breakdown chart and table are showing the
following items:

- **Usage cost**: This is the starting point—the gross cost of all services
  you used during the time period, before any discounts or credits are
  applied.
- **Negotiated savings**: This green bar represents a credit for any special
  pricing or custom discounts negotiated in your contract.
- **Spend-based CUD discounts**: This shows the net impact of your spend-based
  commitments. It appears as a green credit bar representing your savings, but
  can appear as an orange charge bar in the rare case of underutilized
  commitments (waste).
- **Sustained use discounts (SUDs)**: This credit represents the automatic
  savings you receive for running eligible resources for a significant portion
  of the month, with no commitment required.
- **Spending-based discounts**: This credit is for any automatic volume-based
  discounts you receive for high usage of certain services.
- **Subtotal / Total**: The final blue bars show your subtotal after all
  credits are applied, and the final total represents the net costs
  after taxes are added.

[Learn more about the Cost breakdown report](https://cloud.google.com/billing/docs/how-to/cost-breakdown).

## Review your budgets after cost-saving updates

With recent updates to how spend-based CUDs cost savings are calculated, the
total costs tracked by your budgets might now be lower. Commitment savings are
more consistently included in the budget's calculation, giving you a more
accurate view of your actual net spend.

Due to this change, you should ask the following questions:

- Should I lower my budget alert thresholds to avoid missing important
  spending changes?
- Which of my existing budgets are affected and need review?
- How can I create a new budget that accurately reflects my net costs?

We recommend that you visit your budgets dashboard to review any existing
budgets. Since they now track a lower total cost that includes commitment
savings, your original alert thresholds might be too high and might not trigger
when expected. Adjusting your thresholds downward ensures you continue to
receive timely spending alerts based on your actual costs.

When creating or reviewing a budget, the **Savings** scope is the key section
to understand, shown as #7 in the following image.

- This section controls which credits and discounts are subtracted from your
  gross costs to determine the final "total cost" that your budget tracks.
- Because your budget tracks the cost *after* these savings are applied, the
  tracked amount is your net cost. This is why your total tracked cost might
  be lower than it was previously, requiring you to review and potentially
  lower your alert thresholds to match this more accurate, post-savings
  number.

[Learn more about managing budgets](https://cloud.google.com/billing/docs/how-to/budgets).

![The savings options in the budget scope.](https://cloud.google.com/static/docs/images/cuds-create-budget.png)

## New CUD display names

To simplify how commitments are displayed, all spend-based CUDs use a consistent
naming convention. This change, noted in the migration banner at the top of the
page, helps you identify which product a specific commitment applies to directly
from the list view.

Your existing CUDs will migrate to the new consumption model and will be tagged
if they have migrated, shown as #8 in the following image.

![The new CUD display names.](https://cloud.google.com/static/docs/images/cuds-new-names.png)

The display names for all CUD offerings in the new spend-based model use the
following naming pattern:

- **Naming Pattern**: `[Product] CUD` - The name of the product is listed first,
  followed by "CUD".
- **Examples shown in the screenshot**:
  - `AlloyDB for PostgreSQL CUD`
  - `Cloud Run CUD`
  - `Compute Flexible CUD`
  - `Kubernetes Engine CUD`

## Pricing table fields for consumption models

The Pricing page provides a comprehensive list of all available SKUs and their
associated prices for your account. There are new fields in this view, for
example **Consumption model description**, shown as #9 in the following image.

![The pricing view for a project with negotiated pricing.](https://cloud.google.com/static/docs/images/cuds-pricing-field-tables.png)

By using the column chooser on the right side of the table, you have granular
control over your pricing report. This lets you create a view tailored to
your specific needs, whether that's a high-level overview focusing on product
names or a detailed deep-dive that includes specific IDs and taxonomy.

You can choose the data points to show, for example:

- **Identifiers**: `SKU ID` for technical analysis.
- **Descriptions**: `SKU description` and `Consumption model description` for
  better readability.
- **Classification**: `Product taxonomy` to understand how a SKU is
  categorized within the Google Cloud ecosystem.
- **Pricing Details**: `Price reason` to understand why a certain price is
  being applied (e.g., `DEFAULT_PRICE`).

## Pricing and CUD metadata exports to BigQuery

For customizable analysis of your pricing and savings, enable Billing data
exports to BigQuery:

- **Pricing** (updated): This export contains all of your account's SKUs and
  their prices. You can join this data with the detailed usage export to
  perform custom pricing calculations or analysis.
  [Learn more](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/pricing-data)
- **Committed Use Discounts Export** (new): This export provides all the
  metadata related to your *spend-based* CUDs. It lets you analyze your
  commitment portfolio, track utilization over time, and identify
  opportunities for optimization beyond what is available in the standard
  console reports.
  [Learn more](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/cud-export)

In addition, there are new fields added to the **Pricing data export**. For
more information, see [Price export changes](https://cloud.google.com/docs/cuds-multiprice-datamodel#price-export-changes).

## Related topics

- [Spend-based CUD program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline)
- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)
- [Sample queries for the new CUDs data model](https://cloud.google.com/docs/cuds-example-queries)
- [Migrated CUD SKUs, offers, and consumption model IDs](https://cloud.google.com/docs/cuds-migration)

   Was this helpful?

---

# Choose the correct amount of CUD to buyStay organized with collectionsSave and categorize content based on your preferences.

> Learn how to Choose the correct amount of CUD to buy.

# Choose the correct amount of CUD to buyStay organized with collectionsSave and categorize content based on your preferences.

The best way to determine the right CUD amount is with the **CUD
Recommendations** tool. It automatically analyzes your usage for all eligible
SKUs and calculates the commitment that will provide you with maximum savings.
You can also customize the recommendation to cover a specific percentage of your
total spend.

If you prefer a manual approach, use the **CUD Analysis** tool.

1. Review your historical data to identify your consistent hourly
  on-demand spend (shown as gray bars in the chart)
2. Discount the on-demand spend by the expected discount to receive based
  on the SKUs you use and their discount level

The amount you input for CUD purchases would be different in the new model,
because in the new model you share your commitment amount after discount. For
example, in the old model you committed to $100 at On-Demand Price and you
received 30% CUD discounts leading to an effective cost of $70. In the new model
you would specify $70 as that is the discounted rate.

It is complex to manually calculate the exact amount due to the discounts on
different SKUs for CUD might be different in the new model.

## Related topics

- [Spend-based CUD program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline)
- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Sample queries for the new CUDs data model](https://cloud.google.com/docs/cuds-example-queries)
- [Migrated CUD SKUs, offers, and consumption model IDs](https://cloud.google.com/docs/cuds-migration)
- [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements)

   Was this helpful?
