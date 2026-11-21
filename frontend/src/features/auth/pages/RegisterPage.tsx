import { useForm } from '@tanstack/react-form'
import { Link, useNavigate } from 'react-router-dom'

import { getApiErrorMessage } from '@/shared/api/error'
import { TextField } from '@/features/auth/components/TextField'
import { useRegister } from '@/features/auth/hooks/useRegister'
import type { RegisterData } from '@/features/auth/types/auth.types'

export function RegisterPage() {
  const navigate = useNavigate()
  const register = useRegister()
  const form = useForm({
    defaultValues: {
      nombre: '',
      apellido: '',
      email: '',
      celular: '',
      password: '',
    },
    onSubmit: async ({ value }) => {
      const data: RegisterData = {
        ...value,
        nombre: value.nombre.trim(),
        apellido: value.apellido.trim(),
        email: value.email.trim(),
        celular: value.celular.trim() || undefined,
      }

      try {
        await register.mutateAsync(data)
        void navigate('/login', { replace: true })
      } catch {
        // El error se muestra mediante el estado de la mutación.
      }
    },
  })

  return (
    <div className="mx-auto my-12 max-w-lg rounded-lg bg-white p-6 shadow">
      <h1 className="text-3xl font-bold">Crear cuenta</h1>
      {register.isError && (
        <div role="alert" className="mt-4 rounded bg-red-100 p-3 text-red-800">
          {getApiErrorMessage(register.error, 'No se pudo registrar la cuenta')}
        </div>
      )}
      <form
        className="mt-6 grid gap-4 sm:grid-cols-2"
        noValidate
        onSubmit={(event) => {
          event.preventDefault()
          void form.handleSubmit()
        }}
      >
        <form.Field
          name="nombre"
          validators={{
            onChange: ({ value }) =>
              value.trim() ? undefined : 'El nombre es obligatorio',
          }}
        >
          {(field) => (
            <TextField
              field={field}
              id="register-nombre"
              label="Nombre"
            />
          )}
        </form.Field>
        <form.Field
          name="apellido"
          validators={{
            onChange: ({ value }) =>
              value.trim() ? undefined : 'El apellido es obligatorio',
          }}
        >
          {(field) => (
            <TextField
              field={field}
              id="register-apellido"
              label="Apellido"
            />
          )}
        </form.Field>
        <form.Field
          name="email"
          validators={{
            onChange: ({ value }) =>
              /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
                ? undefined
                : 'Ingresa un email válido',
          }}
        >
          {(field) => (
            <TextField
              field={field}
              id="register-email"
              label="Email"
              type="email"
              className="sm:col-span-2"
            />
          )}
        </form.Field>
        <form.Field name="celular">
          {(field) => (
            <TextField
              field={field}
              id="register-celular"
              label="Celular (opcional)"
              type="tel"
              className="sm:col-span-2"
            />
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
            <TextField
              field={field}
              id="register-password"
              label="Contraseña"
              type="password"
              className="sm:col-span-2"
            />
          )}
        </form.Field>
        <button
          type="submit"
          disabled={register.isPending}
          className="rounded bg-blue-600 p-2 font-semibold text-white disabled:opacity-50 sm:col-span-2"
        >
          {register.isPending ? 'Creando cuenta...' : 'Registrarse'}
        </button>
      </form>
      <p className="mt-4 text-sm text-gray-600">
        ¿Ya tienes cuenta?{' '}
        <Link to="/login" className="font-semibold text-blue-700">
          Inicia sesión
        </Link>
      </p>
    </div>
  )
}
