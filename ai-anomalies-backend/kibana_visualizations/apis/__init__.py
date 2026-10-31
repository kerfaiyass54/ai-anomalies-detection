from fastapi import APIRouter

from .get_visualization import router as get_visualization_router
from .list_visualizations import router as list_visualizations_router

router = APIRouter()
router.include_router(list_visualizations_router)
router.include_router(get_visualization_router)

__all__ = ["router"]
