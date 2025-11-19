from odmantic import Model, Field
from datetime import datetime

class Medicamento(Model):
    nome: str
    fabricante: str
    principio_ativo: str
    dosagem: str
    categoria: str
    descricao: str | None = None
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "collection": "medicamentos"
    }