interface TextFieldProps {
  id: string
  label: string
  type?: 'text' | 'email' | 'tel' | 'password'
  className?: string
  field: {
    name: string
    state: { value: string; meta: { errors: unknown[] } }
    handleBlur: () => void
    handleChange: (value: string) => void
  }
}

export function TextField({ field, id, label, type = 'text', className }: TextFieldProps) {
  return (
    <div className={className}>
      <label htmlFor={id} className="block font-medium">{label}</label>
      <input
        id={id}
        name={field.name}
        type={type}
        value={field.state.value}
        onBlur={field.handleBlur}
        onChange={(event) => field.handleChange(event.target.value)}
        className="mt-1 w-full rounded border p-2"
      />
      {field.state.meta.errors.map((message, index) => (
        <p key={index} role="alert" className="text-sm text-red-700">{String(message)}</p>
      ))}
    </div>
  )
}
