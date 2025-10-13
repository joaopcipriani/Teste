import React, { useState } from 'react'


export default function App() {
const [stack, setStack] = useState('')
const [result, setResult] = useState(null)
const [file, setFile] = useState(null)


async function sendText(e){
e.preventDefault()
const fd = new FormData()
fd.append('stack', stack)
const res = await fetch('http://localhost:8000/analyze/text', { method: 'POST', body: fd })
const j = await res.json()
setResult(j)
}


async function sendFile(e){
e.preventDefault()
if(!file) return alert('Selecione um arquivo')
const fd = new FormData()
fd.append('dump', file)
const res = await fetch('http://localhost:8000/analyze/file', { method: 'POST', body: fd })
const j = await res.json()
setResult(j)
}


return (
<div style={{ padding: 24, fontFamily: 'Arial, sans-serif' }}>
<h1>Stack Translator</h1>
<form onSubmit={sendText}>
<textarea rows={12} style={{ width: '100%' }} value={stack} onChange={e=>setStack(e.target.value)} placeholder="Cole o stack trace aqui..." />
<div style={{ marginTop: 8 }}>
<button type="submit">Analisar texto</button>
</div>
</form>


<hr style={{ margin: '20px 0' }} />


<form onSubmit={sendFile}>
<input type="file" onChange={e=>setFile(e.target.files[0])} />
<button type="submit">Enviar minidump</button>
</form>


<pre style={{ background: '#f7f7f7', padding: 12, marginTop: 20 }}>{JSON.stringify(result, null, 2)}</pre>
</div>
)
}
