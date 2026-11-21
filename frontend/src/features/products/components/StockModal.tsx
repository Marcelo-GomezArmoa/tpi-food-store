import { useForm } from '@tanstack/react-form'

import type { Producto } from '@/features/products/types/producto'
import { getApiErrorMessage } from '@/shared/api/error'

interface StockModalProps {
  producto: Producto
  pending: boolean
  error: unknown
  onClose: () => void
  onSubmit: (stock: number) => void
}

export function StockModal({
  producto,
  pending,
  error,
  onClose,
  onSubmit,
}: StockModalProps) {
  const form = useForm({
    defaultValues: { stock: String(producto.stock) },
    onSubmit: ({ value }) => onSubmit(Number(value.stock)),
  })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div role="dialog" aria-modal="true" className="w-full max-w-sm rounded-lg bg-white p-6 shadow-lg">
        <h2 className="text-xl font-bold">Actualizar stock</h2>
        <p className="mt-1 text-gray-600">{producto.nombre}</p>
        {Boolean(error) && (
          <p role="alert" className="mt-3 rounded bg-red-100 p-3 text-red-800">
            {getApiErrorMessage(error)}
          </p>
        )}
        <form
          className="mt-4"
          noValidate
          onSubmit={(event) => {
            event.preventDefault()
            void form.handleSubmit()
          }}
        >
          <form.Field
            name="stock"
            validators={{
              onChange: ({ value }) => {
                const parsed = Number(value)
                return Number.isInteger(parsed) && parsed >= 0
                  ? undefined
                  : 'El stock debe ser un entero mayor o igual a cero'
              },
            }}
          >
            {(field) => (
              <>
                <label className="block font-medium">
                  Stock
                  <input
                    type="number"
                    min="0"
                    step="1"
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    className="mt-1 w-full rounded border p-2"
                  />
                </label>
                {field.state.meta.errors.map((message, index) => (
                  <p key={index} role="alert" className="text-sm text-red-700">
                    {String(message)}
                  </p>
                ))}
              </>
            )}
          </form.Field>
          <p className="mt-3 text-sm text-gray-500">
            La disponibilidad se ajustará automáticamente según el stock.
          </p>
          <div className="mt-5 flex gap-3">
            <button type="button" onClick={onClose} disabled={pending} className="flex-1 rounded bg-gray-200 p-2">
              Cancelar
            </button>
            <button type="submit" disabled={pending} className="flex-1 rounded bg-blue-600 p-2 text-white">
              {pending ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
