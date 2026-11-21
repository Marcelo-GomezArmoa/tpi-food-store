import { QueryClient } from '@tanstack/react-query'
import axios from 'axios'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      gcTime: 1000 * 60 * 10,
      retry: (count, error) =>
        !(axios.isAxiosError(error) && (error.response?.status === 401 || error.response?.status === 403)) && count < 3,
    },
  },
})
