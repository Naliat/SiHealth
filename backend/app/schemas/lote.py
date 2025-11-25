from pydantic import BaseModel, ConfigDict, computed_field
from typing import Optional
from datetime import date, timedelta, datetime

# ... (LoteBase, LoteCreate e LoteUpdate continuam iguais) ...
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

# --- AQUI É A MUDANÇA ---
class LoteResponse(LoteBase):
    id_lote: int
    id_medicamento: int
    quantidade_atual: int
    criado_em: datetime # Assumindo que você importou datetime lá em cima

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def status(self) -> str:
        hoje = date.today()
        # Regra de 30 dias para alerta (pode mudar para 60 se quiser)
        alerta_dias = timedelta(days=30) 

        if self.data_validade < hoje:
            return "Vencido"
        elif self.data_validade <= (hoje + alerta_dias):
            return "Próx. Venc."
        else:
            return "OK"