export interface UsuarioAuth {
  id: number
  nombre: string
  apellido: string
  email: string
  celular?: string | null
  created_at?: string
  updated_at?: string
  deleted_at?: string | null
  roles: string[]
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  nombre: string
  apellido: string
  email: string
  celular?: string | null
  password: string
}

export interface UsuarioAdmin extends UsuarioAuth {
  celular: string | null
  created_at: string
  updated_at: string
  deleted_at: string | null
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
