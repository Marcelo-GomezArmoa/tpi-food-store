from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.modules.pedidos.models import DetallePedido, Pedido
from app.modules.pedidos.schemas import (
    PedidoCreate,
    PedidoEstadoUpdate,
    PedidoRead,
)
from app.modules.pedidos.unit_of_work import PedidosUnitOfWork
from app.modules.usuarios.models import Usuario


class PedidoService:
    def __init__(self, uow: PedidosUnitOfWork) -> None:
        self.uow = uow

    def listar(self, user: Usuario) -> list[PedidoRead]:
        with self.uow as uow:
            pedidos = (
                uow.pedidos.get_all()
                if user.role == "admin"
                else uow.pedidos.get_by_user(self._user_id(user))
            )
            return [PedidoRead.model_validate(pedido) for pedido in pedidos]

    def obtener(self, pedido_id: int, user: Usuario) -> PedidoRead:
        with self.uow as uow:
            pedido = self._get_owned(uow, pedido_id, user)
            return PedidoRead.model_validate(pedido)

    def crear(self, data: PedidoCreate, user: Usuario) -> PedidoRead:
        with self.uow as uow:
            pedido = uow.pedidos.add(
                Pedido(
                    usuario_id=self._user_id(user),
                    forma_pago=data.forma_pago.strip(),
                    direccion_entrega=data.direccion_entrega.strip(),
                    notas=data.notas,
                )
            )
            total = 0.0
            for item in data.items:
                producto = uow.productos.get_active_by_id(item.producto_id)
                if producto is None:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND,
                        f"Producto {item.producto_id} no encontrado",
                    )
                subtotal = round(producto.precio_base * item.cantidad, 2)
                detalle = DetallePedido(
                    pedido=pedido,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    nombre_producto=producto.nombre,
                    precio_unitario=producto.precio_base,
                    subtotal=subtotal,
                )
                uow.detalles.add(detalle)
                total += subtotal
            pedido.total = round(total, 2)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    def actualizar_estado(
        self,
        pedido_id: int,
        data: PedidoEstadoUpdate,
        user: Usuario,
    ) -> PedidoRead:
        with self.uow as uow:
            pedido = self._get_owned(uow, pedido_id, user)
            pedido.estado = data.estado
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    @staticmethod
    def _get_owned(
        uow: PedidosUnitOfWork,
        pedido_id: int,
        user: Usuario,
    ) -> Pedido:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if pedido is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido no encontrado")
        if user.role != "admin" and pedido.usuario_id != PedidoService._user_id(user):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Pedido no pertenece al usuario")
        return pedido

    @staticmethod
    def _user_id(user: Usuario) -> int:
        if user.id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario sin ID")
        return user.id
