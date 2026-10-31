from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ProcessedLog:
    original: str
    normalized: str
    occurred_at: datetime
