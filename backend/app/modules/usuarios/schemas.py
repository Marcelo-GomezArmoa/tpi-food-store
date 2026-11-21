from datetime import datetime

from pydantic import EmailStr, Field, field_validator
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    email: EmailStr
    celular: str | None = None
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_bcrypt_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("La contraseña no puede superar los 72 bytes.")
        return value


class UserPublic(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    celular: str | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    roles: list[str]
