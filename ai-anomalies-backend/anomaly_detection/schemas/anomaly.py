from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


LogSourceType = Literal["k8s", "docker", "jenkins"]


class AnomalyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int | None = None
    occurred_at: datetime
    source_type: LogSourceType
    details: str
    score: float


class AnomalyDetectionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str
    model_version: str
    lines_processed: int
    anomalies_saved: int
    anomalies: list[AnomalyRecord]
