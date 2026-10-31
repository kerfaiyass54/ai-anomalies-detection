from fastapi import APIRouter

from .container_logs import router as container_logs_router
from .containers import router as containers_router
from .pod_logs import router as pod_logs_router
from .pods import router as pods_router

router = APIRouter()
router.include_router(containers_router)
router.include_router(container_logs_router)
router.include_router(pods_router)
router.include_router(pod_logs_router)
