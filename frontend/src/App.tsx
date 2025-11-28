import React, { useState, useEffect } from 'react'
import InventoryUpload from './components/InventoryUpload'
import ForecastView from './components/ForecastView'
import { API_URL } from './config'

export default function App() {
  const [view, setView] = useState<'home' | 'upload' | 'forecast'>('home')
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking')
  const [errorDetails, setErrorDetails] = useState<string>('')

  useEffect(() => {
    const checkAPI = async () => {
      try {
        console.log('Checking API at:', API_URL)
        const response = await fetch(`${API_URL}/health`, {
          method: 'GET',
          headers: { 'Accept': 'application/json' }
        })
        console.log('API Response:', response.status, response.statusText)
        
        if (response.ok) {
          const data = await response.json()
          console.log('API Health:', data)
          setApiStatus('connected')
        } else {
          setApiStatus('error')
          setErrorDetails(`HTTP ${response.status}: ${response.statusText}`)
        }
      } catch (error: any) {
        console.error('API Connection Error:', error)
        setApiStatus('error')
        setErrorDetails(`${error.name}: ${error.message}`)
      }
    }
    checkAPI()
  }, [])

  return (
    <div className="app">
      {apiStatus === 'error' && (
        <div style={{
          background: '#ff4444',
          color: 'white',
          padding: '15px',
          textAlign: 'center',
          fontWeight: 'bold'
        }}>
          ⚠️ API Connection Failed: {errorDetails}
          <br />
          <small style={{ fontSize: '12px', opacity: 0.9 }}>
            API URL: {API_URL} | Check browser console (F12) for details
          </small>
        </div>
      )}
      
      {apiStatus === 'checking' && (
        <div style={{
          background: '#ffa500',
          color: 'white',
          padding: '10px',
          textAlign: 'center'
        }}>
          🔄 Connecting to API at {API_URL}...
        </div>
      )}
      
      {apiStatus === 'connected' && (
        <div style={{
          background: '#4CAF50',
          color: 'white',
          padding: '10px',
          textAlign: 'center'
        }}>
          ✅ Connected to API: {API_URL}
        </div>
      )}
      
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🩸</span>
            <h1>Smart Blood Bank</h1>
          </div>
          <nav className="nav">
            <button 
              className={`nav-btn ${view === 'home' ? 'active' : ''}`}
              onClick={() => setView('home')}
            >
              🏠 Home
            </button>
            <button 
              className={`nav-btn ${view === 'upload' ? 'active' : ''}`}
              onClick={() => setView('upload')}
            >
              📤 Upload
            </button>
            <button 
              className={`nav-btn ${view === 'forecast' ? 'active' : ''}`}
              onClick={() => setView('forecast')}
            >
              📊 Forecast
            </button>
          </nav>
        </div>
      </header>

      <main className="main">
        {view === 'home' && (
          <div className="hero">
            <h2>Welcome to Smart Blood Bank</h2>
            <p>Intelligent inventory management and demand forecasting for blood banks</p>
            
            <div className="features">
              <div className="feature-card" onClick={() => setView('upload')}>
                <div className="feature-icon">📤</div>
                <h3>Upload Inventory</h3>
                <p>Import blood inventory data via CSV files</p>
              </div>
              
              <div className="feature-card" onClick={() => setView('forecast')}>
                <div className="feature-icon">📊</div>
                <h3>Demand Forecast</h3>
                <p>AI-powered predictions for blood demand</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🏥</div>
                <h3>Multi-Hospital</h3>
                <p>Manage inventory across multiple facilities</p>
              </div>
            </div>
          </div>
        )}

        {view === 'upload' && <InventoryUpload />}
        {view === 'forecast' && <ForecastView />}
      </main>

      <footer className="footer">
        <p>🩸 Smart Blood Bank System - Saving Lives Through Technology</p>
      </footer>
    </div>
  )
}
