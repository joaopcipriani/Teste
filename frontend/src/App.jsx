import { useState } from "react";

export default function App() {
  const [result, setResult] = useState(null);

  async function handleUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://backend:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  }

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>Windows Dump Analyzer</h1>
      <input type="file" onChange={handleUpload} />
      {result && (
        <pre
          style={{
            background: "#f3f3f3",
            padding: 10,
            marginTop: 20,
            borderRadius: 8,
            overflowX: "auto",
          }}
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
