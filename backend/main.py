from fastapi import FastAPI
from routes import users

app = FastAPI(title="Meu Backend com FastAPI + MongoDB")

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "API está rodando 🚀"}
