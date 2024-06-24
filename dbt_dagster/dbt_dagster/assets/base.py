from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, KeyPrefixDagsterDbtTranslator, dbt_assets

from dbt_dagster.constants import dbt_manifest_path
from typing import Iterator


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=KeyPrefixDagsterDbtTranslator(asset_key_prefix="build"),
    exclude="resource_type:seed",
)
def dbt_orders_build_asset(context: AssetExecutionContext, dbt: DbtCliResource) -> Iterator:
    """
    This function is a Dagster asset definition that uses the `dbt_assets` decorator to
    define a dbt asset that is built by running the dbt `build` command.

    Args:
        context: The asset execution context.
        dbt: The dbt CLI resource that is used to interact with dbt.

    Yields:
        An iterator of the asset materialization events.
    """
    yield from dbt.cli(["build"], context=context).stream()


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=KeyPrefixDagsterDbtTranslator(asset_key_prefix="test"),
)
def dbt_orders_test_asset(context: AssetExecutionContext, dbt: DbtCliResource) -> Iterator:
    """
    This function is a Dagster asset definition that uses the `dbt_assets` decorator to
    define a dbt asset that is tested by running the dbt `test` command.

    Args:
        context: The asset execution context.
        dbt: The dbt CLI resource that is used to interact with dbt.

    Yields:
        An iterator of the asset materialization events.
    """
    yield from dbt.cli(["test"], context=context).stream()


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=KeyPrefixDagsterDbtTranslator(asset_key_prefix="full_refresh_run"),
)
def dbt_orders_full_refresh_run_asset(context: AssetExecutionContext, dbt: DbtCliResource) -> Iterator:
    """
    This function is a Dagster asset definition that uses the `dbt_assets` decorator to
    define a dbt asset that is built by running the dbt `run` command with the `--full-refresh` flag.

    Args:
        context: The asset execution context.
        dbt: The dbt CLI resource that is used to interact with dbt.

    Yields:
        An iterator of the asset materialization events.
    """
    yield from dbt.cli(["run", "--full-refresh"], context=context).stream()
