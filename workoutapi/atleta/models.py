from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from contrib.models import BaseModel

class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    cpf: Mapped[str]
    idade: Mapped[int]
    peso: Mapped[float]
    altura: Mapped[float]
    sexo: Mapped[str]

    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    categoria: Mapped['CategoriaModel'] = relationship(back_populates='atletas')

    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey('centros_treinamento.pk_id')
    )
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(
        back_populates='atletas'
    )
