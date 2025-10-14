FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y build-essential libmysqlclient-dev default-libmysqlclient-dev curl git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala PowerDNS-Admin
WORKDIR /app
RUN git clone https://github.com/ngoduykhanh/PowerDNS-Admin.git . && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install pymysql

ENV FLASK_APP=run.py

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "run:app"]
