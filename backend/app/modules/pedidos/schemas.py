from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, Field, field_validator
from sqlmodel import SQLModel


class DetallePedidoCreate(SQLModel):
    producto_id: int
    cantidad: int = Field(ge=1)


class PedidoCreate(SQLModel):
    forma_pago: str = Field(min_length=1, max_length=50)
    direccion_entrega: str = Field(min_length=1, max_length=500)
    notas: str | None = Field(default=None, max_length=1000)
    items: list[DetallePedidoCreate] = Field(min_length=1)

    @field_validator("items")
    @classmethod
    def unique_products(
        cls,
        items: list[DetallePedidoCreate],
    ) -> list[DetallePedidoCreate]:
        ids = [item.producto_id for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError("Un pedido no puede repetir productos")
        return items


class PedidoEstadoUpdate(SQLModel):
    estado: Literal["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "CANCELADO"]


class DetallePedidoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    producto_id: int
    cantidad: int
    nombre_producto: str
    precio_unitario: float
    subtotal: float


class PedidoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    estado: str
    forma_pago: str
    direccion_entrega: str
    notas: str | None
    total: float
    created_at: datetime
    updated_at: datetime
    items: list[DetallePedidoRead]
