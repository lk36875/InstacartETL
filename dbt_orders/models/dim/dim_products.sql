with stg_products as (
    select *
    from {{ ref("stg_products") }}
),
seed_aisles as (
    select *
    from {{ ref("seed_aisles") }}
),
seed_departments as (
    select *
    from {{ ref("seed_departments") }}
)
select
    product_id,
    product_name,
    coalesce(aisles.aisle, 'unknown') as aisle,
    coalesce(dep.department, 'unknown') as department,
    updated_at
from stg_products products
left join seed_aisles aisles
    on products.aisle_id = aisles.aisle_id
left join seed_departments dep
    on products.department_id = dep.department_id
