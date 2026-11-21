import { Link } from 'react-router-dom'

export function UnauthorizedPage() {
  return (
    <div className="mx-auto mt-16 max-w-xl rounded-lg bg-white p-8 text-center shadow">
      <h1 className="text-4xl font-bold text-red-700">Acceso denegado</h1>
      <p className="mt-4 text-gray-700">
        Tu usuario no tiene los permisos necesarios para acceder a esta página.
      </p>
      <Link
        to="/"
        className="mt-6 inline-block rounded bg-blue-600 px-5 py-2 font-semibold text-white"
      >
        Volver al inicio
      </Link>
    </div>
  )
}
