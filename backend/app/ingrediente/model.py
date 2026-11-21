from sqlmodel import Field, SQLModel


class Ingrediente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
