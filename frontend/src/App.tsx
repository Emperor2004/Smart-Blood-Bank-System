import React, { useState } from 'react'
import InventoryUpload from './components/InventoryUpload'
import ForecastView from './components/ForecastView'

export default function App() {
  const [view, setView] = useState<'home' | 'upload' | 'forecast'>('home')

  return (
    <div className="app">
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
