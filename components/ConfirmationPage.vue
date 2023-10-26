<template>
  <div class="container">
    <div class="card-container">
      <div v-for="(host, index) in hosts" :key="index">
        <HostCard :host="host" />
      </div>
    </div>
    <NormalButton class="normal-button" @click="downloadConfiguration">Confirm</NormalButton>
  </div>
</template>

<script>
import HostCard from "./HostCard.vue";
import NormalButton from "./NormalButton.vue";
export default {
  name: "ConfirmationPage",
  components: { HostCard, NormalButton },
  computed: {
    hosts() {
      return this.$store.state.hosts;
    },
  },
  methods: {
    downloadConfiguration() {
      // Convert the hosts data to a JSON string
      const jsonString = JSON.stringify(this.$store.state.hosts, null, 2);

      // Create a Blob from the JSON string
      const blob = new Blob([jsonString], { type: "application/json" });

      // Create a link element
      const link = document.createElement("a");

      // Set the link's href to point to the Blob
      link.href = URL.createObjectURL(blob);

      // Set the download attribute to specify the filename
      link.download = "configuration.json";

      // Append the link to the body
      document.body.appendChild(link);

      // Simulate a click on the link
      link.click();

      // Remove the link from the body
      document.body.removeChild(link);
    },
  },
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: 0 auto;
}


.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 20px;
}
.card-container > * {
  flex: 1 0 calc(50% - 20px); /* Adjust this value to change the number of cards per row */
  margin: 10px; /* Adjust this value to change the space between cards */
}

.normal-button {
  display: block;
  margin: 20px auto 50px;
}
</style>
