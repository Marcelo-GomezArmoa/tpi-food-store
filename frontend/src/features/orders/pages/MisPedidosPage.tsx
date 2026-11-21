import { BadgeEstado } from '@/features/orders/components/BadgeEstado'
import { useOrders } from '@/features/orders/hooks/useOrders'
import { getApiErrorMessage } from '@/shared/api/error'
import { EstadoError, EstadoVacio, LoadingState } from '@/shared/components/States'

export function MisPedidosPage() {
  const { orders, cancel } = useOrders()

  return (
    <section className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="text-4xl font-bold">Mis pedidos</h1>
      {orders.isLoading && <LoadingState message="Cargando pedidos..." />}
      {orders.isError && (
        <EstadoError message={getApiErrorMessage(orders.error)} />
      )}
      {cancel.isError && (
        <EstadoError
          message={getApiErrorMessage(cancel.error, 'No se pudo cancelar el pedido')}
        />
      )}
      {orders.data?.items.length === 0 && (
        <EstadoVacio message="Todavía no realizaste ningún pedido." />
      )}
      <div className="mt-6 space-y-5">
        {orders.data?.items.map((pedido) => (
          <article key={pedido.id} className="rounded-lg bg-white p-6 shadow">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold">Pedido #{pedido.id}</h2>
                <p className="text-sm text-gray-600">
                  {new Date(pedido.created_at).toLocaleString('es-AR')}
                </p>
              </div>
              <BadgeEstado estado={pedido.estado} />
            </div>
            <div className="mt-4 divide-y">
              {pedido.items.map((item) => (
                <div key={item.id} className="flex justify-between gap-4 py-2">
                  <div>
                    <p className="font-medium">{item.nombre_producto}</p>
                    <p className="text-sm text-gray-500">
                      {item.cantidad} x ${item.precio_unitario.toFixed(2)}
                    </p>
                  </div>
                  <strong>${item.subtotal.toFixed(2)}</strong>
                </div>
              ))}
            </div>
            <div className="mt-4 grid gap-2 border-t pt-4 text-sm sm:grid-cols-2">
              <p>
                <span className="font-semibold">Forma de pago:</span>{' '}
                {pedido.forma_pago}
              </p>
              <p>
                <span className="font-semibold">Dirección:</span>{' '}
                {pedido.direccion_entrega}
              </p>
              {pedido.notas && (
                <p className="sm:col-span-2">
                  <span className="font-semibold">Notas:</span> {pedido.notas}
                </p>
              )}
              <p className="text-xl font-bold sm:col-span-2">
                Total: ${pedido.total.toFixed(2)}
              </p>
            </div>
            {pedido.estado === 'PENDIENTE' && (
              <button
                type="button"
                disabled={cancel.isPending}
                onClick={() => cancel.mutate(pedido.id)}
                className="mt-4 rounded bg-red-600 px-4 py-2 font-semibold text-white disabled:opacity-50"
              >
                Cancelar pedido
              </button>
            )}
          </article>
        ))}
      </div>
    </section>
  )
}
