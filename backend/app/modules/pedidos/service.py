from datetime import date, datetime, timezone

from app.modules.pedidos.models import DetallePedido, Pedido
from app.modules.pedidos.schemas import (
    PedidoCreate,
    PedidoEstadoUpdate,
    PedidoRead,
    PedidosPaginados,
    ResumenPedidos,
)
from app.modules.pedidos.unit_of_work import PedidosUnitOfWork
from app.modules.usuarios.models import Usuario


class PedidoNoEncontrado(Exception):
    pass


class ProductoNoEncontrado(Exception):
    pass


class PedidoAjeno(Exception):
    pass


class ReglaPedidoInvalida(Exception):
    pass


class TransicionPedidoInvalida(ReglaPedidoInvalida):
    pass


TRANSICIONES = {
    "PENDIENTE": {"EN_PREPARACION", "CANCELADO"},
    "EN_PREPARACION": {"ENTREGADO", "CANCELADO"},
    "ENTREGADO": set(),
    "CANCELADO": set(),
}


class PedidoService:
    def __init__(self, uow: PedidosUnitOfWork) -> None:
        self.uow = uow

    def listar(
        self,
        user: Usuario,
        *,
        skip: int = 0,
        limit: int = 20,
        estado: str | None = None,
    ) -> PedidosPaginados:
        with self.uow as uow:
            total, pedidos = uow.pedidos.list_paginated(
                usuario_id=None if user.role == "admin" else self._user_id(user),
                skip=skip,
                limit=limit,
                estado=estado,
            )
            return PedidosPaginados(
                total=total,
                items=[PedidoRead.model_validate(pedido) for pedido in pedidos],
            )

    def resumen(self) -> ResumenPedidos:
        with self.uow as uow:
            return ResumenPedidos(
                pendientes=uow.pedidos.count_by_estado("PENDIENTE"),
                en_preparacion=uow.pedidos.count_by_estado("EN_PREPARACION"),
                entregados=uow.pedidos.count_by_estado("ENTREGADO"),
                cancelados=uow.pedidos.count_by_estado("CANCELADO"),
                pedidos_hoy=uow.pedidos.count_today(date.today()),
                ingresos_entregados=uow.pedidos.delivered_revenue(),
            )

    def obtener(self, pedido_id: int, user: Usuario) -> PedidoRead:
        with self.uow as uow:
            pedido = self._get_owned(uow, pedido_id, user)
            return PedidoRead.model_validate(pedido)

    def crear(self, data: PedidoCreate, user: Usuario) -> PedidoRead:
        with self.uow as uow:
            self._validar_datos(data)
            pedido = uow.pedidos.add(
                Pedido(
                    usuario_id=self._user_id(user),
                    estado="PENDIENTE",
                    forma_pago=data.forma_pago.strip().upper(),
                    direccion_entrega=data.direccion_entrega.strip(),
                    notas=data.notas.strip() if data.notas else None,
                )
            )
            total = 0.0
            for item in data.items:
                producto = uow.productos.get_active_by_id(item.producto_id)
                if producto is None:
                    raise ProductoNoEncontrado(
                        f"Producto con ID {item.producto_id} no encontrado"
                    )
                if not producto.disponible:
                    raise ReglaPedidoInvalida(
                        f"El producto {producto.nombre} no está disponible"
                    )
                if producto.stock < item.cantidad:
                    raise ReglaPedidoInvalida(
                        f"Stock insuficiente para {producto.nombre}"
                    )

                producto.stock -= item.cantidad
                producto.disponible = producto.stock > 0
                subtotal = round(producto.precio_base * item.cantidad, 2)
                detalle = DetallePedido(
                    pedido=pedido,
                    producto_id=producto.id,
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
    ) -> PedidoRead:
        with self.uow as uow:
            pedido = self._get(uow, pedido_id)
            if data.estado not in TRANSICIONES.get(pedido.estado, set()):
                raise TransicionPedidoInvalida(
                    f"No se puede cambiar {pedido.estado} a {data.estado}"
                )
            if data.estado == "CANCELADO":
                self._restituir_stock(uow, pedido)
            pedido.estado = data.estado
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    def cancelar(self, pedido_id: int, user: Usuario) -> PedidoRead:
        with self.uow as uow:
            pedido = self._get_owned(uow, pedido_id, user)
            if pedido.estado != "PENDIENTE":
                raise ReglaPedidoInvalida(
                    "Sólo se pueden cancelar pedidos pendientes"
                )
            self._restituir_stock(uow, pedido)
            pedido.estado = "CANCELADO"
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    @staticmethod
    def _validar_datos(data: PedidoCreate) -> None:
        if not data.items:
            raise ReglaPedidoInvalida("El pedido debe tener al menos un ítem")
        product_ids = [item.producto_id for item in data.items]
        if len(product_ids) != len(set(product_ids)):
            raise ReglaPedidoInvalida(
                "El pedido no puede repetir productos"
            )
        if data.forma_pago.strip().upper() not in {
            "EFECTIVO",
            "TRANSFERENCIA",
        }:
            raise ReglaPedidoInvalida("Forma de pago inválida")
        address_length = len(data.direccion_entrega.strip())
        if not 5 <= address_length <= 200:
            raise ReglaPedidoInvalida(
                "La dirección debe tener entre 5 y 200 caracteres"
            )

    @staticmethod
    def _restituir_stock(uow: PedidosUnitOfWork, pedido: Pedido) -> None:
        for item in pedido.items:
            producto = uow.productos.get_by_id(item.producto_id)
            if producto is None:
                raise ProductoNoEncontrado(
                    f"Producto con ID {item.producto_id} no encontrado"
                )
            producto.stock += item.cantidad
            if producto.activo and producto.stock > 0:
                producto.disponible = True

    @staticmethod
    def _get(uow: PedidosUnitOfWork, pedido_id: int) -> Pedido:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if pedido is None:
            raise PedidoNoEncontrado(f"Pedido con ID {pedido_id} no encontrado")
        return pedido

    @classmethod
    def _get_owned(
        cls,
        uow: PedidosUnitOfWork,
        pedido_id: int,
        user: Usuario,
    ) -> Pedido:
        pedido = cls._get(uow, pedido_id)
        if user.role != "admin" and pedido.usuario_id != cls._user_id(user):
            raise PedidoAjeno("El pedido no pertenece al usuario")
        return pedido

    @staticmethod
    def _user_id(user: Usuario) -> int:
        if user.id is None:
            raise ReglaPedidoInvalida("El usuario autenticado no tiene ID")
        return user.id
