from types import TracebackType

from sqlalchemy.engine import Engine
from sqlmodel import Session

from app.core.database import engine
from app.pedido.repository import (
    DetallePedidoRepository,
    PedidoRepository,
    ProductoRepository,
)


class UnitOfWork:
    def __init__(self, db_engine: Engine = engine) -> None:
        self.engine = db_engine

    def __enter__(self) -> "UnitOfWork":
        self.session = Session(self.engine)
        self.pedidos = PedidoRepository(self.session)
        self.detalles = DetallePedidoRepository(self.session)
        self.productos = ProductoRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                try:
                    self.session.commit()
                except BaseException:
                    self.session.rollback()
                    raise
            else:
                self.session.rollback()
        finally:
            self.session.close()
