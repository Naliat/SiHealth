# app/schemas/lote.py
from pydantic import BaseModel, ConfigDict, computed_field
from typing import Optional
from datetime import date, timedelta, datetime

# Schema auxiliar para mostrar o nome do remédio dentro do lote
class MedicamentoResumo(BaseModel):
    id_medicamento: int
    nome: str
    principio_ativo: Optional[str] = None
    tarja: Optional[str] = None

class LoteBase(BaseModel):
    numero_lote: str
    numero_caixa: Optional[str] = None
    quantidade_inicial: int
    data_validade: date
    data_fabricacao: Optional[date] = None
    quantidade_por_caixa: Optional[int] = None
    
    # --- NOVOS CAMPOS (Agora obrigatórios ou opcionais na criação do Lote) ---
    fabricante: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None

class LoteCreate(LoteBase):
    id_medicamento: int 

class LoteUpdate(BaseModel):
    quantidade_atual: Optional[int] = None
    # Adicione aqui se quiser permitir atualizar fabricante/dosagem depois

class LoteResponse(LoteBase):
    id_lote: int
    id_medicamento: int
    quantidade_atual: int
    criado_em: datetime
    
    # Traz os dados básicos do remédio
    medicamento: Optional[MedicamentoResumo] = None

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def status(self) -> str:
        hoje = date.today()
        alerta = timedelta(days=30)
        if self.data_validade < hoje:
            return "Vencido"
        elif self.data_validade <= (hoje + alerta):
            return "Próx. Venc."
        else:
            return "OK"