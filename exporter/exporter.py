import os
from pymongo import MongoClient
from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep

# Configurações
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/pritunl")
INFLUX_HOST = os.getenv("INFLUX_HOST", "influxdb")
INFLUX_PORT = int(os.getenv("INFLUX_PORT", 8086))
INFLUX_DB = os.getenv("INFLUX_DB", "pritunl_metrics")
INTERVAL = int(os.getenv("INTERVAL", 60))  # segundos

# Conexões
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_database()
influx_client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
influx_client.switch_database(INFLUX_DB)

def process_auth_logs():
    logs_collection = db['logs']
    logs = list(logs_collection.find({}))
    metrics = {}

    for entry in logs:
        ts = entry.get('timestamp')
        user = entry.get('user_name', 'unknown')
        ip = entry.get('host_address', 'unknown')
        if not ts:
            continue
        dt = datetime.fromisoformat(ts)
        hour = dt.strftime('%Y-%m-%dT%H:00:00')
        key_user = (hour, user)
        key_ip = (hour, ip)

        metrics.setdefault('auth_user', {})
        metrics.setdefault('auth_ip', {})

        metrics['auth_user'][key_user] = metrics['auth_user'].get(key_user, 0) + 1
        metrics['auth_ip'][key_ip] = metrics['auth_ip'].get(key_ip, 0) + 1

    points = []
    for (hour, user), count in metrics['auth_user'].items():
        points.append({
            "measurement": "auth_attempts_user",
            "tags": {"user": user},
            "time": hour,
            "fields": {"count": count}
        })

    for (hour, ip), count in metrics['auth_ip'].items():
        points.append({
            "measurement": "auth_attempts_ip",
            "tags": {"ip": ip},
            "time": hour,
            "fields": {"count": count}
        })

    if points:
        influx_client.write_points(points)
        print(f"[INFO] Enviadas {len(points)} métricas para InfluxDB")

def process_server_usage():
    usage_collection = db['servers_bandwidth']
    usage = list(usage_collection.find({}))
    points = []

    for entry in usage:
        ts = entry.get('timestamp')
        server = entry.get('server_name', 'unknown')
        bytes_sent = entry.get('bytes_sent', 0)
        bytes_recv = entry.get('bytes_recv', 0)
        if not ts:
            continue
        dt = datetime.fromisoformat(ts)
        hour = dt.strftime('%Y-%m-%dT%H:00:00')

        points.append({
            "measurement": "server_bandwidth",
            "tags": {"server": server},
            "time": hour,
            "fields": {"bytes_sent": bytes_sent, "bytes_recv": bytes_recv}
        })

    if points:
        influx_client.write_points(points)
        print(f"[INFO] Enviadas {len(points)} métricas de tráfego para InfluxDB")

# Loop principal
while True:
    process_auth_logs()
    process_server_usage()
    sleep(INTERVAL)
