from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, Field
from sqlmodel import SQLModel


class DetallePedidoCreate(SQLModel):
    producto_id: int
    cantidad: int = Field(ge=1)


class PedidoCreate(SQLModel):
    forma_pago: str
    direccion_entrega: str
    notas: str | None = Field(default=None, max_length=1000)
    items: list[DetallePedidoCreate] = Field(default_factory=list)


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


class PedidosPaginados(SQLModel):
    total: int
    items: list[PedidoRead]


class ResumenPedidos(SQLModel):
    pendientes: int
    en_preparacion: int
    entregados: int
    cancelados: int
    pedidos_hoy: int
    ingresos_entregados: float
