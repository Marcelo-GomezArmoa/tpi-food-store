from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_active_user, require_role
from app.modules.auth.schemas import UserPublic
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.service import UsuarioService

router = APIRouter(
    prefix="/admin/usuarios",
    tags=["administración de usuarios"],
    dependencies=[Depends(require_role("admin"))],
)
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUserDep = Annotated[Usuario, Depends(get_current_active_user)]


@router.get("", response_model=list[UserPublic])
def list_users(session: SessionDep) -> list[UserPublic]:
    return UsuarioService(session).list_users()


@router.post("/{user_id}/activar", response_model=UserPublic)
def activate_user(user_id: int, session: SessionDep) -> UserPublic:
    return UsuarioService(session).activate(user_id)


@router.post("/{user_id}/desactivar", response_model=UserPublic)
def deactivate_user(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> UserPublic:
    return UsuarioService(session).deactivate(user_id, current_user)
