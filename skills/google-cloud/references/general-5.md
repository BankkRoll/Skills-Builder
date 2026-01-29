# Sample queries for the new CUDs data modelStay organized with collectionsSave and categorize content based on your preferences. and more

# Sample queries for the new CUDs data modelStay organized with collectionsSave and categorize content based on your preferences.

> Learn about example queries that use the new CUDs data model.

# Sample queries for the new CUDs data modelStay organized with collectionsSave and categorize content based on your preferences.

## Queries for CUD KPIs

You can use these important KPI metrics to validate that your systems are
functioning well with the new data model:

1. **Commitment savings ($)**: Describes the savings that resulted from your
  commitments. The metric uses the formula `(Cost of resources at on-demand
  rates - cost of resources with commitment discounts)`.
2. **Commitment savings (%)**: Describes the savings percentage that resulted
  from your commitments. The metric uses the formula `(Commitment savings /
  costs of resources at on-demand rates)*100`.
3. **Commitment utilization (%)**: Measures how effectively you use your
  commitments, expressed as a percentage. The metric uses the formula
  `(Commitment applied to eligible spend / total commitment)`.
4. **Effective savings rate (%)**: Explains the return on investment (ROI) for
  commitment discounts. The metric uses the formula `(Commitment Savings /
  On-Demand Equivalent Spend)`.
  To gain better insight into your cost data, the following
  BigQuery sample queries show how to retrieve useful
  information for the following KPIs.

### Choose the correct sample query

To help you update your queries for the changes to the data model, we provide
two versions of the KPI sample queries. Choose one of the following:

