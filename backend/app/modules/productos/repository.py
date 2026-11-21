from sqlalchemy import func
from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.productos.models import Producto


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Producto)

    def get_active_by_id(self, producto_id: int) -> Producto | None:
        return self.session.exec(
            select(Producto).where(
                Producto.id == producto_id,
                Producto.activo == True,  # noqa: E712
            )
        ).first()

    def list_active(
        self,
        *,
        skip: int,
        limit: int,
        search: str | None,
        categoria_id: int | None,
        disponible: bool | None,
    ) -> tuple[int, list[Producto]]:
        conditions = [Producto.activo == True]  # noqa: E712
        if search:
            conditions.append(
                Producto.nombre.ilike(f"%{search.strip()}%")
            )
        if categoria_id is not None:
            conditions.append(Producto.categoria_id == categoria_id)
        if disponible is not None:
            conditions.append(Producto.disponible == disponible)

        total = self.session.exec(
            select(func.count()).select_from(Producto).where(*conditions)
        ).one()
        items = list(
            self.session.exec(
                select(Producto)
                .where(*conditions)
                .order_by(Producto.id)
                .offset(skip)
                .limit(limit)
            ).all()
        )
        return int(total), items
