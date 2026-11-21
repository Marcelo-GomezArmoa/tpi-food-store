import { create } from 'zustand'

interface NotificationState {
  message: string
  visible: boolean
  version: number
  showNotification: (message: string) => void
  hideNotification: () => void
}

export const useNotificationStore = create<NotificationState>((set) => ({
  message: '',
  visible: false,
  version: 0,
  showNotification: (message) => set((state) => ({
    message,
    visible: true,
    version: state.version + 1,
  })),
  hideNotification: () => set({ visible: false }),
}))
