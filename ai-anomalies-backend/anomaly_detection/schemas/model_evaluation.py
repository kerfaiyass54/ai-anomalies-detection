from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from .anomaly import LogSourceType


class ModelEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    evaluated_at: datetime
    source_type: LogSourceType
    model_name: str
    model_version: str
    logs_evaluated: int = Field(ge=1)
    anomalies_detected: int = Field(ge=0)
    anomaly_rate: float = Field(ge=0.0, le=1.0)
    mean_score: float
    median_score: float
    min_score: float
    max_score: float
    dataset_sha256: str = Field(min_length=64, max_length=64)


class ModelEvaluationPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    per_page: int
    total: int
    evaluations: list[ModelEvaluation]


class ModelEvaluationSeries(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evaluations: list[ModelEvaluation]
