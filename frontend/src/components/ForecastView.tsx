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

  const renderChart = () => {
    if (!result?.forecast || result.forecast.length === 0) return null
    
    const data = result.forecast
    const maxVal = Math.max(...data.map((p: any) => p.upper), 5)
    const chartHeight = 280
    const chartWidth = Math.max(data.length * 90, 700)
    const padLeft = 60
    const padRight = 40
    const padTop = 20
    const padBottom = 60
    const plotWidth = chartWidth - padLeft - padRight
    const plotHeight = chartHeight
    
    return (
      <div style={{ marginTop: '2rem', padding: '1.5rem', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '12px', boxShadow: '0 8px 16px rgba(0,0,0,0.1)' }}>
        <h4 style={{ marginBottom: '1.5rem', color: 'white', fontSize: '1.2rem', fontWeight: '600' }}>📈 Demand Forecast Trend Line</h4>
        <div style={{ background: 'white', borderRadius: '8px', padding: '1.5rem', overflowX: 'auto' }}>
          <svg width={chartWidth} height={chartHeight + padTop + padBottom} style={{ display: 'block' }}>
            {/* Grid lines and Y-axis labels */}
            {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => {
              const y = padTop + plotHeight * (1 - ratio)
              return (
                <g key={i}>
                  <line
                    x1={padLeft}
                    y1={y}
                    x2={chartWidth - padRight}
                    y2={y}
                    stroke="#e2e8f0"
                    strokeWidth="1"
                    strokeDasharray="4 4"
                  />
                  <text 
                    x={padLeft - 10} 
                    y={y + 4} 
                    textAnchor="end" 
                    fontSize="12" 
                    fill="#718096"
                  >
                    {(maxVal * ratio).toFixed(1)}
                  </text>
                </g>
              )
            })}
            
            {/* Confidence interval area */}
            <path
              d={(() => {
                let path = ''
                // Top line (upper bound)
                data.forEach((p: any, i: number) => {
                  const x = padLeft + (i / (data.length - 1)) * plotWidth
                  const y = padTop + plotHeight - (p.upper / maxVal) * plotHeight
                  path += (i === 0 ? 'M' : 'L') + ` ${x} ${y} `
                })
                // Bottom line (lower bound) - reverse
                for (let i = data.length - 1; i >= 0; i--) {
                  const p = data[i]
                  const x = padLeft + (i / (data.length - 1)) * plotWidth
                  const y = padTop + plotHeight - (p.lower / maxVal) * plotHeight
                  path += `L ${x} ${y} `
                }
                path += 'Z'
                return path
              })()}
              fill="#bee3f8"
              opacity="0.5"
            />
            
            {/* Main trend line */}
            <polyline
              points={data.map((p: any, i: number) => {
                const x = padLeft + (i / (data.length - 1)) * plotWidth
                const y = padTop + plotHeight - (p.predicted / maxVal) * plotHeight
                return `${x},${y}`
              }).join(' ')}
              fill="none"
              stroke="#667eea"
              strokeWidth="4"
              strokeLinecap="round"
            />
            
            {/* Data points */}
            {data.map((p: any, i: number) => {
              const x = padLeft + (i / (data.length - 1)) * plotWidth
              const y = padTop + plotHeight - (p.predicted / maxVal) * plotHeight
              const date = new Date(p.date)
              
              return (
                <g key={i}>
                  <circle cx={x} cy={y} r="7" fill="white" stroke="#667eea" strokeWidth="3" />
                  <circle cx={x} cy={y} r="3" fill="#667eea" />
                  
                  <text 
                    x={x} 
                    y={padTop + plotHeight + 25} 
                    textAnchor="middle" 
                    fontSize="12" 
                    fill="#4a5568" 
                    fontWeight="600"
                  >
                    {date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </text>
                  
                  <text 
                    x={x} 
                    y={y - 15} 
                    textAnchor="middle" 
                    fontSize="13" 
                    fill="#2d3748" 
                    fontWeight="bold"
                  >
                    {p.predicted.toFixed(1)}
                  </text>
                </g>
              )
            })}
            
            {/* Axis labels */}
            <text 
              x={chartWidth / 2} 
              y={chartHeight + padTop + padBottom - 10} 
              textAnchor="middle" 
              fontSize="14" 
              fill="#4a5568" 
              fontWeight="600"
            >
              Date
            </text>
            <text 
              x={20} 
              y={plotHeight / 2 + padTop} 
              textAnchor="middle" 
              fontSize="14" 
              fill="#4a5568" 
              fontWeight="600"
              transform={`rotate(-90, 20, ${plotHeight / 2 + padTop})`}
            >
              Units Required
            </text>
          </svg>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>📊 Demand Forecast</h2>
      <p style={{ color: '#718096', marginBottom: '2rem' }}>
        AI-powered blood demand predictions with confidence intervals
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

      {result && !error && result.forecast && result.forecast.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          {/* Summary Cards */}
          <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
              <div className="stat-value">{result.forecast.length}</div>
              <div className="stat-label" style={{ color: 'rgba(255,255,255,0.9)' }}>📅 Days Forecast</div>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
              <div className="stat-value">{(result.forecast.reduce((sum: number, p: any) => sum + p.predicted, 0)).toFixed(1)}</div>
              <div className="stat-label" style={{ color: 'rgba(255,255,255,0.9)' }}>📊 Total Demand</div>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
              <div className="stat-value">{(result.forecast.reduce((sum: number, p: any) => sum + p.predicted, 0) / result.forecast.length).toFixed(2)}</div>
              <div className="stat-label" style={{ color: 'rgba(255,255,255,0.9)' }}>📈 Avg Daily</div>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', color: 'white' }}>
              <div className="stat-value">{result.metrics.mae.toFixed(2)}</div>
              <div className="stat-label" style={{ color: 'rgba(255,255,255,0.9)' }}>🎯 MAE</div>
            </div>
          </div>

          {/* Chart */}
          {renderChart()}

          {/* Forecast Table */}
          <div style={{ marginTop: '2rem', background: '#f7fafc', borderRadius: '12px', padding: '1.5rem' }}>
            <h4 style={{ marginBottom: '1rem', color: '#2d3748' }}>📋 Detailed Forecast</h4>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: '#edf2f7', borderBottom: '2px solid #cbd5e0' }}>
                    <th style={{ padding: '12px', textAlign: 'left', color: '#4a5568', fontWeight: '600' }}>Date</th>
                    <th style={{ padding: '12px', textAlign: 'center', color: '#4a5568', fontWeight: '600' }}>Predicted</th>
                    <th style={{ padding: '12px', textAlign: 'center', color: '#4a5568', fontWeight: '600' }}>Lower Bound</th>
                    <th style={{ padding: '12px', textAlign: 'center', color: '#4a5568', fontWeight: '600' }}>Upper Bound</th>
                    <th style={{ padding: '12px', textAlign: 'center', color: '#4a5568', fontWeight: '600' }}>Range</th>
                  </tr>
                </thead>
                <tbody>
                  {result.forecast.map((p: any, i: number) => (
                    <tr key={i} style={{ borderBottom: '1px solid #e2e8f0', background: i % 2 === 0 ? 'white' : '#f7fafc' }}>
                      <td style={{ padding: '12px', color: '#2d3748', fontWeight: '500' }}>
                        {new Date(p.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                      </td>
                      <td style={{ padding: '12px', textAlign: 'center', color: '#3182ce', fontWeight: 'bold', fontSize: '1.1rem' }}>
                        {p.predicted.toFixed(2)}
                      </td>
                      <td style={{ padding: '12px', textAlign: 'center', color: '#718096' }}>
                        {p.lower.toFixed(2)}
                      </td>
                      <td style={{ padding: '12px', textAlign: 'center', color: '#718096' }}>
                        {p.upper.toFixed(2)}
                      </td>
                      <td style={{ padding: '12px', textAlign: 'center' }}>
                        <span style={{ 
                          background: '#bee3f8', 
                          color: '#2c5282', 
                          padding: '4px 12px', 
                          borderRadius: '12px', 
                          fontSize: '0.9rem',
                          fontWeight: '500'
                        }}>
                          ±{((p.upper - p.lower) / 2).toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Model Info */}
          <div style={{ marginTop: '1.5rem', padding: '1rem', background: '#edf2f7', borderRadius: '8px', fontSize: '0.9rem', color: '#4a5568' }}>
            <strong>Model Info:</strong> Generated on {result.generated_at} | 
            History: {result.history_days} days | 
            MAE: {result.metrics.mae.toFixed(2)} | 
            MAPE: {result.metrics.mape.toFixed(2)}%
          </div>
        </div>
      )}

      {result && !error && (!result.forecast || result.forecast.length === 0) && (
        <div style={{ marginTop: '2rem', padding: '2rem', background: '#fff5f5', border: '2px solid #fc8181', borderRadius: '8px', textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📭</div>
          <h3 style={{ color: '#c53030', marginBottom: '0.5rem' }}>No Forecast Data Available</h3>
          <p style={{ color: '#742a2a' }}>
            Insufficient historical data to generate forecast. Need at least 14 days of usage data.
          </p>
        </div>
      )}
    </div>
  )
}
