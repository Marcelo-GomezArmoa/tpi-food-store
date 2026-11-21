export type EstadoPedido =
  | 'PENDIENTE'
  | 'EN_PREPARACION'
  | 'ENTREGADO'
  | 'CANCELADO'

export interface DetallePedido {
  id: number
  pedido_id: number
  producto_id: number
  cantidad: number
  nombre_producto: string
  precio_unitario: number
  subtotal: number
}

export interface Pedido {
  id: number
  usuario_id: number
  estado: EstadoPedido
  forma_pago: string
  direccion_entrega: string
  notas: string | null
  total: number
  created_at: string
  updated_at: string
  items: DetallePedido[]
}

export interface PedidosPaginados {
  total: number
  items: Pedido[]
}

export interface ResumenPedidos {
  pendientes: number
  en_preparacion: number
  entregados: number
  cancelados: number
  pedidos_hoy: number
  ingresos_entregados: number
}

export interface PedidoCreate {
  forma_pago: 'EFECTIVO' | 'TRANSFERENCIA'
  direccion_entrega: string
  notas?: string
  items: Array<{
    producto_id: number
    cantidad: number
  }>
}
