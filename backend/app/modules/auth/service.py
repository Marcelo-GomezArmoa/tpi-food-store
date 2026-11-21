from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import get_password_hash, verify_password
from app.modules.auth.schemas import RegisterRequest, UserResponse
from app.modules.usuarios.repository import UsuarioRepository


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UsuarioRepository(session)

    def register(self, data: RegisterRequest) -> UserResponse:
        username = data.username.strip()
        email = str(data.email).strip().lower()
        if self.users.get_by_username(username) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El username ya está registrado",
            )
        if self.users.get_by_email(email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            )

        user = self.users.create(
            username=username,
            full_name=data.full_name.strip(),
            email=email,
            hashed_password=get_password_hash(data.password),
        )
        self.session.commit()
        self.session.refresh(user)
        return UserResponse.model_validate(user)

    def authenticate(self, username: str, password: str):
        user = self.users.get_by_username(username.strip())
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )
        if user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario deshabilitado",
            )
        return user
