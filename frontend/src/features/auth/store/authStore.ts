import axios from 'axios'
import { create } from 'zustand'
import { api } from '@/shared/api/api'
import { getApiErrorMessage } from '@/shared/api/error'
import { notifyError } from '@/shared/api/notifyError'
import { queryClient } from '@/shared/api/queryClient'
import type { UsuarioAuth } from '@/features/auth/types/auth.types'

interface AuthState {
  user: UsuarioAuth | null
  checking: boolean
  isLoading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  clearSession: () => void
}

let sessionVersion = 0

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  checking: true,
  isLoading: false,
  error: null,
  login: async (email, password) => {
    const version = ++sessionVersion
    set({ isLoading: true, error: null })
    try {
      await api.post('/api/v1/auth/token', new URLSearchParams({
        username: email,
        password,
      }))
      const { data } = await api.get<UsuarioAuth>('/api/v1/auth/me')
      if (version === sessionVersion) {
        queryClient.clear()
        set({ user: data, checking: false })
      }
    } catch (error) {
      if (version === sessionVersion) {
        set({ error: getApiErrorMessage(error), checking: false })
        notifyError(error)
      }
      throw error
    } finally {
      if (version === sessionVersion) set({ isLoading: false })
    }
  },
  logout: async () => {
    ++sessionVersion
    set({ isLoading: true, error: null })
    try {
      await api.post('/api/v1/auth/logout')
    } finally {
      get().clearSession()
    }
  },
  checkAuth: async () => {
    const version = ++sessionVersion
    set({ checking: true, error: null })
    try {
      const { data } = await api.get<UsuarioAuth>('/api/v1/auth/me')
      if (version === sessionVersion) set({ user: data })
    } catch (error) {
      if (version === sessionVersion) {
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          queryClient.clear()
          set({ user: null, error: null })
        } else {
          set({ error: getApiErrorMessage(error) })
          notifyError(error)
        }
      }
    } finally {
      if (version === sessionVersion) set({ checking: false })
    }
  },
  clearSession: () => {
    ++sessionVersion
    queryClient.clear()
    set({ user: null, checking: false, isLoading: false, error: null })
  },
}))
