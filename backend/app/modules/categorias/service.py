from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.modules.categorias.models import Categoria
from app.modules.categorias.schemas import (
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate,
)
from app.modules.categorias.unit_of_work import CategoriasUnitOfWork


class CategoriaService:
    def __init__(self, uow: CategoriasUnitOfWork) -> None:
        self.uow = uow

    def listar(self) -> list[CategoriaRead]:
        with self.uow as uow:
            return [
                CategoriaRead.model_validate(categoria)
                for categoria in uow.categorias.get_active_all()
            ]

    def obtener(self, categoria_id: int) -> CategoriaRead:
        with self.uow as uow:
            categoria = self._get_active(uow, categoria_id)
            return CategoriaRead.model_validate(categoria)

    def crear(self, data: CategoriaCreate) -> CategoriaRead:
        with self.uow as uow:
            if uow.categorias.get_by_nombre(data.nombre.strip()) is not None:
                raise HTTPException(status.HTTP_409_CONFLICT, "La categoría ya existe")
            categoria = uow.categorias.add(
                Categoria(
                    nombre=data.nombre.strip(),
                    descripcion=data.descripcion.strip(),
                    activo=data.activo,
                )
            )
            return CategoriaRead.model_validate(categoria)

    def actualizar(
        self,
        categoria_id: int,
        data: CategoriaUpdate,
    ) -> CategoriaRead:
        with self.uow as uow:
            categoria = self._get_active(uow, categoria_id)
            update_data = data.model_dump(exclude_unset=True)
            if "nombre" in update_data:
                nombre = str(update_data["nombre"]).strip()
                existing = uow.categorias.get_by_nombre(nombre)
                if existing is not None and existing.id != categoria_id:
                    raise HTTPException(
                        status.HTTP_409_CONFLICT,
                        "La categoría ya existe",
                    )
                update_data["nombre"] = nombre
            for field, value in update_data.items():
                setattr(categoria, field, value)
            uow.session.flush()
            return CategoriaRead.model_validate(categoria)

    def eliminar(self, categoria_id: int) -> None:
        with self.uow as uow:
            categoria = self._get_active(uow, categoria_id)
            categoria.activo = False

    @staticmethod
    def _get_active(
        uow: CategoriasUnitOfWork,
        categoria_id: int,
    ) -> Categoria:
        categoria = uow.categorias.get_active_by_id(categoria_id)
        if categoria is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoría no encontrada")
        return categoria
