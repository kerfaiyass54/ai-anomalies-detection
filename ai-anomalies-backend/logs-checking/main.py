from fastapi import FastAPI

from .apis import router as runtime_router

app = FastAPI(title="AI Anomalies Backend", version="0.1.0")
app.include_router(runtime_router)
