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
      (await api.get<ProductosPaginados>('/productos', {
        params,
      })).data,
  })
  const save = useMutation({
    mutationFn: ({ id, data }: { id?: number; data: ProductoData }) =>
      id === undefined
        ? api.post<Producto>('/productos', data)
        : api.put<Producto>(`/productos/${id}`, data),
    onSuccess: (_, { id }) => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification(
        id === undefined ? 'Producto creado.' : 'Producto actualizado.',
      )
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
  const updateStock = useMutation({
    mutationFn: ({ id, stock }: { id: number; stock: number }) =>
      api.patch<Producto>(`/productos/${id}/stock`, { stock }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey })
      useNotificationStore.getState().showNotification('Stock actualizado.')
    },
    onError: notifyError,
  })
  return { query, save, remove, updateStock }
}
