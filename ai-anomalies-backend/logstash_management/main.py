from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .apis.configuration import router

app = FastAPI(title="Logstash Configuration Service", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_methods=["GET", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(router)
