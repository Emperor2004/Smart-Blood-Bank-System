import React from 'react'

interface ErrorDisplayProps {
  error: any
  onRetry?: () => void
}

export default function ErrorDisplay({ error, onRetry }: ErrorDisplayProps) {
  const getErrorMessage = () => {
    if (typeof error === 'string') return error
    if (error?.message) return error.message
    if (error?.detail) return error.detail
    return 'An unexpected error occurred'
  }

  const getErrorDetails = () => {
    if (typeof error === 'object' && error !== null) {
      const details = { ...error }
      delete details.message
      delete details.detail
      if (Object.keys(details).length > 0) {
        return JSON.stringify(details, null, 2)
      }
    }
    return null
  }

  return (
    <div className="error-display">
      <div className="error-icon">⚠️</div>
      <h3 className="error-title">Oops! Something went wrong</h3>
      <p className="error-message">{getErrorMessage()}</p>
      
      {getErrorDetails() && (
        <details className="error-details">
          <summary>Technical Details</summary>
          <pre>{getErrorDetails()}</pre>
        </details>
      )}
      
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          🔄 Try Again
        </button>
      )}
    </div>
  )
}
