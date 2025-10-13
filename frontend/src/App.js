import { useState } from "react";

function App() {
  const [stack, setStack] = useState("");
  const [result, setResult] = useState([]);

  const handleTranslate = async () => {
    const addresses = stack.split("\n").map(line => line.trim()).filter(Boolean);
    const res = await fetch("http://backend:5000/translate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ stack: addresses })
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Symbolic Translator (Linux-friendly)</h1>
      <textarea
        rows={10}
        cols={50}
        value={stack}
        onChange={e => setStack(e.target.value)}
        placeholder="Cole o stack trace aqui"
      />
      <br />
      <button onClick={handleTranslate}>Traduzir</button>
      <pre>{result.join("\n")}</pre>
    </div>
  );
}

export default App;
