<template>
  <div id="app">
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
