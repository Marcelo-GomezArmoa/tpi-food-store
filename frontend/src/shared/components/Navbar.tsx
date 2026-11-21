import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '@/features/auth'
import { notifyError } from '@/shared/api/notifyError'
import { useThemeStore } from '@/shared/store/themeStore'

export function Navbar() {
  const navigate = useNavigate()
  const { user, logout, isLoading } = useAuth()
  const { darkMode, toggleTheme } = useThemeStore()
  const isAdmin = user?.roles.includes('admin') ?? false

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      notifyError(error)
    } finally {
      void navigate('/login', { replace: true })
    }
  }

  return (
    <nav className="bg-linear-to-r from-blue-600 to-blue-900 shadow-lg">
      <div className="mx-auto flex min-h-16 max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-2 sm:px-6 lg:px-8">
        <Link
          to={user ? '/categories' : '/login'}
          className="flex items-center gap-2 text-xl font-bold text-white"
        >
          <span className="text-2xl">🍕</span>
          <span>Food Store UTN</span>
        </Link>

        <button type="button" onClick={toggleTheme} aria-pressed={darkMode} className="rounded border border-white px-3 py-2 text-white">
          {darkMode ? 'Modo claro' : 'Modo oscuro'}
        </button>
        {user ? (
          <div className="flex flex-wrap items-center gap-2">
            <Link to="/categories" className="rounded px-3 py-2 text-white hover:bg-blue-500">
              Categorías
            </Link>
            <Link to="/products" className="rounded px-3 py-2 text-white hover:bg-blue-500">
              Productos
            </Link>
            <Link to="/ingredientes" className="rounded px-3 py-2 text-white hover:bg-blue-500">
              Ingredientes
            </Link>
            {isAdmin && (
              <Link to="/admin/users" className="rounded px-3 py-2 text-white hover:bg-blue-500">
                Usuarios
              </Link>
            )}
            <div className="border-l border-blue-300 pl-3 text-right text-sm text-white">
              <p className="font-semibold">
                {user.nombre} {user.apellido}
              </p>
              <p>{user.roles.join(', ')}</p>
            </div>
            <button
              type="button"
              disabled={isLoading}
              onClick={() => void handleLogout()}
              className="rounded bg-white px-3 py-2 font-medium text-blue-800 disabled:opacity-50"
            >
              Cerrar sesión
            </button>
          </div>
        ) : (
          <div className="flex gap-2">
            <Link to="/login" className="rounded px-3 py-2 text-white hover:bg-blue-500">
              Iniciar sesión
            </Link>
            <Link to="/register" className="rounded bg-white px-3 py-2 font-medium text-blue-800">
              Registrarse
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}
