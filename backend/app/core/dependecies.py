from fastapi import Header, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

# Pega a senha do .env (ou usa um valor padrão se não encontrar)
SYSTEM_PASSWORD = os.getenv("SYSTEM_SECRET_PASSWORD", "senha_padrao")

async def verificar_senha_mestra(x_admin_pass: str = Header(..., alias="X-Admin-Pass")):
    """
    Verifica se o header 'X-Admin-Pass' contém a senha correta.
    O 'alias' permite que o header tenha hífens, mas a variável python use underline.
    """
    if x_admin_pass != SYSTEM_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha de administrador incorreta. Acesso negado."
        )
    return True