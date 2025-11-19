from odmantic import Model, Field
from bson import ObjectId
from datetime import datetime

class Entrada(Model):
    id_lote: ObjectId = Field()
    id_usuario: ObjectId = Field()
    quantidade: int
    data_entrada: datetime = Field(default_factory=datetime.now)
    fornecedor: str
