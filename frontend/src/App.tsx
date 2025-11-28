import React, { useState } from 'react'
import InventoryUpload from './components/InventoryUpload'
import ForecastView from './components/ForecastView'

export default function App() {
  const [view, setView] = useState<'home' | 'upload' | 'forecast'>('home')

  return (
    <div className="app">
      <header className="header">
        <h1>Smart Blood Bank</h1>
        <nav>
          <button onClick={() => setView('home')}>Home</button>
          <button onClick={() => setView('upload')}>Upload Inventory</button>
          <button onClick={() => setView('forecast')}>Forecast</button>
        </nav>
      </header>

      <main className="main">
        {view === 'home' && (
          <div>
            <h2>Welcome</h2>
            <p>Use the navigation to upload inventory CSVs or view forecasts.</p>
          </div>
        )}

        {view === 'upload' && <InventoryUpload />}
        {view === 'forecast' && <ForecastView />}
      </main>

      <footer className="footer">Smart Blood Bank System</footer>
    </div>
  )
}
