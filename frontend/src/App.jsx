import { useState } from "react"
import axios from "axios"
import UploadPanel from "./components/UploadPanel"
import ResultCard from "./components/ResultCard"
import HeatmapViewer from "./components/HeatmapViewer"

export default function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit() {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const res = await axios.post("http://localhost:8000/predict", formData)
      setResult(res.data)
    } catch (err) {
      setError("Something went wrong. Make sure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-700 text-white py-5 px-6 shadow">
        <h1 className="text-2xl font-bold">🏥 Clinical Triage Assistant</h1>
        <p className="text-blue-200 text-sm mt-1">AI-powered chest X-ray analysis with explainability</p>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8 space-y-6">
        <UploadPanel
          onFileSelect={(f) => { setFile(f); setResult(null); }}
          onSubmit={handleSubmit}
          loading={loading}
          file={file}
        />

        {/* Loading state */}
        {loading && (
          <div className="bg-white rounded-2xl shadow-md p-8 text-center">
            <div className="text-4xl mb-3 animate-pulse">🔬</div>
            <p className="text-gray-600 font-medium">Analyzing X-ray...</p>
            <p className="text-gray-400 text-sm mt-1">Running model inference and generating heatmap</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl">{error}</div>
        )}

        {result && (
          <>
            <ResultCard predictions={result.predictions} triage={result.triage} />
            <HeatmapViewer originalFile={file} heatmap={result.heatmap} />
          </>
        )}
      </main>
    </div>
  )
}