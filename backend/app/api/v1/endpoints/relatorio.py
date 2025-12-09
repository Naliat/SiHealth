from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.core.database import get_db
from app.services.relatorio_service import RelatorioService
from app.services.pdf_service import PDFService
from app.core.dependecies import verificar_senha_mestra 

router = APIRouter()

# --- ROTA NOVA: RELATÓRIO TOTAL ---
@router.get("/geral/pdf")
def baixar_relatorio_geral_pdf(
    inicio: date = Query(default=date.today() - timedelta(days=30)),
    fim: date = Query(default=date.today()),
    db: Session = Depends(get_db),
    
):
    """
    Gera um relatório completo (Estoque Atual + Histórico de Dispensação) em PDF.
    """
    service = RelatorioService(db)
    # Busca os dois conjuntos de dados
    estoque, dispensacoes = service.obter_dados_completos(inicio, fim)
    
    # Gera o PDF combinado
    pdf_service = PDFService()
    arquivo_pdf = pdf_service.gerar_relatorio_gerencial(estoque, dispensacoes, inicio, fim)
    
    nome_arquivo = f"relatorio_geral_sihealth_{inicio}_{fim}.pdf"

    return StreamingResponse(
        arquivo_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"}
    )