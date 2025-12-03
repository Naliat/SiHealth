from sqlalchemy.orm import Session
from app.models.saida import Saida
from app.schemas.saida import SaidaCreate

class SaidaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, saida: SaidaCreate, total_calculado: int):
        # Transforma o Pydantic em dict
        dados = saida.model_dump()

        # Remove campos de cálculo que não existem na tabela
        dados.pop('numero_de_caixas', None)
        dados.pop('quantidade_por_caixa', None)

        # Cria o objeto do banco mapeando os campos corretamente
        db_saida = Saida(
            **dados,
            quantidade_total_retirada=total_calculado
        )
        
        self.db.add(db_saida)
        return db_saida