"""Module contains all the job definitions for the dbt-dagster project."""

from dagster import ScheduleDefinition, define_asset_job

from dbt_dagster.assets.base import (
    dbt_orders_build_asset,
    dbt_orders_full_refresh_run_asset,
    dbt_orders_test_asset,
)
from dbt_dagster.assets.seed_dim_date import (
    dbt_orders_dim_date_asset,
    dbt_orders_seed_asset,
)

dbt_orders_test_asset_job = define_asset_job(name="dbt_orders_test_job", selection=[dbt_orders_test_asset])

dbt_orders_full_refresh_run_asset_job = define_asset_job(
    name="dbt_orders_full_refresh_run_job",
    selection=[dbt_orders_full_refresh_run_asset],
)

dbt_orders_dim_date_asset_job = define_asset_job(name="dbt_orders_dim_date_job", selection=[dbt_orders_dim_date_asset])

dbt_orders_seed_asset_job = define_asset_job(name="dbt_orders_seed_job", selection=[dbt_orders_seed_asset])


dbt_orders_build_asset_job = define_asset_job(name="dbt_orders_build_job", selection=[dbt_orders_build_asset])

dbt_orders_build_asset_schedule = ScheduleDefinition(
    job=dbt_orders_build_asset_job,
    cron_schedule="0 0 * * *",
    description="Runs daily at 12 AM.",
)

dbt_orders_dimdate_seed_asset_job = define_asset_job(
    name="dbt_orders_seed_dimdate_job",
    selection=[dbt_orders_dim_date_asset, dbt_orders_seed_asset],
)


ALL_JOBS = [
    dbt_orders_test_asset_job,
    dbt_orders_full_refresh_run_asset_job,
    dbt_orders_dim_date_asset_job,
    dbt_orders_seed_asset_job,
    dbt_orders_build_asset_job,
    dbt_orders_dimdate_seed_asset_job,
]
