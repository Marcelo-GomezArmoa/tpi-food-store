from fastapi import HTTPException, status

from app.modules.productos.models import Producto
from app.modules.productos.schemas import (
    ProductoCreate,
    ProductoRead,
    ProductoUpdate,
)
from app.modules.productos.unit_of_work import ProductosUnitOfWork


class ProductoService:
    def __init__(self, uow: ProductosUnitOfWork) -> None:
        self.uow = uow

    def listar(self) -> list[ProductoRead]:
        with self.uow as uow:
            return [
                ProductoRead.model_validate(producto)
                for producto in uow.productos.get_active_all()
            ]

    def obtener(self, producto_id: int) -> ProductoRead:
        with self.uow as uow:
            return ProductoRead.model_validate(
                self._get_active(uow, producto_id)
            )

    def crear(self, data: ProductoCreate) -> ProductoRead:
        with self.uow as uow:
            self._require_active_category(uow, data.categoria_id)
            producto = uow.productos.add(
                Producto(**data.model_dump())
            )
            return ProductoRead.model_validate(producto)

    def actualizar(
        self,
        producto_id: int,
        data: ProductoUpdate,
    ) -> ProductoRead:
        with self.uow as uow:
            producto = self._get_active(uow, producto_id)
            update_data = data.model_dump(exclude_unset=True)
            if categoria_id := update_data.get("categoria_id"):
                self._require_active_category(uow, categoria_id)
            for field, value in update_data.items():
                setattr(producto, field, value)
            uow.session.flush()
            return ProductoRead.model_validate(producto)

    def eliminar(self, producto_id: int) -> None:
        with self.uow as uow:
            producto = self._get_active(uow, producto_id)
            producto.activo = False
            producto.disponible = False

    @staticmethod
    def _get_active(
        uow: ProductosUnitOfWork,
        producto_id: int,
    ) -> Producto:
        producto = uow.productos.get_active_by_id(producto_id)
        if producto is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Producto no encontrado")
        return producto

    @staticmethod
    def _require_active_category(
        uow: ProductosUnitOfWork,
        categoria_id: int,
    ) -> None:
        if uow.categorias.get_active_by_id(categoria_id) is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Categoría no encontrada",
            )
