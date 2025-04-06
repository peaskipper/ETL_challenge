CREATE OR REPLACE TABLE data_foundation_dev.stg.dim_subcat AS
SELECT DISTINCT
    subcat_id,
    subcat_label,
    cat_id
FROM data_foundation_dev.raw.hier_prod_dlm
WHERE subcat_id IS NOT NULL;
