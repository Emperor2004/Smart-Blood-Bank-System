import React, { useState } from 'react'
import { apiGetForecast } from '../services/api'
import ErrorDisplay from './ErrorDisplay'

const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
const components = ['RBC', 'Platelets', 'Plasma']

export default function ForecastView() {
  const [hospitalId, setHospitalId] = useState('H001')
  const [bloodGroup, setBloodGroup] = useState('A+')
  const [component, setComponent] = useState('RBC')
  const [days, setDays] = useState(7)
  const [result, setResult] = useState<any | null>(null)
  const [error, setError] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const onGet = async () => {
    setLoading(true)
    setResult(null)
    setError(null)
    
    try {
      const res = await apiGetForecast({ 
        hospital_id: hospitalId, 
        blood_group: bloodGroup, 
        component, 
        days 
      })
      setResult(res)
    } catch (err: any) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRetry = () => {
    setError(null)
    onGet()
  }

  return (
    <div className="card">
      <h2>📊 Demand Forecast</h2>
      <p style={{ color: '#718096', marginBottom: '2rem' }}>
        Predict blood demand using AI-powered forecasting
      </p>

      <div className="form-grid">
        <div className="form-group">
          <label className="form-label">🏥 Hospital ID</label>
          <input 
            className="form-input"
            value={hospitalId} 
            onChange={(e) => setHospitalId(e.target.value)} 
            placeholder="e.g., H001" 
          />
        </div>

        <div className="form-group">
          <label className="form-label">🩸 Blood Group</label>
          <select 
            className="form-select"
            value={bloodGroup} 
            onChange={(e) => setBloodGroup(e.target.value)}
          >
            {bloodGroups.map(bg => (
              <option key={bg} value={bg}>{bg}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">💉 Component</label>
          <select 
            className="form-select"
            value={component} 
            onChange={(e) => setComponent(e.target.value)}
          >
            {components.map(comp => (
              <option key={comp} value={comp}>{comp}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">📅 Forecast Days</label>
          <input 
            className="form-input"
            type="number" 
            value={days} 
            onChange={(e) => setDays(Number(e.target.value))} 
            min={1} 
            max={30} 
          />
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
        <button 
          className="btn btn-primary" 
          onClick={onGet} 
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Generating Forecast...
            </>
          ) : (
            <>
              🔮 Generate Forecast
            </>
          )}
        </button>
      </div>

      {error && <ErrorDisplay error={error} onRetry={handleRetry} />}

      {result && !error && (
        <div className="success-display">
          <div className="success-icon">📈</div>
          <h3 className="success-title">Forecast Generated!</h3>
          
          {result.forecast && (
            <>
              <div className="stats-grid" style={{ marginBottom: '1rem' }}>
                <div className="stat-card">
                  <div className="stat-value">{result.forecast.length || 0}</div>
                  <div className="stat-label">Data Points</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{days}</div>
                  <div className="stat-label">Days Ahead</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{bloodGroup}</div>
                  <div className="stat-label">Blood Group</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{component}</div>
                  <div className="stat-label">Component</div>
                </div>
              </div>

              <details className="error-details">
                <summary>View Forecast Data</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </details>
            </>
          )}

          {!result.forecast && (
            <div className="result-content">
              {JSON.stringify(result, null, 2)}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
