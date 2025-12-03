# app/schemas/medicamento.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base agora é bem enxuta
class MedicamentoBase(BaseModel):
    nome: str
    principio_ativo: Optional[str] = None
    tarja: Optional[str] = None

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    principio_ativo: Optional[str] = None
    tarja: Optional[str] = None

class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)