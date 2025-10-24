from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'pedidos',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    group_id='email_service',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("[EMAIL] Aguardando pedidos...")
for mensagem in consumer:
    pedido = mensagem.value
    print(f"[EMAIL] Enviando e-mail para {pedido['usuario']} sobre pedido {pedido['pedido_id']}")
