# ... imports ...
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.repositories.medicamento import MedicamentoRepository
from app.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate

class MedicamentoService:
    def __init__(self, db: Session):
        self.medicamento_repo = MedicamentoRepository(db)

    # Método atualizado com todos os parâmetros
    def listar_medicamentos(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        nome: str = None, 
        tarja: str = None, 
        ordenar_por: str = None, 
        direcao: str = "asc"
    ):
        return self.medicamento_repo.get_all(
            skip=skip, 
            limit=limit, 
            nome_filtro=nome, 
            tarja_filtro=tarja,
            ordenar_por=ordenar_por, 
            direcao=direcao
        )

    # ... Mantenha o resto (criar, update, delete) igual ...
    def criar_medicamento(self, dados: MedicamentoCreate):
        if self.medicamento_repo.get_by_nome(dados.nome):
            raise HTTPException(status_code=400, detail="Já existe um medicamento com este nome.")
        return self.medicamento_repo.create(dados)

    def obter_por_id(self, id_medicamento: int):
        medicamento = self.medicamento_repo.get_by_id(id_medicamento)
        if not medicamento:
            raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
        return medicamento

    def atualizar_medicamento(self, id_medicamento: int, dados: MedicamentoUpdate):
        medicamento = self.obter_por_id(id_medicamento)
        return self.medicamento_repo.update(medicamento, dados)

    def deletar_medicamento(self, id_medicamento: int):
        medicamento = self.obter_por_id(id_medicamento)
        self.medicamento_repo.delete(medicamento)