from fastapi import APIRouter, Depends, Query, Response, status

from app.core.deps import require_role
from app.modules.productos.schemas import (
    ProductoCreate,
    ProductoRead,
    ProductosPaginados,
    ProductoStockUpdate,
    ProductoUpdate,
)
from app.modules.productos.service import ProductoService
from app.modules.productos.unit_of_work import ProductosUnitOfWork

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
)


def get_uow() -> ProductosUnitOfWork:
    return ProductosUnitOfWork()


@router.get("", response_model=ProductosPaginados)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    categoria_id: int | None = Query(None, gt=0),
    disponible: bool | None = None,
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> ProductosPaginados:
    return ProductoService(uow).listar(
        skip=skip,
        limit=limit,
        search=search,
        categoria_id=categoria_id,
        disponible=disponible,
    )


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


@router.patch(
    "/{producto_id}/stock",
    response_model=ProductoRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_stock(
    producto_id: int,
    data: ProductoStockUpdate,
    uow: ProductosUnitOfWork = Depends(get_uow),
) -> ProductoRead:
    return ProductoService(uow).actualizar_stock(producto_id, data)


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
