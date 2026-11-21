import { EmptyState, ErrorState, LoadingState } from "@/shared/components/States";
import { getApiErrorMessage as getErrorMessage } from "@/shared/api/error";
import { useProductCategories } from "@/features/products/hooks/useProductCategories";
import type { Producto } from "@/features/products/types/producto";
import { useAuth } from "@/features/auth";

interface ProductoCategoriasModalProps {
  producto: Producto;
  onClose: () => void;
}

export function ProductoCategoriasModal({ producto, onClose }: ProductoCategoriasModalProps) {
  const { user } = useAuth();
  const isAdmin = user?.roles.includes("admin") ?? false;
  const { categorias, asignadas, asignar, quitar } = useProductCategories(producto.id);
  const mutationError = asignar.error ?? quitar.error;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 p-4">
      <div role="dialog" aria-modal="true" aria-labelledby="categorias-producto-title" className="my-8 w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <h2 id="categorias-producto-title" className="text-2xl font-bold">Categorías de {producto.nombre}</h2>
        {(categorias.isLoading || asignadas.isLoading) && <LoadingState message="Cargando categorías..." />}
        {categorias.error && <ErrorState message={getErrorMessage(categorias.error)} />}
        {asignadas.error && <ErrorState message={getErrorMessage(asignadas.error)} />}
        {(asignar.isError || quitar.isError) && <ErrorState message={getErrorMessage(mutationError)} />}
        {categorias.data && asignadas.data && (
          <div className="mt-4 space-y-4">
            {categorias.data.length === 0 && <EmptyState message="No hay categorías disponibles." />}
            {categorias.data.map((categoria) => {
              const isAssigned = asignadas.data.some((item) => item.id === categoria.id);
              return (
                <div key={categoria.id} className="flex items-center justify-between gap-3 rounded border border-gray-200 p-3">
                  <span>{categoria.nombre}</span>
                  {isAdmin && <button type="button" disabled={asignar.isPending || quitar.isPending} onClick={() => {
                    asignar.reset();
                    quitar.reset();
                    if (isAssigned) quitar.mutate(categoria.id);
                    else asignar.mutate(categoria.id);
                  }} className="rounded bg-blue-600 px-3 py-1 text-white disabled:opacity-50">
                    {isAssigned ? "Quitar" : "Agregar"}
                  </button>}
                </div>
              );
            })}
          </div>
        )}
        <button type="button" onClick={onClose} disabled={asignar.isPending || quitar.isPending} className="mt-4 w-full rounded bg-gray-200 p-2 disabled:opacity-50">Cerrar</button>
      </div>
    </div>
  );
}
