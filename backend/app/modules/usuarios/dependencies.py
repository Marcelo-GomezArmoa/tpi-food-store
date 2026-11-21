from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import or_
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import decode_access_token, get_cookie_name
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token", auto_error=False
)


def get_current_user(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    bearer_token: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> Usuario:
    token = request.cookies.get(get_cookie_name()) or bearer_token
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError, RuntimeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = session.get(Usuario, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(
    current_user: Annotated[Usuario, Depends(get_current_user)],
) -> Usuario:
    if current_user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario desactivada",
        )
    return current_user


def require_role(allowed_roles: list[str] | tuple[str, ...] | set[str]):
    required_roles = set(allowed_roles)

    def verify_role(
        current_user: Annotated[Usuario, Depends(get_current_active_user)],
        session: Annotated[Session, Depends(get_session)],
    ) -> Usuario:
        if current_user.id is None or not required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes",
            )

        now = datetime.now(timezone.utc)
        current_role = session.exec(
            select(Rol.nombre)
            .join(UsuarioRol, UsuarioRol.rol_id == Rol.id)
            .where(
                UsuarioRol.usuario_id == current_user.id,
                Rol.nombre.in_(required_roles),
                or_(
                    UsuarioRol.expires_at.is_(None),
                    UsuarioRol.expires_at > now,
                ),
            )
        ).first()
        if current_role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes",
            )
        return current_user

    return verify_role


__all__ = [
    "get_current_active_user",
    "get_current_user",
    "oauth2_scheme",
    "require_role",
]
