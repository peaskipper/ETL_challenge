CREATE OR REPLACE TABLE data_foundation_dev.stg.dim_styl AS
SELECT DISTINCT
    styl_id,
    styl_label,
    subcat_id
FROM data_foundation_dev.raw.hier_prod_dlm
WHERE styl_id IS NOT NULL;