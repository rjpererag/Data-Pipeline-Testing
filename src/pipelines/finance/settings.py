from decouple import config
from dataclasses import dataclass, field
from typing import Any

_DEFAULT_PARAMS = {
    "symbol": "btc",
    "threshold": 100000
}

_DEFAULT_ENDPOINTS = {}


@dataclass(frozen=False)
class PipelineSettings:
    token: str = config("FINANCE_PIPELINE_CLIENT_TOKEN")
    base_url: str = config("FINANCE_PIPELINE_BASE_URL")
    params: dict[str, Any] = field(
        default_factory=lambda: _DEFAULT_PARAMS.copy()
    )
    endpoints: dict[str, Any] = field(
        default_factory=lambda: _DEFAULT_ENDPOINTS.copy()
    )
