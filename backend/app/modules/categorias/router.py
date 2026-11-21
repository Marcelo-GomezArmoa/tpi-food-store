from fastapi import APIRouter, Depends, Response, status

from app.core.deps import require_role
from app.modules.categorias.schemas import (
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate,
)
from app.modules.categorias.service import CategoriaService
from app.modules.categorias.unit_of_work import CategoriasUnitOfWork

router = APIRouter(
    prefix="/categorias",
    tags=["categorías"],
)


def get_uow() -> CategoriasUnitOfWork:
    return CategoriasUnitOfWork()


@router.get("", response_model=list[CategoriaRead])
def list_categories(
    uow: CategoriasUnitOfWork = Depends(get_uow),
) -> list[CategoriaRead]:
    return CategoriaService(uow).listar()


@router.get("/{categoria_id}", response_model=CategoriaRead)
def get_category(
    categoria_id: int,
    uow: CategoriasUnitOfWork = Depends(get_uow),
) -> CategoriaRead:
    return CategoriaService(uow).obtener(categoria_id)


@router.post(
    "",
    response_model=CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
def create_category(
    data: CategoriaCreate,
    uow: CategoriasUnitOfWork = Depends(get_uow),
) -> CategoriaRead:
    return CategoriaService(uow).crear(data)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_category(
    categoria_id: int,
    data: CategoriaUpdate,
    uow: CategoriasUnitOfWork = Depends(get_uow),
) -> CategoriaRead:
    return CategoriaService(uow).actualizar(categoria_id, data)


@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],
)
def delete_category(
    categoria_id: int,
    uow: CategoriasUnitOfWork = Depends(get_uow),
) -> Response:
    CategoriaService(uow).eliminar(categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
