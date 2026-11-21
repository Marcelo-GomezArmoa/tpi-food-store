from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import require_role
from app.modules.usuarios.schemas import UsuarioRead, UsuarioUpdate
from app.modules.usuarios.service import UsuarioService

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(require_role("admin"))],
)
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[UsuarioRead])
def list_users(session: SessionDep) -> list[UsuarioRead]:
    return UsuarioService(session).list_users()


@router.get("/{usuario_id}", response_model=UsuarioRead)
def get_user(usuario_id: int, session: SessionDep) -> UsuarioRead:
    return UsuarioService(session).get_user(usuario_id)


@router.patch("/{usuario_id}", response_model=UsuarioRead)
def update_user(
    usuario_id: int,
    data: UsuarioUpdate,
    session: SessionDep,
) -> UsuarioRead:
    return UsuarioService(session).update_user(usuario_id, data)
