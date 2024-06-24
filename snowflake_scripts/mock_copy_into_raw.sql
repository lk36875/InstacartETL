
use DW_Manage;

create or replace file format DW_Manage.file_formats.csv_format
    type='csv',
    skip_header = 1
    field_optionally_enclosed_by = '"';

create or replace storage integration azure_integration
    type = external_stage
    storage_provider = azure
    enabled = true
    azure_tenant_id = '---'
    storage_allowed_locations = ('azure://snowflake0dwh.blob.core.windows.net/raw-data');

desc integration azure_integration;

create or replace stage DW_Manage.external_stages.orders_stage
    storage_integration = azure_integration
    url = 'azure://snowflake0dwh.blob.core.windows.net/raw-data/orders/'
    file_format = DW_Manage.file_formats.csv_format;

list @DW_Manage.external_stages.orders_stage;


create or replace stage DW_Manage.external_stages.products_stage
    storage_integration = azure_integration
    url = 'azure://snowflake0dwh.blob.core.windows.net/raw-data/products/'
    file_format = DW_Manage.file_formats.csv_format;

list @DW_Manage.external_stages.products_stage;

create or replace stage DW_Manage.external_stages.order_products_stage
    storage_integration = azure_integration
    url = 'azure://snowflake0dwh.blob.core.windows.net/raw-data/order_products/'
    file_format = DW_Manage.file_formats.csv_format;

list @DW_Manage.external_stages.order_products_stage;


use DW_Orders.RAW;

create or replace table orders (
    order_id int,
    user_id int,
    eval_set varchar(30),
    order_number int,
    order_dow int,
    order_hour_of_day varchar(10),
    days_since_prior_order number(10,2),
    order_date date
);

copy into orders
from @DW_Manage.external_stages.orders_stage;

select * from orders limit 10;

create or replace table products (
    product_id int,
    product_name varchar,
    aisle_id int,
    department_id int,
    updated_at date
);

copy into products
from @DW_Manage.external_stages.products_stage;


select * from products limit 10;


create or replace table order_products (
    order_id int,
    product_id int,
    add_to_cart_order int,
    reordered int
);

copy into order_products
from @DW_Manage.external_stages.order_products_stage;


select * from order_products limit 10;
