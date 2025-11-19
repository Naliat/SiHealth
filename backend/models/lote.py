# models/lote.py
from odmantic import Model, Field
from datetime import date, datetime
from bson import ObjectId

class Lote(Model):
    id_medicamento: ObjectId
    numero_lote: str = Field(unique=True)
    numero_caixa: str
    quantidade_por_caixa: int
    quantidade_inicial: int
    quantidade_atual: int
    data_fabricacao: datetime
    data_validade: datetime
    criado_em: datetime = Field(default_factory=datetime.utcnow)
