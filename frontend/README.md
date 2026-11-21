# Food Store: frontend

Aplicación React, TypeScript y Vite organizada por dominio.

## Ejecución

Desde esta carpeta, con Node.js compatible con Vite y pnpm instalados:

```sh
pnpm install
pnpm dev
```

El backend se espera en `http://localhost:8000`; puede configurarse con
`VITE_API_URL`. La API utiliza cookies (`withCredentials`).
Para verificar el proyecto: `pnpm build` y `pnpm lint`.

## Estructura

- `src/features/`: dominios `auth`, `categories`, `products` e `ingredients`,
  cada uno con su API pública en `index.ts`, páginas, hooks y tipos.
- `src/shared/`: cliente HTTP, componentes y estado de interfaz compartidos.
- `src/routes/`: rutas y protección por sesión y roles.
- `@/` apunta a `src/` tanto en Vite como en TypeScript. Las dependencias entre
  features se importan exclusivamente desde su `index.ts`.

Zustand mantiene la sesión en memoria y la verifica con `/api/v1/auth/me` al
iniciar; no guarda credenciales ni usuario en almacenamiento local. El store
de tema persiste la preferencia en `theme-storage` y el de notificaciones
controla el aviso global. TanStack Query gestiona las consultas y mutaciones.
