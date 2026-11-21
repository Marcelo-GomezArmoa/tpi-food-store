import { useForm } from '@tanstack/react-form'
import { Navigate, useNavigate } from 'react-router-dom'

import { useCartStore } from '@/features/cart/store/cartStore'
import { useOrders } from '@/features/orders/hooks/useOrders'
import { getApiErrorMessage } from '@/shared/api/error'

export function CheckoutPage() {
  const navigate = useNavigate()
  const items = useCartStore((state) => state.items)
  const vaciar = useCartStore((state) => state.vaciar)
  const total = useCartStore((state) => state.total)()
  const { create } = useOrders()
  const form = useForm({
    defaultValues: {
      direccion_entrega: '',
      forma_pago: 'EFECTIVO' as 'EFECTIVO' | 'TRANSFERENCIA',
      notas: '',
    },
    onSubmit: async ({ value }) => {
      await create.mutateAsync({
        direccion_entrega: value.direccion_entrega.trim(),
        forma_pago: value.forma_pago,
        notas: value.notas.trim() || undefined,
        items: items.map((item) => ({
          producto_id: item.producto_id,
          cantidad: item.cantidad,
        })),
      })
      vaciar()
      void navigate('/mis-pedidos', { replace: true })
    },
  })

  if (!items.length) return <Navigate to="/carrito" replace />

  return (
    <section className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-4xl font-bold">Finalizar compra</h1>
      <div className="mt-6 rounded-lg bg-white p-6 shadow">
        <div className="mb-6 border-b pb-4">
          <h2 className="font-semibold">Resumen</h2>
          {items.map((item) => (
            <div key={item.producto_id} className="mt-2 flex justify-between text-sm">
              <span>
                {item.cantidad} x {item.nombre}
              </span>
              <span>
                ${(item.precio_unitario * item.cantidad).toFixed(2)}
              </span>
            </div>
          ))}
          <p className="mt-4 text-right text-xl font-bold">
            Total: ${total.toFixed(2)}
          </p>
        </div>
        {create.isError && (
          <p role="alert" className="mb-4 rounded bg-red-100 p-3 text-red-800">
            {getApiErrorMessage(create.error, 'No se pudo confirmar el pedido')}
          </p>
        )}
        <form
          className="space-y-4"
          noValidate
          onSubmit={(event) => {
            event.preventDefault()
            void form.handleSubmit().catch(() => undefined)
          }}
        >
          <form.Field
            name="direccion_entrega"
            validators={{
              onChange: ({ value }) =>
                value.trim().length >= 5 && value.trim().length <= 200
                  ? undefined
                  : 'La dirección debe tener entre 5 y 200 caracteres',
            }}
          >
            {(field) => (
              <label className="block font-medium">
                Dirección de entrega
                <textarea
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(event) => field.handleChange(event.target.value)}
                  rows={3}
                  className="mt-1 w-full rounded border p-3"
                />
                {field.state.meta.errors.map((error, index) => (
                  <span key={index} className="text-sm text-red-700">
                    {String(error)}
                  </span>
                ))}
              </label>
            )}
          </form.Field>
          <form.Field name="forma_pago">
            {(field) => (
              <label className="block font-medium">
                Forma de pago
                <select
                  value={field.state.value}
                  onChange={(event) =>
                    field.handleChange(
                      event.target.value as 'EFECTIVO' | 'TRANSFERENCIA',
                    )
                  }
                  className="mt-1 w-full rounded border p-3"
                >
                  <option value="EFECTIVO">Efectivo</option>
                  <option value="TRANSFERENCIA">Transferencia</option>
                </select>
              </label>
            )}
          </form.Field>
          <form.Field name="notas">
            {(field) => (
              <label className="block font-medium">
                Notas opcionales
                <textarea
                  value={field.state.value}
                  onChange={(event) => field.handleChange(event.target.value)}
                  rows={3}
                  className="mt-1 w-full rounded border p-3"
                />
              </label>
            )}
          </form.Field>
          <button
            type="submit"
            disabled={create.isPending}
            className="w-full rounded bg-green-600 p-3 font-bold text-white disabled:opacity-50"
          >
            {create.isPending ? 'Confirmando pedido...' : 'Confirmar pedido'}
          </button>
        </form>
      </div>
    </section>
  )
}
