import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, cast

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Response
from jwt import PyJWTError

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 60
DEFAULT_COOKIE_NAME = "access_token"


def get_secret_key() -> str:
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY no está configurada.")
    return secret_key


def get_jwt_algorithm() -> str:
    return os.getenv("JWT_ALGORITHM", "HS256")


def get_access_token_expire_minutes() -> int:
    value = os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        str(DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    try:
        minutes = int(value)
    except ValueError as exc:
        raise RuntimeError(
            "ACCESS_TOKEN_EXPIRE_MINUTES debe ser un número entero."
        ) from exc
    if minutes <= 0:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES debe ser mayor que cero.")
    return minutes


def get_cookie_name() -> str:
    return os.getenv("COOKIE_NAME", DEFAULT_COOKIE_NAME)


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("La contraseña no puede superar los 72 bytes para bcrypt.")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except (TypeError, ValueError, UnicodeError):
        return False


def create_access_token(
    data: Mapping[str, Any] | str | int,
    expires_delta: timedelta | None = None,
    additional_claims: Mapping[str, Any] | None = None,
) -> str:
    if isinstance(data, Mapping):
        claims = dict(data)
    else:
        claims = {"sub": str(data)}

    if additional_claims:
        claims.update(additional_claims)
    if "sub" not in claims:
        raise ValueError("El token debe incluir el claim 'sub'.")

    now = datetime.now(timezone.utc)
    expires = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=get_access_token_expire_minutes())
    )
    claims["sub"] = str(claims["sub"])
    claims.update({"iat": now, "exp": expires})
    return jwt.encode(claims, get_secret_key(), algorithm=get_jwt_algorithm())


def decode_access_token(token: str) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        jwt.decode(
            token,
            get_secret_key(),
            algorithms=[get_jwt_algorithm()],
            options={"require": ["exp", "iat", "sub"]},
        ),
    )


def _cookie_secure() -> bool:
    return os.getenv("COOKIE_SECURE", "False").lower() in {"1", "true", "yes"}


def _cookie_samesite() -> str:
    value = os.getenv("COOKIE_SAMESITE", "lax").lower()
    if value not in {"lax", "strict", "none"}:
        raise RuntimeError("COOKIE_SAMESITE debe ser 'lax', 'strict' o 'none'.")
    if value == "none" and not _cookie_secure():
        raise RuntimeError("COOKIE_SAMESITE='none' requiere COOKIE_SECURE=True.")
    return value


def set_access_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=get_cookie_name(),
        value=token,
        max_age=get_access_token_expire_minutes() * 60,
        httponly=True,
        secure=_cookie_secure(),
        samesite=_cookie_samesite(),
        path="/",
    )


def delete_access_token_cookie(response: Response) -> None:
    response.delete_cookie(
        key=get_cookie_name(),
        httponly=True,
        secure=_cookie_secure(),
        samesite=_cookie_samesite(),
        path="/",
    )


__all__ = [
    "PyJWTError",
    "create_access_token",
    "decode_access_token",
    "delete_access_token_cookie",
    "get_cookie_name",
    "get_jwt_algorithm",
    "hash_password",
    "set_access_token_cookie",
    "verify_password",
]
