import React, { useState, useEffect } from 'react'
import InventoryUpload from './components/InventoryUpload'
import ForecastView from './components/ForecastView'
import Dashboard from './components/Dashboard'
import Transfers from './components/Transfers'
import Donors from './components/Donors'
import { API_URL } from './config'

type View = 'home' | 'dashboard' | 'upload' | 'forecast' | 'transfers' | 'donors'

export default function App() {
  const [view, setView] = useState<View>('home')
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking')
  const [errorDetails, setErrorDetails] = useState<string>('')

  useEffect(() => {
    const checkAPI = async () => {
      try {
        const response = await fetch(`${API_URL}/health`, {
          method: 'GET',
          headers: { 'Accept': 'application/json' }
        })
        
        if (response.ok) {
          setApiStatus('connected')
        } else {
          setApiStatus('error')
          setErrorDetails(`HTTP ${response.status}: ${response.statusText}`)
        }
      } catch (error: any) {
        setApiStatus('error')
        setErrorDetails(`${error.name}: ${error.message}`)
      }
    }
    checkAPI()
  }, [])

  const goHome = () => setView('home')

  const getViewTitle = () => {
    const titles: Record<View, string> = {
      home: 'Home',
      dashboard: 'Dashboard',
      upload: 'Upload Inventory',
      forecast: 'Demand Forecast',
      transfers: 'Transfer Recommendations',
      donors: 'Donor Management'
    }
    return titles[view]
  }

  return (
    <div className="app">
      {apiStatus === 'error' && (
        <div className="alert alert-error">
          <span>⚠️ API Connection Failed: {errorDetails}</span>
          <button onClick={() => window.location.reload()} className="btn-small">
            🔄 Retry
          </button>
        </div>
      )}
      
      {apiStatus === 'checking' && (
        <div className="alert alert-warning">
          🔄 Connecting to API...
        </div>
      )}
      
      {apiStatus === 'connected' && view !== 'home' && (
        <div className="alert alert-success">
          ✅ Connected
        </div>
      )}
      
      <header className="header">
        <div className="header-content">
          <div className="logo" onClick={goHome} style={{ cursor: 'pointer' }} title="Go to Home">
            <span className="logo-icon">🩸</span>
            <h1>Smart Blood Bank</h1>
          </div>
          <nav className="nav">
            <button 
              className={`nav-btn ${view === 'home' ? 'active' : ''}`}
              onClick={goHome}
              title="Home"
            >
              🏠 Home
            </button>
            <button 
              className={`nav-btn ${view === 'dashboard' ? 'active' : ''}`}
              onClick={() => setView('dashboard')}
              title="View Dashboard"
            >
              📊 Dashboard
            </button>
            <button 
              className={`nav-btn ${view === 'upload' ? 'active' : ''}`}
              onClick={() => setView('upload')}
              title="Upload CSV"
            >
              📤 Upload
            </button>
            <button 
              className={`nav-btn ${view === 'forecast' ? 'active' : ''}`}
              onClick={() => setView('forecast')}
              title="View Forecasts"
            >
              📈 Forecast
            </button>
            <button 
              className={`nav-btn ${view === 'transfers' ? 'active' : ''}`}
              onClick={() => setView('transfers')}
              title="Transfer Recommendations"
            >
              🚚 Transfers
            </button>
            <button 
              className={`nav-btn ${view === 'donors' ? 'active' : ''}`}
              onClick={() => setView('donors')}
              title="Search Donors"
            >
              👥 Donors
            </button>
          </nav>
        </div>
      </header>

      <main className="main">
        {view !== 'home' && (
          <div className="breadcrumb">
            <button onClick={goHome} className="back-btn" title="Back to Home">
              ← Back to Home
            </button>
            <span className="current-page">{getViewTitle()}</span>
          </div>
        )}

        {view === 'home' && (
          <div className="hero">
            <h2>Welcome to Smart Blood Bank</h2>
            <p>Intelligent inventory management and demand forecasting for blood banks</p>
            
            <div className="features">
              <div className="feature-card" onClick={() => setView('dashboard')} title="View real-time statistics">
                <div className="feature-icon">📊</div>
                <h3>Dashboard</h3>
                <p>Real-time inventory overview and analytics</p>
                <button className="card-btn">View Dashboard →</button>
              </div>
              
              <div className="feature-card" onClick={() => setView('upload')} title="Upload CSV file">
                <div className="feature-icon">📤</div>
                <h3>Upload Inventory</h3>
                <p>Import blood inventory data via CSV files</p>
                <button className="card-btn">Upload CSV →</button>
              </div>
              
              <div className="feature-card" onClick={() => setView('forecast')} title="View demand predictions">
                <div className="feature-icon">📈</div>
                <h3>Demand Forecast</h3>
                <p>AI-powered predictions for blood demand</p>
                <button className="card-btn">View Forecast →</button>
              </div>
              
              <div className="feature-card" onClick={() => setView('transfers')} title="Get transfer recommendations">
                <div className="feature-icon">🚚</div>
                <h3>Transfer Recommendations</h3>
                <p>Intelligent redistribution between hospitals</p>
                <button className="card-btn">View Transfers →</button>
              </div>
              
              <div className="feature-card" onClick={() => setView('donors')} title="Search and notify donors">
                <div className="feature-icon">👥</div>
                <h3>Donor Management</h3>
                <p>Search and mobilize eligible donors</p>
                <button className="card-btn">Search Donors →</button>
              </div>
              
              <div className="feature-card" title="Multi-hospital support">
                <div className="feature-icon">🏥</div>
                <h3>Multi-Hospital</h3>
                <p>Manage inventory across multiple facilities</p>
                <button className="card-btn disabled">Coming Soon</button>
              </div>
            </div>
          </div>
        )}

        {view === 'dashboard' && <Dashboard onBack={goHome} />}
        {view === 'upload' && <InventoryUpload onBack={goHome} />}
        {view === 'forecast' && <ForecastView onBack={goHome} />}
        {view === 'transfers' && <Transfers onBack={goHome} />}
        {view === 'donors' && <Donors onBack={goHome} />}
      </main>

      <footer className="footer">
        <p>🩸 Smart Blood Bank System - Saving Lives Through Technology</p>
        <p className="footer-links">
          <a href="#" onClick={(e) => { e.preventDefault(); alert('API Docs: http://localhost:8000/docs'); }}>API Docs</a>
          <span>•</span>
          <a href="#" onClick={(e) => { e.preventDefault(); alert('Version 1.0.0'); }}>Version 1.0.0</a>
          <span>•</span>
          <a href="#" onClick={(e) => { e.preventDefault(); setView('home'); }}>Home</a>
        </p>
      </footer>
    </div>
  )
}
