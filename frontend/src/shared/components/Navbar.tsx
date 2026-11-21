import { Link } from 'react-router-dom'

import { useCartStore } from '@/features/cart/store/cartStore'
import { useAuth } from '@/features/auth'
import { useThemeStore } from '@/shared/store/themeStore'

export function Navbar() {
  const { usuario, logout, cargando } = useAuth()
  const items = useCartStore((state) => state.items)
  const itemCount = items.reduce((sum, item) => sum + item.cantidad, 0)
  const { darkMode, toggleTheme } = useThemeStore()

  return (
    <nav className="bg-linear-to-r from-blue-600 to-blue-900 shadow-lg">
      <div className="mx-auto flex min-h-16 max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-2 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-white">
          <span className="text-2xl">🍕</span>
          <span>Food Store UTN</span>
        </Link>

        <div className="flex flex-wrap items-center gap-2 text-white">
          <Link to="/" className="rounded px-3 py-2 hover:bg-blue-500">
            Catálogo
          </Link>
          <Link to="/carrito" className="rounded px-3 py-2 hover:bg-blue-500">
            Carrito ({itemCount})
          </Link>
          {usuario && (
            <Link to="/mis-pedidos" className="rounded px-3 py-2 hover:bg-blue-500">
              Mis pedidos
            </Link>
          )}
          {usuario?.role === 'admin' && (
            <>
              <Link to="/admin/categorias" className="rounded px-3 py-2 hover:bg-blue-500">
                Categorías
              </Link>
              <Link to="/admin/productos" className="rounded px-3 py-2 hover:bg-blue-500">
                Productos
              </Link>
              <Link to="/admin/usuarios" className="rounded px-3 py-2 hover:bg-blue-500">
                Usuarios
              </Link>
            </>
          )}
          <button
            type="button"
            onClick={toggleTheme}
            aria-pressed={darkMode}
            className="rounded border border-white px-3 py-2"
          >
            {darkMode ? 'Modo claro' : 'Modo oscuro'}
          </button>
          {usuario ? (
            <>
              <span className="hidden text-sm sm:inline">{usuario.full_name}</span>
              <button
                type="button"
                disabled={cargando}
                onClick={() => void logout()}
                className="rounded bg-white px-3 py-2 font-medium text-blue-800 disabled:opacity-50"
              >
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="rounded px-3 py-2 hover:bg-blue-500">
                Iniciar sesión
              </Link>
              <Link to="/register" className="rounded bg-white px-3 py-2 font-medium text-blue-800">
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
