from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.core.security import create_access_token
from app.modules.auth.schemas import LoginResponse, RegisterRequest, UserResponse
from app.modules.auth.service import AuthService
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, session: SessionDep) -> UserResponse:
    return AuthService(session).register(data)


@router.post("/login", response_model=LoginResponse)
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
        path="/",
    )
    return LoginResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> Response:
    response.delete_cookie("access_token", path="/")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
def me(
    user: Annotated[Usuario, Depends(get_current_active_user)],
) -> UserResponse:
    return UserResponse.model_validate(user)
