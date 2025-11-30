import React, { useState } from 'react'
import { API_URL } from '../config'

interface Transfer {
  source_hospital: string
  destination_hospital: string
  blood_group: string
  component: string
  units: number
  urgency_score: number
  distance_km: number
  eta_minutes: number
}

interface Props {
  onBack?: () => void
}

export default function Transfers({ onBack }: Props) {
  const [hospitalId, setHospitalId] = useState('')
  const [bloodGroup, setBloodGroup] = useState('')
  const [component, setComponent] = useState('')
  const [transfers, setTransfers] = useState<Transfer[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchRecommendations = async () => {
    if (!hospitalId.trim()) {
      setError('Please enter Hospital ID')
      return
    }

    try {
      setLoading(true)
      setError('')
      
      const params = new URLSearchParams({ hospital_id: hospitalId })
      if (bloodGroup) params.append('blood_group', bloodGroup)
      if (component) params.append('component', component)
      
      const res = await fetch(`${API_URL}/api/transfers/recommendations?${params}`)
      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `HTTP ${res.status}`)
      }
      
      const data = await res.json()
      setTransfers(data.recommendations || [])
    } catch (err: any) {
      setError(err.message)
      setTransfers([])
    } finally {
      setLoading(false)
    }
  }

  const clearFilters = () => {
    setHospitalId('')
    setBloodGroup('')
    setComponent('')
    setTransfers([])
    setError('')
  }

  return (
    <div className="transfers">
      <div className="page-header">
        <h2>🚚 Transfer Recommendations</h2>
      </div>

      <div className="info-message">
        <p>💡 Get intelligent transfer recommendations based on urgency, distance, and surplus inventory.</p>
      </div>
      
      <div className="form-card">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="hospitalId">Hospital ID *</label>
            <input
              id="hospitalId"
              type="text"
              placeholder="e.g., H001"
              value={hospitalId}
              onChange={(e) => setHospitalId(e.target.value)}
              title="Enter hospital ID"
            />
          </div>

          <div className="form-group">
            <label htmlFor="bloodGroup">Blood Group</label>
            <select 
              id="bloodGroup"
              value={bloodGroup} 
              onChange={(e) => setBloodGroup(e.target.value)}
              title="Filter by blood group"
            >
              <option value="">All Blood Groups</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="component">Component</label>
            <select 
              id="component"
              value={component} 
              onChange={(e) => setComponent(e.target.value)}
              title="Filter by component"
            >
              <option value="">All Components</option>
              <option value="RBC">RBC</option>
              <option value="Platelets">Platelets</option>
              <option value="Plasma">Plasma</option>
            </select>
          </div>
        </div>

        <div className="form-actions">
          <button 
            onClick={fetchRecommendations} 
            disabled={loading || !hospitalId.trim()}
            className="btn-primary"
            title="Get transfer recommendations"
          >
            {loading ? '⏳ Loading...' : '🔍 Get Recommendations'}
          </button>
          <button 
            onClick={clearFilters} 
            className="btn-secondary"
            title="Clear all filters"
          >
            🗑️ Clear
          </button>
        </div>
      </div>

      {error && (
        <div className="error-box">
          <p>❌ {error}</p>
        </div>
      )}

      {!loading && transfers.length === 0 && !error && hospitalId && (
        <div className="info-box">
          <p>ℹ️ No transfer recommendations found. Try different filters or check if hospital has inventory.</p>
        </div>
      )}

      {transfers.length > 0 && (
        <div className="transfers-list">
          <h3>Found {transfers.length} Recommendation(s)</h3>
          {transfers.map((t, idx) => (
            <div key={idx} className="transfer-card">
              <div className="transfer-header">
                <span 
                  className="urgency" 
                  style={{
                    background: t.urgency_score > 0.7 ? '#ff4444' : t.urgency_score > 0.4 ? '#ffa500' : '#4CAF50'
                  }}
                  title={`Urgency score: ${(t.urgency_score * 100).toFixed(0)}%`}
                >
                  {t.urgency_score > 0.7 ? '🔴 High' : t.urgency_score > 0.4 ? '🟡 Medium' : '🟢 Low'} Urgency
                </span>
              </div>
              <div className="transfer-details">
                <p><strong>From:</strong> {t.source_hospital}</p>
                <p><strong>To:</strong> {t.destination_hospital}</p>
                <p><strong>Blood:</strong> {t.blood_group} {t.component}</p>
                <p><strong>Units:</strong> {t.units}</p>
                <p><strong>Distance:</strong> {t.distance_km.toFixed(1)} km</p>
                <p><strong>ETA:</strong> {t.eta_minutes} min</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
