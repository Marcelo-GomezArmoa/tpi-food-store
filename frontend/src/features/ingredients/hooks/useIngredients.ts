import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'
import type { Ingrediente } from '@/features/ingredients/types/ingrediente'

const queryKey = ['ingredientes']

export function useIngredients() {
  const queryClient = useQueryClient()
  const query = useQuery({
    queryKey,
    queryFn: async () => {
      try {
        return (await api.get<Ingrediente[]>('/ingredientes')).data
      } catch (error) {
        notifyError(error)
        throw error
      }
    },
  })
  const save = useMutation({
    mutationFn: ({ id, data }: { id?: number; data: Omit<Ingrediente, 'id'> }) =>
      id === undefined ? api.post('/ingredientes', data) : api.put(`/ingredientes/${id}`, data),
    onSuccess: (_, { id }) => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification(id === undefined ? 'Ingrediente creado.' : 'Ingrediente actualizado.')
    },
    onError: notifyError,
  })
  const remove = useMutation({
    mutationFn: (id: number) => api.delete(`/ingredientes/${id}`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Ingrediente eliminado.')
    },
    onError: notifyError,
  })
  return { query, save, remove }
}
