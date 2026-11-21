import { useAuthStore } from '@/features/auth/store/authStore'

export function useAuth() {
  const usuario = useAuthStore((state) => state.usuario)
  const cargando = useAuthStore((state) => state.cargando)
  const error = useAuthStore((state) => state.error)
  const login = useAuthStore((state) => state.login)
  const logout = useAuthStore((state) => state.logout)
  return { usuario, cargando, error, login, logout }
}
