<template>
  <div class="settings-container">
    <div class="banner">General Settings</div>
    <div class="form-group">
      <fieldset class="nice-form-group">
        <div class="nice-form-group switch-group">
          <label for="privacy-mode" class="switch-label">Privacy Mode</label>
          <input
            type="checkbox"
            id="privacy-mode"
            class="switch"
            v-model="currentSettings.privacyMode"
          />
        </div>
      </fieldset>

      <fieldset class="nice-form-group protocol-group">
        <legend>Protocol</legend>
        <label>
          <input type="radio" value="http" v-model="currentSettings.protocol" /> HTTP
        </label>
        <label>
          <input type="radio" value="https" v-model="currentSettings.protocol" /> HTTPS
        </label>
      </fieldset>

      <div class="nice-form-group port-number-group">
        <label for="port-number">Port Number:</label>
        <input
          type="number"
          id="port-number"
          class="form-control"
          v-model="currentSettings.port"
        />
      </div>
    </div>
    <NormalButton @click="saveSettings" class="buttonsave"> Save </NormalButton>
    <div class="current-settings">
    <span class="setting-label">Privacy Mode:</span> {{ serverSettings.privacyMode ? 'True' : 'False' }} |
    <span class="setting-label">Protocol:</span> {{ serverSettings.protocol }} |
    <span class="setting-label">Port:</span> {{ serverSettings.port }}
  </div>  
  </div> 
   
</template>

<script>
import axios from "axios";
import NormalButton from "./NormalButton.vue";

export default {
  components: {
    NormalButton,
  },
  data() {
    return {
      serverSettings: {
        privacyMode: false,
        protocol: "http",
        port: 80,
      },
      currentSettings: {
        privacyMode: false,
        protocol: "http",
        port: 80,
      },
    };
  },
  mounted() {
    this.getSettings();
  },
  methods: {
    getSettings() {
      axios
        .get("http://localhost:5000/getsettings")
        .then((response) => {
          if (response.data.success) {
            this.serverSettings = response.data.settings;
            this.currentSettings = { ...response.data.settings }; // Copy the values to currentSettings
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    saveSettings() {
      axios
        .post("http://localhost:5000/changesettings", this.currentSettings)
        .then((response) => {
          if (response.data.success) {
            this.getSettings();
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.settings-container {
  text-align: center;
}
.banner {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  margin-top: 20px;
}
.switch-group {
  display: flex;
  align-items: center;
  justify-content: center;
}
.switch-label {
  margin-right: 10px;
}
.protocol-group label {
  display: inline-block;
  margin-right: 15px;
}
.port-number-group {
  margin: 10px auto;
}
.form-group {
  border: 2px solid rgb(54, 167, 219); /* Adjust color and thickness as needed */
  padding: 10px; /* Optional padding for better appearance */
  margin: 10px; /* Centering and spacing */
  display: inline-block; /* Aligning elements */
}
.buttonsave {
  margin: 10px auto;
}

.current-settings {
  border: 3px solid #ccc; /* Thin border around the area */
  border-radius: 3%;
  padding: 10px; /* Padding inside the area */
  display: inline-block; /* Horizontal layout */
  align-items: center; /* Center items vertically */
  justify-content: center; /* Center items horizontally */
  background-color: #f5f1f1;
}

.setting-label {
  font-weight: bold; /* Thicker font for the labels */
  margin-right: 5px; /* Space after the labels */
}
/* Additional styling can be added here */
</style>
