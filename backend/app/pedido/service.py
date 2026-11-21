from datetime import datetime, timezone

from app.pedido.models import DetallePedido, Pedido
from app.pedido.schemas import PedidoCreate, PedidoRead, PedidoUpdateEstado
from app.pedido.unit_of_work import UnitOfWork


class PedidoNoEncontrado(Exception):
    pass


class ProductoNoEncontrado(Exception):
    pass


class PedidoService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def listar(self) -> list[PedidoRead]:
        with self.uow as uow:
            return [PedidoRead.model_validate(pedido) for pedido in uow.pedidos.get_all()]

    def obtener(self, pedido_id: int) -> PedidoRead:
        with self.uow as uow:
            pedido = self._obtener_activo(uow, pedido_id)
            return PedidoRead.model_validate(pedido)

    def crear(self, data: PedidoCreate, usuario_id: int) -> PedidoRead:
        with self.uow as uow:
            pedido = Pedido(usuario_id=usuario_id)
            uow.pedidos.add(pedido)
            if pedido.id is None:
                raise RuntimeError("No se pudo obtener el ID del pedido")
            for item in data.detalles:
                producto = uow.productos.get_by_id(item.producto_id)
                if producto is None:
                    raise ProductoNoEncontrado(
                        f"Producto con ID {item.producto_id} no encontrado"
                    )
                detalle = DetallePedido(
                    pedido_id=pedido.id,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=producto.precio_base,
                    pedido=pedido,
                )
                uow.detalles.add(detalle)
                pedido.total += item.cantidad * producto.precio_base
            return PedidoRead.model_validate(pedido)

    def actualizar_estado(self, pedido_id: int, data: PedidoUpdateEstado) -> PedidoRead:
        with self.uow as uow:
            pedido = self._obtener_activo(uow, pedido_id)
            pedido.estado = data.estado
            return PedidoRead.model_validate(pedido)

    def eliminar(self, pedido_id: int) -> None:
        with self.uow as uow:
            pedido = self._obtener_activo(uow, pedido_id)
            pedido.deleted_at = datetime.now(timezone.utc)

    @staticmethod
    def _obtener_activo(uow: UnitOfWork, pedido_id: int) -> Pedido:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if pedido is None:
            raise PedidoNoEncontrado(f"Pedido con ID {pedido_id} no encontrado")
        return pedido
