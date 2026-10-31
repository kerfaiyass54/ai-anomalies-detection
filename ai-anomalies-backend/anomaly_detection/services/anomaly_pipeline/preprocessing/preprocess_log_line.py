import re
from datetime import datetime, timezone

from ....schemas.processed_log import ProcessedLog

_TIMESTAMP = re.compile(
    r"^\[?(?P<timestamp>\d{4}-\d{2}-\d{2}[T ][0-9:.+-]+(?:Z)?)\]?\s*"
)
_UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,}\b")
_IP_ADDRESS = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_NUMBER = re.compile(r"\b\d+\b")


def preprocess_log_line(line: str, *, occurred_at: datetime | None = None) -> ProcessedLog | None:
    """Parse a single event and normalize variable timestamps and identifiers."""
    original = line.strip()
    if not original:
        return None

    event_time = occurred_at or datetime.now(timezone.utc)
    match = _TIMESTAMP.match(original)
    message = original
    if match:
        timestamp = match.group("timestamp").replace("Z", "+00:00")
        try:
            event_time = datetime.fromisoformat(timestamp)
            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=timezone.utc)
            message = original[match.end():].strip()
        except ValueError:
            pass

    normalized = _UUID.sub("<UUID>", message)
    normalized = _IP_ADDRESS.sub("<IP>", normalized)
    normalized = _NUMBER.sub("<NUM>", normalized)
    return ProcessedLog(original, normalized, event_time) if normalized else None
