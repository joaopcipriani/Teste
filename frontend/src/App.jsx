import { useState } from 'react'
import axios from 'axios'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    if (!file) return alert("Selecione um arquivo .dmp")
    setLoading(true)
    const formData = new FormData()
    formData.append("file", file)
    try {
      const res = await axios.post("http://192.168.31.134:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      setResult(res.data.result)
    } catch (err) {
      alert("Erro ao analisar o dump: " + err)
    }
    setLoading(false)
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>🧠 Dump Analyzer</h1>
      <input type="file" accept=".dmp" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analisando..." : "Enviar"}
      </button>
      {result && (
        <pre style={{ marginTop: '2rem', background: '#eee', padding: '1rem' }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  )
}

export default App
