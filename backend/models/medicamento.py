from odmantic import Model, Field
from datetime import datetime
from typing import Optional # <--- Adicione esta linha!


class Medicamento(Model):
    nome: str
    fabricante: str
    principio_ativo: str
    dosagem: str
    categoria: str
    
    # CORREÇÃO APLICADA
    descricao: Optional[str] = None
    
    criado_em: datetime = Field(default_factory=datetime.now)

    # O campo 'id' é implícito pelo Odmantic

    model_config = {
        "collection": "medicamentos"
    }