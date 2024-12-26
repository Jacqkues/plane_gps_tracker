from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from aiokafka import AIOKafkaConsumer
import json
import os

websocket_router = APIRouter()

# Environment variables
BROKER_IP = os.getenv("BROKER_IP", "127.0.0.1")

KAFKA_BROKERS = [f'{BROKER_IP}:9092', f'{BROKER_IP}:9094', f'{BROKER_IP}:9096']


async def consume_kafka_messages(websocket: WebSocket, topic: str):
    """
    Consomme les messages Kafka pour un topic, les enregistre dans PostgreSQL,
    et les transmet via WebSocket.

    Args:
    - websocket (WebSocket): Connexion WebSocket pour envoyer les coordonnées.
    - topic (str): Le topic Kafka à écouter.
    """
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKERS,
        group_id='gps-group',
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # Décoder le message Kafka
            message = json.loads(msg.value.decode('utf-8'))
            print("Message reçu de Kafka : ", message)
            # Envoyer le message via WebSocket
            await websocket.send_json(message)
            print(f"Message envoyé au WebSocket : {message}")
    finally:
        await consumer.stop()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket connecté")
    await websocket.accept()

    try:
        # Le topic Kafka à écouter
        topic = "gps_raw"
        # Lancer le consommateur Kafka et envoyer les données au client WebSocket
        await consume_kafka_messages(websocket, topic)
    except WebSocketDisconnect:
        print("Le client WebSocket s'est déconnecté.")
    except Exception as e:
        print(f"Erreur WebSocket ou Kafka : {e}")
    finally:
        print("Connexion WebSocket fermée")

        