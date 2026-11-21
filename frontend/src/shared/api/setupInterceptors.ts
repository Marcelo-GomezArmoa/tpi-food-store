import axios from 'axios'
import { useAuthStore } from '@/features/auth'
import { api } from '@/shared/api/api'
import { useNotificationStore } from '@/shared/store/notificationStore'

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      const path = (error.config?.url ?? '').split(/[?#]/, 1)[0].replace(/\/+$/, '')
      const isAuthCheck = path.endsWith('/auth/token') || path.endsWith('/auth/me')
      if (error.response?.status === 401 && !isAuthCheck) {
        useAuthStore.getState().clearSession()
      } else if (error.response?.status === 403) {
        useNotificationStore.getState().showNotification('Acceso denegado: no tienes permisos para realizar esta acción.')
      }
    }
    return Promise.reject(error)
  },
)
