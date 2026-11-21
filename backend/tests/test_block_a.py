import os
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

with patch.dict(os.environ, {"DATABASE_URL": "sqlite://"}):
    from app.core.database import get_session
    from app.core.security import get_password_hash
    from app.db.seed import seed_database
    from app.main import app
    from app.modules.categorias.router import get_uow as get_categorias_uow
    from app.modules.categorias.unit_of_work import CategoriasUnitOfWork
    from app.modules.pedidos.models import DetallePedido, Pedido
    from app.modules.pedidos.router import get_uow as get_pedidos_uow
    from app.modules.pedidos.unit_of_work import PedidosUnitOfWork
    from app.modules.productos.models import Producto
    from app.modules.productos.router import get_uow as get_productos_uow
    from app.modules.productos.unit_of_work import ProductosUnitOfWork
    from app.modules.usuarios.models import Usuario


def build_test_client() -> tuple[TestClient, object]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_database(session)

    def test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = test_session
    app.dependency_overrides[get_categorias_uow] = (
        lambda: CategoriasUnitOfWork(engine)
    )
    app.dependency_overrides[get_productos_uow] = (
        lambda: ProductosUnitOfWork(engine)
    )
    app.dependency_overrides[get_pedidos_uow] = lambda: PedidosUnitOfWork(engine)
    return TestClient(app), engine


def login(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "Admin1234!"},
    )
    assert response.status_code == 200, response.text
    assert "access_token=" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]


def test_seed_is_idempotent_and_has_required_data() -> None:
    client, engine = build_test_client()
    try:
        with Session(engine) as session:
            seed_database(session)
            assert len(session.exec(select(Usuario)).all()) == 1
            assert len(session.exec(select(Producto)).all()) == 8
            assert len(session.exec(select(Pedido)).all()) == 0
    finally:
        client.close()


def test_api_is_under_v1_and_catalog_crud_uses_unit_of_work() -> None:
    client, _ = build_test_client()
    try:
        login(client)
        categories = client.get("/api/v1/categorias")
        assert categories.status_code == 200
        assert len(categories.json()) == 3

        product_response = client.post(
            "/api/v1/productos",
            json={
                "categoria_id": categories.json()[0]["id"],
                "nombre": "Producto de prueba",
                "descripcion": "Prueba",
                "precio_base": 123.45,
                "imagen_url": "https://example.com/producto.jpg",
                "stock": 12,
            },
        )
        assert product_response.status_code == 201, product_response.text
        assert product_response.json()["stock"] == 12

        response = client.delete(
            f"/api/v1/productos/{product_response.json()['id']}"
        )
        assert response.status_code == 204
        assert client.get(
            f"/api/v1/productos/{product_response.json()['id']}"
        ).status_code == 404
    finally:
        client.close()


def test_order_copies_product_name_and_price() -> None:
    client, engine = build_test_client()
    try:
        login(client)
        products = client.get("/api/v1/productos").json()
        response = client.post(
            "/api/v1/pedidos",
            json={
                "forma_pago": "EFECTIVO",
                "direccion_entrega": "Calle 123",
                "items": [{"producto_id": products[0]["id"], "cantidad": 2}],
            },
        )
        assert response.status_code == 201, response.text
        order = response.json()
        assert order["items"][0]["nombre_producto"] == products[0]["nombre"]
        assert order["items"][0]["precio_unitario"] == products[0]["precio_base"]
        assert order["total"] == products[0]["precio_base"] * 2

        with Session(engine) as session:
            stored_product = session.get(Producto, products[0]["id"])
            assert stored_product is not None
            stored_product.precio_base = 1.0
            session.commit()

        response = client.get(f"/api/v1/pedidos/{order['id']}")
        assert response.status_code == 200
        assert response.json()["items"][0]["precio_unitario"] == (
            products[0]["precio_base"]
        )
    finally:
        client.close()


def test_rollback_leaves_no_partial_order() -> None:
    client, engine = build_test_client()
    try:
        login(client)
        products = client.get("/api/v1/productos").json()
        response = client.post(
            "/api/v1/pedidos",
            json={
                "forma_pago": "EFECTIVO",
                "direccion_entrega": "Calle 123",
                "items": [
                    {"producto_id": products[0]["id"], "cantidad": 1},
                    {"producto_id": 999999, "cantidad": 1},
                ],
            },
        )
        assert response.status_code == 404
        with Session(engine) as session:
            assert session.exec(select(Pedido)).all() == []
            assert session.exec(select(DetallePedido)).all() == []
    finally:
        client.close()
