<template>
  <div class="page-container">
    <header class="header">
      <img src="image.png" alt="Logo avion" class="logo" />
      <h1 class="title">Flight Radar</h1>
    </header>

    <main>
      <div>
        <p v-if="!isConnected" class="error">Tentative de connexion au serveur...</p>
        <div id="map" class="map"></div>
      </div>
    </main>

    <footer class="footer">
      <p>© 2024 Flight Radar | Construit avec Leaflet et WebSocket</p>
    </footer>
  </div>
</template>

<script>
import L from "leaflet";

export default {
  data() {
    return {
      websocket: null,
      map: null,
      isConnected: false,
      planes: {},
      colorMap: {},
      emojiMap: {},
      emojis: ["✈️", "🛩️", "🚀", "🛸", "🛬", "🛫", "🦅"],
    };
  },
  methods: {
    connectWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8000/ws");

      this.websocket.onopen = () => {
        console.log("WebSocket connecté !");
        this.isConnected = true;
      };

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const plane_id = data.plane_id || data.device_id;
        const { latitude, longitude } = data;

        if (!this.planes[plane_id]) {
          const randomColor = this.getRandomColor();
          const randomEmoji = this.getRandomEmoji();

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
            color: randomColor,
          };
        }

        const plane = this.planes[plane_id];
        plane.coordinates.push([latitude, longitude]);

        if (plane.polyline) {
          plane.polyline.setLatLngs(plane.coordinates);
        } else {
          plane.polyline = L.polyline(plane.coordinates, { color: plane.color }).addTo(this.map);
        }

        if (plane.marker) {
          plane.marker.setLatLng([latitude, longitude]);
        } else {
          plane.marker = L.marker([latitude, longitude], { icon: plane.icon }).addTo(this.map);
        }

        if (plane.coordinates.length === 1) {
          this.map.setView([latitude, longitude], 6);
        }
      };

      this.websocket.onclose = () => {
        console.error("WebSocket fermé, tentative de reconnexion...");
        this.isConnected = false;
        setTimeout(this.connectWebSocket, 3000);
      };

      this.websocket.onerror = (error) => {
        console.error("Erreur WebSocket :", error);
      };
    },
    getRandomColor() {
      const letters = "0123456789ABCDEF";
      let color = "#";
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    getRandomEmoji() {
      const index = Math.floor(Math.random() * this.emojis.length);
      return this.emojis[index];
    },
    initializeMap() {
      this.map = L.map("map").setView([48.8566, 2.3522], 6);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);
    },
  },
  mounted() {
    this.initializeMap();
    this.connectWebSocket();
  },
};
</script>

<style scoped>
/* Global Page Style */
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

/* Header */
.header {
  background-color: #1e2a38;
  color: white;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.logo {
  height: 50px;
}

.title {
  font-size: 24px;
  margin: 0;
}

/* Map Section */
.map {
  height: 700px;
  width: 80%;
  margin: 20px auto;
  border: 2px solid #ccc;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.error {
  color: red;
  text-align: center;
  margin: 10px 0;
}

/* Footer */
.footer {
  background-color: #1e2a38;
  color: white;
  text-align: center;
  padding: 10px 0;
  margin-top: auto;
  font-size: 14px;
}
</style>
