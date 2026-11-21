import { useForm } from "@tanstack/react-form";
import { ErrorState } from "@/shared/components/States";
import type { Producto } from "@/features/products/types/producto";

type ProductoData = Omit<Producto, "id">;

interface ProductoModalProps {
  producto: Producto | null;
  error: string | null;
  isPending: boolean;
  onClose: () => void;
  onSubmit: (data: ProductoData) => void;
}

export function ProductoModal({ producto, error, isPending, onClose, onSubmit }: ProductoModalProps) {
  const form = useForm({
    defaultValues: {
      nombre: producto?.nombre ?? "",
      descripcion: producto?.descripcion ?? "",
      precio_base: producto ? String(producto.precio_base) : "",
      imagenes_url: producto?.imagenes_url.join(", ") ?? "",
      disponible: producto?.disponible ?? true,
    },
    onSubmit: ({ value }) => onSubmit({
      nombre: value.nombre.trim(),
      descripcion: value.descripcion.trim(),
      precio_base: Number(value.precio_base),
      imagenes_url: value.imagenes_url.split(",").map((url) => url.trim()).filter(Boolean),
      disponible: value.disponible,
    }),
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 p-4">
      <div role="dialog" aria-modal="true" aria-labelledby="producto-modal-title" className="my-8 w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <h2 id="producto-modal-title" className="text-2xl font-bold">{producto ? "Editar producto" : "Nuevo producto"}</h2>
        {error && <ErrorState message={error} />}
        <form noValidate onSubmit={(event) => { event.preventDefault(); void form.handleSubmit(); }} className="mt-4 space-y-4">
          <form.Field name="nombre" validators={{ onChange: ({ value }) => value.trim() ? undefined : "El nombre es obligatorio" }}>
            {(field) => (
              <div>
                <label htmlFor="producto-nombre" className="mb-1 block font-medium">Nombre</label>
                <input id="producto-nombre" name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="w-full rounded border border-gray-300 p-2" />
                {field.state.meta.errors.map((message, index) => <p role="alert" className="text-sm text-red-700" key={index}>{message}</p>)}
              </div>
            )}
          </form.Field>
          <form.Field name="descripcion">
            {(field) => (
              <div>
                <label htmlFor="producto-descripcion" className="mb-1 block font-medium">Descripción (opcional)</label>
                <textarea id="producto-descripcion" name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="w-full rounded border border-gray-300 p-2" rows={3} />
              </div>
            )}
          </form.Field>
          <form.Field name="precio_base" validators={{ onChange: ({ value }) => value.trim() && Number.isFinite(Number(value)) && Number(value) >= 0 ? undefined : "Ingresa un precio válido mayor o igual a cero" }}>
            {(field) => (
              <div>
                <label htmlFor="producto-precio" className="mb-1 block font-medium">Precio base</label>
                <input id="producto-precio" name={field.name} type="number" step="any" min="0" value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="w-full rounded border border-gray-300 p-2" />
                {field.state.meta.errors.map((message, index) => <p role="alert" className="text-sm text-red-700" key={index}>{message}</p>)}
              </div>
            )}
          </form.Field>
          <form.Field name="imagenes_url">
            {(field) => (
              <div>
                <label htmlFor="producto-imagenes" className="mb-1 block font-medium">URLs de imágenes (separadas por comas)</label>
                <input id="producto-imagenes" name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="w-full rounded border border-gray-300 p-2" />
              </div>
            )}
          </form.Field>
          <form.Field name="disponible">
            {(field) => (
              <div className="flex items-center gap-2">
                <input id="producto-disponible" name={field.name} type="checkbox" checked={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.checked)} />
                <label htmlFor="producto-disponible">Disponible</label>
              </div>
            )}
          </form.Field>
          <div className="flex gap-3">
            <button type="button" disabled={isPending} onClick={onClose} className="flex-1 rounded bg-gray-200 p-2 disabled:opacity-50">Cancelar</button>
            <button type="submit" disabled={isPending} className="flex-1 rounded bg-purple-600 p-2 text-white disabled:opacity-50">{isPending ? "Guardando..." : "Guardar"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
