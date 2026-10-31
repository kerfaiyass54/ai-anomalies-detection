from fastapi import APIRouter, HTTPException

from ..errors import KibanaVisualizationServiceError
from ..schemas import KibanaVisualization
from ..services import get_visualization

router = APIRouter(prefix="/api/v1/kibana/visualizations", tags=["Kibana visualizations"])


@router.get("/{visualization_id}", response_model=KibanaVisualization)
def get_visualization_by_id(visualization_id: str) -> KibanaVisualization:
    try:
        return get_visualization(visualization_id)
    except KibanaVisualizationServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
