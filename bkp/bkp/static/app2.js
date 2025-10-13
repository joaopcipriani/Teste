async function listFiles(){
  const res = await fetch('/files');
  const files = await res.json();
  const container = document.getElementById('files');
  container.innerHTML = '';
  if(!files.length){ container.innerHTML = '<p>(vazio)</p>'; return; }

  files.forEach(f => {
    const div = document.createElement('div');
    div.className = 'file-row';

    const name = document.createElement('div'); name.textContent = f.name;
    const size = document.createElement('div'); size.textContent = (f.size/1024).toFixed(1)+' KB';
    const mtime = document.createElement('div'); mtime.textContent = new Date(f.mtime*1000).toLocaleString();

    const dl = document.createElement('a'); dl.href='/download/'+encodeURIComponent(f.name); dl.textContent='Download'; dl.setAttribute('download','');

    const delBtn = document.createElement('button'); delBtn.textContent='Apagar';
    delBtn.onclick = async ()=>{
      if(!confirm('Apagar '+f.name+'?')) return;
      const r = await fetch('/delete/'+encodeURIComponent(f.name), {method:'DELETE'});
      if(r.ok) listFiles(); else alert('Erro ao apagar');
    };

    div.appendChild(name); div.appendChild(size); div.appendChild(mtime); div.appendChild(dl); div.appendChild(delBtn);
    container.appendChild(div);
  });
}

document.getElementById('uploadForm').addEventListener('submit', async e=>{
  e.preventDefault();
  const input = document.getElementById('fileInput');
  if(!input.files.length) return alert('Escolha um arquivo');
  const fd = new FormData();
  fd.append('file', input.files[0]);
  const res = await fetch('/upload', {method:'POST', body:fd});
  if(res.ok){ alert('Enviado'); input.value=''; listFiles(); }
  else { const txt = await res.text(); alert('Erro: '+txt); }
});

listFiles();
