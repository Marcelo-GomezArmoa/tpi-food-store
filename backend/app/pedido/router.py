from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.pedido.schemas import PedidoCreate, PedidoRead, PedidoUpdateEstado
from app.pedido.service import PedidoNoEncontrado, PedidoService, ProductoNoEncontrado
from app.pedido.unit_of_work import UnitOfWork
from app.modules.usuarios.dependencies import (
    get_current_active_user,
    require_role,
)
from app.modules.usuarios.models import Usuario


router = APIRouter(prefix="/pedidos", tags=["pedidos"])


def get_uow() -> UnitOfWork:
    return UnitOfWork()


@router.get(
    "",
    response_model=list[PedidoRead],
    dependencies=[Depends(get_current_active_user)],
)
def listar_pedidos(uow: UnitOfWork = Depends(get_uow)) -> list[PedidoRead]:
    return PedidoService(uow).listar()


@router.get(
    "/{pedido_id}",
    response_model=PedidoRead,
    dependencies=[Depends(get_current_active_user)],
)
def obtener_pedido(
    pedido_id: int, uow: UnitOfWork = Depends(get_uow)
) -> PedidoRead:
    try:
        return PedidoService(uow).obtener(pedido_id)
    except PedidoNoEncontrado as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate,
    current_user: Annotated[
        Usuario, Depends(require_role(["user", "admin"]))
    ],
    uow: UnitOfWork = Depends(get_uow),
) -> PedidoRead:
    try:
        if current_user.id is None:
            raise RuntimeError("El usuario autenticado no tiene ID.")
        return PedidoService(uow).crear(data, current_user.id)
    except ProductoNoEncontrado as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put(
    "/{pedido_id}",
    response_model=PedidoRead,
    dependencies=[Depends(require_role(["admin"]))],
)
def actualizar_pedido(
    pedido_id: int,
    data: PedidoUpdateEstado,
    uow: UnitOfWork = Depends(get_uow),
) -> PedidoRead:
    try:
        return PedidoService(uow).actualizar_estado(pedido_id, data)
    except PedidoNoEncontrado as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["admin"]))],
)
def eliminar_pedido(
    pedido_id: int, uow: UnitOfWork = Depends(get_uow)
) -> Response:
    try:
        PedidoService(uow).eliminar(pedido_id)
    except PedidoNoEncontrado as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
