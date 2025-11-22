from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Entrada(Base):
    __tablename__ = "entradas"

    id_entrada = Column(Integer, primary_key=True, index=True)
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    
    quantidade = Column(Integer, nullable=False)
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    fornecedor = Column(String, nullable=True)

    lote = relationship("Lote", back_populates="entradas")
    usuario = relationship("Usuario", back_populates="entradas")