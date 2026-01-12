const API_BASE_URL = '/api/v1'

export interface EntradaPayload {
  id_lote: number
  quantidade: number
  id_usuario: number
  fornecedor?: string
}

export async function registrarEntrada (payload: EntradaPayload) {
  const res = await fetch(`${API_BASE_URL}/movimentacao/entrada`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const errBody = await res.json().catch(() => null)
    const message = errBody?.detail || `HTTP ${res.status}`
    const error: any = new Error(message)
    error.status = res.status
    error.body = errBody
    throw error
  }

  return res.json()
}
