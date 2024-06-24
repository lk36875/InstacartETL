with raw_products as (
    select *
    from {{ source('dw_orders', 'raw_products') }}
)
select
    product_id,
    product_name,
    aisle_id,
    department_id,
    updated_at
from raw_products