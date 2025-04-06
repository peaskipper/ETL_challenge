CREATE OR REPLACE TABLE data_foundation_dev.stg.dim_dept AS
SELECT DISTINCT
    dept_id,
    dept_label
FROM data_foundation_dev.raw.hier_prod_dlm
WHERE dept_id IS NOT NULL;