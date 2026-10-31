from fastapi import APIRouter

from .anomalies import router as anomalies_router
from .evaluations import router as evaluations_router
from .evaluation_series import router as evaluation_series_router
from .get_evaluation import router as get_evaluation_router
from .model_retraining import router as model_retraining_router

router = APIRouter()
router.include_router(anomalies_router)
router.include_router(evaluations_router)
router.include_router(evaluation_series_router)
router.include_router(get_evaluation_router)
router.include_router(model_retraining_router)
