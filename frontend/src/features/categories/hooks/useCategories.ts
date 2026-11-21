import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'
import type { Categoria } from '@/features/categories/types/categoria'

const queryKey = ['categorias']

export function useCategories() {
  const queryClient = useQueryClient()
  const query = useQuery({
    queryKey,
    queryFn: async () => {
      try {
        return (await api.get<Categoria[]>('/categorias')).data
      } catch (error) {
        notifyError(error)
        throw error
      }
    },
  })
  const save = useMutation({
    mutationFn: ({ id, data }: { id?: number; data: Omit<Categoria, 'id'> }) =>
      id === undefined ? api.post('/categorias', data) : api.put(`/categorias/${id}`, data),
    onSuccess: (_, { id }) => {
      void queryClient.invalidateQueries({ queryKey })
      void queryClient.invalidateQueries({ queryKey: ['producto-categorias'] })
      useNotificationStore.getState().showNotification(id === undefined ? 'Categoría creada.' : 'Categoría actualizada.')
    },
    onError: notifyError,
  })
  const remove = useMutation({
    mutationFn: (id: number) => api.delete(`/categorias/${id}`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      void queryClient.invalidateQueries({ queryKey: ['producto-categorias'] })
      useNotificationStore.getState().showNotification('Categoría eliminada.')
    },
    onError: notifyError,
  })
  return { query, save, remove }
}
