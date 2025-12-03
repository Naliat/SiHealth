# app/schemas/relatorio.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# Representa uma linha da tabela do relatório
class RelatorioDispensacaoItem(BaseModel):
    data_hora: datetime
    nome_medicamento: str
    fabricante: Optional[str] = None
    lote: str
    quantidade: int
    cns_paciente: str
    tipo_saida: str
    
    model_config = ConfigDict(from_attributes=True)

# Resposta final da API (JSON)
class RelatorioResponse(BaseModel):
    periodo_inicio: str
    periodo_fim: str
    total_registros: int
    itens: List[RelatorioDispensacaoItem]