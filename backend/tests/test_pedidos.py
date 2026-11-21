import os
import unittest
from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

with patch.dict(os.environ, {"DATABASE_URL": "postgresql+psycopg2://test:test@localhost/test"}):
    from app.main import app
    from app.core.database import get_session
    from app.core.security import hash_password
    from app.modules.usuarios.models import Rol, Usuario, UsuarioRol
    from app.pedido.models import DetallePedido, Pedido
    from app.pedido.router import get_uow
    from app.pedido.unit_of_work import UnitOfWork
    from app.producto.model import Producto


class PedidoApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.secret_patch = patch.dict(os.environ, {"SECRET_KEY": "test-secret-key-at-least-32-bytes-long"})
        self.secret_patch.start()
        self.addCleanup(self.secret_patch.stop)
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        @event.listens_for(self.engine, "connect")
        def enable_foreign_keys(dbapi_connection, _connection_record):
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

        SQLModel.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            session.add_all(
                [
                    Usuario(
                        id=1, nombre="Admin", apellido="Prueba",
                        email="admin@example.com", password_hash=hash_password("Test-1234!"),
                    ),
                    Rol(id=1, nombre="admin"),
                    UsuarioRol(usuario_id=1, rol_id=1),
                    Producto(
                        id=1, nombre="Uno", descripcion="", precio_base=10.5
                    ),
                    Producto(
                        id=2, nombre="Dos", descripcion="", precio_base=3.0
                    ),
                ]
            )
            session.commit()
        app.dependency_overrides[get_uow] = lambda: UnitOfWork(self.engine)
        def test_session():
            with Session(self.engine) as session:
                yield session

        app.dependency_overrides[get_session] = test_session
        self.client = TestClient(app)
        response = self.client.post(
            "/api/v1/auth/token",
            data={"username": "admin@example.com", "password": "Test-1234!"},
        )
        self.assertEqual(response.status_code, 200, response.text)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.pop(get_uow, None)
        app.dependency_overrides.pop(get_session, None)
        self.engine.dispose()

    def test_crear_listar_y_actualizar_guardan_precio_original(self) -> None:
        response = self.client.post(
            "/pedidos",
            json={
                "detalles": [
                    {"producto_id": 1, "cantidad": 2},
                    {"producto_id": 2, "cantidad": 3},
                ]
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        pedido = response.json()
        self.assertEqual(pedido["estado"], "PENDIENTE")
        self.assertEqual(pedido["total"], 30.0)
        self.assertIsNone(pedido["deleted_at"])
        self.assertIsNotNone(datetime.fromisoformat(pedido["fecha"]).utcoffset())
        detalles = {item["producto_id"]: item for item in pedido["detalles"]}
        self.assertEqual(detalles[1]["precio_unitario"], 10.5)
        self.assertEqual(detalles[2]["precio_unitario"], 3.0)
        self.assertTrue(all(d["pedido_id"] == pedido["id"] for d in detalles.values()))

        with Session(self.engine) as session:
            producto = session.get(Producto, 1)
            assert producto is not None
            producto.precio_base = 100.0
            session.commit()

        pedido_id = pedido["id"]
        response = self.client.get(f"/pedidos/{pedido_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 30.0)
        detalles = {item["producto_id"]: item for item in response.json()["detalles"]}
        self.assertEqual(detalles[1]["precio_unitario"], 10.5)
        response = self.client.get("/pedidos")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(len(response.json()[0]["detalles"]), 2)

        response = self.client.put(
            f"/pedidos/{pedido_id}", json={"estado": "CONFIRMADO"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "CONFIRMADO")
        self.assertEqual(response.json()["total"], 30.0)

    def test_validacion_de_detalles_y_estado(self) -> None:
        for detalles in (
            [],
            [{"producto_id": 1, "cantidad": 0}],
            [
                {"producto_id": 1, "cantidad": 1},
                {"producto_id": 1, "cantidad": 2},
            ],
        ):
            with self.subTest(detalles=detalles):
                response = self.client.post("/pedidos", json={"detalles": detalles})
                self.assertEqual(response.status_code, 422, response.text)
        response = self.client.put("/pedidos/1", json={"estado": "INVALIDO"})
        self.assertEqual(response.status_code, 422)
        with Session(self.engine) as session:
            self.assertEqual(session.exec(select(Pedido)).all(), [])

    def test_producto_inexistente_revierte_todo(self) -> None:
        response = self.client.post(
            "/pedidos",
            json={
                "detalles": [
                    {"producto_id": 1, "cantidad": 1},
                    {"producto_id": 999, "cantidad": 1},
                ]
            },
        )
        self.assertEqual(response.status_code, 404, response.text)
        with Session(self.engine) as session:
            self.assertEqual(session.exec(select(Pedido)).all(), [])
            self.assertEqual(session.exec(select(DetallePedido)).all(), [])

    def test_error_de_commit_revierte_la_transaccion(self) -> None:
        with self.assertRaises(IntegrityError):
            with UnitOfWork(self.engine) as uow:
                pedido = Pedido(usuario_id=1)
                uow.pedidos.add(pedido)
                assert pedido.id is not None
                uow.detalles.add(
                    DetallePedido(
                        pedido_id=pedido.id, producto_id=1,
                        cantidad=1, precio_unitario=10.5,
                    )
                )
                uow.detalles.add(
                    DetallePedido(
                        pedido_id=pedido.id, producto_id=1,
                        cantidad=1, precio_unitario=10.5,
                    )
                )
        with Session(self.engine) as session:
            self.assertEqual(session.exec(select(Pedido)).all(), [])
            self.assertEqual(session.exec(select(DetallePedido)).all(), [])

    def test_producto_referenciado_se_elimina_logicamente(self) -> None:
        created = self.client.post(
            "/pedidos", json={"detalles": [{"producto_id": 1, "cantidad": 1}]}
        )
        self.assertEqual(created.status_code, 201, created.text)

        response = self.client.delete("/productos/1")
        self.assertEqual(response.status_code, 204, response.text)
        self.assertEqual(self.client.get("/productos/1").status_code, 404)
        self.assertEqual(self.client.get(f"/pedidos/{created.json()['id']}").status_code, 200)
        response = self.client.post(
            "/pedidos", json={"detalles": [{"producto_id": 1, "cantidad": 1}]}
        )
        self.assertEqual(response.status_code, 404, response.text)
        with Session(self.engine) as session:
            producto = session.get(Producto, 1)
            self.assertIsNotNone(producto)
            assert producto is not None
            self.assertIsNotNone(producto.deleted_at)
            self.assertEqual(len(session.exec(select(DetallePedido)).all()), 1)

    def test_registro_y_permisos_de_usuario(self) -> None:
        self.client.post("/api/v1/auth/logout")
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "nombre": "Usuario", "apellido": "Prueba",
                "email": "user@example.com", "password": "Test-1234!",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        self.assertEqual(response.json()["roles"], ["user"])
        user_id = response.json()["id"]
        response = self.client.post(
            "/api/v1/auth/token",
            data={"username": "user@example.com", "password": "Test-1234!"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn("HttpOnly", response.headers["set-cookie"])
        self.assertEqual(self.client.get("/api/v1/auth/me").json()["roles"], ["user"])
        for endpoint in ("/categorias", "/productos", "/ingredientes", "/pedidos"):
            self.assertEqual(self.client.get(endpoint).status_code, 200, endpoint)
        response = self.client.post(
            "/pedidos", json={"detalles": [{"producto_id": 1, "cantidad": 1}]}
        )
        self.assertEqual(response.status_code, 201, response.text)
        with Session(self.engine) as session:
            pedido = session.get(Pedido, response.json()["id"])
            self.assertIsNotNone(pedido)
            assert pedido is not None
            self.assertEqual(pedido.usuario_id, user_id)
        self.assertEqual(self.client.get("/api/v1/auth/admin/usuarios").status_code, 403)
        self.assertEqual(
            self.client.post("/ingredientes", json={"nombre": "Prueba"}).status_code,
            403,
        )
        self.assertEqual(self.client.post("/api/v1/auth/logout").status_code, 204)
        self.assertEqual(self.client.get("/api/v1/auth/me").status_code, 401)

    def test_borrado_logico_y_pedidos_inexistentes(self) -> None:
        response = self.client.post(
            "/pedidos", json={"detalles": [{"producto_id": 1, "cantidad": 1}]}
        )
        pedido_id = response.json()["id"]
        response = self.client.delete(f"/pedidos/{pedido_id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get("/pedidos").json(), [])
        self.assertEqual(self.client.get(f"/pedidos/{pedido_id}").status_code, 404)
        self.assertEqual(
            self.client.put(
                f"/pedidos/{pedido_id}", json={"estado": "CANCELADO"}
            ).status_code,
            404,
        )
        self.assertEqual(self.client.delete(f"/pedidos/{pedido_id}").status_code, 404)
        self.assertEqual(self.client.get("/pedidos/999").status_code, 404)
        with Session(self.engine) as session:
            pedido = session.get(Pedido, pedido_id)
            self.assertIsNotNone(pedido)
            assert pedido is not None
            self.assertIsNotNone(pedido.deleted_at)
            self.assertEqual(len(session.exec(select(DetallePedido)).all()), 1)


if __name__ == "__main__":
    unittest.main()
