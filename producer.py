from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

pedido_id = 1
while True:
    pedido = {
        "pedido_id": pedido_id,
        "usuario": f"usuario{pedido_id}@exemplo.com",
        "itens": [
            {"produto_id": 1, "quantidade": random.randint(1,5)},
            {"produto_id": 2, "quantidade": random.randint(1,3)}
        ]
    }
    producer.send('pedidos', pedido)
    print(f"[PRODUCER] Pedido enviado: {pedido}")
    pedido_id += 1
    time.sleep(3)
