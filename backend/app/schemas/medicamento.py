from pydantic import BaseModel, ConfigDict, computed_field, Field
from typing import Optional, List
from datetime import date, timedelta, datetime

# 1. Criamos um Schema simples só para ler a validade do lote
# Fazemos isso aqui mesmo para evitar erros de importação circular
class LoteSimples(BaseModel):
    data_validade: date
    quantidade_atual: int
    
    model_config = ConfigDict(from_attributes=True)

class MedicamentoBase(BaseModel):
    nome: str
    fabricante: Optional[str] = None
    principio_ativo: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    tarja: Optional[str] = None
    descricao: Optional[str] = None

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    fabricante: Optional[str] = None
    principio_ativo: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    tarja: Optional[str] = None
    descricao: Optional[str] = None

class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    criado_em: datetime

    # --- A CORREÇÃO MÁGICA ESTÁ AQUI ---
    # Declaramos que este modelo TEM uma lista de lotes, para o Pydantic ler do banco.
    # Mas usamos exclude=True para NÃO enviar essa lista pro Front-end (JSON).
    lotes: List[LoteSimples] = Field(default=[], exclude=True) 
    # -----------------------------------

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def status_geral(self) -> str:
        # Agora self.lotes EXISTE porque declaramos ele ali em cima!
        
        # Se a lista estiver vazia
        if not self.lotes:
            return "Sem Estoque"

        hoje = date.today()
        alerta = hoje + timedelta(days=30)
        
        tem_vencido = False
        tem_alerta = False
        tem_estoque_valido = False

        for lote in self.lotes:
            # Lógica de negócio
            if lote.quantidade_atual > 0:
                if lote.data_validade < hoje:
                    tem_vencido = True
                elif lote.data_validade <= alerta:
                    tem_alerta = True
                else:
                    tem_estoque_valido = True
        
        # Prioridades
        if tem_vencido:
            return "Vencido"
        elif tem_alerta:
            return "Prox. Venc."
        elif tem_estoque_valido:
            return "OK"
        else:
            return "Sem Estoque"