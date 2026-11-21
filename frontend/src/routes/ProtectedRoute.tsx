import { Navigate, Outlet } from 'react-router-dom'

import type { UserRole } from '@/features/auth/types/auth.types'
import { useAuthStore } from '@/features/auth/store/authStore'

interface ProtectedRouteProps {
  allowedRoles?: UserRole[]
}

export function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
  const usuario = useAuthStore((state) => state.usuario)
  const cargando = useAuthStore((state) => state.cargando)

  if (cargando) {
    return (
      <div className="p-12 text-center" role="status" aria-live="polite">
        Verificando sesión...
      </div>
    )
  }
  if (!usuario) return <Navigate to="/login" replace />
  if (allowedRoles && !allowedRoles.includes(usuario.role)) {
    return <Navigate to="/unauthorized" replace />
  }
  return <Outlet />
}
