import { useAuthStore } from '@/features/auth/store/authStore'

export function useAuth() {
  const user = useAuthStore((state) => state.user)
  const checking = useAuthStore((state) => state.checking)
  const isLoading = useAuthStore((state) => state.isLoading)
  const error = useAuthStore((state) => state.error)
  const login = useAuthStore((state) => state.login)
  const logout = useAuthStore((state) => state.logout)
  return { user, checking, isLoading, error, login, logout }
}
