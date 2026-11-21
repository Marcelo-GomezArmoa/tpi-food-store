import { useEffect } from 'react'
import { useNotificationStore } from '@/shared/store/notificationStore'

export function Toast() {
  const { message, visible, version, hideNotification } = useNotificationStore()

  useEffect(() => {
    if (!visible) return
    const timer = window.setTimeout(hideNotification, 3000)
    return () => window.clearTimeout(timer)
  }, [visible, version, hideNotification])

  if (!visible) return null
  return (
    <div role="status" aria-live="polite" className="fixed bottom-4 right-4 z-50 max-w-sm rounded bg-gray-900 p-4 text-white shadow-lg">
      {message}
      <button type="button" onClick={hideNotification} aria-label="Cerrar notificación" className="ml-4 font-bold">×</button>
    </div>
  )
}
