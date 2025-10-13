FROM python:3.11-slim

WORKDIR /app

# Copia apenas o requirements primeiro para cache de dependências
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do backend
COPY backend/app /app

EXPOSE 8000

# Comando para rodar o FastAPI via Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
