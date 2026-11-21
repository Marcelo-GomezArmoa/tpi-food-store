from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.core.config import settings
from app.core.security import create_access_token
from app.modules.auth.schemas import LoginResponse, RegisterRequest, UserPublic
from app.modules.auth.service import AuthService
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, session: SessionDep) -> UserPublic:
    return AuthService(session).register(data)


@router.post("/token", response_model=LoginResponse)
def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> LoginResponse:
    user = AuthService(session).authenticate(form_data.username, form_data.password)
    if user.id is None:
        raise RuntimeError("El usuario autenticado no tiene ID")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return LoginResponse()


@router.post("/logout")
def logout(response: Response) -> Response:
    response.delete_cookie(
        "access_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )
    response.status_code = status.HTTP_200_OK
    return response


@router.get("/me", response_model=UserPublic)
def me(
    user: Annotated[Usuario, Depends(get_current_active_user)],
) -> UserPublic:
    return UserPublic.model_validate(user)
