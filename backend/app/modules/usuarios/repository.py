from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.usuarios.models import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Usuario)

    def get_by_username(self, username: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

    def get_by_email(self, email: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()

    def create(
        self,
        *,
        username: str,
        full_name: str,
        email: str,
        hashed_password: str,
        role: str = "user",
    ) -> Usuario:
        return self.add(
            Usuario(
                username=username,
                full_name=full_name,
                email=email,
                hashed_password=hashed_password,
                role=role,
            )
        )
