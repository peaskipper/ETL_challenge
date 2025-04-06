CREATE OR REPLACE TABLE data_foundation_dev.stg.dim_cat AS
SELECT DISTINCT
    cat_id,
    cat_label,
    dept_id
FROM data_foundation_dev.raw.hier_prod_dlm
WHERE cat_id IS NOT NULL;
