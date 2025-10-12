FROM python:3.12-slim

WORKDIR /app

# Copia e instala dependências
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO o conteúdo da pasta app (incluindo static/)
COPY app/ .

# Confirma se o arquivo existe (útil para debug)
RUN ls -R /app/static || echo "❌ Pasta static não encontrada durante o build!"

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
