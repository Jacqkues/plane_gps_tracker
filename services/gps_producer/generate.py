import time
import random
import math
import threading
import json
from kafka import KafkaProducer
import argparse

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

def generate_coordinates(device_id, start_lat, start_lon, end_lat, end_lon, speed_kmh):
    """
    Génère des coordonnées GPS pour simuler un déplacement d'un point de départ à un point d'arrivée,
    avec une vitesse donnée (en km/h) comme un trajet d'avion.
    """
    # Initialisation
    current_lat, current_lon = start_lat, start_lon
    remaining_distance = haversine(current_lat, current_lon, end_lat, end_lon)
    time_interval = 0.1  # Intervalle de mise à jour en secondes
    speed_per_second = speed_kmh / 3600  # Vitesse initiale en km/s

    while remaining_distance > 0.001:  # Arrêt lorsque la distance restante est négligeable
        # Appliquer une variation à la vitesse
        speed_kmh += random.uniform(-100, 100)  # Variation de ±10 km/h
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
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Afficher les coordonnées générées
        print(f"[{device_id}] Coordonnées générées : {coord}")

        # Envoyer à Kafka
        producer.send("gps_raw", key=device_id.encode(), value=json.dumps(coord).encode())

        # Pause avant la mise à jour suivante
        time.sleep(time_interval)

    # Lorsque l'appareil arrive à destination, on le marque comme arrivé
    print(f"[{device_id}] Arrivé au point final.")

if __name__ == "__main__":
    # Configurer argparse pour gérer les arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Simuler un trajet GPS pour un avion.")
    parser.add_argument("--plane_id", type=str, required=True, help="Identifiant de l'avion (plane ID).")
    # parser.add_argument("--plane_start", type=str, required=True, help="Coordonnées de départ (latitude,longitude).")
    parser.add_argument("--plane_end", type=str, required=True, help="Coordonnées d'arrivée (latitude,longitude).")

    args = parser.parse_args()

    # Récupérer les coordonnées de départ et d'arrivée
    try:
        # plane_start = tuple(map(float, args.plane_start.split(",")))  # Convertir en tuple de floats
        plane_end = tuple(map(float, args.plane_end.split(",")))
    except ValueError:
        print("Erreur : Les coordonnées doivent être fournies au format 'latitude,longitude' (ex : 48.8566,2.3522).")
        exit(1)

    plane_start = (48.8566, 2.352)
    
    # Configurer Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=["10.227.211.97:9094", "10.227.211.97:9092", "10.227.211.97:9096"],
        key_serializer=lambda k: k.encode() if isinstance(k, str) else k,
        value_serializer=lambda v: json.dumps(v).encode() if isinstance(v, dict) else v
    )
    msg = {
        "plane_id":args.plane_id,
        "message" : f"start from {plane_end}",
        "timestamp" : time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # Créer un thread pour l'appareil
    thread = threading.Thread(
        target=generate_coordinates,
        args=(args.plane_id, plane_start[0], plane_start[1], plane_end[0], plane_end[1], 900)
    )
    thread.start()

    # Attendre que le thread termine
    thread.join()