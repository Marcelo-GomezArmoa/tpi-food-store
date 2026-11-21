export function Skeleton() {
  return (
    <div
      role="status"
      aria-label="Cargando producto"
      className="animate-pulse overflow-hidden rounded-xl bg-white shadow"
    >
      <div className="h-48 bg-gray-200" />
      <div className="space-y-3 p-5">
        <div className="h-4 w-1/3 rounded bg-gray-200" />
        <div className="h-6 w-2/3 rounded bg-gray-200" />
        <div className="h-12 rounded bg-gray-200" />
        <div className="h-9 rounded bg-gray-200" />
      </div>
    </div>
  )
}
