from collections import deque
from threading import Lock
from time import monotonic

from prometheus_client import Gauge

ANOMALY_RATE = Gauge(
    "anomaly_rate",
    "Number of anomalies detected during the preceding 60 seconds.",
)
_anomaly_times: deque[float] = deque()
_lock = Lock()
_WINDOW_SECONDS = 60.0


def record_anomalies(count: int) -> None:
    if count <= 0:
        return
    now = monotonic()
    with _lock:
        _anomaly_times.extend([now] * count)
        _refresh(now)


def refresh_anomaly_rate() -> None:
    with _lock:
        _refresh(monotonic())


def _refresh(now: float) -> None:
    cutoff = now - _WINDOW_SECONDS
    while _anomaly_times and _anomaly_times[0] <= cutoff:
        _anomaly_times.popleft()
    ANOMALY_RATE.set(len(_anomaly_times))
