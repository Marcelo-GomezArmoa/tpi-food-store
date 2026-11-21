from datetime import datetime

from pydantic import ConfigDict, EmailStr
from sqlmodel import SQLModel


class UsuarioRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: EmailStr
    role: str
    disabled: bool
    created_at: datetime


class UsuarioUpdate(SQLModel):
    full_name: str | None = None
    disabled: bool | None = None
