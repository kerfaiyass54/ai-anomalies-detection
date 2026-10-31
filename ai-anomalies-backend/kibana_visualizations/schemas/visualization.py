from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class KibanaVisualization(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str = ""
    visualization_type: str | None = None
    updated_at: datetime | None = None
    vis_state: dict[str, Any] | None = None
    search_source: dict[str, Any] | None = None
    references: list[dict[str, Any]] = Field(default_factory=list)
