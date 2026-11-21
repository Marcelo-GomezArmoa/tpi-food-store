from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.deps import get_current_active_user, require_role
from app.modules.pedidos.schemas import (
    PedidoCreate,
    PedidoEstadoUpdate,
    PedidoRead,
    PedidosPaginados,
    ResumenPedidos,
)
from app.modules.pedidos.service import (
    PedidoAjeno,
    PedidoNoEncontrado,
    PedidoService,
    ProductoNoEncontrado,
    ReglaPedidoInvalida,
)
from app.modules.pedidos.unit_of_work import PedidosUnitOfWork
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
UserDep = Annotated[Usuario, Depends(get_current_active_user)]


def get_uow() -> PedidosUnitOfWork:
    return PedidosUnitOfWork()


def translate_domain_error(exc: Exception) -> HTTPException:
    if isinstance(exc, (PedidoNoEncontrado, ProductoNoEncontrado)):
        return HTTPException(status.HTTP_404_NOT_FOUND, str(exc))
    if isinstance(exc, PedidoAjeno):
        return HTTPException(status.HTTP_403_FORBIDDEN, str(exc))
    if isinstance(exc, ReglaPedidoInvalida):
        return HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))
    raise exc


@router.get("", response_model=PedidosPaginados)
def list_orders(
    user: UserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    estado: Literal[
        "PENDIENTE",
        "EN_PREPARACION",
        "ENTREGADO",
        "CANCELADO",
    ]
    | None = None,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidosPaginados:
    return PedidoService(uow).listar(
        user,
        skip=skip,
        limit=limit,
        estado=estado,
    )


@router.get(
    "/resumen",
    response_model=ResumenPedidos,
    dependencies=[Depends(require_role("admin"))],
)
def order_summary(
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> ResumenPedidos:
    return PedidoService(uow).resumen()


@router.get("/{pedido_id}", response_model=PedidoRead)
def get_order(
    pedido_id: int,
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    try:
        return PedidoService(uow).obtener(pedido_id, user)
    except (PedidoNoEncontrado, PedidoAjeno) as exc:
        raise translate_domain_error(exc) from exc


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_order(
    data: PedidoCreate,
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    try:
        return PedidoService(uow).crear(data, user)
    except (
        ProductoNoEncontrado,
        ReglaPedidoInvalida,
    ) as exc:
        raise translate_domain_error(exc) from exc


@router.patch(
    "/{pedido_id}/estado",
    response_model=PedidoRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_order_status(
    pedido_id: int,
    data: PedidoEstadoUpdate,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    try:
        return PedidoService(uow).actualizar_estado(pedido_id, data)
    except (
        PedidoNoEncontrado,
        ProductoNoEncontrado,
        ReglaPedidoInvalida,
    ) as exc:
        raise translate_domain_error(exc) from exc


@router.patch("/{pedido_id}/cancelar", response_model=PedidoRead)
def cancel_order(
    pedido_id: int,
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    try:
        return PedidoService(uow).cancelar(pedido_id, user)
    except (
        PedidoNoEncontrado,
        ProductoNoEncontrado,
        PedidoAjeno,
        ReglaPedidoInvalida,
    ) as exc:
        raise translate_domain_error(exc) from exc
