from kafka import KafkaConsumer
import psycopg2
import json
import threading
from generate import generate_coordinates

def get_city_coordinates(city_name, db_config):
    """
    Récupère les coordonnées GPS d'une ville depuis la base de données PostgreSQL.
    
    Args:
        city_name (str): Le nom de la ville.
        db_config (dict): Configuration de la connexion PostgreSQL.

    Returns:
        tuple: (latitude, longitude) si la ville est trouvée, sinon None.
    """
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )
        cur = conn.cursor()

        # Requête pour récupérer les coordonnées
        query = "SELECT latitude, longitude FROM cities WHERE name = %s"
        cur.execute(query, (city_name,))
        result = cur.fetchone()

        # Fermer la connexion
        cur.close()
        conn.close()

        return result  # Retourne un tuple (latitude, longitude)
        
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

def handle_message(message, kafka_servers, db_config):
    """
    Traite un message Kafka et lance la simulation de vol.

    Args:
        message (dict): Message contenant les informations du vol.
        kafka_servers (list): Liste des serveurs Kafka.
        db_config (dict): Configuration de la connexion PostgreSQL.
    """
    plane_id = message["plane_id"]
    city_start = message["city_start"]
    city_end = message["city_end"]

    print(f"Réception des informations pour l'avion {plane_id}: départ {city_start}, arrivée {city_end}")

    # Récupérer les coordonnées des villes depuis la base de données
    start_coords = get_city_coordinates(city_start, db_config)
    end_coords = get_city_coordinates(city_end, db_config)

    if not start_coords or not end_coords:
        print(f"Impossible de démarrer le vol pour {plane_id}. Coordonnées manquantes.")
        return

    # Lancer la simulation de vol
    thread = threading.Thread(
        target=generate_coordinates,
        args=(plane_id, start_coords[0], start_coords[1], end_coords[0], end_coords[1], 900, "gps_raw", kafka_servers)
    )
    thread.start()

def listen_to_kafka(topic, kafka_servers, db_config):
    """
    Écoute un topic Kafka pour recevoir les commandes de vol.

    Args:
        topic (str): Nom du topic Kafka à écouter.
        kafka_servers (list): Liste des serveurs Kafka.
        db_config (dict): Configuration de la connexion PostgreSQL.
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_servers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    print(f"Écoute du topic '{topic}' pour les commandes de vol...")

    for message in consumer:
        handle_message(message.value, kafka_servers, db_config)

if __name__ == "__main__":
    # Configuration Kafka
    kafka_servers = ["192.168.152.97:9094", "192.168.152.97:9092", "192.168.152.97:9096"]
    topic = "test_topic"

    # Configuration PostgreSQL
    db_config = {
        "dbname": "cities_db",
        "user": "user",
        "password": "password",
        "host": "localhost",
        "port": 5432
    }

    # Lancer l'écoute
    listen_to_kafka(topic, kafka_servers, db_config)
