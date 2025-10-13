"""
Módulo simples de análise.


No MVP ele faz parsing básico de stacks textuais (detecção de linhas com endereços hex e heurística
para linguagem .NET / C# / Java / C++). Para minidumps, adicionamos placeholder que deve ser
substituído por integração com 'symbolic', 'minidump-stackwalk', 'llvm-symbolizer' ou serviço externo.
"""
import re
from typing import List


HEX_ADDR = re.compile(r"0x[0-9a-fA-F]{4,}")




def analyze_stack_text(text: str) -> dict:
lines = text.splitlines()
parsed = []
for i, ln in enumerate(lines, 1):
addr = HEX_ADDR.search(ln)
parsed.append({
"line_no": i,
"raw": ln,
"has_hex": bool(addr),
"hex": addr.group(0) if addr else None,
"note": _classify_line(ln)
})
summary = {
"lines": parsed,
"counts": {"total": len(lines), "with_hex": sum(1 for p in parsed if p['has_hex'])}
}
return summary




def _classify_line(ln: str) -> str:
ln_l = ln.lower()
if 'exception' in ln_l or 'error' in ln_l:
return 'error-line'
if 'at ' in ln_l and '(' in ln_l:
return 'stackframe'
return 'other'




def analyze_minidump(content: bytes) -> dict:
# Placeholder: aqui você pode integrar com python package 'symbolic' ou chamar um binário
# como 'minidump_stackwalk' via subprocess, salvando o binário temporariamente.
# Por enquanto retornamos tamanho e sugestão de próximos passos.
return {
"note": "minidump received (analysis placeholder)",
"size_bytes": len(content),
"suggested_actions": [
"Instalar e integrar 'symbolic' (Sentry) ou 'minidump-stackwalk'",
"Configurar repositório de símbolos (PDB/sym) para resolvers",
"Executar arquitetura de symbolicator se precisar de traduções massivas"
]
}
