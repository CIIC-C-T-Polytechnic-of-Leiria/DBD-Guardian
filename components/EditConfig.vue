<template>
  <div class="form-container">
    <div class="nice-form-group">
      <label>Host</label>
      <input
        type="text"
        v-model="selectedHost.identifier"
        placeholder="Host Identifier"
        required
      />
    </div>

    <div class="nice-form-group">
      <label>Host Address</label>
      <input
        type="text"
        v-model="selectedHost.address"
        placeholder="Hostname or IP Address"
        required
      />
    </div>

    <div class="button-group">
      <label class="button-label">Add/Remove Datasource</label>
      <CustomButton class="button-margin" @click="addDatasource"
        >+</CustomButton
      >
      <CustomButton class="button-margin" @click="removeDatasource"
        >-</CustomButton
      >
    </div>

    <div
      class="datasource-group"
      v-for="(datasource, index) in selectedHost.datasources"
      :key="index"
    >
      <div class="nice-form-group">
        <label>Datasource Name</label>
        <input
          type="text"
          v-model="datasource.name"
          placeholder="Name of the Datasource"
          required
        />
      </div>

      <div class="nice-form-group">
        <label>Datasource Path</label>
        <input
          type="text"
          v-model="datasource.path"
          placeholder="Path to the Datasource"
          required
        />
      </div>

      <div class="nice-form-group">
        <label>Datasource Format</label>
        <select v-model="datasource.format">
          <option>.csv</option>
          <option>.json</option>
          <option>.raw</option>
          <option>.txt</option>
        </select>
      </div>

      <div class="nice-form-group">
        <label>Datasource Parsing Type</label>
        <select v-model="datasource.parsingType">
          <option>Access (apache)</option>
          <option>Access (mariadb)</option>
          <option>Auth</option>
          <option>General Query</option>
          <option>Syslog</option>
        </select>
      </div>
    </div>
    <div class="button-container">
      <NormalButton class="normal-button" @click="saveChanges"
        >Save Changes</NormalButton
      >
      <NormalButton class="normal-button" @click="deleteHost"
        >Delete</NormalButton
      >
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import CustomButton from "./CustomButton.vue";
import NormalButton from "./NormalButton.vue";

export default {
  name: "EditConfig",
  components: { CustomButton, NormalButton },
  computed: {
    ...mapState(["selectedHost"]),
  },
  methods: {
    addDatasource() {
      // Add a new datasource to selectedHost.datasources
      this.selectedHost.datasources.push({
        name: "",
        path: "",
        format: ".csv",
        parsingType: "Access (apache)",
      });
    },
    removeDatasource() {
      // Remove the last datasource from selectedHost.datasources
      this.selectedHost.datasources.pop();
    },
    saveChanges() {
      // Save the changes to the selectedHost in the Vuex store
      this.$store.commit("updateHost", this.selectedHost);
      // Navigate back to the confirmation page
      this.$router.push("/confirmation");
    },
    deleteHost() {
      // Dispatch 'deleteHost' action to Vuex store
      this.$store.dispatch("deleteHost", this.selectedHost).then(() => {
        // Check if there are any hosts left
        if (this.$store.state.hosts.length === 0) {
          // If not, redirect to the ConfigurationPage
          this.$router.push("/configuration");
        } else {
          // If there are hosts left, redirect to the confirmation page
          this.$router.push("/confirmation");
        }
      });
    },
  },
};
</script>
<style scoped>
.form-container {
  max-width: 600px; /* Adjust this value to change the form width */
  margin: 0 auto; /* This centers the form */
  padding: 20px; /* This adds some space around the form */
}

.button-group {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 170px;
}

.button-normal {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.button-margin {
  justify-content: center;
  display: flex;
  margin: 25px 10px;
  /* Adjust these values to change the space around the buttons */
}

.button-label {
  margin-right: 10px;
  font-weight: 450; /* Adjust this value to change the space between the buttons and the label */
}

.datasource-group {
  border: 10px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  margin: 10px 0;
}

.normal-button {
  margin: 0 10px;
}

.button-container {
  display: flex;
  justify-content: space-between;
  width: fit-content;
  margin: 20px auto 20px;
}
</style>