- [Sample KPI queries using the legacy data model](#format-before-opt-in)
- [Sample KPI queries using the new data model](#format-after-opt-in)

### Sample KPI queries using the legacy data model

Use these sample queries if you *aren't* using the new data model.

These queries are only for Compute flexible CUDs. To query for other spend-based
CUD products, you must change the following values:

- `cud_product`
- `sku.description`
- `credit.type`

#### CUD cost plus CUD savings

```
WITH
 cost_data AS (
   SELECT *
   FROM project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN
   WHERE invoice.month = 'month'
 ),
 cud_product_data AS (
   SELECT * FROM UNNEST(
     [
       STRUCT(
         'Compute Engine Flexible CUDs' AS cud_product,
         'Commitment - dollar based v1: GCE' AS cud_fee_regex,
         'GCE Commitments' AS cud_credit_regex)])
 ),
 cud_costs AS (
   SELECT
     invoice.month AS invoice_month,
     cud_product_data.cud_product,
     IFNULL(
       (
         SELECT l.value
         FROM UNNEST(labels) l
         WHERE l.key = 'goog-originating-service-id'
       ),
       service.id) AS service,
     SUM(cost) AS cost
   FROM
     cost_data
   JOIN cud_product_data
     ON
       REGEXP_CONTAINS(
         sku.description, cud_fee_regex)
   GROUP BY 1, 2, 3
 ),
 cud_credits AS (
   SELECT
     invoice.month AS invoice_month,
     cud_product,
     service.id AS service,
     SUM(credit.amount) AS spend_cud_credits
   FROM
     cost_data, UNNEST(credits) AS credit
   JOIN cud_product_data
     ON
       REGEXP_CONTAINS(
         credit.full_name, cud_credit_regex)
   WHERE
     credit.type = 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE'
   GROUP BY 1, 2, 3
 )
SELECT
 invoice_month,
 cud_product,
 cost As commitment_cost,
 -1 * (cost + IFNULL(spend_cud_credits, 0)) AS commitment_savings
FROM cud_costs
LEFT JOIN cud_credits
 USING (invoice_month, cud_product, service);
```

- `month` is the current year and month in `YYYYMM` format, for example '202504'.

#### Commitment utilization

```
WITH
 cost_data AS (
   SELECT *
   FROM project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN
   WHERE invoice.month = 'month'
 ),
 cud_product_data AS (
   SELECT * FROM UNNEST(
     [
       STRUCT(
         'Compute Engine Flexible CUDs' AS cud_product,
         'Commitment - dollar based v1: GCE' AS cud_fee_regex,
         'GCE Commitments' AS cud_credit_regex)])
),
 cud_commitment_amount AS (
   SELECT
     invoice.month AS invoice_month,
     cud_product_data.cud_product,
     SUM(usage.amount_in_pricing_units / 100) AS commitment_amount,
   FROM
     cost_data
   JOIN cud_product_data
     ON
       REGEXP_CONTAINS(
         sku.description, cud_fee_regex)
   GROUP BY 1, 2
 ),
 cud_utilized_commitment_amount AS (
   SELECT
     invoice.month AS invoice_month,
     cud_product,
     ABS(SUM(credit.amount / currency_conversion_rate))
       AS utilized_commitment_amount
   FROM
     cost_data, UNNEST(credits) AS credit
   JOIN cud_product_data
     ON
       REGEXP_CONTAINS(
         credit.full_name, cud_credit_regex)
   WHERE
     credit.type = 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE'
   GROUP BY 1, 2
 )
SELECT
 invoice_month,
 cud_product,
 utilized_commitment_amount / commitment_amount *100 AS commitment_utilization
FROM cud_commitment_amount
LEFT JOIN cud_utilized_commitment_amount
 USING (invoice_month, cud_product);
```

- `month` is the current year and month in `YYYYMM` format, for example '202504'.

#### Effective savings rate

```
WITH
 cost_data AS (
   SELECT *
   FROM project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN
   WHERE invoice.month = 'month'
 ),
 cud_product_data AS (
   SELECT * FROM UNNEST(
     [
       STRUCT(
         'Compute Engine Flexible CUDs' AS cud_product,
         'Commitment - dollar based v1: GCE' AS cud_fee_regex,
         'GCE Commitments' AS cud_credit_regex)])
 ),
 eligible_cud_skus AS (
   SELECT sku_id
   FROM example_project.dataset.flex_cud_skus
 ),
 eligible_cud_spend AS (
   SELECT
     invoice.month AS invoice_month,
     SUM(cost) AS cost,
     SUM(
       IFNULL(
         (
           SELECT SUM(credit.amount)
           FROM UNNEST(credits) AS credit
           WHERE
             credit.type IN (
               'COMMITTED_USAGE_DISCOUNT',
               'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE',
               'DISCOUNT',
               'FREE_TIER')
         ),
         0)) AS costs_ineligible_for_cud,
   FROM cost_data
   JOIN eligible_cud_skus
     ON sku.id = sku_id
   GROUP BY 1
 ),
 cud_costs AS (
   SELECT
     invoice.month AS invoice_month,
     cud_product_data.cud_product,
     IFNULL(
       (
         SELECT l.value
         FROM UNNEST(labels) l
         WHERE l.key = 'goog-originating-service-id'
       ),
       service.id) AS service,
     SUM(cost) AS cost
   FROM
     cost_data
   JOIN cud_product_data
     ON
       REGEXP_CONTAINS(
         sku.description, cud_fee_regex)
   GROUP BY 1, 2, 3
 ),
 cud_credits AS (
   SELECT
     invoice.month AS invoice_month,
     SUM(credit.amount) AS spend_cud_credits
   FROM
     cost_data, UNNEST(credits) AS credit
   WHERE
     credit.type = 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE'
     AND REGEXP_CONTAINS(credit.full_name, 'GCE Commitments')
   GROUP BY 1
 ),
cud_savings AS (
  SELECT
   invoice_month,
   Cud_product,
   spend_cud_credits as spend_cud_credits,
   -1 * (cost + IFNULL(spend_cud_credits, 0)) AS commitment_savings
FROM cud_costs
LEFT JOIN cud_credits
 USING (invoice_month)
)
SELECT
 Invoice_month,
 commitment_savings * 100
   / (cost + costs_ineligible_for_cud - IFNULL(spend_cud_credits, 0))
   AS effective_savings_rate
FROM eligible_cud_spend
LEFT JOIN cud_savings
 USING (invoice_month);
```

- `month` is the current year and month in `YYYYMM` format, for example '202504'.

### Sample KPI queries using the new data model

Use this sample query if you *have* adopted the new data model.

These queries are only for Compute flexible CUDs. To query for other spend-based
CUD products, you must change the following values:

- `cud_fee_skus`
- `consumption_model.id`

```
SET bigquery_billing_project = billing-project-id;

WITH
  cost_data AS (
    SELECT *
    FROM
      project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN
    WHERE invoice.month = 'month'
  ),
  cud_fee_skus AS (
    SELECT * FROM UNNEST(
      [
        '5515-81A8-03A2',
        'B22F-51BE-D599'])
      fee_sku_id
  ),
  cud_costs AS (
    SELECT
      invoice.month AS invoice_month,
      subscription.instance_id AS subscription_instance_id,
      IFNULL(
        (
          SELECT l.value
          FROM UNNEST(labels) l
          WHERE l.key = 'goog-originating-service-id'
        ),
        service.id) AS service,
      SUM(cost) AS commitment_cost,
      SUM(
        (
          SELECT SUM(credit.amount)
          FROM UNNEST(credits) credit
          WHERE credit.type = 'FEE_UTILIZATION_OFFSET'
        )) AS fee_utilization_offset
    FROM
      cost_data
    JOIN cud_fee_skus
      ON fee_sku_id = sku.id
    GROUP BY 1, 2, 3
  ),
  cud_savings AS (
    SELECT
      invoice.month AS invoice_month,
      subscription.instance_id AS subscription_instance_id,
      service.id AS service,
      SUM(cost - cost_at_effective_price_default) AS cud_savings_amount,
      SUM(cost_at_effective_price_default) AS on_demand_costs
    FROM
      cost_data
    WHERE
      consumption_model.id IS NOT NULL
      AND consumption_model.id IN ('D97B-0795-975B','70D7-D1AB-12A4')
    GROUP BY 1, 2, 3
  )
SELECT
  invoice_month,
  subscription_instance_id,
  service,
  commitment_cost,
  commitment_cost + fee_utilization_offset + IFNULL(cud_savings_amount, 0)
    AS commitment_savings,
  ABS(fee_utilization_offset) / commitment_cost * 100 AS cud_utilization_percent,
  (commitment_cost + fee_utilization_offset + IFNULL(cud_savings_amount, 0))
    / IFNULL(on_demand_costs, 1) * 100 AS effective_savings_rate
FROM cud_costs
LEFT JOIN cud_savings
  USING (invoice_month, subscription_instance_id, service);
```

- `month` is the current year and month in `YYYYMM` format, for example '202504'.

## Query and analyze historical Compute flexible CUDs

The following query lets you analyze your historical CUDs within a single
query. It detects your opt-in date and handles data types present in both the
old and new CUD models. To use this query, you must already be migrated to the
new CUD model.

This query is only for Compute flexible CUDs. To query for other
spend-based CUD products, you must change the following values:

- `cud_product`
- `sku.description`
- `Credit.type`
- `Credit.full_name`
- `cud_fee_skus`
- `consumption_model.id`

```
-- This query calculates both legacy and new model CUD KPIs, splitting the data by a migration event.
-- The migration event is defined as the first time the consumption_model.description is not 'Default'.
-- It calculates commitment cost, savings, utilization, and effective savings rate for both models.

WITH
 -- Determine the migration timestamp based on the first usage of a non-default consumption model
 migration_hour AS (
   SELECT
     MIN(t.usage_start_time) AS smallest_usage_start_time
   FROM
     `project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN` AS t
   WHERE
     t.consumption_model.description != 'Default'
 ),
 -- Filter for cost data that occurred before the migration
 legacy_cost_data AS (
   SELECT
    *
   FROM
     `project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN`
   WHERE
     usage_start_time < (
       SELECT
         smallest_usage_start_time
       FROM
         migration_hour
     )
 ),
 -- Filter for cost data that occurred at or after the migration
 new_cost_data AS (
   SELECT
    *
   FROM
     `project.dataset.gcp_billing_export_resource_v1_NNNNNN_NNNNNN_NNNNNN`
   WHERE
     usage_start_time >= (
       SELECT
         smallest_usage_start_time
       FROM
         migration_hour
     )
 ),
 -- Define CUD product metadata for matching fees and credits
 cud_product_data AS (
   SELECT
    *
   FROM
     UNNEST([ STRUCT( 'Compute Engine Flexible CUDs' AS cud_product, 'Commitment - dollar based v1: GCE' AS cud_fee_regex, 'GCE Commitments' AS cud_credit_regex)])
 ),
 -- =================================================================================================
 -- Part 1: Legacy Model Calculations (before migration)
 -- =================================================================================================
 legacy_commitment_costs AS (
   SELECT
     usage_start_time,
     pd.cud_product,
     IFNULL((
       SELECT
         l.value
       FROM
         UNNEST(labels) l
       WHERE
         l.key = 'goog-originating-service-id'
     ), service.id) AS service,
     SUM(cost) AS cost
   FROM
     legacy_cost_data
     JOIN cud_product_data AS pd ON REGEXP_CONTAINS(sku.description, pd.cud_fee_regex)
   GROUP BY
     1,
     2,
     3
 ),
 legacy_cud_credits AS (
   SELECT
     usage_start_time,
     pd.cud_product,
     service.id AS service,
     SUM(credit.amount) AS spend_cud_credits
   FROM
     legacy_cost_data,
     UNNEST(credits) AS credit
     JOIN cud_product_data AS pd ON REGEXP_CONTAINS(credit.full_name, pd.cud_credit_regex)
   WHERE
     credit.type = 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE'
   GROUP BY
     1,
     2,
     3
 ),
 legacy_commitment_savings AS (
   SELECT
     c.usage_start_time,
     c.cud_product,
     c.service,
     SUM(c.cost) AS commitment_cost,
     SUM(-1 * (c.cost + IFNULL(cr.spend_cud_credits, 0))) AS commitment_savings
   FROM
     legacy_commitment_costs AS c
     LEFT JOIN legacy_cud_credits AS cr USING (usage_start_time, cud_product, service)
   GROUP BY
     1,
     2,
     3
 ),
 legacy_commitment_amount AS (
   SELECT
     usage_start_time,
     pd.cud_product,
     SUM(usage.amount_in_pricing_units / 100) AS commitment_amount
   FROM
     legacy_cost_data
     JOIN cud_product_data AS pd ON REGEXP_CONTAINS(sku.description, pd.cud_fee_regex)
   GROUP BY
     1,
     2
 ),
 legacy_utilized_commitment AS (
   SELECT
     usage_start_time,
     pd.cud_product,
     ABS(SUM(credit.amount / currency_conversion_rate)) AS utilized_commitment_amount
   FROM
     legacy_cost_data,
     UNNEST(credits) AS credit
     JOIN cud_product_data AS pd ON REGEXP_CONTAINS(credit.full_name, pd.cud_credit_regex)
   WHERE
     credit.type = 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE'
   GROUP BY
     1,
     2
 ),
 legacy_cud_utilization AS (
   SELECT
     ca.usage_start_time,
     ca.cud_product,
     SAFE_DIVIDE(uc.utilized_commitment_amount, ca.commitment_amount) * 100 AS cud_utilization_percent
   FROM
     legacy_commitment_amount AS ca
     LEFT JOIN legacy_utilized_commitment AS uc USING (usage_start_time, cud_product)
 ),
 eligible_cud_skus AS (
   SELECT
     sku_id
   FROM
     UNNEST([ /* Insert the full list of CUD eligible SKUs 'F35A-5D39-DA9D', '7E09-0800-D3BA', '1641-654E-D130', 'D616-27D3-51E1'*/ ]) AS sku_id
 ),
 eligible_cud_spend AS (
   SELECT
     usage_start_time,
     SUM(cost) AS cost,
     SUM(IFNULL((
       SELECT
         SUM(credit.amount)
       FROM
         UNNEST(credits) AS credit
       WHERE
         credit.type IN ('COMMITTED_USAGE_DISCOUNT', 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE', 'DISCOUNT', 'FREE_TIER')
     ), 0)) AS costs_ineligible_for_cud
   FROM
     legacy_cost_data
     JOIN eligible_cud_skus ON sku.id = eligible_cud_skus.sku_id
   GROUP BY
     1
 ),
 total_cud_savings AS (
   SELECT
     c.usage_start_time,
     -1 * (c.cost + IFNULL(cr.spend_cud_credits, 0)) AS commitment_savings,
     cr.spend_cud_credits
   FROM (
     SELECT
       usage_start_time,
       SUM(cost) AS cost
     FROM
       legacy_cost_data
       JOIN cud_product_data pd ON REGEXP_CONTAINS(sku.description, pd.cud_fee_regex)
     GROUP BY
       1
   ) AS c
     LEFT JOIN (
       SELECT
         usage_start_time,
         SUM(credit.amount) AS spend_cud_credits
       FROM
         legacy_cost_data,
         UNNEST(credits) AS credit
       WHERE
         credit.type = 'COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE'
         AND REGEXP_CONTAINS(credit.full_name, 'GCE Commitments')
       GROUP BY
         1
     ) AS cr USING (usage_start_time)
 ),
 -- =================================================================================================
 -- Part 2: New Model Calculations (at or after migration)
 -- =================================================================================================
 new_model_commitment_costs AS (
   SELECT
     usage_start_time, -- Changed from invoice.month
     subscription.instance_id AS subscription_instance_id,
     IFNULL((
       SELECT
         l.value
       FROM
         UNNEST(labels) l
       WHERE
         l.key = 'goog-originating-service-id'
     ), service.id) AS service,
     SUM(cost) AS commitment_cost,
     SUM((
       SELECT
         SUM(credit.amount)
       FROM
         UNNEST(credits) credit
       WHERE
         credit.type = 'FEE_UTILIZATION_OFFSET'
     )) AS fee_utilization_offset
   FROM
     new_cost_data
     JOIN (
       SELECT
        *
       FROM
         UNNEST(['5515-81A8-03A2', 'B22F-51BE-D599']) fee_sku_id
     ) AS cud_fee_skus ON fee_sku_id = sku.id
   GROUP BY
     1,
     2,
     3
 ),
 new_model_cud_savings AS (
   SELECT
     usage_start_time, -- Changed from invoice.month
     subscription.instance_id AS subscription_instance_id,
     service.id AS service,
     SUM(cost - cost_at_effective_price_default) AS cud_savings_amount,
     SUM(cost_at_effective_price_default) AS on_demand_costs
   FROM
     new_cost_data
   WHERE
     consumption_model.id IS NOT NULL
     AND consumption_model.id IN ('D97B-0795-975B', '70D7-D1AB-12A4')
   GROUP BY
     1,
     2,
     3
 ),
 -- =================================================================================================
 -- Final Combination
 -- =================================================================================================
 legacy_kpis AS (
   SELECT
     cs.usage_start_time,
     'legacy' AS model_version,
     CAST(NULL AS STRING) AS subscription_instance_id,
     cs.cud_product,
     cs.service,
     cs.commitment_cost,
     cs.commitment_savings,
     u.cud_utilization_percent,
     NULL AS effective_savings_rate
   FROM
     legacy_commitment_savings AS cs
     LEFT JOIN legacy_cud_utilization AS u USING (usage_start_time, cud_product)
   UNION ALL
   SELECT
     es.usage_start_time,
     'legacy' AS model_version,
     CAST(NULL AS STRING) AS subscription_instance_id,
     NULL AS cud_product,
     NULL AS service,
     NULL AS commitment_cost,
     NULL AS commitment_savings,
     NULL AS cud_utilization_percent,
     SAFE_DIVIDE(s.commitment_savings, (es.cost + es.costs_ineligible_for_cud - IFNULL(s.spend_cud_credits, 0))) * 100 AS effective_savings_rate
   FROM
     eligible_cud_spend AS es
     LEFT JOIN total_cud_savings AS s USING (usage_start_time)
 ),
 new_kpis AS (
   SELECT
     ncc.usage_start_time,
     'new' AS model_version,
     CAST(ncc.subscription_instance_id AS STRING) AS subscription_instance_id,
     CAST(NULL AS STRING) AS cud_product,
     ncc.service,
     ncc.commitment_cost,
     ncc.commitment_cost + ncc.fee_utilization_offset + IFNULL(ncs.cud_savings_amount, 0) AS commitment_savings,
     SAFE_DIVIDE(ABS(ncc.fee_utilization_offset), ncc.commitment_cost) * 100 AS cud_utilization_percent,
     SAFE_DIVIDE((ncc.commitment_cost + ncc.fee_utilization_offset + IFNULL(ncs.cud_savings_amount, 0)), IFNULL(ncs.on_demand_costs, 1)) * 100 AS effective_savings_rate
   FROM
     new_model_commitment_costs AS ncc
     LEFT JOIN new_model_cud_savings AS ncs USING (usage_start_time, subscription_instance_id, service)
 )
SELECT
*
FROM
 legacy_kpis
UNION ALL
SELECT
*
FROM
 new_kpis;
```

## Related topics

- [Spend-based CUD program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline)
- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)
- [Migrated CUD SKUs, offers, and consumption model IDs](https://cloud.google.com/docs/cuds-migration)
- [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements)

   Was this helpful?

---

# Migrated CUD SKUs,offers,and new consumption modelsStay organized with collectionsSave and categorize content based on your preferences.

> Learn about the migrated CUD SKUs, offers, and consumption model IDs as part of the new CUDs program.

# Migrated CUD SKUs,offers,and new consumption modelsStay organized with collectionsSave and categorize content based on your preferences.

## New CUD product information

As part of the migration to the new CUD data model, all [in-scope
CUDs](https://cloud.google.com/docs/cuds-multiprice#affected-cuds)
have new offer IDs, new consumption model IDs, and new CUD fee SKU IDs. You can
use the following details to help you adjust your queries and dashboards.

### New offer IDs and consumption model IDs

The following table shows the new offer IDs and new consumption model IDs.

| Product Name | Term | Old Offer ID | New Offer ID | Consumption Model ID |
| --- | --- | --- | --- | --- |
| Cloud Run | 1 Year | 55435965-baf5-485f-baea-3fde53566e5e | 392802d4-e57b-40d3-9684-a1e8cdca6fb5 | 73A1-AD60-B867 |
| Cloud Run | 3 Years | a8b22b6c-2992-48d3-9b73-98fc7a47d61c | 88a5fc51-d63b-4865-bf3b-c49e05a8c5c0 | A4B6-DEDF-1A65 |
| Bigtable | 1 Year | 5a0a5567-1552-445e-9f1b-f1ac69fb0f39 | c0bf8ba5-65ee-4f7d-9e1e-3953433cf193 | A03A-2A56-8086 |
| Bigtable | 3 Years | 26e8485e-acef-4e73-9a13-f0b2109befff | 460fb2ef-456d-4263-a070-4f993fa37996 | 4F61-4520-4936 |
| Dataflow | 1 Year | 42ae4415-0361-404f-8bc5-1e7c041c2d82 | 127d79e4-1d52-48b0-9f31-8ba02586ff95 | 75D9-38E7-870F |
| Dataflow | 3 Years | cac998b8-3d49-4672-ae5b-e5b3c56e05f2 | 03f4d3b1-44b8-4e88-9e75-b1d4e2d04573 | 9E06-4EF0-37D8 |
| Memorystore for Redis | 1 Year | fe93270a-f338-4a76-b303-c323608a9d37 | 8e0da7cb-196b-4351-bc32-6a6ba94f1456 | DD5B-8EB3-C48D |
| Memorystore for Redis | 3 Years | 8f20579e-7630-4592-8fa6-0d7d3b749354 | 2a3729ac-1e38-4a34-bc96-bd988028351f | 8E4B-B283-45D8 |
| Cloud Spanner | 1 Year | 29829e5f-681c-4810-a471-8e4611a8042b | 359db5c2-8c2c-49e3-a21d-26176c4cd403 | 558C-892D-2291 |
| Cloud Spanner | 3 Years | 709f6c69-8a49-4032-97f7-ce21fe340603 | a6a32e10-1d76-4df8-8485-eee10d08a1cf | 38C3-A961-A68B |
| Kubernetes Engine | 1 Year | ae2672e6-47a8-41dc-9448-6956d7f4fbc1 | 2f48e468-a86a-452d-88df-edacd94a3c44 | 2F93-FEF4-BD6E |
| Kubernetes Engine | 3 Years | fcf378c1-fbe0-4aaa-b05e-9597f8b45578 | 89027902-6f83-40aa-8861-7c2446b11015 | 6E88-5C17-F3E1 |
| AlloyDB for PostgreSQL | 1 Year | adbca020-a973-48c9-b9b6-f5d70527790c | ff04ec3e-278c-4ec8-8278-12f875a8cea2 | C100-AA7B-33B1 |
| AlloyDB for PostgreSQL | 3 Years | 56e5948f-f1ed-45ce-84d6-a8408092e7d5 | 9522b4d8-bff7-4141-81d6-b71d9113c69a | 4920-CA74-2184 |
| Cloud SQL | 1 Year | 266e6a8c-2a0d-4b92-af9c-5795760f1fc9 | d31cf078-36a2-4a8a-a2e6-b23caec0e7a3 | 61F8-639B-D89C |
| Cloud SQL | 3 Years | 4998bf0a-51dd-4ce0-8405-aa529dd86d33 | 48960309-1646-4fa2-9bf8-d7e72090d2b8 | 52FB-D69D-95BE |
| Compute Flexible | 1 Year | ffe0f6a3-2f98-437e-8d49-fc443a05d3c2 | 1b2601a4-9d76-462d-bd5b-5b835d245f93 | D97B-0795-975B |
| Compute Flexible | 3 Years | 062a285d-8989-4ce7-8f9a-bed8d183236f | 61612674-a9a9-4687-8449-baca71fbd0d1 | 70D7-D1AB-12A4 |
| Managed Service for Apache Kafka | 1 Year | e1636f7d-1a29-4d53-a89e-c1f60e8dadcf | 647db981-009c-4e95-b62e-6aff19384956 | 03DE-CED5-0B0E |
| Managed Service for Apache Kafka | 3 Years | 31d79333-0c0e-4208-9b20-c6e4f27e5d1d | 9a7ed994-d3df-4680-b4e6-7c3d932add66 | FBB4-D107-5857 |
| Cloud Firestore | 1 Year | f8485012-b340-4562-8302-7e27d48f8cfd | de6aa077-3170-4250-89b6-0ccd470f9e21 | 3892-BA17-92A7 |
| Cloud Firestore | 3 Years | 0b48b55a-1fa6-48bc-a3de-2d88f0b99e15 | e8f59240-c088-4a22-87c3-e58722cca300 | 2FD9-44B6-D2AC |
| BigQuery | 1 Year | 6e72d4d4-5591-4c7f-aa9f-88d277d9280c | d73ae4d8-d096-4c9b-9c20-cd92c3c53724 | DD83-D9A3-79AF |
| BigQuery | 3 Years | ad5539c4-a0d9-4abd-82c9-1104a7c8ad64 | f43d480d-3e77-4079-946c-e1b2ab640a8a | 4D8D-49A7-C5B1 |
| Backup For Oracle | 1 Year | 5b446c4d-ce38-4d1a-8c76-e8b04ad50069 | 16e6132e-8a72-4a7f-8941-bf52246afc82 | AEA3-CEC2-9DF3 |
| Backup For Oracle | 3 Years | 0dba7aa1-3215-4d44-9581-e1c34ca94471 | 1e028b05-4344-4bca-87e7-235ee3536354 | 224F-258C-7F84 |

### New CUD Fee SKUs

The following tables show the old and new CUD fee SKU IDs, per product.

#### Cloud Run

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 3491-4A9E-B163 | 82DD-7D25-A063 |
| 15D9-4AD0-A9B7 | AB82-48AE-6F3A |
| 10A9-4C3F-BB16 | A1B8-DECC-D1F7 |
| 3301-404B-B3EF | E5D3-CEFB-02D4 |
| CFB2-4EB2-9990 | 090D-54AC-DA77 |
| 8837-4C45-A7DA | 41C3-F36A-16D9 |
| 4867-4C8F-B76A | 02B2-B3FA-95FF |
| C5B8-425D-97D5 | F4A5-B4CF-3788 |
| E0CE-460F-8D64 | 46A3-E4AA-351A |
| 74A6-44D2-960C | 4407-BF28-CF37 |
| 7859-4826-8C52 | 19BF-9700-359E |
| AA48-4683-AF1F | 8974-2D16-9117 |
| B508-4B0F-B7BB | 2F4D-5F46-993B |
| 3BF1-4FB4-83F2 | BD61-7988-3E95 |
| A57E-4819-AF94 | A716-5EEA-8CEE |
| 1B33-49CF-B32F | 1B45-09D5-5F07 |
| 1210-4E9B-A04D | BB5E-6431-CCA8 |
| 80E4-45AE-A1AF | 947D-BBB3-5380 |
| BA12-4198-A539 | D9E1-9988-DB66 |
| 4C73-409B-A4F1 | 9169-B592-96AF |
| 865F-4611-92E1 | 931E-6A8E-E314 |
| BF34-44E8-91A6 | 408B-0952-2677 |
| 15BA-4E4A-992E | 89BF-B220-F319 |
| E00E-4B5F-B8BD | 1719-823D-05F0 |
| ECF8-4229-BC67 | B1DA-56DC-EC9F |
| 973E-434A-801F | EA00-7F7B-944D |
| 3552-4DD3-A7E8 | 9CFC-DEAA-A82B |
| 4552-4772-A6F6 | 3898-3657-CECE |
| 06EA-D424-083A | E255-3419-0687 |
| 6FE3-4982-4D7A | 5F70-CBCF-4F13 |
| D14C-4A3B-80A6 | 03CC-6BAC-3FE9 |
| B202-4829-9B84 | 81D8-AFBA-BB76 |
| 20AE-4E52-B828 | F5E2-7791-3712 |
| 552F-4CC8-99A1 | 8BFE-E1FE-8066 |
| A9CC-4C7B-A5D9 | DF3D-33E3-8AD0 |
| 9CB8-4FD1-8CD9 | 03DD-CE93-0CE3 |
| 33FF-492C-8385 | 7E0C-A90C-6CCB |
| 9422-4554-83D9 | C823-5E65-5B1E |
| 0638-44AB-9DF9 | 804C-2860-D291 |
| 5209-48D5-9FA5 | CEDA-B53B-B6DD |
| 7A23-4F77-BA5C | 5684-226D-B356 |
| 8187-444D-8CD0 | 047C-F7E7-E5CD |
| 13D2-4FA4-A8E0 | 4F47-9C0A-D62B |
| 7630-473A-8C92 | FE58-B5C7-E882 |
| 0B46-4BA0-913E | 3B69-08EE-4E6E |
| EB81-4CDD-94E4 | 2488-2C37-724F |
| 83A5-422F-8FBB | 2A9F-A082-92D7 |
| 100C-4499-9C9B | 5B2A-EE57-91E3 |
| BCDC-49BB-9D32 | E9C0-4BCD-7D32 |
| 18F0-430F-9067 | B9A5-A3B0-D95F |
| B13B-4D35-9798 | FCC6-5787-1F3C |
| BD0A-4FBC-8912 | 9FA3-FFEA-92BC |
| 4E43-44D2-82BC | 309B-91F8-C95D |
| 1127-425D-A3C0 | 738D-8CAD-9A3B |
| 4FF9-4DDE-8B5D | 4CC1-460A-9FF1 |
| 7608-491D-B962 | 7011-33D8-298B |
| 8C7A-4ABA-A82B | 4284-87CF-A006 |
| A650-43B3-A5E6 | 3BFB-24B0-73E4 |
| 71AA-41B0-9A01 | 691E-644F-6644 |
| 59DD-4247-B7F7 | CC1A-95E6-D6EB |
| BCBA-4D9D-9F55 | 2A32-2138-B345 |
| 95C7-472A-AED4 | 30ED-3509-C62D |
| 0760-B78B-9026 | DDC3-5FD5-A0B6 |
| A1F6-87A0-FE7E | A8FA-9147-ABB5 |
| 21D4-45D3-9D60 | 1EE3-51D2-3396 |
| 5485-49C0-B8EB | B0B4-343F-135D |
| 4CBE-4359-9150 | 6093-28F8-6788 |
| C51F-4A06-9E7C | F33E-8239-F352 |
| F62F-4B66-9291 | 9FB6-C854-5100 |
| 6B98-4F1A-B5B5 | FAF0-0ECD-9314 |
| CAFE-418A-853C | EAAC-55EA-2E64 |
| 420E-4559-A155 | BCF2-B50C-03B9 |
| DA27-406E-B0B0 | 52EA-5CFF-7F43 |
| E147-4670-92DC | 7E41-C976-49DD |
| 8B4F-4C3D-9FDA | 4E7A-8DA1-AD53 |
| F0E7-4A07-828B | FDDF-1F04-6258 |
| 51BF-496E-97B0 | 3485-48FC-C988 |
| D83D-43BD-9CE9 | 1E98-BE57-4954 |
| FFFE-459E-AA3A | 29A9-0609-9125 |
| 879E-4DD5-9563 | 6683-573B-AEBF |
| A342-4583-9883 | 514E-BB03-A6F5 |
| 6CEC-4088-9057 | 9EF2-4BCB-6A7A |
| 288E-4410-B596 | 3071-1939-D0B5 |
| 02B6-47BE-9322 | 9CA4-124C-2041 |
| 059C-46F1-9D30 | 1E77-1051-139B |
| 0208-4868-BB79 | 75EF-1DBD-84EA |
| A37A-4CBB-8C2A | 54B3-12CB-2105 |
| 3AB6-4ED4-9DFD | 8F45-B49A-430F |
| C39C-4F0E-8356 | 3F20-8CC9-6406 |
| 8E40-4212-9075 | 37C7-19B2-BE1B |
| 8B23-49BA-A445 | 56B5-8B48-DAA8 |
| FFDA-4C02-97F5 | B2E8-0BA2-6F9E |

#### Bigtable

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| B5A6-424E-9B40 | 3A81-0BBB-DB6B |
| D0B1-4BBE-B88E | 80F1-1914-BE00 |

#### Dataflow

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| B010-4451-8FE0 | 9E04-DE04-2E16 |
| A151-46E9-B512 | 09B2-AF74-BAD1 |

#### Memorystore For Redis

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 15A2-40AC-9DCD | 8C3A-9182-D105 |
| C4C9-475B-BEFF | EF24-D476-1BAD |

#### Cloud Spanner

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 131F-4968-89D1 | 3238-2675-F039 |
| 75AD-448A-95DE | 80C0-BC99-0991 |

#### Kubernetes Engine

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 8AC5-995C-49BE | CC42-04B0-71A9 |
| 4643-4C68-3D9E | 080E-0344-2B2F |
| D4CC-4550-92C1 | 237A-224A-C622 |
| 292A-4422-B188 | 9607-3DD9-8D78 |
| CAFC-43E1-9291 | 6FFC-4E81-8ECA |
| CA8D-496F-86F4 | D634-1142-E1DD |
| 787B-46D9-80CC | 825F-9C72-CE1C |
| FEAB-4A93-849F | F986-9574-3D32 |
| 3D8D-4826-AE85 | EC2F-D6E6-6DC2 |
| 28C5-4353-B536 | 2279-940A-C438 |
| 3F48-4DB8-A865 | 2ED8-47E3-FCF4 |
| 1566-42A4-931C | 282D-9866-204C |
| 050E-4401-87A1 | CA20-3B01-28F7 |
| CDB8-47E5-A134 | 59AF-8D6A-6F93 |
| A38D-42A4-AB93 | 9B4B-9C98-A1C1 |
| 0C28-42D3-9354 | BF16-00E1-9106 |
| 22D5-4505-87E0 | A045-427D-09F5 |
| 5406-46FC-B538 | FD8F-FDDC-078F |
| 69BD-4ED5-A9D4 | 8572-D615-AD9D |
| AB2C-4C01-B3AE | 3630-EF1B-2849 |
| 9940-4B80-8F2D | DF19-A1EF-AC84 |
| 29B1-476B-A3DB | B6D8-7A7B-2327 |
| 1E09-4D6B-A08F | 1DD6-B96F-9F27 |
| 48DF-4B4E-82A6 | 5FAA-AF2F-2CFF |
| CFB5-43DC-A225 | DB7F-F9C1-F79F |
| 6E00-453A-AD09 | 8E6B-7160-6255 |
| 6E7C-45B4-A4AC | 2EFE-41D6-A0C2 |
| 7792-4C59-A018 | 10F6-AFF0-0AFF |
| 2FA1-3003-EB9D | 960E-36EC-8042 |
| 7713-78D0-0F12 | 3E91-E048-B73C |
| C468-411F-855C | 1256-77D9-0785 |
| AE7A-43D7-92D6 | A816-98F0-52A4 |
| 8C09-9532-9994 | 1FA3-D1FF-DF7D |
| 126A-5503-0210 | E225-278E-E970 |
| 1C8A-2D9A-EF3A | 544B-6343-3D8A |
| 7246-58AB-2C77 | 2426-FF2F-0C1A |
| CBA4-4F0A-B6EA | 0506-34EE-01BB |
| 8118-4430-9AE6 | B1D8-AED9-A5BA |
| 3346-4681-9789 | D2AF-530E-0C1E |
| 68AA-48D8-BACB | 4770-2E09-F22D |
| 8994-46B7-8815 | 24E8-5C67-2FA1 |
| 28D9-45E5-A3DD | 9650-1FA3-E633 |
| 2B69-4C94-BF9E | 6BBB-0D1E-F6A0 |
| 3786-4FA4-BFC4 | B1F5-F09E-9D52 |
| 7706-4477-A57C | 92A3-6AD1-1CDC |
| 87D6-42D9-9F62 | BBD9-D7C3-575B |
| 21E7-322C-27F2 | E01E-1EF6-7971 |
| 341E-CEB6-046E | D90C-946F-2B5E |
| AD40-52E0-FE6C | F6DF-FCCA-46C5 |
| 802C-66F0-3337 | D66E-D04C-046D |
| 8B7F-F32F-26D1 | 1F34-433C-2846 |
| 1AA3-04A4-3E0D | A7A1-5FAE-4B5E |
| BC4D-78A4-A637 | 3EAD-2395-D76A |
| BEAC-8E7A-2D03 | FA9B-EA76-BBF8 |
| 76D0-2F62-2BF8 | 49AB-FEFE-1FFC |
| AA6F-4C19-BF8F | B1B4-5EBE-BCD2 |
| 28B5-4B48-81D9 | 86DF-B23C-E1CD |
| ADDA-42C7-B88E | 90EC-1D9C-7D21 |
| 46F2-47A7-33EF | E6E7-57D4-9C0A |
| C2A4-1557-17BB | 148C-E8E8-47DB |
| 960E-4BAF-BA31 | 1653-1F57-D31D |
| AF6C-4CFA-A138 | 876B-D94C-91BA |
| E753-8F76-0172 | D911-23CD-56DF |
| 4E22-CFF4-F8B5 | 6525-244F-BA05 |
| E007-44F3-AB00 | 6408-2258-A93E |
| D137-4062-A817 | F6D4-F4E6-A4E9 |
| 2951-40E8-9F50 | 65FB-4059-F5FE |
| 85A6-4DDF-A844 | CA80-AC52-9C98 |
| 4147-4BB2-B0AE | 3AFE-F408-82E4 |
| 69E0-47B1-8E89 | 1231-1AEB-C12D |
| 4010-49AF-81F2 | E84C-D51D-8BD9 |
| D864-472C-A694 | 5CDA-E09B-6022 |
| 243F-A48C-F7EF | 6D26-164E-1A01 |
| 6078-4495-46F5 | 1311-7F3B-818F |
| 93F1-4469-DABE | EB76-19CB-4ACB |
| C155-5C1F-4255 | 4DA3-B935-AE67 |
| 2E22-DE3D-8183 | 67F0-37CB-3E46 |
| 1C2C-3A27-09A4 | 8E2A-C5BF-989A |
| 90DA-4F69-9BF0 | 5124-2121-DC46 |
| 1DEA-4A3A-BE97 | 249B-0942-FD5B |
| AD12-4E74-AB33 | 2201-9FE1-AE72 |
| 1206-4292-B7B5 | BFC1-4238-31C5 |
| 60D1-4AAA-AEBB | 99FF-B3FC-0977 |
| 199A-4EFA-A898 | 360A-0EDD-20F6 |
| 1A3B-4A36-878D | A628-E73A-A7D9 |
| C83E-4CDC-8D3A | 9022-BB2D-48FD |
| 2BFF-48AA-1752 | 7D54-59A4-DB94 |
| DF97-6D3D-692F | EC34-4E0B-667F |

#### AlloyDB For PostgreSQL

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 7734-4CEB-A7D9 | 98FC-4179-825D |
| 9486-406B-8ED7 | 1989-EC4C-1D98 |

#### Cloud SQL

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 9D5B-87A9-EAC3 | 7BE0-E374-B1EB |
| A770-1549-F8EA | 2F30-30DA-482C |
| CF8D-4BC1-B957 | 2080-5BCD-9F5B |
| 3FE2-4DD8-B090 | A007-6570-4B0B |
| 3673-4665-96DC | 2D3A-EB5A-D80A |
| F4E5-4E4C-9EC6 | ACB8-45AE-4E5F |
| C242-48A2-A571 | 7A59-B85C-DFC6 |
| 1D4C-45A7-B37E | D32B-2B6E-5CA3 |
| 488D-482D-9543 | 0F65-F4F8-9ADD |
| B770-4F2C-87A0 | 0988-3A03-D2D0 |
| CEFD-4948-9339 | FC83-C9EF-C4EB |
| 2E6B-409B-9759 | EEF1-4F76-CAC5 |
| 0667-4EED-A427 | 7878-600A-64CC |
| F731-4BC8-B099 | 8BF0-605D-DCAD |
| 6098-26E0-DA90 | F8FE-F09B-8D35 |
| 3D97-72FB-A745 | 7E81-74D4-4C48 |
| B4F3-4753-84D8 | B247-B6A5-B42B |
| 8BC6-431C-83A0 | 7F34-9E6B-7BC9 |
| 2222-A6FD-1B34 | 6C75-9500-A545 |
| 52F4-C022-9628 | 696E-7A2B-022B |
| 1CEC-44BF-A72F | F1D9-293C-905B |
| 40B4-4A3F-9ADE | 0B7E-2F8F-2091 |
| 5C18-C0DE-424C | E8EE-4E7C-A1BF |
| E2C2-75CF-0834 | FAD7-E6E2-FDEC |
| 82AD-EFDB-31EB | B316-B58B-DB2F |
| A462-30B5-2815 | 2C5E-F50B-ABA3 |
| 08CF-4B12-9DDF | 6DA1-960A-8264 |
| 9A44-4649-A4BA | 5F97-E2D9-D908 |
| 1D65-0D70-30D9 | 7D50-89D5-ADA7 |
| 42AE-51A3-4BA6 | 8EB6-5293-4347 |
| AC25-43CD-B2CF | BCE7-3E2D-E6B4 |
| 5BBD-4280-BDAA | 3969-6A93-428C |
| 4E88-49D2-A8CA | 676C-96F3-A28B |
| 2F5E-1738-A349 | 1D2B-767A-C27A |
| EF34-C6E5-642A | A63F-26C0-0B5D |
| D828-2DE2-B6E9 | 6EC2-F52B-AFDC |
| BB36-4ABF-964B | C6AF-A820-F06F |
| 0B80-4201-92E9 | 2815-72DD-688F |
| D74A-49A5-A0F3 | D70C-6262-E655 |
| AEE9-48F0-8F1B | 04DE-7EE7-4993 |
| 4752-4CCD-A896 | 5D05-BF2A-90B6 |
| 1046-418C-80D5 | 8225-3967-A427 |
| D948-7796-816E | 3B87-C788-A1F7 |
| 9705-467B-A0C7 | 4D55-316F-A430 |
| E5E4-4AAB-8E72 | 6CD7-D35C-F75E |
| 7D57-410C-88E6 | CB3A-4E59-80BB |
| BB27-9695-34DB | 1440-FD58-A7E1 |
| 43C1-1E6F-B339 | 175F-18C1-FFAC |
| 7B24-9F72-4868 | 025D-CDA8-6051 |
| 1585-37B8-2C7C | 4D4A-15C1-8651 |
| FD3D-B041-5D8B | 01B6-1103-473E |
| FA42-12B8-92F4 | E40E-9744-A5C7 |
| D495-4DEF-5C3D | 49F7-68DD-3287 |
| 50B7-9B49-78AD | 2F50-AA2C-17E8 |
| CB27-32EF-3A69 | CE5E-FF5D-E8E4 |
| 052B-DDF0-EF60 | BE7D-D12F-2FE7 |
| C978-4C07-962E | 76A9-FC9C-60AB |
| 313C-4901-A0DF | 5912-F0F8-9BB2 |
| BB74-D061-874C | A5FC-B0A2-23C0 |
| 1B05-93AA-D889 | 644E-57BA-68FE |
| 1E40-0BE2-0127 | 245F-F68B-DC02 |
| A8A3-DA81-5FC1 | A707-293C-E2F8 |
| 5DBA-4145-8DA5 | 7FD7-0B89-CD20 |
| 6D15-4BF1-8C40 | 2002-A615-BF6B |
| D7C4-37F2-B8FA | B9B3-307F-28D9 |
| 4AA3-5BA3-56C2 | 7427-1C2E-1FB5 |
| 21EA-441C-A33F | 7424-6E54-5CD0 |
| 0B85-44DC-8DB0 | 6C6B-13F3-10E4 |
| 8AA4-4E86-978A | 4E2B-C2E9-DB94 |
| 2724-478C-985F | 249B-CA7E-76BD |
| EA96-4BD2-8085 | 33D8-2A9A-DAEE |
| 5E58-40A1-99ED | 1EFF-46BA-57F9 |
| C388-21EC-0FBE | 4AE3-2CBF-8EAA |
| 2339-A716-18EA | 53EA-4696-1650 |
| F250-468F-B2AE | 0529-A8D8-BF5A |
| 8165-F576-1404 | A26C-35CA-F0B8 |
| 19DE-C9CA-DDC6 | 7498-BC05-A2E1 |
| 447B-6CF7-811F | 116E-20AE-C903 |
| 65FF-4DA1-9D5B | 53E6-C7B8-C112 |
| E666-4D19-9465 | CA16-1FA5-F7E4 |
| B2D6-4532-8EC8 | D09C-4C1F-E156 |
| DF06-4741-84C3 | ECC5-8690-6A62 |
| 199A-4F7E-815F | F8A8-74F4-4FA3 |
| DFEF-4140-B12C | 97E5-A7CD-1BF3 |
| 0DB3-69AD-F2E0 | F71D-B6A4-310F |
| 28F7-A86D-E3AD | 3030-C394-9387 |

#### Compute Flexible

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| F61D-4D51-AAFC | 5515-81A8-03A2 |
| 6723-40D7-8BDC | B22F-51BE-D599 |

#### Managed Service For Apache Kafka

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 8A47-8B1D-C883 | 6B52-5BF3-396B |
| 02BD-82A5-FB44 | 0480-9719-DA84 |

#### BigQuery

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 5C25-BA1C-6AC3 | F000-3255-30F7 |
| 85A1-A5CB-A253 | A133-260C-A5ED |
| 1089-2A27-7730 | D1D5-1109-F1BE |
| 22CF-7E63-10C5 | DA54-C6B9-3587 |
| FC38-FFBD-D72C | A6C1-CEAD-E3EA |
| 61AD-1D3B-D83A | B7D3-119B-713F |
| 7A19-ACF7-3170 | 81A9-185D-8B9E |
| 8F1D-ADEC-2837 | B769-CB81-7010 |
| E1FD-1AAE-BAC3 | CE9C-6026-EAF1 |
| BA9B-1B34-062D | 126B-1147-892C |
| B518-6B3B-41BE | E548-4400-D30A |
| BC97-D9AC-36B6 | 1EFB-B150-3E5E |
| F5B4-8B94-2EEC | 67E8-E098-A01A |
| 16C8-7C38-3239 | 49DB-2BB3-94C9 |
| 7637-096D-622B | 1381-E895-3149 |
| FEB4-715D-30FF | 70B5-F887-399D |
| E116-56B9-FB0A | F28C-5980-130D |
| 380B-3E0B-FD7E | A18F-AF50-E629 |
| E251-BF64-0789 | 37F2-2F57-7D71 |
| 4B5D-E66F-A172 | A804-A110-F1AA |
| CDDF-5E64-7B2D | 86CC-F087-FEBE |
| 5DD6-DA23-9199 | 3814-70D6-EC39 |
| F2E5-5205-B520 | EF36-D8BC-BF62 |
| 51AD-E0EB-150A | 3893-D7F1-5961 |
| C279-46E5-BC9D | 993D-3AFA-2C6D |
| C102-E006-F6FD | F8BA-95FE-EA91 |
| 38C2-4F8B-B035 | 0004-187C-DE75 |
| 32A8-9021-5BD5 | C04C-B96D-4A84 |
| 23F5-5744-16EB | 15AA-0087-D18E |
| A2C7-4AD6-A2C6 | 9AE8-2B2E-9464 |
| 3166-210F-DE55 | 1D65-1DCA-05FE |
| F2F0-0F54-689D | 1F53-D6C9-B57A |
| 74F4-4E1B-06EF | 8CFB-26B1-CF35 |
| F65E-9014-E2CF | 77AE-7A35-21AF |
| 32A8-1856-364F | D707-19EF-8882 |
| 6D08-0C10-CF4F | 2AB8-0AC7-CDA1 |
| 9D7D-D20E-6C52 | F219-044A-0599 |
| 23AB-C773-7CCB | 3F16-8F6A-3A2E |
| 5B41-2E03-EE6B | FA89-BCC4-7723 |
| 72FB-2DE8-9CF3 | 474C-4EC7-9153 |
| F397-9DD1-8408 | 34A7-AD9B-B373 |
| 47BD-22A8-B9FA | C493-8773-3DC3 |
| B8F4-F944-3999 | 7DC0-4FE2-7D72 |
| 5A1D-25D0-4DD4 | 6DC6-A111-AF25 |
| A8C9-8053-F4C3 | 9902-D4A8-4DDD |
| FE8E-B140-8A2B | 416E-5116-4B9F |
| 44DD-7AB8-81B7 | FE3E-6C65-B711 |
| 41D5-58D9-B80D | 0187-7D96-8A07 |
| 8F29-24C6-F828 | DBAC-DC77-7C2E |
| EE58-E484-950D | CA44-8A5B-0CAE |
| B3F0-B4AA-5ABE | 91D5-8E34-A91B |
| C401-6820-D68F | C656-B0D7-DE2D |
| 677E-AF33-A71C | E617-E502-440B |
| 48D9-5554-B194 | 4BCC-3982-623D |
| 2A6A-75A1-8052 | 7CD3-FB97-83F7 |
| 43C7-F7A2-2DF1 | 6DB0-16B2-7D11 |
| A187-636B-D5A3 | 6D66-35BE-F070 |
| 5A75-1900-8479 | 5249-BD73-90B0 |
| 5E39-16C7-C280 | C29B-E97D-DE4B |
| FC92-0AE2-5B99 | 4553-C64D-DAF5 |
| FB7B-18F0-24BF | F3DF-45A6-AAF7 |
| 5A3A-2581-6A90 | 64FB-50DE-2B78 |
| 7EE8-7905-E68A | B296-6C48-B00A |
| 729B-5A59-EC36 | 674E-B7E3-9EDC |
| DDAD-F25F-F336 | E883-C2B3-8B4E |
| 091C-95A6-E3A9 | 6AB4-06A7-EE13 |
| C19D-100F-DEC0 | 80E8-6BBE-9163 |
| 09CF-F2CD-F4CC | 7592-C1C2-0D77 |
| 6CB5-3496-932C | 0A90-CD4E-D30E |
| 6C6D-A7DB-97E9 | 3869-FAC2-CCA2 |
| 995B-4155-179A | 1488-9EA4-3E18 |
| 845D-60E9-0120 | 173E-4EF9-FC23 |
| 7E0C-F2E7-C1F1 | 0B18-F5D9-DACC |
| 5E9E-8E31-FEE2 | 5514-A3D6-79FC |
| 5DE9-5597-C15E | 249F-ADE9-7DED |
| 1D9E-3390-78AC | 6234-FBD2-BB63 |
| BC9A-0555-CADE | B713-BA02-ED74 |
| 04E0-4165-0061 | B272-5B4D-D466 |
| 9009-F18E-930D | 804C-DE02-60F4 |
| 8E10-56F3-B2E2 | 1222-7D7D-FC15 |
| A1C6-0ABC-B0C2 | 4C12-1B3C-D796 |
| 5F0C-E6BB-9AF1 | 977D-C6F2-A8A4 |
| 8DD7-E7F8-FD4E | 37C3-EFCF-3DD3 |
| D77C-204C-E1DC | 00AE-16F3-50C5 |
| 4BD0-DA84-69FE | D4D0-3E8D-7C4B |
| 1227-9303-9DF2 | 160B-98BE-D874 |
| 177D-91E7-05D7 | 2144-0A92-A45A |
| 6659-6ACE-4D24 | 264D-9FB8-F290 |
| 8C0C-CB94-91B4 | CC5A-B5E1-BE39 |
| A5D1-411A-BE45 | 458E-86C9-D76E |
| F949-A74B-2E23 | 7652-043A-65C9 |
| 8864-725F-B5C2 | 08D3-11AC-E124 |

#### Cloud Firestore

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 250C-5A4E-27F9 | 6849-C9A1-9662 |
| 63F9-F5D7-D6BC | 2CF5-3983-EA95 |

#### Backup and DR for Oracle

| Old Fee SKU ID | New Fee SKU ID |
| --- | --- |
| 7938-39D4-78B6 | DA30-A778-1421 |
| 73D2-5A5A-CB09 | 0D95-F79A-4CFA |

## Related topics

- [Spend-based CUD program improvements](https://cloud.google.com/docs/cuds-multiprice)
- [Spend-based CUD data model changes](https://cloud.google.com/docs/cuds-multiprice-datamodel)
- [Timelines for new CUD model migration](https://cloud.google.com/docs/cuds-new-model-timeline)
- [Verify your discounts after migration](https://cloud.google.com/docs/cuds-verify-discounts)
- [Choose the correct amount of CUD to buy](https://cloud.google.com/docs/cuds-choose-correctly)
- [Sample queries for the new CUDs data model](https://cloud.google.com/docs/cuds-example-queries)
- [Billing user interface improvements](https://cloud.google.com/docs/cuds-billing-ui-improvements)

   Was this helpful?
