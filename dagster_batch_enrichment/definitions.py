from dagster import Definitions, define_asset_job, ScheduleDefinition, AssetSelection
from dagster_batch_enrichment.api import EnrichmentAPI
from dagster_batch_enrichment.warehouse import MyWarehouse
from dagster_batch_enrichment.assets import raw_data, enriched_data


# define a job and schedule to run the pipeline
# alternatively could use freshness policies and auto-materialization, partitions, or other ways to orient the schedule
run_assets_job = define_asset_job(
    name="run_etl_pipeline",
    selection=AssetSelection.all()
)

run_assets_5min = ScheduleDefinition(
    name="run_assets_5min",
    job=run_assets_job,
    cron_schedule="*/5 * * * *"
)

defs = Definitions(
    assets=[raw_data, enriched_data],
    schedules=[run_assets_5min],
    jobs=[run_assets_job],
    resources={
        "api": EnrichmentAPI(),
        # place holder for a real warehouse with required connection config
        "warehouse": MyWarehouse(path="raw_data.csv")
    }
)