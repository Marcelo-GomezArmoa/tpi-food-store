import { useState } from "react";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/shared/components/DataTable";
import { NombreModal } from "@/shared/components/NombreModal";
import { EmptyState, ErrorState, LoadingState } from "@/shared/components/States";
import { getApiErrorMessage as getErrorMessage } from "@/shared/api/error";
import { useIngredients } from "@/features/ingredients/hooks/useIngredients";
import type { Ingrediente } from "@/features/ingredients/types/ingrediente";
import { useAuth } from "@/features/auth";

export function IngredientesPage() {
  const { user } = useAuth();
  const isAdmin = user?.roles.includes("admin") ?? false;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState<Ingrediente | null>(null);
  const { query, save, remove } = useIngredients();
  const openModal = (ingrediente: Ingrediente | null) => {
    save.reset();
    setEditing(ingrediente);
    setIsModalOpen(true);
  };
  const columns: ColumnDef<Ingrediente>[] = [
    { accessorKey: "id", header: "ID" },
    { accessorKey: "nombre", header: "Nombre" },
    ...(isAdmin ? [{ id: "acciones", header: "Acciones", enableSorting: false, cell: ({ row }) => (
      <div className="flex gap-2">
        <button type="button" onClick={() => openModal(row.original)} className="rounded bg-blue-600 px-3 py-1 text-white">Editar</button>
        <button type="button" disabled={remove.isPending} onClick={() => {
          if (window.confirm("¿Estás seguro de que deseas eliminar este ingrediente?")) remove.mutate(row.original.id);
        }} className="rounded bg-red-600 px-3 py-1 text-white disabled:opacity-50">Eliminar</button>
      </div>
    ) }] as ColumnDef<Ingrediente>[] : []),
  ];

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-4xl font-bold">Ingredientes</h1>
        {isAdmin && <button type="button" onClick={() => openModal(null)} className="rounded-lg bg-blue-600 px-6 py-2 font-bold text-white">+ Nuevo ingrediente</button>}
      </div>
      {query.isLoading && <LoadingState message="Cargando ingredientes..." />}
      {query.isError && <ErrorState message={getErrorMessage(query.error)} />}
      {remove.isError && <ErrorState message={`Error al eliminar: ${getErrorMessage(remove.error)}`} />}
      {query.data && (query.data.length ? <DataTable data={query.data} columns={columns} /> : <EmptyState message="No hay ingredientes. ¡Crea uno nuevo!" />)}
      {isAdmin && isModalOpen && (
        <NombreModal key={editing?.id ?? "new"} title={editing ? "Editar ingrediente" : "Nuevo ingrediente"} initial={{ nombre: editing?.nombre ?? "", descripcion: "" }} showDescription={false} error={save.error ? getErrorMessage(save.error) : null} isPending={save.isPending} onClose={() => setIsModalOpen(false)} onSubmit={({ nombre }) => save.mutate({ id: editing?.id, data: { nombre } }, { onSuccess: () => { setIsModalOpen(false); setEditing(null); } })} />
      )}
    </div>
  );
}
