# Food Store — TPI Programación 4

Aplicación full stack para la gestión de un comercio de alimentos, desarrollada
para la UTN. El backend implementa FastAPI, SQLModel, PostgreSQL, autenticación
por cookie JWT y el patrón Unit of Work.

Repositorio: <https://github.com/Marcelo-GomezArmoa/tpi-food-store>

## Backend

### Variables de entorno

Copiar `backend/.env.example` como `backend/.env` y configurar:

```ini
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/food_store
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_ORIGIN=http://localhost:5173
```

### Instalación y seed

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.db.seed
```

El seed es idempotente y carga:

- Usuario administrador: `admin`
- Contraseña: `Admin1234!`
- 3 categorías
- 8 productos con stock

### Ejecución

```powershell
fastapi dev app/main.py
```

API local: `http://localhost:8000`

OpenAPI: `http://localhost:8000/docs`

### Estructura

```text
backend/
├── app/
│   ├── core/
│   ├── db/seed.py
│   ├── modules/
│   │   ├── auth/
│   │   ├── usuarios/
│   │   ├── categorias/
│   │   ├── productos/
│   │   └── pedidos/
│   └── main.py
├── tests/
├── .env.example
└── requirements.txt
```

Todas las rutas funcionales del backend se exponen bajo `/api/v1`:

- `/api/v1/auth/register`
- `/api/v1/auth/login` — alias compatible `/api/v1/auth/token`
- `/api/v1/auth/logout`
- `/api/v1/auth/me`
- `/api/v1/usuarios`
- `/api/v1/categorias`
- `/api/v1/productos`
- `/api/v1/pedidos`

### Pruebas

```powershell
cd backend
pytest -q
```

## Frontend

```powershell
cd frontend
pnpm install
pnpm dev
```

La integración completa de las nuevas rutas y del flujo de carrito/pedidos
corresponde al Bloque B.
