with raw_orders as (
    select *
    from {{ source('dw_orders', 'raw_orders') }}
)
select
    order_id,
    user_id,
    order_hour_of_day,
    order_date
from raw_orders