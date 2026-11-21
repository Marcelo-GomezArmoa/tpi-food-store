import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.categoria.model import Categoria
from app.producto.model import Producto, ProductoCategoria

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL no está configurada. Copia backend/.env.example como "
        "backend/.env y configura una URL de PostgreSQL."
    )
if not DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg2://")):
    raise RuntimeError("DATABASE_URL debe apuntar a una base de datos PostgreSQL.")

engine = create_engine(DATABASE_URL, echo=os.getenv("DEBUG", "False").lower() == "true")

# Fuerza el registro de todos los modelos antes de crear las tablas.
REGISTERED_MODELS = (Categoria, Producto, ProductoCategoria)


def create_db_and_tables():
    """Crea todas las tablas en la base de datos."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Proporciona una sesión de base de datos como dependencia."""
    with Session(engine) as session:
        yield session