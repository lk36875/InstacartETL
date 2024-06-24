with date_dimension as (
    {{ 
    dbt_date.get_base_dates(
        start_date= var("dim_date_start_date"), 
        end_date= var("dim_date_end_date"), 
        datepart="hour"
    ) 
    }}
)
select
    cast(
        to_char(date_hour, 'YYYYMMDD') || 
        lpad(extract(hour from date_hour), 2, '0') 
        as int
    ) as date_key,
    date_hour,
    extract(year from date_hour) as year,
    extract(month from date_hour) as month,
    extract(day from date_hour) as day,
    dayofweek(date_hour) as day_of_week,
    extract(week from date_hour) as week_of_year,
    extract(quarter from date_hour) as quarter,
    extract(dayofyear from date_hour) as day_of_year,
    extract(hour from date_hour) as hour
from date_dimension