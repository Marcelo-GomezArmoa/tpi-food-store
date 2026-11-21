from pydantic import ConfigDict, EmailStr, Field
from sqlmodel import SQLModel


class LoginResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: EmailStr
    role: str
    disabled: bool
