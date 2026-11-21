import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import type {
  Producto,
  ProductosPaginados,
  ProductoData,
} from '@/features/products/types/producto'
import { api } from '@/shared/api/api'
import { notifyError } from '@/shared/api/notifyError'
import { useNotificationStore } from '@/shared/store/notificationStore'

interface CatalogParams {
  skip: number
  limit: number
  search?: string
  categoria_id?: number
  disponible?: boolean
}

const queryKey = ['productos']

export function useProducts(params?: CatalogParams) {
  const queryClient = useQueryClient()
  const query = useQuery({
    queryKey: params ? [...queryKey, params] : queryKey,
    queryFn: async () =>
      (await api.get<ProductosPaginados>('/api/v1/productos', {
        params,
      })).data,
  })
  const save = useMutation({
    mutationFn: ({ id, data }: { id?: number; data: ProductoData }) =>
      id === undefined
        ? api.post<Producto>('/api/v1/productos', data)
        : api.put<Producto>(`/api/v1/productos/${id}`, data),
    onSuccess: (_, { id }) => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification(
        id === undefined ? 'Producto creado.' : 'Producto actualizado.',
      )
    },
    onError: notifyError,
  })
  const remove = useMutation({
    mutationFn: (id: number) => api.delete(`/api/v1/productos/${id}`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Producto eliminado.')
    },
    onError: notifyError,
  })
  return { query, save, remove }
}
