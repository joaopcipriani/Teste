FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base

# Atualiza lista de pacotes e instala Python + ferramentas de build
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev git build-essential libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia requirements primeiro para aproveitar cache
COPY req.txt ./req.txt

# Instala dependências Python
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r req.txt
RUN python3 -m pip install --upgrade pip setuptools wheel


# Copia restante da aplicação
COPY app/ ./app/

# Ajusta WORKDIR para onde está o main.py
WORKDIR /app/app

EXPOSE 5000

# Executa a aplicação
CMD ["python3", "main.py"]
