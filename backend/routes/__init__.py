"""
Módulo de Rotas do Sistema de Gerenciamento de Medicamentos

Este módulo centraliza e exporta todas as rotas da API para
facilitar a importação no arquivo principal da aplicação.
"""

from fastapi import APIRouter

# Importar todas as rotas
from .medicamentos import router as medicamentos_router
from .usuarios import router as usuarios_router
from .pacientes import router as pacientes_router

"""
from .lotes import router as lotes_router


from .entradas import router as entradas_router
from .saidas import router as saidas_router
"""

# Router principal que agrupa todas as rotas
main_router = APIRouter()

# Incluir todas as rotas no router principal
main_router.include_router(medicamentos_router)
main_router.include_router(usuarios_router)
main_router.include_router(pacientes_router)
"""
main_router.include_router(lotes_router)


main_router.include_router(entradas_router)
main_router.include_router(saidas_router)

"""
# Lista de todos os routers individuais (para importação seletiva)
__all_routers__ = [
    medicamentos_router,
    usuarios_router,
    pacientes_router,
    """,
    lotes_router,

    
    entradas_router,
    saidas_router
    """
]

# Exportações para facilitar a importação
__all__ = [
    "main_router",
    "medicamentos_router"
    "pacientes_router",
    """,
    "lotes_router", 

    "usuarios_router",
    "entradas_router",
    "saidas_router",
    "__all_routers__"
    """
]