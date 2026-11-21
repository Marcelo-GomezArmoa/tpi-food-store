import { CategoriaCard } from "./CategoriaCard";
import type { Categoria } from "@/features/categories/types/categoria";

interface CategoriaListProps {
  categorias: Categoria[];
  isLoading: boolean;
  isDeleting: boolean;
  onEdit: (categoria: Categoria) => void;
  onDelete: (categoriaId: number) => void;
}

export function CategoriaList({
  categorias,
  isLoading,
  isDeleting,
  onEdit,
  onDelete,
}: CategoriaListProps) {
  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Cargando categorías...</p>
      </div>
    );
  }

  if (categorias.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">
          No hay categorías. ¡Crea una nueva!
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          isDeleting={isDeleting}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
