from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_active_user, require_role
from app.modules.pedidos.schemas import (
    PedidoCreate,
    PedidoEstadoUpdate,
    PedidoRead,
)
from app.modules.pedidos.service import PedidoService
from app.modules.pedidos.unit_of_work import PedidosUnitOfWork
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
UserDep = Annotated[Usuario, Depends(get_current_active_user)]


def get_uow() -> PedidosUnitOfWork:
    return PedidosUnitOfWork()


@router.get("", response_model=list[PedidoRead])
def list_orders(
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> list[PedidoRead]:
    return PedidoService(uow).listar(user)


@router.get("/{pedido_id}", response_model=PedidoRead)
def get_order(
    pedido_id: int,
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    return PedidoService(uow).obtener(pedido_id, user)


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_order(
    data: PedidoCreate,
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    return PedidoService(uow).crear(data, user)


@router.patch(
    "/{pedido_id}/estado",
    response_model=PedidoRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_order_status(
    pedido_id: int,
    data: PedidoEstadoUpdate,
    user: UserDep,
    uow: PedidosUnitOfWork = Depends(get_uow),
) -> PedidoRead:
    return PedidoService(uow).actualizar_estado(pedido_id, data, user)
