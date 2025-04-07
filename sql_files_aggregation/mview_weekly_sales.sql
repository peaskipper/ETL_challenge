select
    distinct concat_ws(':',`pos_site_id`,`sku_id`,`fsclwk_id`,`price_substate_id`,`type`) as weekly_sales_id,
    `pos_site_id`,
    `sku_id`,
    `fsclwk_id`, 
    `price_substate_id`,
    `type`,
    sum(`sales_units`), 
    sum(`sales_dollars`),
    sum(`discount_dollars`)
from raw.fct_transactions_dim fct_trans
group by 
    `pos_site_id`,
    `sku_id`,
    `fsclwk_id`, 
    `price_substate_id`,
    `type`
;