from fastapi import APIRouter

from .configuration import router as configuration_router

router = APIRouter()
router.include_router(configuration_router)
