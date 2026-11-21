import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, select

from app.core.database import engine
from app.core.security import hash_password
from app.ingrediente.model import Ingrediente
from app.pedido.models import DetallePedido, Pedido
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol

load_dotenv(Path(__file__).resolve().parent / ".env")

REGISTERED_MODELS = (Ingrediente, Pedido, DetallePedido)

ROLES_CATALOGO = {
    "admin": "Administrador del sistema",
    "user": "Usuario estándar",
}

# No existe actualmente una tabla EstadoPedido. Pedido.estado conserva estos
# estados como catálogo controlado por la API y sus esquemas.
ESTADOS_PEDIDO = (
    "PENDIENTE",
    "CONFIRMADO",
    "EN_PREPARACION",
    "LISTO",
    "ENTREGADO",
    "CANCELADO",
)


def seed_database(
    session: Session,
    admin_email: str | None = None,
    admin_password: str | None = None,
    admin_nombre: str = "Administrador",
    admin_apellido: str = "Sistema",
) -> None:
    roles: dict[str, Rol] = {}
    for nombre, descripcion in ROLES_CATALOGO.items():
        role = session.exec(select(Rol).where(Rol.nombre == nombre)).first()
        if role is None:
            role = Rol(nombre=nombre, descripcion=descripcion)
            session.add(role)
            session.flush()
        roles[nombre] = role

    email = (admin_email or os.getenv("SEED_ADMIN_EMAIL", "")).strip().lower()
    password = admin_password or os.getenv("SEED_ADMIN_PASSWORD")
    if email:
        user = session.exec(select(Usuario).where(Usuario.email == email)).first()
        if user is None:
            if not password:
                raise RuntimeError(
                    "SEED_ADMIN_PASSWORD es obligatorio para crear el administrador."
                )
            user = Usuario(
                nombre=admin_nombre,
                apellido=admin_apellido,
                email=email,
                password_hash=hash_password(password),
            )
            session.add(user)
            session.flush()

        if user.id is None or roles["admin"].id is None:
            raise RuntimeError("No se pudieron obtener los IDs del seed.")
        assignment = session.get(
            UsuarioRol, (user.id, roles["admin"].id)
        )
        if assignment is None:
            session.add(
                UsuarioRol(
                    usuario_id=user.id,
                    rol_id=roles["admin"].id,
                    asignado_por_id=None,
                    expires_at=None,
                )
            )

    session.commit()


def main() -> None:
    from app.core.database import create_db_and_tables

    create_db_and_tables()
    with Session(engine) as session:
        seed_database(session)
    print("Seed completado correctamente.")


if __name__ == "__main__":
    main()
