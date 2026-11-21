import { useState } from "react";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/shared/components/DataTable";
import { ProductoCategoriasModal } from "@/features/products/components/ProductoCategoriasModal";
import { ProductoModal } from "@/features/products/components/ProductoModal";
import { EmptyState, ErrorState, LoadingState } from "@/shared/components/States";
import { getApiErrorMessage as getErrorMessage } from "@/shared/api/error";
import { useProducts } from "@/features/products/hooks/useProducts";
import type { Producto } from "@/features/products/types/producto";
import { useAuth } from "@/features/auth";

export function ProductsPage() {
  const { user } = useAuth();
  const isAdmin = user?.roles.includes("admin") ?? false;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState<Producto | null>(null);
  const [categoriasProducto, setCategoriasProducto] = useState<Producto | null>(null);
  const { query, save, remove } = useProducts();
  const openModal = (producto: Producto | null) => {
    save.reset();
    setEditing(producto);
    setIsModalOpen(true);
  };
  const columns: ColumnDef<Producto>[] = [
    { accessorKey: "id", header: "ID" },
    { id: "imagen", header: "Imagen", enableSorting: false, cell: ({ row }) => row.original.imagenes_url[0] ? (
      <img
        src={row.original.imagenes_url[0]}
        alt={row.original.nombre}
        className="h-14 w-14 rounded object-cover"
        onError={(event) => {
          event.currentTarget.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect fill='%23ddd' width='100' height='100'/%3E%3Ctext x='50' y='50' text-anchor='middle' dy='.3em' fill='%23999' font-size='14'%3ENo imagen%3C/text%3E%3C/svg%3E";
        }}
      />
    ) : "Sin imagen" },
    { accessorKey: "nombre", header: "Nombre" },
    { accessorKey: "descripcion", header: "Descripción" },
    { accessorKey: "precio_base", header: "Precio", cell: ({ row }) => `$${row.original.precio_base.toFixed(2)}` },
    { accessorKey: "disponible", header: "Disponible", cell: ({ row }) => row.original.disponible ? "Sí" : "No" },
    { id: "acciones", header: "Acciones", enableSorting: false, cell: ({ row }) => (
      <div className="flex flex-wrap gap-2">
        {isAdmin && <button type="button" onClick={() => openModal(row.original)} className="rounded bg-purple-600 px-3 py-1 text-white">Editar</button>}
        <button type="button" onClick={() => setCategoriasProducto(row.original)} className="rounded bg-blue-600 px-3 py-1 text-white">Categorías</button>
        {isAdmin && <button type="button" disabled={remove.isPending} onClick={() => {
          if (window.confirm("¿Estás seguro de que deseas eliminar este producto?")) remove.mutate(row.original.id);
        }} className="rounded bg-red-600 px-3 py-1 text-white disabled:opacity-50">Eliminar</button>}
      </div>
    ) },
  ];

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-4xl font-bold">🍽️ Productos</h1>
        {isAdmin && <button type="button" onClick={() => openModal(null)} className="rounded-lg bg-purple-600 px-6 py-2 font-bold text-white">+ Nuevo producto</button>}
      </div>
      {query.isLoading && <LoadingState message="Cargando productos..." />}
      {query.isError && <ErrorState message={getErrorMessage(query.error)} />}
      {remove.isError && <ErrorState message={`Error al eliminar: ${getErrorMessage(remove.error)}`} />}
      {query.data && (query.data.length ? <DataTable data={query.data} columns={columns} /> : <EmptyState message="No hay productos. ¡Crea uno nuevo!" />)}
      {isAdmin && isModalOpen && (
        <ProductoModal key={editing?.id ?? "new"} producto={editing} error={save.error ? getErrorMessage(save.error) : null} isPending={save.isPending} onClose={() => setIsModalOpen(false)} onSubmit={(data) => save.mutate({ id: editing?.id, data }, { onSuccess: () => { setIsModalOpen(false); setEditing(null); } })} />
      )}
      {categoriasProducto && <ProductoCategoriasModal producto={categoriasProducto} onClose={() => setCategoriasProducto(null)} />}
    </div>
  );
}
