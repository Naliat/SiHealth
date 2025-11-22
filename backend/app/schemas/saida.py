from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SaidaBase(BaseModel):
    numero_de_caixas_entregues: int
    quantidade_por_caixa: int
    observacao: Optional[str] = None

class SaidaCreate(SaidaBase):
    id_lote: int
    id_paciente: int
    id_usuario_responsavel: int 

class SaidaResponse(SaidaBase):
    id_saida: int
    quantidade_total_entregue: int
    data_saida: datetime

    model_config = ConfigDict(from_attributes=True)