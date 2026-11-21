import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface CartItem {
  producto_id: number
  nombre: string
  precio_unitario: number
  cantidad: number
}

interface CartState {
  items: CartItem[]
  agregar: (item: Omit<CartItem, 'cantidad'> & { cantidad?: number }) => void
  quitar: (productoId: number) => void
  cambiarCantidad: (productoId: number, cantidad: number) => void
  vaciar: () => void
  total: () => number
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      agregar: (item) => {
        const cantidad = Math.max(1, item.cantidad ?? 1)
        set((state) => {
          const existing = state.items.find(
            (current) => current.producto_id === item.producto_id,
          )
          if (!existing) {
            return { items: [...state.items, { ...item, cantidad }] }
          }
          return {
            items: state.items.map((current) =>
              current.producto_id === item.producto_id
                ? { ...current, cantidad: current.cantidad + cantidad }
                : current,
            ),
          }
        })
      },
      quitar: (productoId) =>
        set((state) => ({
          items: state.items.filter(
            (item) => item.producto_id !== productoId,
          ),
        })),
      cambiarCantidad: (productoId, cantidad) => {
        if (cantidad <= 0) {
          get().quitar(productoId)
          return
        }
        set((state) => ({
          items: state.items.map((item) =>
            item.producto_id === productoId
              ? { ...item, cantidad }
              : item,
          ),
        }))
      },
      vaciar: () => set({ items: [] }),
      total: () =>
        get().items.reduce(
          (total, item) => total + item.precio_unitario * item.cantidad,
          0,
        ),
    }),
    { name: 'food-store-cart' },
  ),
)
