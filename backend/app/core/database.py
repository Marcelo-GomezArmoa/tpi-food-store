from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

session_factory = Session


def create_all_tables() -> None:
    from app.modules.categorias.models import Categoria
    from app.modules.pedidos.models import DetallePedido, Pedido
    from app.modules.productos.models import Producto
    from app.modules.usuarios.models import Usuario

    _ = (Categoria, Producto, Pedido, DetallePedido, Usuario)
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with session_factory(engine) as session:
        yield session