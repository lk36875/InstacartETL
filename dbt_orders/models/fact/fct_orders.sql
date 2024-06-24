{{
    config(
        materialized = 'incremental',
        on_schema_change = 'fail'
    )
}}

with stg_orders as (
    select *
    from {{ ref("stg_orders") }}
),
stg_order_products as (
    select *
    from {{ ref("stg_order_products") }}
),
orders_w_date_key as (
    select
        order_id,
        user_id,
        cast(
            to_char(order_date, 'YYYYMMDD') || 
            lpad(order_hour_of_day, 2, '0') 
            as int
        ) as date_key
    from stg_orders
)
select
    {{ dbt_utils.generate_surrogate_key(['o.order_id', 'o.user_id', 'op.product_id', 'o.date_key']) }} as order_product_id,
    o.order_id,
    o.user_id,
    o.date_key,
    op.product_id,
    op.cart_sequence_number
from orders_w_date_key o
left join stg_order_products op
    on o.order_id = op.order_id

{% if is_incremental() %}
    {% if var("start_date", False) and var("end_date", False) %}
        where o.date_key between {{ var("start_date") }} and {{ var("end_date") }}
    {% else %}
        where o.date_key > (select max(date_key) from {{ this }})
    {% endif %}
{% endif %}
