from pydantic import BaseModel
from typing import Optional

class Medicamento_completo(BaseModel):
    id: str
    nome: str
    principio_ativo: str
    dosagem: str
    fabricante: Optional[str] = None
    
    numero_caixa: Optional[int] = None
    lote: Optional[str] = None
    validade: Optional[str] = None
    quantidade_atual: Optional[int] = None
    quantidade_por_caixa: Optional[int] = None
