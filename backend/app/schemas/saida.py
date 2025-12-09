# app/schemas/saida.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SaidaBase(BaseModel):
    # Dados do Paciente
    cns_paciente: str
    nome_paciente: Optional[str] = None
    numero_receita: Optional[str] = None
    
    # Dados da Saída
    tipo_saida: str 
    observacao: Optional[str] = None
    quantidade: int

# INPUT: O usuário digita o NÚMERO do lote, não o ID
class SaidaCreate(SaidaBase):
    numero_lote: str

# OUTPUT: O sistema responde com os dados salvos
class SaidaResponse(SaidaBase):
    id_saida: int
    data_saida: datetime
    
    # Campo opcional para mostrar na confirmação qual remédio foi
    nome_medicamento_snapshot: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)