from ..errors import KibanaVisualizationServiceError
from ..schemas import KibanaVisualization
from .kibana_saved_objects import get_visualization_object
from .list_visualizations import _to_visualization


def get_visualization(visualization_id: str) -> KibanaVisualization:
    saved_object = get_visualization_object(visualization_id)
    if saved_object.get("type") != "visualization":
        raise KibanaVisualizationServiceError("Kibana returned an unexpected saved-object type.")
    try:
        return _to_visualization(saved_object)
    except (KeyError, TypeError, ValueError) as exc:
        raise KibanaVisualizationServiceError("Kibana returned an invalid visualization object.") from exc
