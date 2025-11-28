import React, { useState } from 'react'
import { apiGetForecast } from '../services/api'

export default function ForecastView() {
  const [hospitalId, setHospitalId] = useState('H001')
  const [bloodGroup, setBloodGroup] = useState('A+')
  const [component, setComponent] = useState('RBC')
  const [days, setDays] = useState(7)
  const [result, setResult] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)

  const onGet = async () => {
    setLoading(true)
    setResult(null)
    try {
      const res = await apiGetForecast({ hospital_id: hospitalId, blood_group: bloodGroup, component, days })
      setResult(res)
    } catch (err: any) {
      setResult({ error: err?.message || err })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Forecast</h2>
      <div style={{ display: 'grid', gap: 8, maxWidth: 520 }}>
        <input value={hospitalId} onChange={(e) => setHospitalId(e.target.value)} placeholder="Hospital ID" />
        <input value={bloodGroup} onChange={(e) => setBloodGroup(e.target.value)} placeholder="Blood Group" />
        <input value={component} onChange={(e) => setComponent(e.target.value)} placeholder="Component" />
        <input type="number" value={days} onChange={(e) => setDays(Number(e.target.value))} min={1} max={30} />
        <button onClick={onGet} disabled={loading}>Get Forecast</button>
      </div>

      {result && (
        <pre style={{ whiteSpace: 'pre-wrap', marginTop: 12 }}>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  )
}
