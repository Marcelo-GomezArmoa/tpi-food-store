from datetime import date

from sqlalchemy import func
from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.pedidos.models import DetallePedido, Pedido


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Pedido)

    def list_paginated(
        self,
        *,
        usuario_id: int | None,
        skip: int,
        limit: int,
        estado: str | None,
    ) -> tuple[int, list[Pedido]]:
        conditions = []
        if usuario_id is not None:
            conditions.append(Pedido.usuario_id == usuario_id)
        if estado is not None:
            conditions.append(Pedido.estado == estado)

        total = self.session.exec(
            select(func.count()).select_from(Pedido).where(*conditions)
        ).one()
        pedidos = list(
            self.session.exec(
                select(Pedido)
                .where(*conditions)
                .order_by(Pedido.created_at.desc(), Pedido.id.desc())
                .offset(skip)
                .limit(limit)
            ).all()
        )
        return int(total), pedidos

    def count_by_estado(self, estado: str) -> int:
        return int(
            self.session.exec(
                select(func.count())
                .select_from(Pedido)
                .where(Pedido.estado == estado)
            ).one()
        )

    def count_today(self, today: date) -> int:
        return int(
            self.session.exec(
                select(func.count())
                .select_from(Pedido)
                .where(func.date(Pedido.created_at) == today.isoformat())
            ).one()
        )

    def delivered_revenue(self) -> float:
        value = self.session.exec(
            select(func.coalesce(func.sum(Pedido.total), 0.0)).where(
                Pedido.estado == "ENTREGADO"
            )
        ).one()
        return float(value or 0.0)


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetallePedido)
