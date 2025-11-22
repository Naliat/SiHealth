from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime

class LoteBase(BaseModel):
    numero_lote: str
    numero_caixa: Optional[str] = None
    quantidade_por_caixa: Optional[int] = None
    quantidade_inicial: int
    data_fabricacao: Optional[date] = None
    data_validade: date

class LoteCreate(LoteBase):
    # Obrigatório informar o ID do medicamento ao criar o lote
    id_medicamento: int 

class LoteUpdate(BaseModel):
    numero_lote: Optional[str] = None
    quantidade_atual: Optional[int] = None # Podemos ajustar estoque manualmente se necessário
    data_validade: Optional[date] = None
    # Adicione outros campos se quiser permitir edição

class LoteResponse(LoteBase):
    id_lote: int
    id_medicamento: int
    quantidade_atual: int # Retorna o estoque atual calculado/armazenado
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)