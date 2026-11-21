from sqlmodel import Session, select

from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate


class IngredienteService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def listar(self) -> list[Ingrediente]:
        return list(self.session.exec(select(Ingrediente)).all())

    def obtener_por_id(self, ingrediente_id: int) -> Ingrediente | None:
        return self.session.get(Ingrediente, ingrediente_id)

    def crear(self, datos: IngredienteCreate) -> Ingrediente:
        ingrediente = Ingrediente(**datos.model_dump())
        self.session.add(ingrediente)
        self.session.commit()
        self.session.refresh(ingrediente)
        return ingrediente

    def actualizar(
        self,
        ingrediente_id: int,
        datos: IngredienteUpdate,
    ) -> Ingrediente | None:
        ingrediente = self.obtener_por_id(ingrediente_id)
        if ingrediente is None:
            return None

        ingrediente.nombre = datos.nombre
        self.session.add(ingrediente)
        self.session.commit()
        self.session.refresh(ingrediente)
        return ingrediente

    def eliminar(self, ingrediente_id: int) -> bool:
        ingrediente = self.obtener_por_id(ingrediente_id)
        if ingrediente is None:
            return False

        self.session.delete(ingrediente)
        self.session.commit()
        return True
