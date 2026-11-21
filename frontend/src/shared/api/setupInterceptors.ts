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
      const detail = error.response?.data
      const disabledAccount =
        typeof detail === 'object' &&
        detail !== null &&
        'detail' in detail &&
        (detail.detail === 'Cuenta de usuario desactivada' ||
          detail.detail === 'Usuario deshabilitado')
      if ((error.response?.status === 401 && !isAuthCheck) ||
          (error.response?.status === 400 && disabledAccount)) {
        useAuthStore.getState().clearSession()
      } else if (error.response?.status === 403) {
        useNotificationStore.getState().showNotification('Acceso denegado: no tienes permisos para realizar esta acción.')
      }
    }
    return Promise.reject(error)
  },
)
