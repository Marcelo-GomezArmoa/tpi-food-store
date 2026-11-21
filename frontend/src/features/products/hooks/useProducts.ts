import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'
import type { Producto } from '@/features/products/types/producto'

const queryKey = ['productos']

export function useProducts() {
  const queryClient = useQueryClient()
  const query = useQuery({
    queryKey,
    queryFn: async () => {
      try {
        return (await api.get<Producto[]>('/productos')).data
      } catch (error) {
        notifyError(error)
        throw error
      }
    },
  })
  const save = useMutation({
    mutationFn: ({ id, data }: { id?: number; data: Omit<Producto, 'id'> }) =>
      id === undefined ? api.post('/productos', data) : api.put(`/productos/${id}`, data),
    onSuccess: (_, { id }) => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification(id === undefined ? 'Producto creado.' : 'Producto actualizado.')
    },
    onError: notifyError,
  })
  const remove = useMutation({
    mutationFn: (id: number) => api.delete(`/productos/${id}`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Producto eliminado.')
    },
    onError: notifyError,
  })
  return { query, save, remove }
}
