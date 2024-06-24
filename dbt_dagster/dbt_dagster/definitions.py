"""Definitions for the dbt_dagster project."""

import os

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from .assets import base, seed_dim_date
from .constants import dbt_project_dir
from .jobs import ALL_JOBS
from .schedules import schedules

all_assets = load_assets_from_modules([base, seed_dim_date])


defs = Definitions(
    assets=all_assets,
    jobs=ALL_JOBS,
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)
