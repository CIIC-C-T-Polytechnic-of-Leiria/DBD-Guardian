<template>
  <div>
    <form @submit.prevent="submitForm">
      <label for="host">Host:</label>
      <input id="host" v-model="host" type="text" />

      <label for="port">Port:</label>
      <input id="port" v-model="port" type="text" />

      <label for="protocol">Protocol:</label>
      <select id="protocol" v-model="protocol">
        <option value="http">http</option>
        <option value="https">https</option>
      </select>

      <button type="submit">Connect</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      host: "",
      port: "",
      protocol: "http",
    };
  },
  methods: {
    submitForm() {
      axios
        .post("http://localhost:5000/connect", {
          host: this.host,
          port: this.port,
          protocol: this.protocol,
        })
        .then((response) => {
          if (response.data.status === "Connection successful") {
            this.$store.commit("setConnection", response.data.connection);
            this.$router.push({ name: "query" });
          } else {
            console.error("Connection failed");
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
