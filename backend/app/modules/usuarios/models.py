from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime
from sqlmodel import Column, Field, Relationship, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UsuarioRol(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    rol_id: int = Field(foreign_key="rol.id", primary_key=True)
    asignado_por_id: int | None = Field(
        default=None, foreign_key="usuario.id"
    )
    expires_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    usuario: "Usuario" = Relationship(
        back_populates="usuario_roles",
        sa_relationship_kwargs={"foreign_keys": "[UsuarioRol.usuario_id]"},
    )
    rol: "Rol" = Relationship(back_populates="usuario_roles")
    asignado_por: Optional["Usuario"] = Relationship(
        back_populates="roles_asignados",
        sa_relationship_kwargs={"foreign_keys": "[UsuarioRol.asignado_por_id]"},
    )


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str = Field(unique=True, index=True)
    celular: str | None = None
    password_hash: str
    created_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            onupdate=_utc_now,
        ),
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            index=True,
        ),
    )

    roles: list["Rol"] = Relationship(
        back_populates="usuarios",
        link_model=UsuarioRol,
        sa_relationship_kwargs={
            "primaryjoin": "Usuario.id == UsuarioRol.usuario_id",
            "secondaryjoin": "Rol.id == UsuarioRol.rol_id",
            "overlaps": "rol,usuario",
        },
    )
    usuario_roles: list["UsuarioRol"] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={
            "foreign_keys": "[UsuarioRol.usuario_id]",
            "overlaps": "roles",
        },
    )
    roles_asignados: list["UsuarioRol"] = Relationship(
        back_populates="asignado_por",
        sa_relationship_kwargs={"foreign_keys": "[UsuarioRol.asignado_por_id]"},
    )


class Rol(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    descripcion: str | None = None

    usuarios: list["Usuario"] = Relationship(
        back_populates="roles",
        link_model=UsuarioRol,
        sa_relationship_kwargs={
            "primaryjoin": "Rol.id == UsuarioRol.rol_id",
            "secondaryjoin": "Usuario.id == UsuarioRol.usuario_id",
            "overlaps": "rol,usuario,usuario_roles",
        },
    )
    usuario_roles: list["UsuarioRol"] = Relationship(
        back_populates="rol",
        sa_relationship_kwargs={"overlaps": "roles,usuarios"},
    )
