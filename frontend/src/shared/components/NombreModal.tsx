import { useForm } from "@tanstack/react-form";
import { ErrorState } from "@/shared/components/States";

export interface NombreFormData {
  nombre: string;
  descripcion: string;
}

interface NombreModalProps {
  title: string;
  initial: NombreFormData;
  showDescription: boolean;
  error: string | null;
  isPending: boolean;
  onClose: () => void;
  onSubmit: (data: NombreFormData) => void;
}

export function NombreModal({ title, initial, showDescription, error, isPending, onClose, onSubmit }: NombreModalProps) {
  const form = useForm({
    defaultValues: initial,
    onSubmit: ({ value }) => onSubmit({
      nombre: value.nombre.trim(),
      descripcion: value.descripcion.trim(),
    }),
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div role="dialog" aria-modal="true" aria-labelledby="nombre-modal-title" className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <h2 id="nombre-modal-title" className="text-2xl font-bold">{title}</h2>
        {error && <ErrorState message={error} />}
        <form noValidate onSubmit={(event) => { event.preventDefault(); void form.handleSubmit(); }} className="mt-4 space-y-4">
          <form.Field name="nombre" validators={{ onChange: ({ value }) => value.trim() ? undefined : "El nombre es obligatorio" }}>
            {(field) => (
              <div>
                <label htmlFor="nombre" className="mb-1 block font-medium">Nombre</label>
                <input id="nombre" name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="w-full rounded border border-gray-300 p-2" />
                {field.state.meta.errors.map((message, index) => <p role="alert" className="text-sm text-red-700" key={index}>{message}</p>)}
              </div>
            )}
          </form.Field>
          {showDescription && (
            <form.Field name="descripcion">
              {(field) => (
                <div>
                  <label htmlFor="descripcion" className="mb-1 block font-medium">Descripción (opcional)</label>
                  <textarea id="descripcion" name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="w-full rounded border border-gray-300 p-2" rows={3} />
                </div>
              )}
            </form.Field>
          )}
          <div className="flex gap-3">
            <button type="button" disabled={isPending} onClick={onClose} className="flex-1 rounded bg-gray-200 p-2 disabled:opacity-50">Cancelar</button>
            <button type="submit" disabled={isPending} className="flex-1 rounded bg-blue-600 p-2 text-white disabled:opacity-50">{isPending ? "Guardando..." : "Guardar"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
