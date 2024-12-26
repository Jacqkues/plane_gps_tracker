<template>
  <div>
    <h1>Carte avec Leaflet et WebSocket</h1>
    <p v-if="!isConnected" class="error">Tentative de connexion au serveur...</p>
    <div id="map" style="height: 700px; width: 700px; transition: all 0.3s ease;"></div>
  </div>
</template>

<script>
import L from "leaflet";

export default {
  data() {
    return {
      websocket: null, // Instance WebSocket
      map: null, // Instance de la carte Leaflet
      isConnected: false, // État de la connexion WebSocket
      planes: {}, // Données des avions (marqueurs, polylignes, coordonnées)
      colorMap: {}, // Stocke les couleurs uniques pour chaque avion
      emojiMap: {}, // Stocke les emojis uniques pour chaque avion
      emojis: ["✈️", "🛩️", "🚀", "🛸", "🛬", "🛫", "🦅"], // Liste des emojis disponibles
    };
  },
  methods: {
    // Méthode pour établir la connexion WebSocket
    connectWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8000/ws");

      // Gestion de l'événement : connexion établie
      this.websocket.onopen = () => {
        console.log("WebSocket connecté !");
        this.isConnected = true;
      };

      // Gestion de l'événement : réception de message
      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data); // Un seul message d'avion
        console.log("Coordonnées reçues :", data);
        //si on recoit des coordonnées
      
          // Identifier l'avion par `plane_id` ou `device_id`
          const plane_id = data.plane_id || data.device_id;
          const { latitude, longitude } = data;

          // Si l'avion n'existe pas encore dans le système, initialiser ses données
          if (!this.planes[plane_id]) {
            // Générer une couleur unique pour l'avion
            const randomColor = this.getRandomColor();

            // Attribuer un emoji unique
            const randomEmoji = this.getRandomEmoji();

            // Stocker les informations de l'avion
            this.colorMap[plane_id] = randomColor;
            this.emojiMap[plane_id] = randomEmoji;

            this.planes[plane_id] = {
              marker: null,
              polyline: null,
              coordinates: [],
              icon: L.divIcon({
                className: "plane-marker",
                html: `<div style="font-size: 24px;">${randomEmoji}</div>`,
                iconSize: [24, 24],
                iconAnchor: [12, 12],
              }),
              color: randomColor, // Couleur unique
            };
          }

          const plane = this.planes[plane_id];

          // Ajouter la nouvelle coordonnée à la liste
          plane.coordinates.push([latitude, longitude]);

          // Mettre à jour ou créer la polyline pour cet avion
          if (plane.polyline) {
            plane.polyline.setLatLngs(plane.coordinates);
          } else {
            plane.polyline = L.polyline(plane.coordinates, { color: plane.color }).addTo(this.map);
          }

          // Mettre à jour ou créer le marqueur pour cet avion
          if (plane.marker) {
            plane.marker.setLatLng([latitude, longitude]);
          } else {
            plane.marker = L.marker([latitude, longitude], { icon: plane.icon }).addTo(this.map);
          }

          // Centrer la carte uniquement sur le premier point
          if (plane.coordinates.length === 1) {
            this.map.setView([latitude, longitude], 6);
          }

      };

      // Gestion de l'événement : fermeture
      this.websocket.onclose = () => {
        console.error("WebSocket fermé, tentative de reconnexion...");
        this.isConnected = false;
        setTimeout(this.connectWebSocket, 3000); // Reconnexion après 3 secondes
      };

      // Gestion de l'événement : erreur
      this.websocket.onerror = (error) => {
        console.error("Erreur WebSocket :", error);
      };
    },

    // Génère une couleur aléatoire
    getRandomColor() {
      const letters = "0123456789ABCDEF";
      let color = "#";
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },

    // Génère un emoji aléatoire
    getRandomEmoji() {
      const index = Math.floor(Math.random() * this.emojis.length);
      return this.emojis[index];
    },

    // Initialisation de la carte Leaflet
    initializeMap() {
      this.map = L.map("map").setView([48.8566, 2.3522], 6); // Carte centrée sur Paris
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);
    },
  },
  mounted() {
    // Initialisation de la carte
    this.initializeMap();

    // Connexion au WebSocket
    this.connectWebSocket();
  },
};
</script>

<style scoped>
.error {
  color: red;
  font-weight: bold;
}

#map {
  margin-top: 20px;
  margin-left: 30%;
}
</style>
