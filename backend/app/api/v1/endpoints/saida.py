from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.saida_service import SaidaService
from app.schemas.saida import SaidaCreate, SaidaResponse
from app.core.security import verificar_senha_mestra 

router = APIRouter()

# --- ROTA DE CRIAÇÃO (POST) ---
# Esta é a rota que o botão "Concluir" do Figma vai chamar.
@router.post("/", response_model=SaidaResponse, status_code=status.HTTP_201_CREATED)
def registrar_saida(
    saida: SaidaCreate,
    db: Session = Depends(get_db),
    # Proteção: Só executa se o Header 'X-Admin-Pass' estiver correto
    autorizado: bool = Depends(verificar_senha_mestra) 
):
    """
    Registra a saída de um medicamento.
    Requer a senha mestra no header 'X-Admin-Pass'.
    """
    service = SaidaService(db)
    return service.registrar_saida(saida)

# --- ROTA DE LISTAGEM (GET) - Opcional, mas recomendada ---
# Útil para o histórico ou dashboard
@router.get("/", response_model=List[SaidaResponse])
def listar_saidas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # Dica: Se quiser filtrar por data ou paciente depois, é aqui que implementamos
    service = SaidaService(db)
    # Como não criei o método 'listar_todos' no Service ainda, 
    # vou deixar o acesso direto ao repo ou você pode adicionar no service:
    return service.saida_repo.get_all(skip=skip, limit=limit)