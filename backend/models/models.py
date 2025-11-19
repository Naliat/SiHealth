from odmantic import Model, Field, Reference
from datetime import datetime, date
from typing import Optional, ClassVar
from enum import Enum
from pydantic import ConfigDict

class Sexo(str, Enum):
    MASCULINO = "M"
    FEMININO = "F"
    OUTRO = "O"

class Medicamento(Model):
    nome: str = Field(min_length=1)
    fabricante: str = Field(min_length=1)
    principio_ativo: str = Field(min_length=1)
    dosagem: str = Field(min_length=1)
    categoria: str = Field(min_length=1)
    descricao: Optional[str] = None
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    # Correção aqui - usando model_config do Pydantic v2
    model_config = ConfigDict(
        collection="medicamentos"
    )

class Lote(Model):
    medicamento: Medicamento = Reference()
    numero_lote: str = Field(unique=True, min_length=1)
    numero_caixa: str = Field(min_length=1)
    quantidade_por_caixa: int = Field(gt=0)
    quantidade_inicial: int = Field(gt=0)
    quantidade_atual: int = Field(ge=0)
    data_fabricacao: date
    data_validade: date
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        collection="lotes"
    )

    @property
    def quantidade_total_inicial(self) -> int:
        return self.quantidade_inicial * self.quantidade_por_caixa

    @property
    def quantidade_total_atual(self) -> int:
        return self.quantidade_atual * self.quantidade_por_caixa

class Paciente(Model):
    CNS: str = Field(unique=True, min_length=1)
    nome: str = Field(min_length=1)
    data_nascimento: date
    sexo: Sexo
    cpf: str = Field(unique=True, min_length=11)
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        collection="pacientes"
    )

class Usuario(Model):
    nome: str = Field(min_length=1)
    email: str = Field(unique=True)
    senha_hash: str = Field(min_length=1)
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        collection="usuarios"
    )

class Entrada(Model):
    lote: Lote = Reference()
    usuario: Usuario = Reference()
    quantidade: int = Field(gt=0)
    data_entrada: datetime = Field(default_factory=datetime.utcnow)
    fornecedor: Optional[str] = None

    model_config = ConfigDict(
        collection="entradas"
    )

class Saida(Model):
    lote: Lote = Reference()
    paciente: Paciente = Reference()
    usuario_responsavel: Usuario = Reference()
    numero_de_caixas_entregues: int = Field(gt=0)
    quantidade_por_caixa: int = Field(gt=0)
    data_saida: datetime = Field(default_factory=datetime.utcnow)
    observacao: Optional[str] = None

    model_config = ConfigDict(
        collection="saidas"
    )

    @property
    def quantidade_total_entregue(self) -> int:
        return self.numero_de_caixas_entregues * self.quantidade_por_caixa