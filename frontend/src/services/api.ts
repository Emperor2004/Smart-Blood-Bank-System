const BACKEND_BASE = (import.meta.env.VITE_API_URL as string) || 'https://yolande-nondivisional-norah.ngrok-free.dev'

export async function apiUploadInventory(form: FormData) {
  try {
    const res = await fetch(`${BACKEND_BASE}/api/inventory/upload`, {
      method: 'POST',
      body: form,
      mode: 'cors',
      credentials: 'omit'
    })

    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || res.statusText)
    }

    return res.json()
  } catch (error: any) {
    if (error.message === 'Failed to fetch') {
      throw new Error(`Cannot connect to backend API at ${BACKEND_BASE}. Please check if the backend is running.`)
    }
    throw error
  }
}

export async function apiGetForecast(params: { hospital_id: string, blood_group?: string, component?: string, days?: number }) {
  try {
    const url = new URL(`${BACKEND_BASE}/api/forecast`)
    Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null) url.searchParams.append(k, String(v)) })

    const res = await fetch(url.toString(), { 
      method: 'GET',
      mode: 'cors',
      credentials: 'omit'
    })
    
    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || res.statusText)
    }
    return res.json()
  } catch (error: any) {
    if (error.message === 'Failed to fetch') {
      throw new Error(`Cannot connect to backend API at ${BACKEND_BASE}. Please check if the backend is running.`)
    }
    throw error
  }
}
