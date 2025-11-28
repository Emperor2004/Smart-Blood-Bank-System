import React, { useState } from 'react'
import { apiUploadInventory } from '../services/api'

export default function InventoryUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(null)
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const onUpload = async () => {
    if (!file) {
      setMessage('Please choose a CSV file')
      return
    }

    setLoading(true)
    try {
      const form = new FormData()
      form.append('file', file)

      const res = await apiUploadInventory(form)
      setMessage(JSON.stringify(res, null, 2))
    } catch (err: any) {
      setMessage(`Upload failed: ${err?.message || err}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Upload Inventory CSV</h2>
      <input type="file" accept=".csv" onChange={onFileChange} />
      <div style={{ marginTop: 8 }}>
        <button onClick={onUpload} disabled={loading}>Upload</button>
      </div>

      {message && (
        <pre style={{ whiteSpace: 'pre-wrap', marginTop: 12 }}>{message}</pre>
      )}
    </div>
  )
}
