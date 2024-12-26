<template>
  <div id="app">
    <h1>Application Vue.js avec WebSocket</h1>
    <WebSocketComponent />
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
#app {
  text-align: center;
  margin-top: 50px;
}
</style>
