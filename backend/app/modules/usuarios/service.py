from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.auth.schemas import UserPublic
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.repository import UsuarioRepository


class UsuarioService:
    def __init__(self, session: Session) -> None:
        self.repository = UsuarioRepository(session)

    def list_users(self) -> list[UserPublic]:
        return [
            UserPublic.model_validate(user)
            for user in self.repository.get_all()
        ]

    def activate(self, user_id: int) -> UserPublic:
        user = self._get_or_404(user_id)
        user.disabled = False
        self.repository.session.commit()
        self.repository.session.refresh(user)
        return UserPublic.model_validate(user)

    def deactivate(self, user_id: int, current_user: Usuario) -> UserPublic:
        user = self._get_or_404(user_id)
        if current_user.id == user.id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "El administrador no puede desactivarse a sí mismo",
            )
        user.disabled = True
        self.repository.session.commit()
        self.repository.session.refresh(user)
        return UserPublic.model_validate(user)

    def _get_or_404(self, user_id: int) -> Usuario:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
        return user
