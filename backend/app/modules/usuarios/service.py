from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.usuarios.repository import UsuarioRepository
from app.modules.usuarios.schemas import UsuarioRead, UsuarioUpdate


class UsuarioService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = UsuarioRepository(session)

    def list_users(self) -> list[UsuarioRead]:
        return [
            UsuarioRead.model_validate(user)
            for user in self.repository.get_all()
        ]

    def get_user(self, user_id: int) -> UsuarioRead:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
        return UsuarioRead.model_validate(user)

    def update_user(self, user_id: int, data: UsuarioUpdate) -> UsuarioRead:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return UsuarioRead.model_validate(user)
