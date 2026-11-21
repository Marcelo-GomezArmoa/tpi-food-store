import axios from 'axios'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

import type { UsuarioAuth } from '@/features/auth/types/auth.types'
import { api } from '@/shared/api/api'
import { getApiErrorMessage } from '@/shared/api/error'
import { queryClient } from '@/shared/api/queryClient'

interface AuthState {
  usuario: UsuarioAuth | null
  cargando: boolean
  error: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
  checkSession: () => Promise<void>
  clearSession: () => void
}

let sessionVersion = 0

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      usuario: null,
      cargando: true,
      error: null,
      login: async (username, password) => {
        const version = ++sessionVersion
        set({ cargando: true, error: null })
        try {
          await api.post('/auth/token', new URLSearchParams({
            username,
            password,
          }))
          const { data } = await api.get<UsuarioAuth>('/auth/me')
          if (version === sessionVersion) {
            queryClient.clear()
            set({ usuario: data, cargando: false, error: null })
          }
        } catch (error) {
          if (version === sessionVersion) {
            set({
              usuario: null,
              cargando: false,
              error: getApiErrorMessage(error),
            })
          }
          throw error
        }
      },
      logout: async () => {
        ++sessionVersion
        try {
          await api.post('/auth/logout')
        } finally {
          get().clearSession()
          window.location.assign('/login')
        }
      },
      checkSession: async () => {
        const version = ++sessionVersion
        set({ cargando: true, error: null })
        try {
          const { data } = await api.get<UsuarioAuth>('/auth/me')
          if (version === sessionVersion) {
            set({ usuario: data, cargando: false, error: null })
          }
        } catch (error) {
          if (version !== sessionVersion) return
          if (
            axios.isAxiosError(error) &&
            (error.response?.status === 401 || error.response?.status === 400)
          ) {
            queryClient.clear()
            set({ usuario: null, cargando: false, error: null })
          } else {
            set({ cargando: false, error: getApiErrorMessage(error) })
          }
        }
      },
      clearSession: () => {
        ++sessionVersion
        queryClient.clear()
        set({
          usuario: null,
          cargando: false,
          error: null,
        })
      },
    }),
    {
      name: 'food-store-auth',
      partialize: (state) => ({ usuario: state.usuario }),
    },
  ),
)
