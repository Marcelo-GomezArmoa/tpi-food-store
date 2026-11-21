import os
from collections.abc import Iterator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

with patch.dict(os.environ, {"DATABASE_URL": "sqlite://"}):
    from app.core.database import get_session
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


@pytest.fixture
def api() -> Iterator[tuple[TestClient, object]]:
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

    app.dependency_overrides.clear()
    app.dependency_overrides[get_session] = test_session
    app.dependency_overrides[get_categorias_uow] = (
        lambda: CategoriasUnitOfWork(engine)
    )
    app.dependency_overrides[get_productos_uow] = (
        lambda: ProductosUnitOfWork(engine)
    )
    app.dependency_overrides[get_pedidos_uow] = lambda: PedidosUnitOfWork(engine)

    client = TestClient(app)
    yield client, engine
    client.close()
    app.dependency_overrides.clear()
    engine.dispose()


def login(client: TestClient, username: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()


def register_user(client: TestClient, username: str = "cliente") -> dict:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "full_name": "Cliente Prueba",
            "email": f"{username}@example.com",
            "password": "Cliente1234!",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def create_order(client: TestClient, product_id: int, quantity: int = 1) -> dict:
    response = client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "Calle Principal 123",
            "items": [{"producto_id": product_id, "cantidad": quantity}],
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def first_product(client: TestClient) -> dict:
    response = client.get("/api/v1/productos")
    assert response.status_code == 200, response.text
    return response.json()["items"][0]


def test_catalog_read_routes_are_public(
    api: tuple[TestClient, object],
) -> None:
    client, _ = api
    categories = client.get("/api/v1/categorias")
    assert categories.status_code == 200
    assert len(categories.json()) == 3
    assert client.get(
        f"/api/v1/categorias/{categories.json()[0]['id']}"
    ).status_code == 200

    products = client.get("/api/v1/productos")
    assert products.status_code == 200
    assert products.json()["total"] == 8
    assert client.get(
        f"/api/v1/productos/{products.json()['items'][0]['id']}"
    ).status_code == 200


def test_auth_contract_and_duplicate_conflicts(
    api: tuple[TestClient, object],
) -> None:
    client, _ = api
    public = register_user(client)
    assert public["role"] == "user"
    assert public["disabled"] is False
    assert "hashed_password" not in public

    duplicate_username = client.post(
        "/api/v1/auth/register",
        json={
            "username": "cliente",
            "full_name": "Otro",
            "email": "otro@example.com",
            "password": "Cliente1234!",
        },
    )
    assert duplicate_username.status_code == 409
    duplicate_email = client.post(
        "/api/v1/auth/register",
        json={
            "username": "cliente-2",
            "full_name": "Otro",
            "email": "cliente@example.com",
            "password": "Cliente1234!",
        },
    )
    assert duplicate_email.status_code == 409

    wrong = client.post(
        "/api/v1/auth/token",
        data={"username": "cliente", "password": "incorrecta"},
    )
    assert wrong.status_code == 401
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "cliente", "password": "Cliente1234!"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Login exitoso"}
    cookie = response.headers["set-cookie"]
    assert "HttpOnly" in cookie
    assert "access_token=" in cookie
    assert "Max-Age=1800" in cookie
    assert client.get("/api/v1/auth/me").status_code == 200

    logout = client.post("/api/v1/auth/logout")
    assert logout.status_code == 200
    assert client.get("/api/v1/auth/me").status_code == 401


def test_admin_users_activation_deactivation_and_self_protection(
    api: tuple[TestClient, object],
) -> None:
    client, engine = api
    user = register_user(client)
    login(client, "admin", "Admin1234!")

    users = client.get("/api/v1/admin/usuarios")
    assert users.status_code == 200
    assert len(users.json()) == 2

    disabled = client.post(f"/api/v1/admin/usuarios/{user['id']}/desactivar")
    assert disabled.status_code == 200
    assert disabled.json()["disabled"] is True
    repeated = client.post(f"/api/v1/admin/usuarios/{user['id']}/desactivar")
    assert repeated.status_code == 200
    assert repeated.json()["disabled"] is True
    assert client.post("/api/v1/admin/usuarios/999/activar").status_code == 404

    with Session(engine) as session:
        admin = session.exec(
            select(Usuario).where(Usuario.username == "admin")
        ).one()
        assert admin.id is not None
        admin_id = admin.id
    assert (
        client.post(f"/api/v1/admin/usuarios/{admin_id}/desactivar").status_code
        == 400
    )

    user_login = client.post(
        "/api/v1/auth/token",
        data={"username": "cliente", "password": "Cliente1234!"},
    )
    assert user_login.status_code == 400
    login(client, "admin", "Admin1234!")
    activated = client.post(f"/api/v1/admin/usuarios/{user['id']}/activar")
    assert activated.status_code == 200
    assert activated.json()["disabled"] is False


def test_catalog_pagination_filters_partial_update_and_logical_delete(
    api: tuple[TestClient, object],
) -> None:
    client, _ = api
    login(client, "admin", "Admin1234!")

    page = client.get("/api/v1/productos?skip=0&limit=3")
    assert page.status_code == 200
    assert page.json()["total"] == 8
    assert len(page.json()["items"]) == 3
    assert client.get("/api/v1/productos?limit=101").status_code == 422

    search = client.get("/api/v1/productos?search=pIzZa")
    assert search.status_code == 200
    assert search.json()["total"] == 3
    filtered = client.get(
        "/api/v1/productos?categoria_id=1&disponible=true"
    )
    assert filtered.json()["total"] >= 3
    assert all(item["categoria_id"] == 1 for item in filtered.json()["items"])
    assert all(item["disponible"] for item in filtered.json()["items"])

    categories = client.get("/api/v1/categorias").json()
    created = client.post(
        "/api/v1/productos",
        json={
            "categoria_id": categories[0]["id"],
            "nombre": "Producto Bloque B",
            "descripcion": "Original",
            "precio_base": 1250.0,
            "imagen_url": "",
            "stock": 4,
        },
    )
    assert created.status_code == 201
    product = created.json()
    assert product["categoria"]["id"] == categories[0]["id"]

    updated = client.put(
        f"/api/v1/productos/{product['id']}",
        json={"nombre": "Producto actualizado"},
    )
    assert updated.status_code == 200
    assert updated.json()["descripcion"] == "Original"
    assert updated.json()["stock"] == 4

    stock = client.patch(
        f"/api/v1/productos/{product['id']}/stock",
        json={"stock": 0},
    )
    assert stock.status_code == 200
    assert stock.json()["stock"] == 0
    assert stock.json()["disponible"] is False

    deleted = client.delete(f"/api/v1/productos/{product['id']}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"/api/v1/productos/{product['id']}").status_code == 404
    hidden = client.get(f"/api/v1/productos?search=actualizado").json()
    assert hidden["total"] == 0


def test_category_contracts_and_delete_keeps_name_reserved(
    api: tuple[TestClient, object],
) -> None:
    client, _ = api
    login(client, "admin", "Admin1234!")
    response = client.post(
        "/api/v1/categorias",
        json={"nombre": "Promos", "descripcion": "Original"},
    )
    assert response.status_code == 201
    category_id = response.json()["id"]
    assert client.post(
        "/api/v1/categorias",
        json={"nombre": "Promos", "descripcion": "Duplicada"},
    ).status_code == 409
    updated = client.put(
        f"/api/v1/categorias/{category_id}",
        json={"nombre": "Promociones"},
    )
    assert updated.status_code == 200
    assert updated.json()["descripcion"] == "Original"

    deleted = client.delete(f"/api/v1/categorias/{category_id}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"/api/v1/categorias/{category_id}").status_code == 404
    assert client.post(
        "/api/v1/categorias",
        json={"nombre": "Promociones", "descripcion": "Duplicada"},
    ).status_code == 409


def test_rn01_validation_and_atomic_stock_rollback(
    api: tuple[TestClient, object],
) -> None:
    client, engine = api
    register_user(client)
    login(client, "cliente", "Cliente1234!")
    products = client.get("/api/v1/productos").json()["items"]
    product = products[0]
    original_stock = product["stock"]

    assert client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "Calle Principal 123",
            "items": [],
        },
    ).status_code == 400
    assert client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "Calle Principal 123",
            "items": [
                {"producto_id": product["id"], "cantidad": 1},
                {"producto_id": product["id"], "cantidad": 1},
            ],
        },
    ).status_code == 400
    assert client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "TARJETA",
            "direccion_entrega": "Calle Principal 123",
            "items": [{"producto_id": product["id"], "cantidad": 1}],
        },
    ).status_code == 400
    assert client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "x",
            "items": [{"producto_id": product["id"], "cantidad": 1}],
        },
    ).status_code == 400
    assert client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "Calle Principal 123",
            "items": [{"producto_id": 99999, "cantidad": 1}],
        },
    ).status_code == 404

    failed = client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "Calle Principal 123",
            "items": [
                {"producto_id": product["id"], "cantidad": 1},
                {"producto_id": 99999, "cantidad": 1},
            ],
        },
    )
    assert failed.status_code == 404
    with Session(engine) as session:
        stored = session.get(Producto, product["id"])
        assert stored is not None
        assert stored.stock == original_stock
        assert session.exec(select(Pedido)).all() == []
        assert session.exec(select(DetallePedido)).all() == []

    unavailable = client.patch(
        f"/api/v1/productos/{products[1]['id']}/stock",
        json={"stock": 0},
    )
    assert unavailable.status_code == 403
    login(client, "admin", "Admin1234!")
    assert client.patch(
        f"/api/v1/productos/{products[1]['id']}/stock",
        json={"stock": 0},
    ).status_code == 200
    login(client, "cliente", "Cliente1234!")
    assert client.post(
        "/api/v1/pedidos",
        json={
            "forma_pago": "EFECTIVO",
            "direccion_entrega": "Calle Principal 123",
            "items": [{"producto_id": products[1]["id"], "cantidad": 1}],
        },
    ).status_code == 400


