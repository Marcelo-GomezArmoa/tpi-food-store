# Food Store — Trabajo Práctico Integrador

Aplicación full stack para Programación 4 (UTN) con FastAPI, SQLModel,
PostgreSQL, React, TypeScript, TanStack Query/Form/Table y Zustand.

## Repositorio y Video de Demostración

- **Repositorio:** https://github.com/Marcelo-GomezArmoa/tpi-food-store.git
- **Video de demostración:** https://youtu.be/q89iKppDJtQ

## Requisitos

- Python 3.11 a 3.13
- PostgreSQL
- Node.js 20 o superior
- pnpm
- Git

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/Marcelo-GomezArmoa/tpi-food-store.git
cd tpi-food-store
```

### 2. Configurar y ejecutar el backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.db.seed
fastapi dev app/main.py
```

El seed es idempotente y crea el administrador, 3 categorías y 8 productos.

Credenciales de administración:

- Usuario: `admin`
- Contraseña: `Admin1234!`

Backend local: `http://localhost:8000`

Documentación OpenAPI: `http://localhost:8000/docs`

### 3. Configurar y ejecutar el frontend

```powershell
cd frontend
pnpm install
Copy-Item .env.example .env
pnpm dev
```

Frontend local: `http://localhost:5173`

## Variables de entorno

### `backend/.env.example`

```ini
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/food_store
SECRET_KEY=change-this-value-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_ORIGIN=http://localhost:5173
```

### `frontend/.env.example`

```ini
VITE_API_URL=http://localhost:8000/api/v1
```

La sesión se mantiene en una cookie `HttpOnly`; el frontend utiliza
`withCredentials` y no persiste tokens en Zustand/localStorage.

## Rutas principales

### Cliente

- `/`
- `/login`
- `/register`
- `/carrito`
- `/checkout`
- `/mis-pedidos`
- `/unauthorized`

### Administración

- `/admin/resumen`
- `/admin/categorias`
- `/admin/productos`
- `/admin/pedidos`
- `/admin/usuarios`

## Verificación

Backend:

```powershell
cd backend
pytest -q
```

Frontend:

```powershell
cd frontend
pnpm build
```

## Arquitectura

```text
backend/app/
├── core/
├── db/
└── modules/
    ├── auth/
    ├── usuarios/
    ├── categorias/
    ├── productos/
    └── pedidos/

frontend/src/
├── features/
├── routes/
└── shared/
```
