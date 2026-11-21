import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'
import type { UsuarioAdmin } from '@/features/auth/types/auth.types'

const USERS_PATH = '/api/v1/auth/admin/usuarios'
const queryKey = ['admin-users']

export function useAdminUsers() {
  const queryClient = useQueryClient()
  const users = useQuery({
    queryKey,
    queryFn: async () => {
      try {
        return (await api.get<UsuarioAdmin[]>(USERS_PATH)).data
      } catch (error) {
        notifyError(error)
        throw error
      }
    },
  })
  const changeStatus = useMutation({
    mutationFn: ({ id, active }: { id: number; active: boolean }) =>
      api.post<UsuarioAdmin>(`${USERS_PATH}/${id}/${active ? 'activar' : 'desactivar'}`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Estado del usuario actualizado.')
    },
    onError: notifyError,
  })
  return { users, changeStatus }
}
