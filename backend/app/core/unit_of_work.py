from types import TracebackType

from sqlalchemy.engine import Engine
from sqlmodel import Session

from app.core.database import engine, session_factory


class UnitOfWork:
    def __init__(self, db_engine: Engine = engine) -> None:
        self.engine = db_engine

    def __enter__(self) -> "UnitOfWork":
        self.session = session_factory(self.engine)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        except BaseException:
            self.session.rollback()
            raise
        finally:
            self.session.close()
