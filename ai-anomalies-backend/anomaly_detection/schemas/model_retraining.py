from pydantic import BaseModel, ConfigDict, Field


class ModelRetrainingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str
    model_version: str
    training_rows: int = Field(ge=1)
    holdout_rows: int = Field(ge=1)
