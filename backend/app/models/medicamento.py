from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean # Adicionei Boolean se não tiver
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    fabricante = Column(String, nullable=True)
    principio_ativo = Column(String, nullable=True)
    dosagem = Column(String, nullable=True)
    categoria = Column(String, nullable=True) # Ex: Analgésico
    tarja = Column(String, nullable=True) # Ex: "Vermelha", "Preta", "Sem Tarja"
    

    descricao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    lotes = relationship("Lote", back_populates="medicamento")