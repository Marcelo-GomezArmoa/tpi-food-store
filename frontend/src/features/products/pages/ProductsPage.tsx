import { useState } from "react";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/shared/components/DataTable";
import { ProductoModal } from "@/features/products/components/ProductoModal";
import { StockModal } from "@/features/products/components/StockModal";
import { EmptyState, ErrorState, LoadingState } from "@/shared/components/States";
import { getApiErrorMessage as getErrorMessage } from "@/shared/api/error";
import { useProducts } from "@/features/products/hooks/useProducts";
import type { Producto } from "@/features/products/types/producto";
import { useAuth } from "@/features/auth";

export function ProductsPage() {
  const { usuario } = useAuth();
  const isAdmin = usuario?.role === "admin";
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState<Producto | null>(null);
  const [stockProduct, setStockProduct] = useState<Producto | null>(null);
  const { query, save, remove, updateStock } = useProducts({ skip: 0, limit: 100 });
  const openModal = (producto: Producto | null) => {
    save.reset();
    setEditing(producto);
    setIsModalOpen(true);
  };
  const columns: ColumnDef<Producto>[] = [
    { accessorKey: "id", header: "ID" },
    { id: "imagen", header: "Imagen", enableSorting: false, cell: ({ row }) => row.original.imagen_url ? (
      <img
        src={row.original.imagen_url}
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
    { accessorKey: "stock", header: "Stock" },
    { accessorKey: "disponible", header: "Disponible", cell: ({ row }) => row.original.disponible ? "Sí" : "No" },
    { id: "acciones", header: "Acciones", enableSorting: false, cell: ({ row }) => (
      <div className="flex flex-wrap gap-2">
        {isAdmin && <button type="button" onClick={() => openModal(row.original)} className="rounded bg-purple-600 px-3 py-1 text-white">Editar</button>}
        {isAdmin && <button type="button" onClick={() => { updateStock.reset(); setStockProduct(row.original); }} className="rounded bg-blue-600 px-3 py-1 text-white">Stock</button>}
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
      {query.data && (query.data.items.length ? <DataTable data={query.data.items} columns={columns} /> : <EmptyState message="No hay productos. ¡Crea uno nuevo!" />)}
      {isAdmin && isModalOpen && (
        <ProductoModal key={editing?.id ?? "new"} producto={editing} error={save.error ? getErrorMessage(save.error) : null} isPending={save.isPending} onClose={() => setIsModalOpen(false)} onSubmit={(data) => save.mutate({ id: editing?.id, data }, { onSuccess: () => { setIsModalOpen(false); setEditing(null); } })} />
      )}
      {isAdmin && stockProduct && (
        <StockModal
          producto={stockProduct}
          pending={updateStock.isPending}
          error={updateStock.error}
          onClose={() => setStockProduct(null)}
          onSubmit={(stock) =>
            updateStock.mutate(
              { id: stockProduct.id, stock },
              { onSuccess: () => setStockProduct(null) },
            )
          }
        />
      )}
    </div>
  );
}
