# 🍕 Food Store - Sistema Full Stack (UTN)

Proyecto desarrollado para la **Unidad 7 (Trabajo Práctico)** de la Tecnicatura Universitaria en Programación (UTN). Consiste en una aplicación Web Full Stack orientada a la gestión integral de un comercio de alimentos, implementando un CRUD completo de productos y categorías con relaciones Muchos a Muchos (M2M).

---

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener instalados:

- **Python 3.10 o superior** ([Descargar](https://www.python.org/downloads/))
- **Node.js 18+ con npm o pnpm** ([Descargar](https://nodejs.org/))
- **Git** (para clonar el repositorio)

Verificar instalación:
```bash
python --version
node --version
npm --version  # o pnpm --version
```

---

## 🚀 Tecnologías Utilizadas

### Backend
* **Python 3.10+**
* **FastAPI** (Framework web moderno y asíncrono)
* **SQLModel / SQLAlchemy** (ORM para modelado de datos)
* **PostgreSQL** (Base de datos relacional)
* **Pydantic** (Validación de datos)

### Frontend
* **React 19** con **Vite** y **TypeScript** (Tipado estático)
* **Tailwind CSS v4** (Diseño moderno y responsivo)
* **TanStack Query (React Query v5)** (Gestión de estado del servidor y caché)
* **React Router DOM v7** (Enrutamiento del lado del cliente SPA)
* **ESLint** (Linting de código)

---

## 🔧 Variables de Entorno

### Backend (.env)
Crear un archivo `.env` en la carpeta `backend/`:

```ini
# Base de datos PostgreSQL
DATABASE_URL=postgresql+psycopg2://usuario:contraseña@localhost:5432/foodstore_db

# FastAPI (opcional)
API_HOST=0.0.0.0
API_PORT=8000
```

La URL debe apuntar a una instancia de PostgreSQL disponible. Copia
`backend/.env.example` como `backend/.env` y reemplaza únicamente allí los
valores de conexión. No se debe publicar el archivo `.env`.

---

## ⚙️ Guía de Instalación y Ejecución Local
### 1. Clonar el Repositorio
```bash
git clone https://github.com/Marcelo-GomezArmoa/tp-7.git
cd tp-7
```

### 2. Configurar y Ejecutar el Backend

```bash
# Entrar a la carpeta del backend
cd backend

# Crear y activar un entorno virtual (recomendado)
python -m venv .venv

# Activar el entorno virtual
# En Windows (PowerShell):
.venv\Scripts\Activate
# En macOS/Linux:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor de desarrollo FastAPI
fastapi dev app/main.py
```

✅ Backend disponible en: **http://localhost:8000**  
📚 Documentación Swagger: **http://localhost:8000/docs**

#### Base existente: migración del esquema

`create_all` crea tablas faltantes, pero no agrega columnas a tablas existentes.
Para la base `food_store` anterior a las columnas `categoria.deleted_at`,
`producto.deleted_at` y `pedido.usuario_id`, hacer primero una copia de seguridad
y ejecutar una sola vez desde `backend`, reemplazando `tu_usuario`:

```powershell
psql -h localhost -U tu_usuario -d food_store -v ON_ERROR_STOP=1 -f .\migrations\20261120_align_food_store.sql
```

La migración es transaccional y requiere que `pedido` esté vacía: si hay pedidos
existentes, se detiene sin cambios para no asignarles propietarios arbitrarios.
En ese caso hay que definir y validar una migración de propietarios antes de
continuar. El script tampoco debe repetirse sobre un esquema ya migrado.

### 3. Configurar y Ejecutar el Frontend

Abre **una nueva terminal** en la raíz del proyecto:

```bash
# Entrar a la carpeta del frontend
cd frontend

# Instalar dependencias
pnpm install
# o si usas npm:
npm install

# Iniciar el servidor de desarrollo Vite
npm run dev
```

✅ Frontend disponible en: **http://localhost:5173**

---

## 📦 Comandos Disponibles

### Backend
```bash
# Iniciar desarrollo con reloading automático
fastapi dev app/main.py

# Crear tablas en la BD
python -c "from app.core.database import create_db_and_tables; create_db_and_tables()"
```

### Frontend
```bash
# Desarrollo con HMR
npm run dev

# Build para producción
npm run build

# Preview de build
npm run preview

# Linting
npm run lint
```

---

## 🌐 Endpoints API Disponibles

### Categorías
- `GET /categorias` - Lista todas las categorías
- `GET /categorias/{id}` - Obtiene una categoría por ID
- `POST /categorias` - Crea una nueva categoría
- `PUT /categorias/{id}` - Actualiza una categoría
- `DELETE /categorias/{id}` - Elimina una categoría

### Productos
- `GET /productos` - Lista todos los productos
- `GET /productos/{id}` - Obtiene un producto por ID
- `POST /productos` - Crea un nuevo producto
- `PUT /productos/{id}` - Actualiza un producto
- `DELETE /productos/{id}` - Elimina un producto

### Relación Producto-Categoría (M2M)
- `POST /productos/{id}/categorias` - Asigna una categoría a un producto
- `GET /productos/{id}/categorias` - Lista categorías de un producto
- `DELETE /productos/{id}/categorias/{categoria_id}` - Desvincula una categoría

También hay una colección de solicitudes manuales en [`backend/api.http`](./backend/api.http).

---

## 🏗️ Estructura del Proyecto

```text
tp-7/
├── backend/
│   ├── app/
│   │   ├── categoria/        # Modelos, schemas y routers de categorías
│   │   │   ├── model.py      # Modelo SQLModel de Categoria
│   │   │   ├── schema.py     # Schemas Pydantic (Create, Read, Update)
│   │   │   ├── service.py    # Lógica de negocio CRUD
│   │   │   └── router.py     # Endpoints FastAPI
│   │   │
│   │   ├── producto/         # Modelos, schemas y routers de productos (con M2M)
│   │   │   ├── model.py      # Modelos Producto y ProductoCategoria
│   │   │   ├── schema.py     # Schemas Pydantic
│   │   │   ├── service.py    # Lógica CRUD + M2M
│   │   │   └── router.py     # Endpoints con relaciones
│   │   │
│   │   ├── core/
│   │   │   └── database.py   # Configuración BD y sesiones SQLModel
│   │   │
│   │   ├── __init__.py
│   │   └── main.py           # Punto de entrada FastAPI
│   │
│   ├── requirements.txt      # Dependencias Python
│   ├── .env.example          # Template de variables de entorno
│   └── api.http              # Pruebas manuales de endpoints
│
├── frontend/
│   ├── src/
│   │   ├── types/            # Interfaces TypeScript
│   │   │   ├── categoria.ts  # Interface Categoria
│   │   │   └── producto.ts   # Interface Producto
│   │   │
│   │   ├── services/         # Clientes HTTP y servicios API
│   │   │   ├── api.ts        # Cliente HTTP genérico fetchApi
│   │   │   ├── categoriaService.ts
│   │   │   └── productoService.ts
│   │   │
│   │   ├── components/       # Componentes reutilizables
│   │   │   ├── CategoriaCard.tsx
│   │   │   ├── CategoriaList.tsx
│   │   │   ├── CategoriaModal.tsx
│   │   │   └── Navbar.tsx
│   │   │
│   │   ├── pages/            # Páginas principales
│   │   │   ├── HomePage.tsx
│   │   │   ├── CategoriasPage.tsx
│   │   │   └── ProductsPage.tsx
│   │   │
│   │   ├── App.tsx           # Configuración de rutas
│   │   ├── App.css           # Estilos globales
│   │   ├── main.tsx          # Punto de entrada
│   │   └── index.css         # Importación Tailwind
│   │
│   ├── public/               # Assets públicos
│   ├── package.json          # Dependencias Node.js
│   ├── tsconfig.json         # Configuración TypeScript
│   ├── vite.config.ts        # Configuración Vite
│   ├── tailwind.config.js    # Configuración Tailwind CSS
│   ├── postcss.config.js     # Configuración PostCSS
│   └── eslint.config.js      # Configuración ESLint
│
└── README.md                 # Este archivo
```

---

## ✨ Características Principales

✅ **Arquitectura Modular:** Separación clara entre lógica de negocio (backend) y presentación (frontend)

✅ **Tipado Estricto:** Interfaces TypeScript sincronizadas con esquemas Pydantic/SQLModel

✅ **Manejo de Errores Robusto:** Cliente HTTP personalizado (`ApiError`) que captura detalles del servidor

✅ **Gestión Asíncrona Eficiente:** Caché inteligente, invalidación automática y reintentos con TanStack Query

✅ **Relaciones M2M:** Interfaz completa para asignar/remover categorías en productos

✅ **Interfaz Responsiva:** Diseño moderno con Tailwind CSS funcional en desktop, tablet y móvil

✅ **Validación de Datos:** Validación frontend y backend coordinada

✅ **SPA Completa:** Enrutamiento dinámico sin recargas con React Router

---

## 🤝 Contribuciones

Este es un proyecto académico de la UTN. Para sugerencias o mejoras, abre un **Issue** o **Pull Request**.

---

## 📞 Contacto y Soporte

- **Repositorio:** https://github.com/Marcelo-GomezArmoa/tp-7
- **Autor:** Marcelo Gómez Armoa
- **Institución:** Tecnicatura Universitaria en Programación (UTN)
- **Unidad:** 7 (Trabajo Práctico Integrador)