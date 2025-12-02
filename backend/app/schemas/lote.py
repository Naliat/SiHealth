from pydantic import BaseModel, ConfigDict, computed_field
from typing import Optional
from datetime import date, timedelta, datetime

# --- NOVO SCHEMA AUXILIAR ---
# Criamos esse pequeno modelo só para mostrar os dados do remédio dentro do lote
class MedicamentoResumo(BaseModel):
    id_medicamento: int
    nome: str
    dosagem: Optional[str] = None
    principio_ativo: Optional[str] = None
    fabricante: Optional[str] = None
    tarja: Optional[str] = None

# ... (LoteBase, LoteCreate, LoteUpdate continuam iguais) ...
class LoteBase(BaseModel):
    numero_lote: str
    numero_caixa: Optional[str] = None
    quantidade_por_caixa: Optional[int] = None
    quantidade_inicial: int
    data_fabricacao: Optional[date] = None
    data_validade: date

class LoteCreate(LoteBase):
    id_medicamento: int 

class LoteUpdate(BaseModel):
    numero_lote: Optional[str] = None
    quantidade_atual: Optional[int] = None
    data_validade: Optional[date] = None

class LoteResponse(LoteBase):
    id_lote: int
    id_medicamento: int
    quantidade_atual: int
    criado_em: datetime

    # --- AQUI ESTÁ A MÁGICA ---
    # O campo deve ter o MESMO nome do relacionamento no Model (lote.py -> medicamento)
    medicamento: MedicamentoResumo 
    # --------------------------

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def status(self) -> str:
        hoje = date.today()
        alerta_dias = timedelta(days=30) 
        if self.data_validade < hoje:
            return "Vencido"
        elif self.data_validade <= (hoje + alerta_dias):
            return "Próx. Venc."
        else:
            return "OK"