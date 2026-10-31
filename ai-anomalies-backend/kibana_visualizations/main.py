from fastapi import FastAPI

from .apis import router

app = FastAPI(title="Kibana Visualizations Service", version="0.1.0")
app.include_router(router)
