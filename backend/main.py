from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users

app = FastAPI(title="Meu Backend com FastAPI + MongoDB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restrinja
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
