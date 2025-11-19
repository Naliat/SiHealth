from odmantic import Model
from datetime import datetime

class Usuario(Model):
    nome: str
    email: str
    senha_hash: str
    criado_em: datetime = datetime.now()
