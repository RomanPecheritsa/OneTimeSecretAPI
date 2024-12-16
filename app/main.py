from fastapi import FastAPI

from app.routes.secret_route import secret_router
from app.routes.user_route import user_router

app = FastAPI(title="One Time Secret")

app.include_router(secret_router, prefix="")
app.include_router(user_router, prefix="/auth")
