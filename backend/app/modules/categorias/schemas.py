from pydantic import Field
from sqlmodel import SQLModel


class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(default="", max_length=500)
    activo: bool = True


class CategoriaUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    activo: bool | None = None


class CategoriaRead(SQLModel):
    model_config = {"from_attributes": True}

    id: int
    nombre: str
    descripcion: str
    activo: bool
