import time
import random
import math
import json
from kafka import KafkaProducer

def haversine(lat1, lon1, lat2, lon2):
    """Calcule la distance en km entre deux coordonnées GPS (utilise la formule de Haversine)."""
    R = 6371  # Rayon de la Terre en kilomètres
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Retourne la distance en kilomètres

def move_towards(lat1, lon1, lat2, lon2, distance_to_travel):
    """
    Calcule les nouvelles coordonnées après avoir avancé d'une certaine distance en ligne droite.
    """
    total_distance = haversine(lat1, lon1, lat2, lon2)
    if total_distance == 0 or distance_to_travel >= total_distance:
        return lat2, lon2  # Arrivé ou distance restante parcourue
    
    ratio = distance_to_travel / total_distance
    new_lat = lat1 + (lat2 - lat1) * ratio
    new_lon = lon1 + (lon2 - lon1) * ratio
    return new_lat, new_lon

def generate_coordinates(device_id, start_lat, start_lon, end_lat, end_lon, speed_kmh, kafka_topic, kafka_servers):
    """
    Génère des coordonnées GPS pour simuler un déplacement d'un point de départ à un point d'arrivée,
    avec une vitesse donnée (en km/h) comme un trajet d'avion.
    """
    # Configurer Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=kafka_servers,
        key_serializer=lambda k: k.encode() if isinstance(k, str) else k,
        value_serializer=lambda v: json.dumps(v).encode() if isinstance(v, dict) else v
    )

    # Initialisation
    current_lat, current_lon = start_lat, start_lon
    remaining_distance = haversine(current_lat, current_lon, end_lat, end_lon)
    time_interval = 0.1  # Intervalle de mise à jour en secondes
    speed_per_second = speed_kmh / 3600  # Vitesse initiale en km/s

    print(f"[{device_id}] Simulation commencée : départ {start_lat, start_lon}, arrivée {end_lat, end_lon}")
    while remaining_distance > 0.001:  # Arrêt lorsque la distance restante est négligeable
        # Appliquer une variation à la vitesse
        speed_kmh += random.uniform(-100, 100)  # Variation de ±100 km/h
        speed_kmh = max(500, min(1000, speed_kmh))  # Limiter la vitesse entre 500 et 1000 km/h
        speed_per_second = speed_kmh / 3600  # Recalculer la vitesse en km/s

        # Calculer la distance à parcourir dans cet intervalle de temps
        distance_to_travel = speed_per_second * time_interval

        # Mettre à jour la position
        current_lat, current_lon = move_towards(current_lat, current_lon, end_lat, end_lon, distance_to_travel)

        # Recalculer la distance restante
        remaining_distance = haversine(current_lat, current_lon, end_lat, end_lon)

        # Créer les coordonnées actuelles
        coord = {
            "plane_id": device_id,
            "latitude": round(current_lat, 6),
            "longitude": round(current_lon, 6),
            "speed_kmh": round(speed_kmh, 2),  # Ajouter la vitesse actuelle
            # "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Envoyer les coordonnées à Kafka
        producer.send(kafka_topic, key=device_id, value=coord)

        # Afficher les données générées
        print(f"[{device_id}] Coordonnées générées : {coord}")

        # Pause avant la mise à jour suivante
        time.sleep(time_interval)

    # Lorsque l'appareil arrive à destination, on le marque comme arrivé
    print(f"[{device_id}] Arrivé au point final.")
