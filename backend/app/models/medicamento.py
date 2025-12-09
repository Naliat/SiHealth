# app/models/medicamento.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False) # Ex: Dipirona
    principio_ativo = Column(String, nullable=True)   # Ex: Dipirona Monohidratada
    tarja = Column(String, nullable=True)             # Ex: Sem Tarja
    
    # Detalhes específicos foram movidos para o Lote
    
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    lotes = relationship("Lote", back_populates="medicamento")