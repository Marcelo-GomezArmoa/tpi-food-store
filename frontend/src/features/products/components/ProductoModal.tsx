import { useForm } from '@tanstack/react-form'

import type { Producto, ProductoData } from '@/features/products/types/producto'
import { ErrorState } from '@/shared/components/States'

interface ProductoModalProps {
  producto: Producto | null
  error: string | null
  isPending: boolean
  onClose: () => void
  onSubmit: (data: ProductoData) => void
}

export function ProductoModal({
  producto,
  error,
  isPending,
  onClose,
  onSubmit,
}: ProductoModalProps) {
  const form = useForm({
    defaultValues: {
      categoria_id: String(producto?.categoria_id ?? 1),
      nombre: producto?.nombre ?? '',
      descripcion: producto?.descripcion ?? '',
      precio_base: producto ? String(producto.precio_base) : '',
      imagen_url: producto?.imagen_url ?? '',
      stock: String(producto?.stock ?? 0),
      disponible: producto?.disponible ?? true,
    },
    onSubmit: ({ value }) =>
      onSubmit({
        categoria_id: Number(value.categoria_id),
        nombre: value.nombre.trim(),
        descripcion: value.descripcion.trim(),
        precio_base: Number(value.precio_base),
        imagen_url: value.imagen_url.trim(),
        stock: Number(value.stock),
        disponible: value.disponible,
      }),
  })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 p-4">
      <div role="dialog" aria-modal="true" aria-labelledby="producto-modal-title" className="my-8 w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <h2 id="producto-modal-title" className="text-2xl font-bold">
          {producto ? 'Editar producto' : 'Nuevo producto'}
        </h2>
        {error && <ErrorState message={error} />}
        <form
          noValidate
          onSubmit={(event) => {
            event.preventDefault()
            void form.handleSubmit()
          }}
          className="mt-4 space-y-4"
        >
          <form.Field name="categoria_id">
            {(field) => (
              <label className="block">
                Categoría ID
                <input className="mt-1 w-full rounded border p-2" type="number" min="1" value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} />
              </label>
            )}
          </form.Field>
          <form.Field name="nombre" validators={{ onChange: ({ value }) => value.trim() ? undefined : 'El nombre es obligatorio' }}>
            {(field) => (
              <label className="block">
                Nombre
                <input className="mt-1 w-full rounded border p-2" value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} />
              </label>
            )}
          </form.Field>
          <form.Field name="descripcion">
            {(field) => (
              <label className="block">
                Descripción
                <textarea className="mt-1 w-full rounded border p-2" rows={3} value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} />
              </label>
            )}
          </form.Field>
          <form.Field name="precio_base">
            {(field) => (
              <label className="block">
                Precio base
                <input className="mt-1 w-full rounded border p-2" type="number" min="0" step="any" value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} />
              </label>
            )}
          </form.Field>
          <form.Field name="imagen_url">
            {(field) => (
              <label className="block">
                URL de imagen
                <input className="mt-1 w-full rounded border p-2" value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} />
              </label>
            )}
          </form.Field>
          <form.Field name="stock">
            {(field) => (
              <label className="block">
                Stock
                <input className="mt-1 w-full rounded border p-2" type="number" min="0" value={field.state.value} onChange={(event) => field.handleChange(event.target.value)} />
              </label>
            )}
          </form.Field>
          <form.Field name="disponible">
            {(field) => (
              <label className="flex items-center gap-2">
                <input type="checkbox" checked={field.state.value} onChange={(event) => field.handleChange(event.target.checked)} />
                Disponible
              </label>
            )}
          </form.Field>
          <div className="flex gap-3">
            <button type="button" disabled={isPending} onClick={onClose} className="flex-1 rounded bg-gray-200 p-2">Cancelar</button>
            <button type="submit" disabled={isPending} className="flex-1 rounded bg-purple-600 p-2 text-white">{isPending ? 'Guardando...' : 'Guardar'}</button>
          </div>
        </form>
      </div>
    </div>
  )
}
