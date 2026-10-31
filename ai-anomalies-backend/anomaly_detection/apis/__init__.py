from fastapi import APIRouter

from .anomalies import router as anomalies_router

router = APIRouter()
router.include_router(anomalies_router)
