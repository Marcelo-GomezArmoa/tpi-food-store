from sqlmodel import Session, select

from app.pedido.models import DetallePedido, Pedido
from app.producto.model import Producto


class PedidoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Pedido]:
        statement = select(Pedido).where(Pedido.deleted_at.is_(None))
        return list(self.session.exec(statement).all())

    def get_by_id(self, pedido_id: int) -> Pedido | None:
        statement = select(Pedido).where(
            Pedido.id == pedido_id, Pedido.deleted_at.is_(None)
        )
        return self.session.exec(statement).first()

    def add(self, pedido: Pedido) -> None:
        self.session.add(pedido)
        self.session.flush()


class DetallePedidoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, detalle: DetallePedido) -> None:
        self.session.add(detalle)


class ProductoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, producto_id: int) -> Producto | None:
        return self.session.exec(
            select(Producto).where(
                Producto.id == producto_id,
                Producto.deleted_at.is_(None),
            )
        ).first()
