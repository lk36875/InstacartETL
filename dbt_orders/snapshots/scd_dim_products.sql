{% snapshot scd_dim_products %}

{{
    config(
        target_schema='DEV',
        unique_key='product_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deleted_rows=True
    )
}}

select * from {{ ref('dim_products') }}

{% endsnapshot %}