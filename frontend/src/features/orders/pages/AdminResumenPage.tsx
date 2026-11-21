import { useOrderSummary } from '@/features/orders/hooks/useOrders'
import { getApiErrorMessage } from '@/shared/api/error'
import { ErrorState, LoadingState } from '@/shared/components/States'

export function AdminResumenPage() {
  const summary = useOrderSummary()

  if (summary.isLoading) {
    return <LoadingState message="Cargando resumen..." />
  }
  if (summary.isError) {
    return <ErrorState message={getApiErrorMessage(summary.error)} />
  }

  const cards = summary.data
    ? [
        ['Pendientes', summary.data.pendientes],
        ['En preparación', summary.data.en_preparacion],
        ['Entregados', summary.data.entregados],
        ['Cancelados', summary.data.cancelados],
        ['Pedidos de hoy', summary.data.pedidos_hoy],
        [
          'Ingresos entregados',
          `$${summary.data.ingresos_entregados.toFixed(2)}`,
        ],
      ]
    : []

  return (
    <section className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-4xl font-bold">Resumen de pedidos</h1>
      <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map(([label, value]) => (
          <article key={label} className="rounded-xl bg-white p-6 shadow">
            <p className="text-sm font-medium text-gray-500">{label}</p>
            <p className="mt-2 text-3xl font-bold text-blue-700">{value}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
