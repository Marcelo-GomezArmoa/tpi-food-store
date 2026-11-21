from sqlmodel import Session, select

from app.core.database import create_all_tables, engine
from app.core.security import get_password_hash
from app.modules.categorias.models import Categoria
from app.modules.productos.models import Producto
from app.modules.usuarios.models import Usuario

CATEGORIES = (
    ("Pizzas", "Pizzas artesanales para compartir"),
    ("Bebidas", "Bebidas frías y calientes"),
    ("Postres", "Opciones dulces"),
)

PRODUCTS = (
    ("Pizzas", "Pizza Muzza", "Mozzarella, tomate y aceitunas", 5200.0, 30),
    ("Pizzas", "Pizza Napolitana", "Mozzarella, tomate y albahaca", 6100.0, 20),
    ("Pizzas", "Pizza Fugazzeta", "Cebolla, mozzarella y orégano", 5900.0, 18),
    ("Bebidas", "Coca-Cola 500 ml", "Gaseosa cola individual", 1800.0, 80),
    ("Bebidas", "Agua mineral 500 ml", "Agua mineral sin gas", 1400.0, 100),
    ("Bebidas", "Limonada 1 L", "Limonada casera para compartir", 2900.0, 25),
    ("Postres", "Tiramisú", "Postre de café y mascarpone", 3500.0, 16),
    ("Postres", "Brownie con helado", "Brownie tibio con helado de vainilla", 4200.0, 14),
)


def seed_database(session: Session) -> None:
    admin = session.exec(
        select(Usuario).where(Usuario.username == "admin")
    ).first()
    if admin is None:
        session.add(
            Usuario(
                username="admin",
                full_name="Administrador Food Store",
                email="admin@example.com",
                hashed_password=get_password_hash("Admin1234!"),
                role="admin",
            )
        )

    categories: dict[str, Categoria] = {}
    for nombre, descripcion in CATEGORIES:
        categoria = session.exec(
            select(Categoria).where(Categoria.nombre == nombre)
        ).first()
        if categoria is None:
            categoria = Categoria(nombre=nombre, descripcion=descripcion)
            session.add(categoria)
            session.flush()
        categories[nombre] = categoria

    for categoria_nombre, nombre, descripcion, precio, stock in PRODUCTS:
        existing = session.exec(
            select(Producto).where(Producto.nombre == nombre)
        ).first()
        if existing is None:
            categoria = categories[categoria_nombre]
            if categoria.id is None:
                raise RuntimeError("La categoría seed no tiene ID")
            session.add(
                Producto(
                    categoria_id=categoria.id,
                    nombre=nombre,
                    descripcion=descripcion,
                    precio_base=precio,
                    imagen_url="",
                    stock=stock,
                    disponible=True,
                    activo=True,
                )
            )

    session.commit()


def main() -> None:
    create_all_tables()
    with Session(engine) as session:
        seed_database(session)
    print("Seed completado: admin, 3 categorías y 8 productos.")


if __name__ == "__main__":
    main()
