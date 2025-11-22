from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class PacienteBase(BaseModel):
    nome: str
    cns: str
    cpf: Optional[str] = None
    data_nascimento: date
    sexo: Optional[str] = None # 'M', 'F'

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id_paciente: int
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)