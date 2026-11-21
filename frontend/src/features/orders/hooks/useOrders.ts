import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import type {
  Pedido,
  PedidoCreate,
  PedidosPaginados,
  ResumenPedidos,
} from '@/features/orders/types/pedido'
import { api } from '@/shared/api/api'

const ordersKey = ['pedidos']

export function useOrders(estado?: Pedido['estado']) {
  const queryClient = useQueryClient()
  const orders = useQuery({
    queryKey: [...ordersKey, estado ?? 'todos'],
    queryFn: async () =>
      (await api.get<PedidosPaginados>('/pedidos', {
        params: { skip: 0, limit: 100, estado },
      })).data,
  })
  const create = useMutation({
    mutationFn: async (data: PedidoCreate) =>
      (await api.post<Pedido>('/pedidos', data)).data,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ordersKey })
      void queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
  const cancel = useMutation({
    mutationFn: async (pedidoId: number) =>
      (
        await api.patch<Pedido>(
          `/pedidos/${pedidoId}/cancelar`,
        )
      ).data,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ordersKey })
      void queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
  const changeStatus = useMutation({
    mutationFn: async ({
      pedidoId,
      estado,
    }: {
      pedidoId: number
      estado: Pedido['estado']
    }) =>
      (
        await api.patch<Pedido>(`/pedidos/${pedidoId}/estado`, { estado })
      ).data,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ordersKey })
      void queryClient.invalidateQueries({ queryKey: ['pedido-resumen'] })
      void queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
  return { orders, create, cancel, changeStatus }
}

export function useOrderSummary() {
  return useQuery({
    queryKey: ['pedido-resumen'],
    queryFn: async () =>
      (await api.get<ResumenPedidos>('/pedidos/resumen')).data,
  })
}
