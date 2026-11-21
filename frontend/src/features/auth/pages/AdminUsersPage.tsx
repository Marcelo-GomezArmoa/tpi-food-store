import { getApiErrorMessage } from '@/shared/api/error'
import { DataTable } from '@/shared/components/DataTable'
import { ErrorState, LoadingState } from '@/shared/components/States'
import { useAdminUsers } from '@/features/auth/hooks/useAdminUsers'
import type { UsuarioAdmin } from '@/features/auth/types/auth.types'
import type { ColumnDef } from '@tanstack/react-table'
import { useAuth } from '@/features/auth'

export function AdminUsersPage() {
  const { users, changeStatus } = useAdminUsers()
  const { usuario } = useAuth()

  const columns: ColumnDef<UsuarioAdmin>[] = [
    { accessorKey: 'id', header: 'ID' },
    { accessorKey: 'username', header: 'Usuario' },
    {
      id: 'full_name',
      header: 'Nombre completo',
      cell: ({ row }) =>
        row.original.full_name,
    },
    { accessorKey: 'email', header: 'Email' },
    {
      accessorKey: 'role',
      header: 'Rol',
    },
    {
      id: 'estado',
      header: 'Estado',
      cell: ({ row }) =>
        row.original.disabled ? 'Desactivado' : 'Activo',
    },
    {
      id: 'acciones',
      header: 'Acciones',
      enableSorting: false,
      cell: ({ row }) => {
        const active = !row.original.disabled
        if (active && row.original.id === usuario?.id) {
          return <span className="text-sm text-gray-500">Sesión actual</span>
        }
        return (
          <button
            type="button"
            disabled={changeStatus.isPending}
            onClick={() =>
              changeStatus.mutate({ id: row.original.id, active: !active })
            }
            className={`rounded px-3 py-1 font-medium text-white disabled:opacity-50 ${
              active ? 'bg-red-600' : 'bg-green-600'
            }`}
          >
            {active ? 'Desactivar' : 'Activar'}
          </button>
        )
      },
    },
  ]

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-4xl font-bold">Administración de usuarios</h1>
      {users.isLoading && <LoadingState message="Cargando usuarios..." />}
      {users.isError && <ErrorState message={getApiErrorMessage(users.error)} />}
      {changeStatus.isError && (
        <ErrorState
          message={getApiErrorMessage(changeStatus.error, 'No se pudo cambiar el estado')}
        />
      )}
      {users.data && <DataTable data={users.data} columns={columns} />}
    </div>
  )
}
