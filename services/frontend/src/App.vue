<template>
  <div id="app">
    <header class="header">
      <img src="image.png" alt="Logo avion" class="logo" />
      <h1 class="title">Flight Radar</h1>
    </header>

    <WebSocketComponent />

    <footer class="footer">
      <p>© 2024 Flight Radar | Construit avec Leaflet et WebSocket</p>
    </footer>
  </div>
</template>

<script>
import WebSocketComponent from "./components/WebSocketComponent.vue";
import "leaflet/dist/leaflet.css";


export default {
  name: "App",
  components: {
    WebSocketComponent,
  },
};
</script>

<style>

* {
    margin: 0;
    padding: 0;
}


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
.footer {
  background-color: #1e2a38;
  color: white;
  text-align: center;
  padding: 10px 0;
  margin-top: auto;
  font-size: 14px;
  position: absolute;
  bottom: 0;
  right: 0;
  left: 0;
}
</style>
