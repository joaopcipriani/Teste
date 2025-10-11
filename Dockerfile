FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Adiciona log pra sabermos o que falha
RUN echo "Instalando dependências..." && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
