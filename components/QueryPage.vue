<template>
    <div>
      <button @click="query">Query</button>
      <div v-if="result">
        <h2>Result:</h2>
        <pre>{{ result }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapState } from 'vuex';
  
  export default {
    computed: mapState(['connection']),
    data() {
      return {
        result: null,
      };
    },
    methods: {
      query() {
        axios.post('http://localhost:5000/query', {
          connection: this.connection,
        })
        .then(response => {
          this.result = response.data.result;
        })
        .catch(error => {
          console.error(error);
        });
      },
    },
  };
  </script>
  