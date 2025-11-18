# from fastapi import APIRouter
# from database import engine
# from models import User

# router = APIRouter(prefix="/users", tags=["Users"])

# @router.post("/")
# async def create_user(user: User):
#     await engine.save(user)
#     return {"message": "Usuário criado com sucesso!"}

# @router.get("/")
# async def list_users():
#     return await engine.find(User)
