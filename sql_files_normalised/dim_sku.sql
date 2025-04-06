CREATE OR REPLACE TABLE data_foundation_dev.stg.dim_sku AS
SELECT DISTINCT
    sku_id,
    sku_label,
    stylclr_id,
    stylclr_label,
    styl_id,
    issvc,
    isasmbly,
    isnfs
FROM data_foundation_dev.raw.hier_prod_dlm
WHERE sku_id IS NOT NULL;