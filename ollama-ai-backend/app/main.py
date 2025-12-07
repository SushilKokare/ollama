from fastapi import FastAPI
from app.api.v1.routes import health,user

app = FastAPI(title="Base Template API", version="0.1.0")

app.include_router(health.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")