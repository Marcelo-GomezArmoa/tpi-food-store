from datetime import datetime, timezone

from sqlalchemy import or_
from sqlmodel import Session, select

from app.modules.usuarios.models import Rol, Usuario, UsuarioRol


class UsuarioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()

    def get_by_id(self, user_id: int) -> Usuario | None:
        return self.session.get(Usuario, user_id)

    def get_all(self) -> list[Usuario]:
        return list(self.session.exec(select(Usuario)).all())

    def get_active_roles(self, user_id: int) -> list[str]:
        now = datetime.now(timezone.utc)
        result = self.session.exec(
            select(Rol.nombre)
            .join(UsuarioRol, UsuarioRol.rol_id == Rol.id)
            .where(
                UsuarioRol.usuario_id == user_id,
                or_(
                    UsuarioRol.expires_at.is_(None),
                    UsuarioRol.expires_at > now,
                ),
            )
            .order_by(Rol.nombre)
        )
        return list(result.all())

    def get_role_by_name(self, nombre: str) -> Rol | None:
        return self.session.exec(
            select(Rol).where(Rol.nombre == nombre)
        ).first()

    def add(self, user: Usuario) -> None:
        self.session.add(user)
        self.session.flush()

    def add_role(self, role: Rol) -> None:
        self.session.add(role)
        self.session.flush()

    def add_user_role(self, assignment: UsuarioRol) -> None:
        self.session.add(assignment)
