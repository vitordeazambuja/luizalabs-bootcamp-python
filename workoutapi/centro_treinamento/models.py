from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from contrib.models import BaseModel

class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    endereco: Mapped[str]
    proprietario: Mapped[str]

    atletas: Mapped[list['AtletaModel']] = relationship(
        back_populates='centro_treinamento'
    )
