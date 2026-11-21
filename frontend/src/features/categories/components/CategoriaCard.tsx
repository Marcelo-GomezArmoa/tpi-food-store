import type { Categoria } from "@/features/categories/types/categoria";

interface CategoriaCardProps {
  categoria: Categoria;
  isDeleting: boolean;
  onEdit: (categoria: Categoria) => void;
  onDelete: (categoriaId: number) => void;
}

export function CategoriaCard({
  categoria,
  isDeleting,
  onEdit,
  onDelete,
}: CategoriaCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h2 className="text-xl font-bold text-gray-900">
            {categoria.nombre}
          </h2>
          <p className="text-gray-600 mt-2">{categoria.descripcion}</p>
        </div>
        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
          ID: {categoria.id}
        </span>
      </div>

      <div className="flex gap-2 pt-4 border-t border-gray-200">
        <button
          type="button"
          onClick={() => onEdit(categoria)}
          className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors duration-200"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onDelete(categoria.id)}
          disabled={isDeleting}
          className="flex-1 bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded transition-colors duration-200"
        >
          {isDeleting ? "Eliminando..." : "Eliminar"}
        </button>
      </div>
    </div>
  );
}
