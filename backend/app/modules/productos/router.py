from fastapi import APIRouter, Depends, Response, status

from app.core.deps import get_current_active_user, require_role
from app.modules.productos.schemas import (
    ProductoCreate,
    ProductoRead,
    ProductoUpdate,
)
from app.modules.productos.service import ProductoService
from app.modules.productos.unit_of_work import ProductosUnitOfWork

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    dependencies=[Depends(get_current_active_user)],
)


def get_uow() -> ProductosUnitOfWork:
    return ProductosUnitOfWork()


@router.get("", response_model=list[ProductoRead])
def list_products(
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> list[ProductoRead]:
    return ProductoService(uow).listar()


@router.get("/{producto_id}", response_model=ProductoRead)
def get_product(
    producto_id: int,
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> ProductoRead:
    return ProductoService(uow).obtener(producto_id)


@router.post(
    "",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
def create_product(
    data: ProductoCreate,
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> ProductoRead:
    return ProductoService(uow).crear(data)


@router.put(
    "/{producto_id}",
    response_model=ProductoRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_product(
    producto_id: int,
    data: ProductoUpdate,
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> ProductoRead:
    return ProductoService(uow).actualizar(producto_id, data)


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],
)
def delete_product(
    producto_id: int,
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> Response:
    ProductoService(uow).eliminar(producto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
