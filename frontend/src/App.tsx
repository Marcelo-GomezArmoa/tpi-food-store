import { useEffect } from 'react'
import { useAuthStore } from '@/features/auth'
import { AppRouter } from '@/routes/AppRouter'
import { Toast } from '@/shared/components/Toast'

function App() {
  const checkSession = useAuthStore((state) => state.checkSession)

  useEffect(() => {
    void checkSession()
  }, [checkSession])

  return <><AppRouter /><Toast /></>
}

export default App
