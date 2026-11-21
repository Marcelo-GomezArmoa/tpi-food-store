from typing import Annotated

from pydantic import ConfigDict, StringConstraints
from sqlmodel import SQLModel


class IngredienteCreate(SQLModel):
    nombre: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
    ]


class IngredienteUpdate(SQLModel):
    nombre: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
    ]


class IngredienteRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
