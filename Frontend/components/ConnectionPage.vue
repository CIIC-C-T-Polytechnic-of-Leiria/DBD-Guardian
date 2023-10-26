<template>
  <div class="container">
    <div class="banner" v-if="!isDataLoaded">Connecting...</div>
    <div class="card-container" v-else>
      <StatusCard
        v-for="host in statuses"
        :key="host.identifier"
        :host="host"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import StatusCard from "./StatusCard.vue";

export default {
  name: "ConnectionPage",
  components: {
    StatusCard,
  },
  data() {
    return {
      statuses: {},
      isDataLoaded: false,
    };
  },
  created() {
    this.checkStatus();
    setInterval(this.checkStatus, 30000); 
  },
  methods: {
    checkStatus() {
      axios
        .get("http://localhost:5000/connectstatus")
        .then((response) => {
          const data = response.data;
          this.statuses = Object.keys(data).map((identifier) => ({
            identifier,
            status: data[identifier].status,
            datasources: Object.keys(data[identifier].datasources).map(
              (name) => ({
                name,
                status: data[identifier].datasources[name],
              })
            ),
          }));
          this.isDataLoaded = true;
        })
        .catch((error) => {
          console.error(error);
          this.statuses = [];
          this.isDataLoaded = true;
        });
    },
  },
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: 20px auto;
  padding: 20px;
}

.banner {
  text-align: center;
  padding: 15px 0;
  font-size: 26px;
  font-weight: 500;
  color: #fff;
  background: linear-gradient(45deg, #3f51b5, #9c27b0);
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* Centers the cards */
}

.card-container > * {
  flex: 1 0 calc(33.333% - 10px);  /* Adjusted for 3 cards per row */
  margin: 10px 5px;  /* Reduced horizontal margin for lesser space between cards */
  max-width: calc(33.333% - 10px); /* Ensure the width does not exceed the specified value */
}
</style>