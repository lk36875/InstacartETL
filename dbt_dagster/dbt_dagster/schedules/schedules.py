"""Schedules for dbt_dagster."""

from dagster import ScheduleDefinition

from dbt_dagster.jobs import dbt_orders_build_asset_job

schedules = [
    ScheduleDefinition(
        job=dbt_orders_build_asset_job,
        job_name="materialize_dbt_models",
        cron_schedule="0 0 * * *",  # Run daily at 12 AM
    ),
]
