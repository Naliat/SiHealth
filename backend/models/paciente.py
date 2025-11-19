from enum import Enum
from odmantic import Model
from datetime import datetime

class Sexo(str, Enum):
    """Enum para representar o sexo do paciente"""
    MASCULINO = "M"
    FEMININO = "F"
    OUTRO = "O"

class Paciente(Model):
    nome: str
    CNS: str          # Cartão Nacional de Saúde (único)
    cpf: str | None = None
    data_nascimento: datetime | None = None
    sexo: str | None = None
    criado_em: datetime = datetime.now()

    
