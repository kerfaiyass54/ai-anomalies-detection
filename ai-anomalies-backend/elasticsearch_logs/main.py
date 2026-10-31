from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .apis.logs import router as logs_router

app = FastAPI(title="Elasticsearch Logs Service", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)
app.include_router(logs_router)
