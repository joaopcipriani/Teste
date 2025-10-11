async function listFiles() {
  const res = await fetch('/files_json');
  const files = await res.json();

  const container = document.getElementById('files');
  container.innerHTML = '';

  if (!files.length) {
    container.innerHTML = '<p>Nenhum arquivo enviado.</p>';
    return;
  }

  files.forEach(f => {
    const div = document.createElement('div');
    div.className = 'file-row';

    const info = document.createElement('div');
    info.className = 'file-info';
    info.innerHTML = `
      <strong>${f.name}</strong>
      <small>Tamanho: ${(f.size / 1024).toFixed(2)} KB</small>
      <small>Criado: ${new Date(f.ctime*1000).toLocaleString()}</small>
      <small>Modificado: ${new Date(f.mtime*1000).toLocaleString()}</small>
    `;

    const actions = document.createElement('div');
    actions.className = 'file-actions';

    const download = document.createElement('a');
    download.href = '/download/' + encodeURIComponent(f.name);
    download.textContent = 'Download';
    download.setAttribute('download', '');

    const delBtn = document.createElement('button');
    delBtn.textContent = 'Apagar';
    delBtn.className = 'delete';
    delBtn.onclick = async () => {
      if (!confirm(`Apagar ${f.name}?`)) return;
      const r = await fetch('/delete/' + encodeURIComponent(f.name), { method: 'DELETE' });
      if (r.ok) listFiles(); else alert('Erro ao apagar');
    };

    actions.appendChild(download);
    actions.appendChild(delBtn);

    div.appendChild(info);
    div.appendChild(actions);
    container.appendChild(div);
  });
}

document.getElementById('uploadForm').addEventListener('submit', async e => {
  e.preventDefault();
  const input = document.getElementById('fileInput');
  if (!input.files.length) return alert('Escolha um arquivo');

  const fd = new FormData();
  fd.append('file', input.files[0]);

  const res = await fetch('/upload', { method: 'POST', body: fd });
  if (res.ok) {
    alert('Arquivo enviado com sucesso!');
    input.value = '';
    listFiles();
  } else {
    const txt = await res.text();
    alert('Erro: ' + txt);
  }
});

listFiles();
