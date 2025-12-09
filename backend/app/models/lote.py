# app/models/lote.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lote(Base):
    __tablename__ = "lotes"

    id_lote = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("medicamentos.id_medicamento"), nullable=False)
    
    numero_lote = Column(String, unique=True, index=True, nullable=False)
    numero_caixa = Column(String, nullable=True)
    quantidade_inicial = Column(Integer, nullable=False)
    quantidade_atual = Column(Integer, nullable=False)
    quantidade_por_caixa = Column(Integer, nullable=True)
    
    # --- NOVOS CAMPOS (Vieram do Medicamento) ---
    fabricante = Column(String, nullable=True)  # Ex: Medley
    dosagem = Column(String, nullable=True)     # Ex: 500mg
    categoria = Column(String, nullable=True)   # Ex: Analgésico
    descricao = Column(Text, nullable=True)
    # --------------------------------------------

    data_fabricacao = Column(Date, nullable=True)
    data_validade = Column(Date, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento
    medicamento = relationship("Medicamento", back_populates="lotes")