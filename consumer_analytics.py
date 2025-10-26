from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'pedidos',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    group_id='analytics_service',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("[ANALYTICS] Aguardando pedidos...")
for mensagem in consumer:
    pedido = mensagem.value
    print(f"[ANALYTICS] Registrando dados do pedido {pedido['pedido_id']}")
