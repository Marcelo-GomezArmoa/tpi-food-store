import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import type { UsuarioAdmin } from '@/features/auth/types/auth.types'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'

const USERS_PATH = '/admin/usuarios'
const queryKey = ['admin-users']

export function useAdminUsers() {
  const queryClient = useQueryClient()
  const users = useQuery({
    queryKey,
    queryFn: async () => (await api.get<UsuarioAdmin[]>(USERS_PATH)).data,
  })
  const changeStatus = useMutation({
    mutationFn: ({ id, active }: { id: number; active: boolean }) =>
      api.post<UsuarioAdmin>(
        `${USERS_PATH}/${id}/${active ? 'activar' : 'desactivar'}`,
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification(
        'Estado del usuario actualizado.',
      )
    },
    onError: notifyError,
  })
  return { users, changeStatus }
}
