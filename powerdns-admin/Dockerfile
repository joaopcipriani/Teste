FROM powerdnsadmin/pda-legacy:latest

USER root

# Atualiza repositórios e instala pip se necessário
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install pymysql && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER 1000
