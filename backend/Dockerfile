FROM python:3.12-slim

# Evita perguntas interativas do apt
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala dependências de compilação (necessárias para pdbparse, minidump)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
