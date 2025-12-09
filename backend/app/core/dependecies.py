# app/api/dependencies.py
from fastapi import Header, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

# Nome da variável na sua .env
SYSTEM_PASSWORD = os.getenv("SYSTEM_SECRET_PASSWORD", "senha_padrao")

async def verificar_senha_mestra(x_admin_pass: str = Header(..., alias="X-Admin-Pass")):
    """
    O FastAPI vai buscar automaticamente um Header chamado 'X-Admin-Pass'.
    Se não vier, ou vier errado, ele nem deixa a função da rota rodar.
    """
    if x_admin_pass != SYSTEM_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha de administrador incorreta. Acesso negado."
        )
    return True