import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import type {
  Pedido,
  PedidoCreate,
  PedidosPaginados,
} from '@/features/orders/types/pedido'
import { api } from '@/shared/api/api'

const ordersKey = ['pedidos']

export function useOrders() {
  const queryClient = useQueryClient()
  const orders = useQuery({
    queryKey: ordersKey,
    queryFn: async () =>
      (await api.get<PedidosPaginados>('/api/v1/pedidos')).data,
  })
  const create = useMutation({
    mutationFn: async (data: PedidoCreate) =>
      (await api.post<Pedido>('/api/v1/pedidos', data)).data,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ordersKey })
      void queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
  const cancel = useMutation({
    mutationFn: async (pedidoId: number) =>
      (
        await api.patch<Pedido>(
          `/api/v1/pedidos/${pedidoId}/cancelar`,
        )
      ).data,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ordersKey })
      void queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
  return { orders, create, cancel }
}
