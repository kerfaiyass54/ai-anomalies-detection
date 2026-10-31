from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


BinaryLabel = Annotated[int, Field(strict=True, ge=0, le=1)]


class ModelEvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(min_length=1, max_length=255)
    model_version: str = Field(min_length=1, max_length=64)
    y_true: list[BinaryLabel] = Field(min_length=1)
    y_pred: list[BinaryLabel] = Field(min_length=1)

    @model_validator(mode="after")
    def labels_have_same_length(self) -> "ModelEvaluationRequest":
        if len(self.y_true) != len(self.y_pred):
            raise ValueError("y_true and y_pred must contain the same number of labels.")
        return self


class ModelEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    evaluated_at: datetime
    model_name: str
    model_version: str
    samples_evaluated: int = Field(ge=1)
    precision: float = Field(ge=0.0, le=1.0)
    recall: float = Field(ge=0.0, le=1.0)
    f1_score: float = Field(ge=0.0, le=1.0)
    classification_report: dict[str, Any]
    input_sha256: str = Field(min_length=64, max_length=64)


class ModelEvaluationPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    per_page: int
    total: int
    evaluations: list[ModelEvaluation]


class ModelEvaluationSeries(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evaluations: list[ModelEvaluation]
