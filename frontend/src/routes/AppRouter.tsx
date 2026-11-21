import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AdminUsersPage, LoginPage, RegisterPage } from '@/features/auth'
import { CarritoPage } from '@/features/cart/pages/CarritoPage'
import { CatalogoPage } from '@/features/catalog/pages/CatalogoPage'
import { CategoriasPage } from '@/features/categories'
import { CheckoutPage } from '@/features/orders/pages/CheckoutPage'
import { MisPedidosPage } from '@/features/orders/pages/MisPedidosPage'
import { ProductsPage } from '@/features/products'
import { ProtectedRoute } from '@/routes/ProtectedRoute'
import { Navbar } from '@/shared/components/Navbar'
import { UnauthorizedPage } from '@/shared/components/UnauthorizedPage'
import { useThemeStore } from '@/shared/store/themeStore'

export function AppRouter() {
  const darkMode = useThemeStore((state) => state.darkMode)
  return (
    <BrowserRouter>
      <div className={`${darkMode ? 'dark' : ''} flex min-h-screen flex-col bg-gray-50`}>
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<CatalogoPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/carrito" element={<CarritoPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/checkout" element={<CheckoutPage />} />
              <Route path="/mis-pedidos" element={<MisPedidosPage />} />
            </Route>

            <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
              <Route path="/admin/categorias" element={<CategoriasPage />} />
              <Route path="/admin/productos" element={<ProductsPage />} />
              <Route path="/admin/usuarios" element={<AdminUsersPage />} />
            </Route>

            <Route
              path="*"
              element={
                <div className="p-8 text-center">
                  <h1 className="text-4xl font-bold">404</h1>
                  <p>Página no encontrada</p>
                </div>
              }
            />
          </Routes>
        </main>
        <footer className="mt-12 bg-gray-900 py-6 text-center text-white">
          🍕 Food Store UTN
        </footer>
      </div>
    </BrowserRouter>
  )
}