def test_rn02_to_rn05_ownership_transitions_cancel_and_summary(
    api: tuple[TestClient, object],
) -> None:
    client, engine = api
    owner = register_user(client, "duenio")
    register_user(client, "intruso")
    login(client, "duenio", "Cliente1234!")
    product = first_product(client)
    order = create_order(client, product["id"], 2)
    assert order["estado"] == "PENDIENTE"
    assert order["usuario_id"] == owner["id"]
    assert order["items"][0]["nombre_producto"] == product["nombre"]
    assert order["items"][0]["precio_unitario"] == product["precio_base"]
    assert order["items"][0]["subtotal"] == product["precio_base"] * 2
    assert order["total"] == order["items"][0]["subtotal"]

    listing = client.get("/api/v1/pedidos?estado=PENDIENTE")
    assert listing.status_code == 200
    assert listing.json()["total"] == 1
    assert login(client, "intruso", "Cliente1234!")
    assert client.get(f"/api/v1/pedidos/{order['id']}").status_code == 403
    assert (
        client.patch(f"/api/v1/pedidos/{order['id']}/cancelar").status_code
        == 403
    )

    login(client, "admin", "Admin1234!")
    assert client.patch(
        f"/api/v1/pedidos/{order['id']}/estado",
        json={"estado": "ENTREGADO"},
    ).status_code == 400
    preparing = client.patch(
        f"/api/v1/pedidos/{order['id']}/estado",
        json={"estado": "EN_PREPARACION"},
    )
    assert preparing.status_code == 200
    assert preparing.json()["estado"] == "EN_PREPARACION"
    delivered = client.patch(
        f"/api/v1/pedidos/{order['id']}/estado",
        json={"estado": "ENTREGADO"},
    )
    assert delivered.status_code == 200
    assert client.patch(
        f"/api/v1/pedidos/{order['id']}/estado",
        json={"estado": "CANCELADO"},
    ).status_code == 400
    summary = client.get("/api/v1/pedidos/resumen")
    assert summary.status_code == 200
    assert summary.json()["entregados"] == 1
    assert summary.json()["ingresos_entregados"] == order["total"]
    assert summary.json()["pedidos_hoy"] == 1

    login(client, "duenio", "Cliente1234!")
    cancel_terminal = client.patch(
        f"/api/v1/pedidos/{order['id']}/cancelar"
    )
    assert cancel_terminal.status_code == 400
    with Session(engine) as session:
        stored = session.get(Producto, product["id"])
        assert stored is not None
        assert stored.stock == product["stock"] - 2


