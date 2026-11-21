import { useForm } from '@tanstack/react-form'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { useAuth } from '@/features/auth/hooks/useAuth'

export function LoginPage() {
  const navigate = useNavigate()
  const { usuario, cargando, error, login } = useAuth()

  const form = useForm({
    defaultValues: { username: '', password: '' },
    onSubmit: async ({ value }) => {
      await login(value.username.trim(), value.password)
      void navigate('/', { replace: true })
    },
  })

  if (usuario) return <Navigate to="/" replace />

  return (
    <div className="mx-auto mt-12 max-w-md rounded-lg bg-white p-6 shadow">
      <h1 className="text-3xl font-bold">Iniciar sesión</h1>
      <p className="mt-2 text-gray-600">Accede con tu email y contraseña.</p>
      {error && (
        <div role="alert" className="mt-4 rounded bg-red-100 p-3 text-red-800">
          {error}
        </div>
      )}
      <form
        className="mt-6 space-y-4"
        noValidate
        onSubmit={(event) => {
          event.preventDefault()
          void form.handleSubmit().catch(() => undefined)
        }}
      >
        <form.Field
          name="username"
          validators={{
            onChange: ({ value }) =>
              value.trim().length >= 3
                ? undefined
                : 'El usuario debe tener al menos 3 caracteres',
          }}
        >
          {(field) => (
            <div>
              <label htmlFor="login-email" className="block font-medium">
                Usuario
              </label>
              <input
                id="login-email"
                type="text"
                autoComplete="username"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded border p-2"
              />
              {field.state.meta.errors.map((message, index) => (
                <p key={index} role="alert" className="text-sm text-red-700">
                  {String(message)}
                </p>
              ))}
            </div>
          )}
        </form.Field>
        <form.Field
          name="password"
          validators={{
            onChange: ({ value }) =>
              value.length >= 8
                ? undefined
                : 'La contraseña debe tener al menos 8 caracteres',
          }}
        >
          {(field) => (
            <div>
              <label htmlFor="login-password" className="block font-medium">
                Contraseña
              </label>
              <input
                id="login-password"
                type="password"
                autoComplete="current-password"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded border p-2"
              />
              {field.state.meta.errors.map((message, index) => (
                <p key={index} role="alert" className="text-sm text-red-700">
                  {String(message)}
                </p>
              ))}
            </div>
          )}
        </form.Field>
        <button
          type="submit"
          disabled={cargando}
          className="w-full rounded bg-blue-600 p-2 font-semibold text-white disabled:opacity-50"
        >
          {cargando ? 'Ingresando...' : 'Ingresar'}
        </button>
      </form>
      <p className="mt-4 text-sm text-gray-600">
        ¿No tienes cuenta?{' '}
        <Link to="/register" className="font-semibold text-blue-700">
          Regístrate
        </Link>
      </p>
    </div>
  )
}
