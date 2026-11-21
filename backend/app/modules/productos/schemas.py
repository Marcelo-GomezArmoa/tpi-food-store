from pydantic import Field
from sqlmodel import SQLModel


class ProductoCreate(SQLModel):
    categoria_id: int
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str = Field(default="", max_length=1000)
    precio_base: float = Field(ge=0)
    imagen_url: str = ""
    stock: int = Field(default=0, ge=0)
    disponible: bool = True
    activo: bool = True


class ProductoUpdate(SQLModel):
    categoria_id: int | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    descripcion: str | None = Field(default=None, max_length=1000)
    precio_base: float | None = Field(default=None, ge=0)
    imagen_url: str | None = None
    stock: int | None = Field(default=None, ge=0)
    disponible: bool | None = None
    activo: bool | None = None


class ProductoRead(SQLModel):
    model_config = {"from_attributes": True}

    id: int
    categoria_id: int
    nombre: str
    descripcion: str
    precio_base: float
    imagen_url: str
    stock: int
    disponible: bool
    activo: bool
