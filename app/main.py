from fastapi import FastAPI
from app.routes.secrets_route import router

app = FastAPI(title="One Time Secret")

app.include_router(router, prefix="")
