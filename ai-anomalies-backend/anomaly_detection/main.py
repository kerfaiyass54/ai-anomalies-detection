from fastapi import FastAPI

from . import settings  # noqa: F401 - load environment configuration before service imports
from .apis import router

app = FastAPI(title="Log Anomaly Detection Service", version="0.1.0")
app.include_router(router)
