<template>
  <div class="list-component" v-if="data">
    <div class="header-container">
      <h2>{{ data.query }}</h2>
      <button class="close-button" @click="closeList">×</button>
    </div>
    <hr class="delimiter" />
    <div v-if="isNoResultsMessage(data.result)">
      <p>{{ data.result }}</p>
    </div>
    <ul v-else>
      <li v-for="(item, index) in data.result" :key="index">
        <p v-for="(value, key) in parseResult(item)" :key="key">{{ key }} {{ value }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  name: "ListComponent",
  props: {
    data: {
      type: Object,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  methods: {
    ...mapMutations(['removeResponse']),
    closeList() {
      this.$emit('close', this.index);
      console.log("listcomponent index",this.index);
    },
    isNoResultsMessage(result) {
      return typeof result === 'string' && result.trim() === 'No results found';
    },
    parseResult(result) {
  const strResult = result[0]; // get the first element of the array
  const parts = strResult.split(' #');
  const parsedResult = {};
  for (let i = 0; i < parts.length; i++) {
    if (parts[i]) {
      let [key, value] = parts[i].split('#:');
      key = key.replace(/#/g, '').trim(); // remove all # from key and trim spaces
      value = value ? value.replace(/#/g, '').replace(/:$/, '').trim() : ''; // remove all # from value, remove trailing colon, and trim spaces
      
      parsedResult[key] = value;
    }
  }
  return parsedResult;
}

  },
};
</script>
  <style scoped>
  .list-component {
    border: 1px solid #ddd;
    padding: 10px;
    width: 400px;
    height: auto;
    overflow: auto;
    background-color: #f9f9f9;
    border-radius: 5px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  }
  .header-container {
  display: flex;
  justify-content: space-between;
  align-items: center; /* Align vertically if needed */
}

.close-button {
  background-color: bisque;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.close-button:hover {
  background-color: #f44336;
  color: white;
}
  
  .list-component h2 {
    font-size: 1em;
  font-weight: bold;
  margin-bottom: 10px;
  }
  
 
  
  .list-component ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .list-component li {
    border: 1px solid #ddd;
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
    background-color: #fff;
  }
  
  .list-component li p {
    margin: 0;
    color: #1a202c;
  }
  .list-component hr.delimiter {
  border: 0;
  border-top: 2px solid #0084ff !important;
  margin-bottom: 10px;
}
  </style>