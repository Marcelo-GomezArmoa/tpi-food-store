from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.security import hash_password, verify_password
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol
from app.modules.usuarios.repository import UsuarioRepository
from app.modules.usuarios.schemas import UserCreate, UserPublic


class UsuarioService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = UsuarioRepository(session)

    def register(self, data: UserCreate) -> UserPublic:
        email = self._normalize_email(data.email)
        if self.repository.get_by_email(email) is not None:
            self._raise_email_conflict()

        role = self.repository.get_role_by_name("user")
        if role is None:
            role = Rol(nombre="user", descripcion="Usuario estándar")
            self.repository.add_role(role)

        user = Usuario(
            nombre=data.nombre,
            apellido=data.apellido,
            email=email,
            celular=data.celular,
            password_hash=hash_password(data.password),
        )
        self.repository.add(user)
        if user.id is None or role.id is None:
            raise RuntimeError("No se pudo obtener el ID del usuario o rol.")
        self.repository.add_user_role(
            UsuarioRol(
                usuario_id=user.id,
                rol_id=role.id,
                asignado_por_id=None,
                expires_at=None,
            )
        )

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            self._raise_email_conflict()
        self.session.refresh(user)
        return self.to_public(user)

    def authenticate(self, email: str, password: str) -> Usuario:
        user = self.repository.get_by_email(self._normalize_email(email))
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cuenta de usuario desactivada",
            )
        return user

    def list_users(self) -> list[UserPublic]:
        return [self.to_public(user) for user in self.repository.get_all()]

    def activate(self, user_id: int) -> UserPublic:
        user = self._get_user_or_404(user_id)
        user.deleted_at = None
        user.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(user)
        return self.to_public(user)

    def deactivate(self, user_id: int) -> UserPublic:
        user = self._get_user_or_404(user_id)
        user.deleted_at = datetime.now(timezone.utc)
        user.updated_at = user.deleted_at
        self.session.commit()
        self.session.refresh(user)
        return self.to_public(user)

    def to_public(self, user: Usuario) -> UserPublic:
        if user.id is None:
            raise RuntimeError("El usuario no tiene un ID asignado.")
        return UserPublic(
            id=user.id,
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email,
            celular=user.celular,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
            roles=self.repository.get_active_roles(user.id),
        )

    def _get_user_or_404(self, user_id: int) -> Usuario:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return user

    @staticmethod
    def _normalize_email(email: str) -> str:
        return str(email).strip().lower()

    @staticmethod
    def _raise_email_conflict() -> None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        )
