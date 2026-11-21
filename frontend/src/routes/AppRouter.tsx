import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AdminUsersPage, LoginPage, RegisterPage, useAuth } from '@/features/auth'
import { CategoriasPage } from '@/features/categories'
import { ProductsPage } from '@/features/products'
import { IngredientesPage } from '@/features/ingredients'
import { ProtectedRoute } from '@/routes/ProtectedRoute'
import { Navbar } from '@/shared/components/Navbar'
import { UnauthorizedPage } from '@/shared/components/UnauthorizedPage'
import { useThemeStore } from '@/shared/store/themeStore'

function InitialRedirect() {
  const { user, checking } = useAuth()
  if (checking) return <div role="status">Verificando sesión...</div>
  return <Navigate to={user ? '/categories' : '/login'} replace />
}

export function AppRouter() {
  const darkMode = useThemeStore((state) => state.darkMode)
  return (
    <BrowserRouter>
      <div className={`${darkMode ? 'dark' : ''} flex min-h-screen flex-col bg-gray-50`}>
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<InitialRedirect />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            <Route element={<ProtectedRoute />}>
              <Route path="/categories" element={<CategoriasPage />} />
              <Route path="/categorias" element={<Navigate to="/categories" replace />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/productos" element={<Navigate to="/products" replace />} />
              <Route path="/ingredientes" element={<IngredientesPage />} />
              <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                <Route path="/admin/users" element={<AdminUsersPage />} />
              </Route>
            </Route>
            <Route path="*" element={<div className="p-8 text-center"><h1 className="text-4xl font-bold">404</h1><p>Página no encontrada</p></div>} />
          </Routes>
        </main>
        <footer className="mt-12 bg-gray-900 py-6 text-center text-white">
          🍕 Food Store UTN • Full Stack Development
        </footer>
      </div>
    </BrowserRouter>
  )
}
