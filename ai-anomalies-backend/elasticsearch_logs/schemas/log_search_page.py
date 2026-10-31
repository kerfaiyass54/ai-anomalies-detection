from pydantic import BaseModel, ConfigDict

from .log_entry import LogEntry


class LogSearchPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int
    logs: list[LogEntry]
    next_cursor: str | None = None
