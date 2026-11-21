from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, field_validator
from sqlmodel import Field, SQLModel


class DetallePedidoCreate(SQLModel):
    producto_id: int
    cantidad: int = Field(ge=1)


class PedidoCreate(SQLModel):
    detalles: list[DetallePedidoCreate] = Field(min_length=1)

    @field_validator("detalles")
    @classmethod
    def validar_productos_unicos(
        cls, detalles: list[DetallePedidoCreate]
    ) -> list[DetallePedidoCreate]:
        ids = [detalle.producto_id for detalle in detalles]
        if len(ids) != len(set(ids)):
            raise ValueError("No se permiten productos repetidos en un pedido")
        return detalles


class PedidoUpdateEstado(SQLModel):
    estado: Literal[
        "PENDIENTE",
        "CONFIRMADO",
        "EN_PREPARACION",
        "LISTO",
        "ENTREGADO",
        "CANCELADO",
    ]


class DetallePedidoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float


class PedidoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    estado: str
    total: float
    deleted_at: datetime | None
    detalles: list[DetallePedidoRead]
