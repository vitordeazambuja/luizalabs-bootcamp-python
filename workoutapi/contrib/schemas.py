from typing import Annotated
from pydantic import BaseModel, ConfigDict, UUID4, Field
from datetime import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True
    )

class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]