import axios from 'axios'

export function getApiErrorMessage(
  error: unknown,
  fallback = 'No se pudo completar la operación',
): string {
  if (axios.isAxiosError<unknown>(error)) {
    const body = error.response?.data
    const detail = typeof body === 'object' && body !== null && 'detail' in body
      ? body.detail
      : undefined
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
      const messages = detail.flatMap((item) => {
        if (
          typeof item === 'object' &&
          item !== null &&
          'msg' in item &&
          typeof item.msg === 'string'
        ) {
          return [item.msg]
        }
        return []
      })
      if (messages.length > 0) return messages.join('; ')
    }
    if (typeof body === 'object' && body !== null && 'message' in body && typeof body.message === 'string') {
      return body.message
    }
  }

  return error instanceof Error ? error.message : fallback
}
