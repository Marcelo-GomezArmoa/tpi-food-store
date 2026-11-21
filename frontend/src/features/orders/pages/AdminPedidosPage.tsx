import { useState } from 'react'
import type { ColumnDef } from '@tanstack/react-table'

import { BadgeEstado } from '@/features/orders/components/BadgeEstado'
import { useOrders } from '@/features/orders/hooks/useOrders'
import type {
  EstadoPedido,
  Pedido,
} from '@/features/orders/types/pedido'
import { getApiErrorMessage } from '@/shared/api/error'
import { DataTable } from '@/shared/components/DataTable'
import { ErrorState, LoadingState } from '@/shared/components/States'

const nextStates: Partial<Record<EstadoPedido, EstadoPedido>> = {
  PENDIENTE: 'EN_PREPARACION',
  EN_PREPARACION: 'ENTREGADO',
}

export function AdminPedidosPage() {
  const [estado, setEstado] = useState<EstadoPedido | undefined>()
  const { orders, changeStatus } = useOrders(estado)

  const columns: ColumnDef<Pedido>[] = [
    { accessorKey: 'id', header: 'Pedido' },
    {
      id: 'cliente',
      header: 'Usuario ID',
      cell: ({ row }) => row.original.usuario_id,
    },
    {
      id: 'fecha',
      header: 'Fecha',
      cell: ({ row }) =>
        new Date(row.original.created_at).toLocaleString('es-AR'),
    },
    {
      accessorKey: 'estado',
      header: 'Estado',
      cell: ({ row }) => <BadgeEstado estado={row.original.estado} />,
    },
    {
      accessorKey: 'total',
      header: 'Total',
      cell: ({ row }) => `$${row.original.total.toFixed(2)}`,
    },
    {
      id: 'acciones',
      header: 'Acciones',
      enableSorting: false,
      cell: ({ row }) => {
        const next = nextStates[row.original.estado]
        const canCancel = ['PENDIENTE', 'EN_PREPARACION'].includes(
          row.original.estado,
        )
        return (
          <div className="flex flex-wrap gap-2">
            {next && (
              <button
                type="button"
                disabled={changeStatus.isPending}
                onClick={() =>
                  changeStatus.mutate({
                    pedidoId: row.original.id,
                    estado: next,
                  })
                }
                className="rounded bg-blue-600 px-3 py-1 text-white"
              >
                {next === 'ENTREGADO' ? 'Entregar' : 'Preparar'}
              </button>
            )}
            {canCancel && (
              <button
                type="button"
                disabled={changeStatus.isPending}
                onClick={() =>
                  changeStatus.mutate({
                    pedidoId: row.original.id,
                    estado: 'CANCELADO',
                  })
                }
                className="rounded bg-red-600 px-3 py-1 text-white"
              >
                Cancelar
              </button>
            )}
          </div>
        )
      },
    },
  ]

  return (
    <section className="mx-auto max-w-7xl px-4 py-8">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-4xl font-bold">Administración de pedidos</h1>
        <label className="flex items-center gap-2">
          Estado
          <select
            value={estado ?? ''}
            onChange={(event) =>
              setEstado(
                (event.target.value || undefined) as EstadoPedido | undefined,
              )
            }
            className="rounded border bg-white p-2"
          >
            <option value="">Todos</option>
            <option value="PENDIENTE">Pendiente</option>
            <option value="EN_PREPARACION">En preparación</option>
            <option value="ENTREGADO">Entregado</option>
            <option value="CANCELADO">Cancelado</option>
          </select>
        </label>
      </div>
      {orders.isLoading && <LoadingState message="Cargando pedidos..." />}
      {orders.isError && <ErrorState message={getApiErrorMessage(orders.error)} />}
      {changeStatus.isError && (
        <ErrorState
          message={getApiErrorMessage(
            changeStatus.error,
            'No se pudo cambiar el estado',
          )}
        />
      )}
      {orders.data && <DataTable data={orders.data.items} columns={columns} />}
    </section>
  )
}
