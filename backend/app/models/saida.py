from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Saida(Base):
    __tablename__ = "saidas"

    id_saida = Column(Integer, primary_key=True, index=True)
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"), nullable=False)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario_responsavel = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    
    numero_de_caixas_entregues = Column(Integer, nullable=True)
    quantidade_por_caixa = Column(Integer, nullable=True)
    quantidade_total_entregue = Column(Integer, nullable=False)
    
    data_saida = Column(DateTime(timezone=True), server_default=func.now())
    observacao = Column(Text, nullable=True)

    lote = relationship("Lote", back_populates="saidas")
    paciente = relationship("Paciente", back_populates="saidas")
    usuario_responsavel = relationship("Usuario", back_populates="saidas")