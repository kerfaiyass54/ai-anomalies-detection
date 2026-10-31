import os

import httpx

from ...errors import ConfigurationServiceError


def get_reload_counts() -> tuple[int, int]:
    api_url = os.getenv("LOGSTASH_API_URL", "http://logstash:9600").rstrip("/")
    try:
        response = httpx.get(f"{api_url}/_node/stats/reloads", timeout=3.0)
        response.raise_for_status()
        reloads = response.json().get("reloads", {})
        return int(reloads.get("successes", 0)), int(reloads.get("failures", 0))
    except (httpx.HTTPError, ValueError, TypeError) as exc:
        raise ConfigurationServiceError("Logstash reload API is unavailable.") from exc
