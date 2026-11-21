from app.core.unit_of_work import UnitOfWork
from app.modules.pedidos.repository import (
    DetallePedidoRepository,
    PedidoRepository,
)
from app.modules.productos.repository import ProductoRepository


class PedidosUnitOfWork(UnitOfWork):
    def __enter__(self) -> "PedidosUnitOfWork":
        super().__enter__()
        self.pedidos = PedidoRepository(self.session)
        self.detalles = DetallePedidoRepository(self.session)
        self.productos = ProductoRepository(self.session)
        return self
