import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useCategories, type Categoria } from '@/features/categories'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'

export function useProductCategories(productId: number) {
  const { query: categorias } = useCategories()
  const queryClient = useQueryClient()
  const queryKey = ['producto-categorias', productId]
  const asignadas = useQuery({
    queryKey,
    queryFn: async () => {
      try {
        return (await api.get<Categoria[]>(`/productos/${productId}/categorias`)).data
      } catch (error) {
        notifyError(error)
        throw error
      }
    },
  })
  const asignar = useMutation({
    mutationFn: (id: number) => api.post(`/productos/${productId}/categorias`, { categoria_id: id }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Categoría asignada.')
    },
    onError: notifyError,
  })
  const quitar = useMutation({
    mutationFn: (id: number) => api.delete(`/productos/${productId}/categorias/${id}`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Categoría quitada.')
    },
    onError: notifyError,
  })
  return { categorias, asignadas, asignar, quitar }
}
