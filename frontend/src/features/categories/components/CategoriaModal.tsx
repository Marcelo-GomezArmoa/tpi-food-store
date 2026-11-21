import { useState, type FormEvent } from "react";
import type { Categoria } from "@/features/categories/types/categoria";

export interface CategoriaFormData {
  nombre: string;
  descripcion: string;
}

interface CategoriaModalProps {
  categoria: Categoria | null;
  error: string | null;
  isPending: boolean;
  onClose: () => void;
  onSubmit: (data: CategoriaFormData) => void;
}

export function CategoriaModal({
  categoria,
  error,
  isPending,
  onClose,
  onSubmit,
}: CategoriaModalProps) {
  const [formData, setFormData] = useState<CategoriaFormData>({
    nombre: categoria?.nombre ?? "",
    descripcion: categoria?.descripcion ?? "",
  });
  const isEditing = categoria !== null;

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          {isEditing ? "Editar Categoría" : "Nueva Categoría"}
        </h2>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre
            </label>
            <input
              type="text"
              value={formData.nombre}
              onChange={(event) =>
                setFormData({ ...formData, nombre: event.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ej: Bebidas"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Descripción
            </label>
            <textarea
              value={formData.descripcion}
              onChange={(event) =>
                setFormData({ ...formData, descripcion: event.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder="Ej: Bebidas varias"
              rows={4}
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={isPending}
              className="flex-1 bg-gray-300 hover:bg-gray-400 disabled:bg-gray-200 text-gray-900 font-bold py-2 px-4 rounded transition-colors duration-200"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isPending}
              className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded transition-colors duration-200"
            >
              {isPending
                ? isEditing
                  ? "Guardando..."
                  : "Creando..."
                : isEditing
                  ? "Guardar"
                  : "Crear"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