def test_cancel_pending_restores_stock_and_admin_list_sees_all(
    api: tuple[TestClient, object],
) -> None:
    client, engine = api
    register_user(client, "duenio")
    register_user(client, "otro")
    login(client, "duenio", "Cliente1234!")
    product = first_product(client)
    first = create_order(client, product["id"], 3)
    login(client, "otro", "Cliente1234!")
    second_product = client.get("/api/v1/productos").json()["items"][1]
    create_order(client, second_product["id"], 1)
    assert client.get("/api/v1/pedidos").json()["total"] == 1

    login(client, "duenio", "Cliente1234!")
    cancelled = client.patch(f"/api/v1/pedidos/{first['id']}/cancelar")
    assert cancelled.status_code == 200
    assert cancelled.json()["estado"] == "CANCELADO"
    assert client.patch(
        f"/api/v1/pedidos/{first['id']}/cancelar"
    ).status_code == 400
    with Session(engine) as session:
        restored = session.get(Producto, product["id"])
        assert restored is not None
        assert restored.stock == product["stock"]
        assert restored.disponible is True

    login(client, "admin", "Admin1234!")
    admin_list = client.get("/api/v1/pedidos")
    assert admin_list.status_code == 200
    assert admin_list.json()["total"] == 2


def test_admin_cancellation_returns_stock_and_respects_terminal_states(
    api: tuple[TestClient, object],
) -> None:
    client, engine = api
    register_user(client)
    login(client, "cliente", "Cliente1234!")
    product = first_product(client)
    order = create_order(client, product["id"], 1)

    login(client, "admin", "Admin1234!")
    assert client.patch(
        f"/api/v1/pedidos/{order['id']}/estado",
        json={"estado": "CANCELADO"},
    ).status_code == 200
    assert client.patch(
        f"/api/v1/pedidos/{order['id']}/estado",
        json={"estado": "EN_PREPARACION"},
    ).status_code == 400
    with Session(engine) as session:
        restored = session.get(Producto, product["id"])
        assert restored is not None
        assert restored.stock == product["stock"]


def test_rn05_order_has_no_edit_or_delete_endpoints(
    api: tuple[TestClient, object],
) -> None:
    client, _ = api
    login(client, "admin", "Admin1234!")
    assert client.delete("/api/v1/pedidos/1").status_code == 405
    assert client.put(
        "/api/v1/pedidos/1",
        json={"direccion_entrega": "Otra calle"},
    ).status_code == 405
