"""FastAPI application entry point."""
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.categoria.router import router as categoria_router
from app.ingrediente.model import Ingrediente
from app.modules.usuarios import Rol, Usuario, UsuarioRol
from app.modules.usuarios.router import router as usuarios_router
from app.ingrediente.router import router as ingrediente_router
from app.pedido.models import DetallePedido, Pedido
from app.pedido.router import router as pedido_router
from app.producto.router import router as producto_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="FastAPI Productos",
    description="API REST para gestionar productos y categorías",
    version="1.0.0",
    lifespan=lifespan,
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
app.include_router(pedido_router)
app.include_router(usuarios_router)


@app.get("/")
async def root():
    return {"message": "Bienvenido a FastAPI Productos API"}

