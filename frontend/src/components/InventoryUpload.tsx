import React, { useState, useRef } from 'react'
import { apiUploadInventory } from '../services/api'
import ErrorDisplay from './ErrorDisplay'

export default function InventoryUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.csv')) {
        setFile(droppedFile)
        setResult(null)
        setError(null)
      } else {
        setError('Please upload a CSV file')
      }
    }
  }

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setResult(null)
    setError(null)
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const onUpload = async () => {
    if (!file) {
      setError('Please choose a CSV file')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await apiUploadInventory(form)
      setResult(res)
      if (res.success) {
        setFile(null)
        if (fileInputRef.current) fileInputRef.current.value = ''
      }
    } catch (err: any) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRetry = () => {
    setError(null)
    setResult(null)
    if (file) {
      onUpload()
    }
  }

  return (
    <div className="card">
      <h2>📤 Upload Inventory</h2>
      <p style={{ color: '#718096', marginBottom: '2rem' }}>
        Upload CSV file with blood inventory data
      </p>
      
      <div 
        className={`upload-area ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="upload-icon">📁</div>
        <div className="upload-text">
          {file ? `✓ ${file.name}` : 'Drag & drop CSV file here'}
        </div>
        <div className="upload-hint">
          {file ? 'Click to change file' : 'or click to browse'}
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={onFileChange}
          className="file-input"
        />
      </div>

      <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
        <button 
          className="btn btn-primary" 
          onClick={onUpload} 
          disabled={loading || !file}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Uploading...
            </>
          ) : (
            <>
              ⬆️ Upload Inventory
            </>
          )}
        </button>
      </div>

      {error && <ErrorDisplay error={error} onRetry={handleRetry} />}

      {result && result.success && (
        <div className="success-display">
          <div className="success-icon">✅</div>
          <h3 className="success-title">Upload Successful!</h3>
          <p className="success-message">{result.message}</p>
          
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{result.success_count || 0}</div>
              <div className="stat-label">✓ Success</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{result.error_count || 0}</div>
              <div className="stat-label">✗ Errors</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{result.duplicates?.length || 0}</div>
              <div className="stat-label">⚠ Duplicates</div>
            </div>
          </div>

          {result.errors && result.errors.length > 0 && (
            <details className="error-details" style={{ marginTop: '1rem' }}>
              <summary>View Errors ({result.errors.length})</summary>
              <pre>{JSON.stringify(result.errors, null, 2)}</pre>
            </details>
          )}
        </div>
      )}

      {result && !result.success && (
        <ErrorDisplay error={result} onRetry={handleRetry} />
      )}
    </div>
  )
}
