FROM python:3.12-slim

WORKDIR /app

# Dependências básicas para compilar pacotes
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev build-essential curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
