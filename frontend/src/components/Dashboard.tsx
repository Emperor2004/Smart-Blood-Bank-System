import React, { useState, useEffect } from 'react'
import { API_URL } from '../config'

interface DashboardData {
  data: {
    total_units: number
    total_records: number
    high_risk_count: number
    high_risk_units: number
  }
}

interface Props {
  onBack?: () => void
}

export default function Dashboard({ onBack }: Props) {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    try {
      setLoading(true)
      setError('')
      const res = await fetch(`${API_URL}/api/dashboard/summary`)
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      const result = await res.json()
      setData(result)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading dashboard data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error-box">
          <h3>❌ Error Loading Dashboard</h3>
          <p>{error}</p>
          <button onClick={fetchDashboard} className="btn-primary" title="Retry loading">
            🔄 Retry
          </button>
        </div>
      </div>
    )
  }

  if (!data || !data.data) {
    return (
      <div className="dashboard">
        <div className="info-box">
          <p>No dashboard data available</p>
          <button onClick={fetchDashboard} className="btn-primary">
            🔄 Refresh
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h2>📊 Dashboard Overview</h2>
        <button onClick={fetchDashboard} className="btn-secondary" title="Refresh data">
          🔄 Refresh
        </button>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card" title="Total blood units in inventory">
          <div className="stat-icon">🩸</div>
          <div className="stat-value">{data.data.total_units}</div>
          <div className="stat-label">Total Units</div>
        </div>
        
        <div className="stat-card" title="Total inventory records">
          <div className="stat-icon">📋</div>
          <div className="stat-value">{data.data.total_records}</div>
          <div className="stat-label">Records</div>
        </div>
        
        <div className="stat-card alert" title="Units expiring soon (≤3 days)">
          <div className="stat-icon">⚠️</div>
          <div className="stat-value">{data.data.high_risk_units}</div>
          <div className="stat-label">High Risk Units</div>
          <div className="stat-sublabel">{data.data.high_risk_count} records</div>
        </div>
      </div>

      <div className="info-message">
        <p>💡 <strong>Tip:</strong> High risk units are expiring within 3 days. Consider transfer recommendations.</p>
      </div>
    </div>
  )
}
