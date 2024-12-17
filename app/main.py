from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.secrets.routes import secret_router
from app.users.routes import user_router

app = FastAPI(title="One Time Secret")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(secret_router, prefix="", tags=["secrets"])
app.include_router(user_router, prefix="/auth", tags=["users"])
