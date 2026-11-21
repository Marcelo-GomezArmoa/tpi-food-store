from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.pedidos.models import DetallePedido, Pedido


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Pedido)

    def get_by_user(self, usuario_id: int) -> list[Pedido]:
        return list(
            self.session.exec(
                select(Pedido)
                .where(Pedido.usuario_id == usuario_id)
                .order_by(Pedido.created_at.desc())
            ).all()
        )


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetallePedido)
