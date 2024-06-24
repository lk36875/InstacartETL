select
    distinct date_key
from {{ ref("fct_orders") }}
except
select date_key
from {{ ref("dim_date") }}