from enum import Enum
from odmantic import Model
from datetime import datetime
from typing import Optional 

class Sexo(str, Enum):
    """Enum para representar o sexo do paciente"""
    MASCULINO = "M"
    FEMININO = "F"
    OUTRO = "O"

class Paciente(Model):
    nome: str
    CNS: str          # Cartão Nacional de Saúde (único)
    cpf: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    sexo: Optional[Sexo] = None  # Usando o Enum 'Sexo'
    criado_em: datetime = datetime.now()