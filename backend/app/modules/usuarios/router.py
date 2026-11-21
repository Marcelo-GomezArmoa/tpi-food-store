from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import (
    create_access_token,
    delete_access_token_cookie,
    set_access_token_cookie,
)
from app.modules.usuarios.dependencies import (
    get_current_active_user,
    require_role,
)
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.schemas import UserCreate, UserPublic
from app.modules.usuarios.service import UsuarioService

router = APIRouter(prefix="/api/v1/auth", tags=["autenticación"])
SessionDependency = Annotated[Session, Depends(get_session)]


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserCreate, session: SessionDependency) -> UserPublic:
    return UsuarioService(session).register(data)


@router.post("/token")
def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDependency,
) -> dict[str, str]:
    user = UsuarioService(session).authenticate(
        form_data.username, form_data.password
    )
    if user.id is None:
        raise RuntimeError("El usuario autenticado no tiene ID.")
    token = create_access_token(user.id)
    set_access_token_cookie(response, token)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> Response:
    delete_access_token_cookie(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserPublic)
def me(
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
    session: SessionDependency,
) -> UserPublic:
    return UsuarioService(session).to_public(current_user)


@router.get(
    "/admin/usuarios",
    response_model=list[UserPublic],
    dependencies=[Depends(require_role(["admin"]))],
)
def list_users(session: SessionDependency) -> list[UserPublic]:
    return UsuarioService(session).list_users()


@router.post(
    "/admin/usuarios/{user_id}/activar",
    response_model=UserPublic,
    dependencies=[Depends(require_role(["admin"]))],
)
def activate_user(user_id: int, session: SessionDependency) -> UserPublic:
    return UsuarioService(session).activate(user_id)


@router.post(
    "/admin/usuarios/{user_id}/desactivar",
    response_model=UserPublic,
    dependencies=[Depends(require_role(["admin"]))],
)
def deactivate_user(user_id: int, session: SessionDependency) -> UserPublic:
    return UsuarioService(session).deactivate(user_id)
