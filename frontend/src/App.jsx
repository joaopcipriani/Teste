import React, { useState } from "react";

export default function App(){
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [status, setStatus] = useState('');
  const [urlContains, setUrlContains] = useState('');
  const [queryResult, setQueryResult] = useState(null);

  const handleUpload = async () => {
    if(!file) return alert('Selecione um arquivo .log');
    const fd = new FormData();
    fd.append('file', file);
    const res = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: fd
    });
    const data = await res.json();
    setUploadResult(data);
  };

  const handleQuery = async () => {
    const params = new URLSearchParams();
    if(start) params.append('start', start);
    if(end) params.append('end', end);
    if(status) params.append('status', status);
    if(urlContains) params.append('url_contains', urlContains);
    const res = await fetch('http://localhost:8000/analyze?' + params.toString());
    const data = await res.json();
    setQueryResult(data);
  };

  return (
    <div style={{maxWidth:900, margin:'24px auto', fontFamily:'Arial, sans-serif', padding:20}}>
      <h1>IIS Log Analyzer</h1>

      <section style={{marginTop:20, padding:12, border:'1px solid #ddd', borderRadius:8}}>
        <h3>Upload de um log (um por vez)</h3>
        <input type="file" accept=".log" onChange={e => setFile(e.target.files[0])} />
        <button onClick={handleUpload} style={{marginLeft:8}}>Enviar</button>

        {uploadResult && (
          <div style={{marginTop:12, background:'#f7f7f7', padding:10, borderRadius:6}}>
            <div><strong>{uploadResult.filename || uploadResult.message}</strong></div>
            <div>Total: {uploadResult.analysis?.total_requests ?? uploadResult.total_requests}</div>
            <div>Avg time: {uploadResult.analysis?.avg_response_time_ms ?? uploadResult.avg_response_time_ms} ms</div>
          </div>
        )}
      </section>

      <section style={{marginTop:20, padding:12, border:'1px solid #ddd', borderRadius:8}}>
        <h3>Filtros e consulta (aplique sobre todos os logs upados)</h3>
        <div style={{display:'flex', gap:8, marginBottom:8}}>
          <input type="date" value={start} onChange={e=>setStart(e.target.value)} />
          <input type="date" value={end} onChange={e=>setEnd(e.target.value)} />
          <input placeholder="status (e.g. 200)" value={status} onChange={e=>setStatus(e.target.value)} />
          <input placeholder="URL contém..." value={urlContains} onChange={e=>setUrlContains(e.target.value)} />
          <button onClick={handleQuery}>Aplicar</button>
        </div>

        {queryResult && (
          <div style={{marginTop:12}}>
            <div><strong>Total Requests:</strong> {queryResult.total_requests}</div>
            <div style={{marginTop:8}}>
              <table style={{width:'100%', borderCollapse:'collapse'}}>
                <thead>
                  <tr style={{background:'#eee'}}>
                    <th style={{border:'1px solid #ddd', padding:6}}>URL</th>
                    <th style={{border:'1px solid #ddd', padding:6}}>Hits</th>
                    <th style={{border:'1px solid #ddd', padding:6}}>Avg time (ms)</th>
                  </tr>
                </thead>
                <tbody>
                  {(queryResult.summary_by_url || []).map((r, i) => (
                    <tr key={i}>
                      <td style={{border:'1px solid #ddd', padding:6}}>{r['cs-uri-stem'] || r['cs-uri-stem']}</td>
                      <td style={{border:'1px solid #ddd', padding:6}}>{r.hits}</td>
                      <td style={{border:'1px solid #ddd', padding:6}}>{Number(r.avg_time_ms).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
