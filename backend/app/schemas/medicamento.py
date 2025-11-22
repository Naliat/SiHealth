from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Base: Campos comuns (evita repetição de código)
class MedicamentoBase(BaseModel):
    nome: str
    fabricante: Optional[str] = None
    principio_ativo: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None

# Create: O que o usuário envia para CRIAR (POST)
class MedicamentoCreate(MedicamentoBase):
    pass  # Herda tudo da base, todos os campos opcionais lá continuam opcionais

# Update: O que o usuário envia para ATUALIZAR (PUT/PATCH)
# Tudo vira opcional aqui, pois posso querer mudar só o 'fabricante'
class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    fabricante: Optional[str] = None
    principio_ativo: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None

# Response: O que a API devolve para o usuário
class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    criado_em: datetime

    # Configuração necessária para o Pydantic ler os dados do SQLAlchemy (ORM)
    model_config = ConfigDict(from_attributes=True)