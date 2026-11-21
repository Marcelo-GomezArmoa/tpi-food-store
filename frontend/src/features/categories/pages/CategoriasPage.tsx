import { useState } from "react";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/shared/components/DataTable";
import { NombreModal } from "@/shared/components/NombreModal";
import { EmptyState, ErrorState, LoadingState } from "@/shared/components/States";
import { getApiErrorMessage as getErrorMessage } from "@/shared/api/error";
import { useCategories } from "@/features/categories/hooks/useCategories";
import type { Categoria } from "@/features/categories/types/categoria";
import { useAuth } from "@/features/auth";

export function CategoriasPage() {
  const { user } = useAuth();
  const isAdmin = user?.roles.includes("admin") ?? false;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState<Categoria | null>(null);
  const { query, save, remove } = useCategories();
  const openModal = (categoria: Categoria | null) => {
    save.reset();
    setEditing(categoria);
    setIsModalOpen(true);
  };
  const columns: ColumnDef<Categoria>[] = [
    { accessorKey: "id", header: "ID" },
    { accessorKey: "nombre", header: "Nombre" },
    { accessorKey: "descripcion", header: "Descripción" },
    ...(isAdmin ? [{ id: "acciones", header: "Acciones", enableSorting: false, cell: ({ row }) => (
      <div className="flex gap-2">
        <button type="button" onClick={() => openModal(row.original)} className="rounded bg-blue-600 px-3 py-1 text-white">Editar</button>
        <button type="button" disabled={remove.isPending} onClick={() => {
          if (window.confirm("¿Estás seguro de que deseas eliminar esta categoría?")) remove.mutate(row.original.id);
        }} className="rounded bg-red-600 px-3 py-1 text-white disabled:opacity-50">Eliminar</button>
      </div>
    ) }] as ColumnDef<Categoria>[] : []),
  ];

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-4xl font-bold">📂 Categorías</h1>
        {isAdmin && <button type="button" onClick={() => openModal(null)} className="rounded-lg bg-blue-600 px-6 py-2 font-bold text-white">+ Nueva categoría</button>}
      </div>
      {query.isLoading && <LoadingState message="Cargando categorías..." />}
      {query.isError && <ErrorState message={getErrorMessage(query.error)} />}
      {remove.isError && <ErrorState message={`Error al eliminar: ${getErrorMessage(remove.error)}`} />}
      {query.data && (query.data.length ? <DataTable data={query.data} columns={columns} /> : <EmptyState message="No hay categorías. ¡Crea una nueva!" />)}
      {isAdmin && isModalOpen && (
        <NombreModal key={editing?.id ?? "new"} title={editing ? "Editar categoría" : "Nueva categoría"} initial={{ nombre: editing?.nombre ?? "", descripcion: editing?.descripcion ?? "" }} showDescription error={save.error ? getErrorMessage(save.error) : null} isPending={save.isPending} onClose={() => setIsModalOpen(false)} onSubmit={(data) => save.mutate({ id: editing?.id, data }, { onSuccess: () => { setIsModalOpen(false); setEditing(null); } })} />
      )}
    </div>
  );
}
