from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    ativo: bool = True

class UsuarioCreate(UsuarioBase):
    senha: str # Senha é obrigatória na criação

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    criado_em: datetime
    # NUNCA retornamos a senha na resposta

    model_config = ConfigDict(from_attributes=True)