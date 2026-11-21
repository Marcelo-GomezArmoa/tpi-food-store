from sqlmodel import Field, SQLModel


class ProductoCreate(SQLModel):
    nombre: str
    descripcion: str
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] = Field(default_factory=list)
    disponible: bool = True


class ProductoRead(SQLModel):
    id: int
    nombre: str
    descripcion: str
    precio_base: float = Field(ge=0)
    imagenes_url: list[str]
    disponible: bool


class ProductoUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio_base: float | None = Field(default=None, ge=0)
    imagenes_url: list[str] | None = None
    disponible: bool | None = None


class AsignarCategoria(SQLModel):
    categoria_id: int
