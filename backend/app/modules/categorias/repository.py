from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.categorias.models import Categoria


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Categoria)

    def get_by_nombre(self, nombre: str) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(Categoria.nombre == nombre)
        ).first()

    def get_active_by_id(self, categoria_id: int) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(
                Categoria.id == categoria_id,
                Categoria.activo == True,  # noqa: E712
            )
        ).first()

    def get_active_all(self) -> list[Categoria]:
        return list(
            self.session.exec(
                select(Categoria).where(Categoria.activo == True)  # noqa: E712
            ).all()
        )
