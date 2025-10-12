FROM python:3.12-slim

WORKDIR /app

# Dependências básicas do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev build-essential curl \
 && rm -rf /var/lib/apt/lists/*

# Copia e instala pacotes Python
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copia o projeto
COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
