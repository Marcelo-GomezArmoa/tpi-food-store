from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlmodel import Column, Field, Relationship, SQLModel

from app.producto.model import ProductoCategoria

if TYPE_CHECKING:
    from app.producto.model import Producto


class CategoriaBase(SQLModel):
    nombre: str = Field(index=True, unique=True)
    descripcion: str


class Categoria(CategoriaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, index=True),
    )
    productos: list["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria,
    )