import { useState } from 'react'

import { useCategories } from '@/features/categories/hooks/useCategories'
import { useProducts } from '@/features/products/hooks/useProducts'
import { useCartStore } from '@/features/cart/store/cartStore'
import { Skeleton } from '@/shared/components/Skeleton'
import { EstadoError, EstadoVacio } from '@/shared/components/States'
import { getApiErrorMessage } from '@/shared/api/error'

const PAGE_SIZE = 12

export function CatalogoPage() {
  const [page, setPage] = useState(0)
  const [search, setSearch] = useState('')
  const [categoriaId, setCategoriaId] = useState<number | undefined>()
  const categories = useCategories()
  const products = useProducts({
    skip: page * PAGE_SIZE,
    limit: PAGE_SIZE,
    search: search || undefined,
    categoria_id: categoriaId,
    disponible: true,
  })
  const agregar = useCartStore((state) => state.agregar)
  const pageCount = products.query.data
    ? Math.max(1, Math.ceil(products.query.data.total / PAGE_SIZE))
    : 1

  const updateSearch = (value: string) => {
    setSearch(value)
    setPage(0)
  }

  return (
    <section className="mx-auto max-w-7xl px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900">Nuestro catálogo</h1>
        <p className="mt-2 text-gray-600">
          Elegí tus productos y prepará tu pedido.
        </p>
      </div>

      <div className="mb-8 grid gap-3 md:grid-cols-[1fr_240px]">
        <label>
          <span className="sr-only">Buscar productos</span>
          <input
            type="search"
            value={search}
            onChange={(event) => updateSearch(event.target.value)}
            placeholder="Buscar productos..."
            className="w-full rounded border border-gray-300 bg-white p-3"
          />
        </label>
        <label>
          <span className="sr-only">Filtrar por categoría</span>
          <select
            value={categoriaId ?? ''}
            onChange={(event) => {
              setCategoriaId(
                event.target.value ? Number(event.target.value) : undefined,
              )
              setPage(0)
            }}
            className="w-full rounded border border-gray-300 bg-white p-3"
          >
            <option value="">Todas las categorías</option>
            {categories.query.data?.map((categoria) => (
              <option key={categoria.id} value={categoria.id}>
                {categoria.nombre}
              </option>
            ))}
          </select>
        </label>
      </div>

      {products.query.isLoading && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }, (_, index) => (
            <Skeleton key={index} />
          ))}
        </div>
      )}
      {products.query.isError && (
        <EstadoError message={getApiErrorMessage(products.query.error)} />
      )}
      {products.query.data && products.query.data.items.length === 0 && (
        <EstadoVacio message="No se encontraron productos con esos filtros." />
      )}
      {products.query.data && products.query.data.items.length > 0 && (
        <>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {products.query.data.items.map((producto) => (
              <article key={producto.id} className="overflow-hidden rounded-xl bg-white shadow">
                <div className="h-48 bg-gray-100">
                  {producto.imagen_url ? (
                    <img
                      src={producto.imagen_url}
                      alt={producto.nombre}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full items-center justify-center text-5xl">
                      🍽️
                    </div>
                  )}
                </div>
                <div className="p-5">
                  <p className="text-sm font-medium text-blue-700">
                    {producto.categoria.nombre}
                  </p>
                  <h2 className="mt-1 text-xl font-bold">{producto.nombre}</h2>
                  <p className="mt-2 min-h-12 text-sm text-gray-600">
                    {producto.descripcion}
                  </p>
                  <div className="mt-4 flex items-center justify-between gap-3">
                    <span className="text-xl font-bold text-green-700">
                      ${producto.precio_base.toFixed(2)}
                    </span>
                    <button
                      type="button"
                      disabled={!producto.disponible || producto.stock === 0}
                      onClick={() =>
                        agregar({
                          producto_id: producto.id,
                          nombre: producto.nombre,
                          precio_unitario: producto.precio_base,
                        })
                      }
                      className="rounded bg-blue-600 px-4 py-2 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      Agregar al carrito
                    </button>
                  </div>
                  <p className="mt-2 text-xs text-gray-500">
                    Stock disponible: {producto.stock}
                  </p>
                </div>
              </article>
            ))}
          </div>
          <div className="mt-8 flex items-center justify-center gap-4">
            <button
              type="button"
              disabled={page === 0}
              onClick={() => setPage((current) => current - 1)}
              className="rounded border bg-white px-4 py-2 disabled:opacity-40"
            >
              Anterior
            </button>
            <span>
              Página {page + 1} de {pageCount}
            </span>
            <button
              type="button"
              disabled={page + 1 >= pageCount}
              onClick={() => setPage((current) => current + 1)}
              className="rounded border bg-white px-4 py-2 disabled:opacity-40"
            >
              Siguiente
            </button>
          </div>
        </>
      )}
    </section>
  )
}
