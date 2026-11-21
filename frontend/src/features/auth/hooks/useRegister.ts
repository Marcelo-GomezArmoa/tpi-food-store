import { useMutation } from '@tanstack/react-query'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'
import type { RegisterData, UsuarioAuth } from '@/features/auth/types/auth.types'

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterData) => api.post<UsuarioAuth>('/auth/register', data),
    onSuccess: () => useNotificationStore.getState().showNotification('Cuenta creada correctamente.'),
    onError: notifyError,
  })
}
