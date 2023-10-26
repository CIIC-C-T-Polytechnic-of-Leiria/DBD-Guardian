<template>
  <div class="form-container">
    <PopupCostum
      :show="showPopup"
      :title="popupTitle"
      :content="popupContent"
      @close="showPopup = false"
    />
    <div class="nice-form-group">
      <label>Upload Configuration File</label>
      <input type="file" />
    </div>
    <div class="button-normal">
      <NormalButton @click="loadFile">Load Configuration File</NormalButton>
    </div>
  </div>
</template>

<script>
import NormalButton from "./NormalButton.vue";
import PopupCostum from "./PopupCostum.vue";
import axios from "axios";

export default {
  name: "LoadConfig",
  data() {
    return {
      showPopup: false,
      popupTitle: "",
      popupContent: "",
    };
  },
  components: { NormalButton, PopupCostum },
  methods: {
    async loadFile() {
      const file = document.querySelector("input[type=file]").files[0];
      //if the file isnt a .json file
      if (!file || file.name.split(".").pop() != "json") {
        this.popupTitle = "Error";
        this.popupContent = "File must be a .json file";
        this.showPopup = true;
        return;
      }

      // Create a FormData instance
      const formData = new FormData();
      // Add the file to the form data
      formData.append("file", file);

      // Send the file to the backend
      try {
        const response = await axios.post(
          "http://localhost:5000/upload",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log(response.data);
        if (response.status == 200 ){
          this.popupTitle = "Success";
          this.popupContent = "File uploaded successfully";
          this.showPopup = true;
        }
      } catch (error) {
        console.error(error);
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

.button-normal {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 25px 10px;
}
</style>
