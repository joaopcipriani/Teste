FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base

# Instala Python e git
RUN apt-get update && apt-get install -y python3 python3-pip git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia arquivos
COPY app/ ./app/
COPY requirements.txt ./requirements.txt

# Instala dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app/app

EXPOSE 5000
CMD ["python3", "main.py"]
