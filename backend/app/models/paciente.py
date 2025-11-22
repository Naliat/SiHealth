from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id_paciente = Column(Integer, primary_key=True, index=True)
    cns = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String, nullable=True) # M, F, O
    cpf = Column(String, unique=True, index=True, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    saidas = relationship("Saida", back_populates="paciente")