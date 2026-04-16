from .pipeline import FinancePipeline
from .settings import PipelineSettings

from dataclasses import asdict


def create_settings(
        parms: dict | None = None,
        endpoints: dict | None = None,
        base_url: str | None = None,
) -> PipelineSettings:

    settings = PipelineSettings()

    if parms:
        settings.params = parms

    elif endpoints:
        settings.endpoints = endpoints

    elif base_url:
        settings.base_url = base_url

    return settings


def setup_pipeline(settings: PipelineSettings) -> FinancePipeline | None:
    try:
        print("Setting up Finance Pipeline")

        if not settings.token:
            raise Exception("No token provided, stopping pipeline")

        settings_dict = asdict(settings)
        pipeline = FinancePipeline(**settings_dict)

        print("All ready to run!")

        return pipeline

    except Exception as err:
        print(f"Error while setting up pipeline: {err}")
        return None

def run_pipeline(**kwargs) -> None:

    settings = create_settings(**kwargs)
    pipeline = setup_pipeline(settings)

    if not pipeline:
        return
    pipeline.run()
