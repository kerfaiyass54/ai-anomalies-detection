from typing import Any

from pydantic import BaseModel, ConfigDict


class LogEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    index: str
    source: dict[str, Any]
