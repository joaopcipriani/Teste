FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base

# Instala Python e ferramentas de build
RUN apt-get install -y python3 python3-pip git build-essential libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /

# Copia requirements antes do app para aproveitar cache
COPY req.txt ./req.txt

RUN pip3 install
RUN pip3 install --no-cache-dir -r req.txt

# Copia o restante da aplicação
COPY app/ ./app/

WORKDIR /app/app

EXPOSE 5000
CMD ["python3", "main.py"]
