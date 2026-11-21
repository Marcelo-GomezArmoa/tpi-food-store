from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.categoria.model import Categoria


class ProductoCategoria(SQLModel, table=True):
    producto_id: int | None = Field(
        default=None, foreign_key="producto.id", primary_key=True
    )
    categoria_id: int | None = Field(
        default=None, foreign_key="categoria.id", primary_key=True
    )


class ProductoBase(SQLModel):
    nombre: str = Field(index=True)
    descripcion: str
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    disponible: bool = Field(default=True)


class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, index=True),
    )
    categorias: list["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoria,
    )