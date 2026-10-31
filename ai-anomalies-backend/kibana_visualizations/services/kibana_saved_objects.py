import os
import re
from typing import Any
from urllib.parse import quote

import httpx

from ..errors import KibanaVisualizationServiceError

_SPACE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def _auth() -> tuple[str, str] | None:
    username = os.getenv("KIBANA_USERNAME", "")
    password = os.getenv("KIBANA_PASSWORD", "")
    if username or password:
        return username, password
    return None


def _headers() -> dict[str, str]:
    headers = {"Accept": "application/json"}
    api_key = os.getenv("KIBANA_API_KEY", "")
    if api_key:
        headers["Authorization"] = f"ApiKey {api_key}"
    return headers


def _saved_objects_url(path: str) -> str:
    base_url = os.getenv("KIBANA_URL", "http://kibana:5601").rstrip("/")
    space_id = os.getenv("KIBANA_SPACE", "default")
    if not _SPACE_ID_PATTERN.fullmatch(space_id):
        raise KibanaVisualizationServiceError("KIBANA_SPACE must be a valid Kibana space identifier.", status_code=500)
    space_path = "" if space_id == "default" else f"/s/{quote(space_id, safe='')}"
    return f"{base_url}{space_path}/api/saved_objects{path}"


def find_visualization_objects(*, page: int, per_page: int, search: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {
        "type": "visualization",
        "page": page,
        "per_page": per_page,
        "sort_field": "title",
    }
    if search:
        params["search"] = search
        params["search_fields"] = "title"

    return _request_json("GET", _saved_objects_url("/_find"), params=params)


def get_visualization_object(visualization_id: str) -> dict[str, Any]:
    encoded_id = quote(visualization_id, safe="")
    return _request_json("GET", _saved_objects_url(f"/visualization/{encoded_id}"), not_found=True)


def _request_json(method: str, url: str, *, params: dict[str, Any] | None = None, not_found: bool = False) -> dict[str, Any]:
    timeout = httpx.Timeout(float(os.getenv("KIBANA_REQUEST_TIMEOUT_SECONDS", "10")))
    try:
        response = httpx.request(
            method,
            url,
            params=params,
            headers=_headers(),
            auth=_auth(),
            timeout=timeout,
        )
        if not_found and response.status_code == 404:
            raise KibanaVisualizationServiceError("Kibana visualization was not found.", status_code=404)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Expected Kibana to return a JSON object.")
        return payload
    except KibanaVisualizationServiceError:
        raise
    except httpx.HTTPStatusError as exc:
        raise KibanaVisualizationServiceError(
            f"Kibana returned HTTP {exc.response.status_code} while retrieving saved visualizations."
        ) from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise KibanaVisualizationServiceError("Could not retrieve saved visualizations from Kibana.") from exc
