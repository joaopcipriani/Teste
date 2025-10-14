FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base

# Instala Python e ferramentas de build necessárias
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential libffi-dev libssl-dev git && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho da aplicação
WORKDIR /

# Copia requirements primeiro para aproveitar cache do Docker
COPY requirements.txt ./requirements.txt

# Atualiza pip usando a flag --user para evitar problemas de permissão
RUN python3 -m pip install --upgrade --user pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY app/ ./app/

# Ajusta WORKDIR para a pasta onde o main.py está
WORKDIR /app/app

EXPOSE 5000

# Executa a aplicação
CMD ["python3", "main.py"]

