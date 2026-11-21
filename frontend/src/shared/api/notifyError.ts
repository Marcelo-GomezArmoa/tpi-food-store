import axios from 'axios'
import { getApiErrorMessage } from '@/shared/api/error'
import { useNotificationStore } from '@/shared/store/notificationStore'

export function notifyError(error: unknown) {
  if (axios.isAxiosError(error) && error.response?.status === 403) return
  useNotificationStore.getState().showNotification(getApiErrorMessage(error))
}
