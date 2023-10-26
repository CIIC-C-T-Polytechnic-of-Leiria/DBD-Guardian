<template>
  <div class="form-container">
    <PopupCostum
      :show="showPopup"
      :title="popupTitle"
      :content="popupContent"
      @close="showPopup = false"
    />
    <div class="nice-form-group">
      <label>Host</label>
      <input
        type="text"
        v-model="host.identifier"
        placeholder="Host Identifier"
        required
      />
    </div>

    <div class="nice-form-group">
      <label>Host Address</label>
      <input
        type="text"
        v-model="host.address"
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
      v-for="(datasource, index) in datasources"
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
    <div class="button-normal">
      <NormalButton @click="checkAndSaveHost">Add Host</NormalButton>
      <NormalButton @click="saveConfiguration">Save Configuration</NormalButton>
    </div>
  </div>
</template>

<script>
import CustomButton from "./CustomButton.vue";
import NormalButton from "./NormalButton.vue";
import PopupCostum from "./PopupCostum.vue";
export default {
  name: "ConfigurationPage",
  components: { CustomButton, NormalButton, PopupCostum },
  data() {
    return {
      host: {
        identifier: "",
        address: "",
      },
      hosts: [],
      datasources: [],
      showPopup: false,
      popupTitle: "",
      popupContent: "",
    };
  },
  methods: {
    addDatasource() {
      this.datasources.push({
        name: "",
        path: "",
        format: "",
        parsingType: "",
      });
    },
    removeDatasource() {
      if (this.datasources.length > 0) {
        this.datasources.pop();
      }
    },
    checkAndSaveHost() {
      console.log(
        this.host.identifier.trim() === "" ||
          this.host.address.trim() === "" ||
          (this.datasources.length > 0 &&
            this.datasources.some(
              (datasource) =>
                datasource.name.trim() === "" ||
                datasource.path.trim() === "" ||
                datasource.format.trim() === "" ||
                datasource.parsingType.trim() === ""
            ))
      );
      if (
        this.host.identifier.trim() === "" ||
        this.host.address.trim() === "" ||
        (this.datasources.length > 0 &&
          this.datasources.some(
            (datasource) =>
              datasource.name.trim() === "" ||
              datasource.path.trim() === "" ||
              datasource.format.trim() === "" ||
              datasource.parsingType.trim() === ""
          ))
      ) {
        this.popupTitle = "Error";
        this.popupContent = "Please fill all information";
        this.showPopup = true;
      } else {
        this.saveHost();
      }
    },
    saveHost() {
      const hostCopy = JSON.parse(JSON.stringify(this.host));
      const datasourcesCopy = JSON.parse(JSON.stringify(this.datasources));
      this.hosts.push({ ...hostCopy, datasources: datasourcesCopy });
      this.host = { identifier: "", address: "" };
      this.datasources = [];
      this.showPopup = true;
      this.popupTitle = "Success";
      this.popupContent = "Host Saved Sucessfuly!";
    },
    saveConfiguration() {
      if (this.hosts) {
        console.log(this.hosts);
        this.$store.commit('addHosts', this.hosts);
        this.$router.push({ name: "confirmation" });
      } else {
        this.popupTitle = "Error";
        this.popupContent = "Please fill all information";
        this.showPopup = true;
      }
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
</style>
