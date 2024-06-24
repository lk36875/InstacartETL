with raw_orders as (
    select *
    from {{ source('dw_orders', 'raw_order_products') }}
)
select
    order_id,
    product_id,
    add_to_cart_order as cart_sequence_number
from raw_orders