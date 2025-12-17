from typing import Annotated
from pydantic import Field, UUID4
from contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', examples=['Scale'], max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Nome da categoria', examples=['Scale'])]