# app/models/saida.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Saida(Base):
    __tablename__ = "saidas"

    id_saida = Column(Integer, primary_key=True, index=True)
    
    # Único relacionamento real: O LOTE (Estoque)
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"), nullable=False)
    
    # Dados do Paciente (Salvos como texto agora)
    cns_paciente = Column(String, nullable=False)
    nome_paciente = Column(String, nullable=True)
    
    # Dados da Transação
    quantidade = Column(Integer, nullable=False)
    numero_receita = Column(String, nullable=True) # Ex: "REC-123"
    tipo_saida = Column(String, nullable=False)    # Ex: "Receita Médica"
    observacao = Column(Text, nullable=True)
    
    data_saida = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento para acessar dados do remédio depois (ex: no dashboard)
    lote = relationship("Lote")