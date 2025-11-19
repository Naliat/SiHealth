from odmantic import Model, Field
from datetime import datetime
from bson import ObjectId

class Saida(Model):
    id_lote: ObjectId = Field(...)
    id_paciente: ObjectId = Field(...)
    id_usuario_responsavel: ObjectId = Field(...)
    
    numero_de_caixas_entregues: int
    quantidade_por_caixa: int
    quantidade_total_entregue: int
    
    data_saida: datetime = Field(default_factory=datetime.now)
    observacao: str | None = None

