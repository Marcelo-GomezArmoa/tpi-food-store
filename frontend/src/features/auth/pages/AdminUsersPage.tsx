import { getApiErrorMessage } from '@/shared/api/error'
import { DataTable } from '@/shared/components/DataTable'
import { ErrorState, LoadingState } from '@/shared/components/States'
import { useAdminUsers } from '@/features/auth/hooks/useAdminUsers'
import type { UsuarioAdmin } from '@/features/auth/types/auth.types'
import type { ColumnDef } from '@tanstack/react-table'

export function AdminUsersPage() {
  const { users, changeStatus } = useAdminUsers()

  const columns: ColumnDef<UsuarioAdmin>[] = [
    { accessorKey: 'id', header: 'ID' },
    {
      id: 'nombre',
      header: 'Usuario',
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
