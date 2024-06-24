import json

from dagster import AssetExecutionContext, Config
from dagster_dbt import DbtCliResource, KeyPrefixDagsterDbtTranslator, dbt_assets

from dbt_dagster.constants import dbt_manifest_path
from typing import Iterator


class DimDateAssetConfig(Config):
    """The configuration schema for the `dim_date` dbt asset."""

    dim_date_start_date: str
    dim_date_end_date: str


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=KeyPrefixDagsterDbtTranslator(asset_key_prefix="seed"),
    select="resource_type:seed",
)
def dbt_orders_seed_asset(context: AssetExecutionContext, dbt: DbtCliResource) -> Iterator:
    """
    This function is a Dagster asset definition that uses the `dbt_assets` decorator to
    define a dbt asset that is seeded by running the dbt `seed` command.

    Args:
        context: The asset execution context.
        dbt: The dbt CLI resource that is used to interact with dbt.

    Yields:
        An iterator of the asset materialization events.
    """
    yield from dbt.cli(["seed"], context=context).stream()


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=KeyPrefixDagsterDbtTranslator(asset_key_prefix="dim_date"),
    select="dim_date",
)
def dbt_orders_dim_date_asset(
    context: AssetExecutionContext, dbt: DbtCliResource, config: DimDateAssetConfig
) -> Iterator:
    """
    This function is a Dagster asset definition that uses the `dbt_assets` decorator to
    define a dbt asset that is built by running the dbt `build` command with custom variables.
    Custom variables are used to define the `dim_date_start_date` and `dim_date_end_date`.

    Args:
        context: The asset execution context.
        dbt: The dbt CLI resource that is used to interact with dbt.
        config: The configuration for the `dim_date` dbt asset.

    Yields:
        An iterator of the asset materialization events.
    """
    dbt_vars = {
        "dim_date_start_date": config.dim_date_start_date,
        "dim_date_end_date": config.dim_date_end_date,
    }

    dbt_build_args = ["build", "--vars", json.dumps(dbt_vars)]

    yield from dbt.cli(dbt_build_args, context=context).stream()
