import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Selecione um arquivo .dmp primeiro!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data.result);
    } catch (err) {
      console.error(err);
      alert("Erro ao enviar o dump!");
    }
  };

  return (
    <div className="p-6 text-center">
      <h1 className="text-2xl font-bold mb-4">🧠 Dump Analyzer</h1>
      <input type="file" accept=".dmp" onChange={(e) => setFile(e.target.files[0])} />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded ml-2"
        onClick={handleUpload}
      >
        Enviar
      </button>

      {result && (
        <pre className="bg-gray-100 text-left mt-4 p-2 rounded">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
