import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '@/features/auth'

export function ProtectedRoute({ allowedRoles }: { allowedRoles?: string[] }) {
  const { user, checking } = useAuth()

  if (checking) return <div role="status" aria-live="polite">Verificando sesión...</div>
  if (!user) return <Navigate to="/login" replace />
  if (allowedRoles && !user.roles.some((role) => allowedRoles.includes(role))) {
    return <Navigate to="/unauthorized" replace />
  }
  return <Outlet />
}
