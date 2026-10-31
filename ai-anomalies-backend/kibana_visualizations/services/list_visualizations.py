import json
from typing import Any

from ..errors import KibanaVisualizationServiceError
from ..schemas import KibanaVisualization, KibanaVisualizationPage
from .kibana_saved_objects import find_visualization_objects


def _parse_json_attribute(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _to_visualization(saved_object: dict[str, Any]) -> KibanaVisualization:
    attributes = saved_object.get("attributes")
    if not isinstance(attributes, dict):
        raise ValueError("Kibana visualization attributes are missing.")
    vis_state = _parse_json_attribute(attributes.get("visState"))
    metadata = attributes.get("kibanaSavedObjectMeta") or {}
    if not isinstance(metadata, dict):
        metadata = {}
    search_source = _parse_json_attribute(metadata.get("searchSourceJSON"))
    return KibanaVisualization(
        id=saved_object["id"],
        title=attributes.get("title", ""),
        description=attributes.get("description", ""),
        visualization_type=vis_state.get("type") if vis_state else None,
        updated_at=saved_object.get("updated_at"),
        vis_state=vis_state,
        search_source=search_source,
        references=saved_object.get("references", []) if isinstance(saved_object.get("references", []), list) else [],
    )


def list_visualizations(*, page: int = 1, per_page: int = 100, search: str | None = None) -> KibanaVisualizationPage:
    payload = find_visualization_objects(page=page, per_page=per_page, search=search)
    saved_objects = payload.get("saved_objects")
    if not isinstance(saved_objects, list):
        raise KibanaVisualizationServiceError("Kibana returned an invalid saved-objects response.")
    try:
        return KibanaVisualizationPage(
            page=int(payload.get("page", page)),
            per_page=int(payload.get("per_page", per_page)),
            total=int(payload.get("total", 0)),
            visualizations=[_to_visualization(item) for item in saved_objects],
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise KibanaVisualizationServiceError("Kibana returned an invalid visualization object.") from exc
