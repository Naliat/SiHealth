from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EntradaBase(BaseModel):
    quantidade: int
    fornecedor: Optional[str] = None

class EntradaCreate(EntradaBase):
    id_lote: int
    id_usuario: int # No futuro, pegaremos isso do Token de Login

class EntradaResponse(EntradaBase):
    id_entrada: int
    id_lote: int
    data_entrada: datetime

    model_config = ConfigDict(from_attributes=True)