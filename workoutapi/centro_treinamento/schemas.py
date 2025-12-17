from typing import Annotated
from pydantic import Field
from workoutapi.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', examples=['CT King'], max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', examples=['CT Rua X, Q02'], max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', examples=['Marcos'], max_length=30)]