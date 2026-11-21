import { Link } from 'react-router-dom'

import { useCartStore } from '@/features/cart/store/cartStore'
import { EstadoVacio } from '@/shared/components/States'

export function CarritoPage() {
  const items = useCartStore((state) => state.items)
  const cambiarCantidad = useCartStore((state) => state.cambiarCantidad)
  const quitar = useCartStore((state) => state.quitar)
  const vaciar = useCartStore((state) => state.vaciar)
  const total = useCartStore((state) => state.total)()

  if (!items.length) {
    return (
      <section className="mx-auto max-w-4xl px-4 py-12 text-center">
        <EstadoVacio message="Tu carrito está vacío." />
        <Link to="/" className="rounded bg-blue-600 px-5 py-2 font-semibold text-white">
          Ver catálogo
        </Link>
      </section>
    )
  }

  return (
    <section className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-4xl font-bold">Carrito</h1>
        <button type="button" onClick={vaciar} className="rounded border border-red-500 px-3 py-2 text-red-700">
          Vaciar carrito
        </button>
      </div>
      <div className="space-y-4">
        {items.map((item) => (
          <article key={item.producto_id} className="flex flex-wrap items-center justify-between gap-4 rounded-lg bg-white p-5 shadow">
            <div>
              <h2 className="font-bold">{item.nombre}</h2>
              <p className="text-gray-600">
                ${item.precio_unitario.toFixed(2)} c/u
              </p>
            </div>
            <label className="flex items-center gap-2 text-sm">
              Cantidad
              <input
                type="number"
                min="1"
                value={item.cantidad}
                onChange={(event) =>
                  cambiarCantidad(item.producto_id, Number(event.target.value))
                }
                className="w-20 rounded border p-2"
              />
            </label>
            <strong>
              ${(item.precio_unitario * item.cantidad).toFixed(2)}
            </strong>
            <button
              type="button"
              onClick={() => quitar(item.producto_id)}
              className="rounded bg-red-600 px-3 py-2 text-white"
            >
              Eliminar
            </button>
          </article>
        ))}
      </div>
      <div className="mt-8 flex items-center justify-between rounded-lg bg-white p-5 shadow">
        <p className="text-2xl font-bold">Total: ${total.toFixed(2)}</p>
        <Link
          to="/checkout"
          className="rounded bg-green-600 px-6 py-3 font-semibold text-white"
        >
          Continuar al checkout
        </Link>
      </div>
    </section>
  )
}
