from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Base: Campos comuns
class MedicamentoBase(BaseModel):
    nome: str
    fabricante: Optional[str] = None
    principio_ativo: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    tarja: Optional[str] = None 
    
    descricao: Optional[str] = None

# ... O restante do arquivo (Create, Update, Response) continua igual ...
# ... pois eles herdam de MedicamentoBase ...

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    fabricante: Optional[str] = None
    principio_ativo: Optional[str] = None
    dosagem: Optional[str] = None
    categoria: Optional[str] = None
    tarja: Optional[str] = None # Adicionei aqui também para permitir atualizar só a tarja
    descricao: Optional[str] = None

class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)