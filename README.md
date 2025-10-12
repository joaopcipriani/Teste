# IIS Log Analyzer (Dockerized)

Estrutura:
- backend: FastAPI que recebe upload de logs IIS, processa com pandas e salva análises em `backend/data/analyses`.
- frontend: Vite + React com UI simples para upload e filtros.
- docker-compose.yml orquestra frontend + backend.

Como rodar (pré-requisitos: Docker + Docker Compose):

1. Construa e suba os containers:
   ```
   docker compose up --build
   ```

2. Acesse:
   - Frontend: http://localhost:3000
   - API backend: http://localhost:8000

Endpoints principais:
- `POST /upload` — upload de 1 arquivo .log (multipart/form-data, campo "file")
- `GET /analyze` — consulta agregada com query params: `start`, `end` (ISO dates), `status` (integer), `url_contains` (string)

Notas:
- Os arquivos upados são salvos em `backend/data/uploads`. As análises por arquivo ficam em `backend/data/analyses`.
- O parser é simples e cobre o formato W3C típico de logs IIS (espaço separado). Dependendo da sua configuração de logs IIS os campos/ordem podem variar — ajuste `backend/main.py` se necessário.

