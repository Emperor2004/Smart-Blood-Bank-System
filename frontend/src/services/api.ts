const BACKEND_BASE = (import.meta.env.VITE_BACKEND_URL as string) || 'http://localhost:8000'

export async function apiUploadInventory(form: FormData) {
  const res = await fetch(`${BACKEND_BASE}/api/inventory/upload`, {
    method: 'POST',
    body: form
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }

  return res.json()
}

export async function apiGetForecast(params: { hospital_id: string, blood_group?: string, component?: string, days?: number }) {
  const url = new URL(`${BACKEND_BASE}/api/forecast`)
  Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null) url.searchParams.append(k, String(v)) })

  const res = await fetch(url.toString(), { method: 'GET' })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  return res.json()
}
