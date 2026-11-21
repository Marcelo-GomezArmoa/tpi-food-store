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

    def get_active_all(self) -> list[Producto]:
        return list(
            self.session.exec(
                select(Producto).where(Producto.activo == True)  # noqa: E712
            ).all()
        )
