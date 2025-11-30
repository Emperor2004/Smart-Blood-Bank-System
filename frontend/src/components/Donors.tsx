import React, { useState } from 'react'
import { API_URL } from '../config'

interface Donor {
  donor_id: number
  name: string
  phone: string
  email: string
  blood_group: string
  eligible: boolean
  distance_km?: number
}

interface Props {
  onBack?: () => void
}

export default function Donors({ onBack }: Props) {
  const [bloodGroup, setBloodGroup] = useState('')
  const [eligibleOnly, setEligibleOnly] = useState(true)
  const [donors, setDonors] = useState<Donor[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [notifying, setNotifying] = useState<number | null>(null)

  const searchDonors = async () => {
    try {
      setLoading(true)
      setError('')
      
      const params = new URLSearchParams()
      if (bloodGroup) params.append('blood_group', bloodGroup)
      if (eligibleOnly) params.append('eligible_only', 'true')
      
      const res = await fetch(`${API_URL}/api/donors/search?${params}`)
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      
      const data = await res.json()
      setDonors(data.donors || [])
    } catch (err: any) {
      setError(err.message)
      setDonors([])
    } finally {
      setLoading(false)
    }
  }

  const notifyDonor = async (donorId: number, donorName: string) => {
    if (!confirm(`Send notification to ${donorName}?`)) return

    try {
      setNotifying(donorId)
      const res = await fetch(`${API_URL}/api/notifications/donor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          donor_id: donorId,
          hospital_name: 'City Hospital',
          blood_group: bloodGroup || 'O+',
          contact_phone: '+91-1234567890'
        })
      })
      
      if (!res.ok) throw new Error('Failed to send notification')
      alert(`✅ Notification sent to ${donorName}!`)
    } catch (err: any) {
      alert(`❌ Error: ${err.message}`)
    } finally {
      setNotifying(null)
    }
  }

  const clearFilters = () => {
    setBloodGroup('')
    setEligibleOnly(true)
    setDonors([])
    setError('')
  }

  return (
    <div className="donors">
      <div className="page-header">
        <h2>👥 Donor Search</h2>
      </div>

      <div className="info-message">
        <p>💡 Search for eligible donors and send notifications for urgent blood requirements.</p>
      </div>
      
      <div className="form-card">
        <div className="form-row">
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
          
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={eligibleOnly}
                onChange={(e) => setEligibleOnly(e.target.checked)}
                title="Show only eligible donors"
              />
              <span>Eligible donors only</span>
            </label>
          </div>
        </div>

        <div className="form-actions">
          <button 
            onClick={searchDonors} 
            disabled={loading}
            className="btn-primary"
            title="Search for donors"
          >
            {loading ? '⏳ Searching...' : '🔍 Search Donors'}
          </button>
          <button 
            onClick={clearFilters} 
            className="btn-secondary"
            title="Clear filters"
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

      {!loading && donors.length === 0 && !error && (
        <div className="info-box">
          <p>ℹ️ No donors found. Try different filters or add donors to the system.</p>
        </div>
      )}

      {donors.length > 0 && (
        <div className="donors-list">
          <h3>Found {donors.length} Donor(s)</h3>
          {donors.map((d) => (
            <div key={d.donor_id} className="donor-card">
              <div className="donor-info">
                <h4>{d.name}</h4>
                <p><strong>Blood Group:</strong> <span className="blood-badge">{d.blood_group}</span></p>
                <p><strong>Phone:</strong> {d.phone}</p>
                <p><strong>Email:</strong> {d.email}</p>
                <p>
                  <strong>Status:</strong> 
                  {d.eligible ? 
                    <span className="status-badge eligible">✅ Eligible</span> : 
                    <span className="status-badge not-eligible">❌ Not Eligible</span>
                  }
                </p>
                {d.distance_km && <p><strong>Distance:</strong> {d.distance_km} km</p>}
              </div>
              {d.eligible && (
                <button 
                  onClick={() => notifyDonor(d.donor_id, d.name)}
                  disabled={notifying === d.donor_id}
                  className="btn-primary"
                  title={`Send notification to ${d.name}`}
                >
                  {notifying === d.donor_id ? '⏳ Sending...' : '📱 Notify'}
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
