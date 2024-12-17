from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.secrets.routes import secret_router
from app.users.routes import user_router

app = FastAPI(
    title="OneTimeSecret API",
    description="This project implements a service for securely storing and sharing one-time secrets",
    version="1.0.0",
    contact={
        "name": "Roman Pecheritsa",
        "email": "pecheritsa.roman@gmail.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(secret_router, prefix="", tags=["secrets"])
app.include_router(user_router, prefix="/auth", tags=["users"])
