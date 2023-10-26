<template>
  <div class="container center">
    <div class="card">
      <h2 class="card-title">{{ host.identifier }}</h2>
      <hr />
      <p class="card-body">{{ host.address }}</p>
      <div v-for="(datasource, index) in host.datasources" :key="index">
        <h3>{{ datasource.name }}</h3>
        <p class="datasource-info">Path: {{ datasource.path }}</p>
        <p class="datasource-info">Format: {{ datasource.format }}</p>
        <p class="datasource-info">
          Parsing Type: {{ datasource.parsingType }}
        </p>
      </div>
      <button class="edit-button" @click="editHost">Edit</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HostCard",
  props: {
    host: {
      type: Object,
      required: true,
    },
  },
  created() {
    console.log(this.host);
  },
  methods: {
    editHost() {
      this.$store.commit('setSelectedHost', this.host);
      this.$router.push({ name: "edit" });
    },
  },
};
</script>

<style lang="scss" scoped>
$black: #282828;
$point: rgb(54, 167, 219);
$point-light: lighten($point, 5%);

$ratio: 1.618;
$card_width: 300px;
$card_height: $card_width * $ratio;
$card_padding: 20px;
$card-bgcolor: white;
$card_margin: 5px;
$card_round: 10px;
$card-shadow: -20px -20px 0px 0px $point-light;

$card-padding-basis: 15px;
$card_head_padding: 0px 0px $card-padding-basis 0px;

* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: $point;
}

.container {
  width: 80%;
  min-height: 100vh;
  display: -webkit-box;
  justify-content: flex-start;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;

  margin-left: auto;
  margin-right: auto;
}



.center {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
}

.card {
  background-color: $card-bgcolor;
  width: $card_width;
  min-height: $card_height;

  display: -webkit-box;

  display: -ms-flexbox;

  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  padding: $card_padding;
  margin: $card_margin;

  -webkit-box-shadow: $card-shadow;

  box-shadow: $card-shadow;
  border-radius: $card_round;

  -webkit-animation-name: shadow-show; /* Safari 4.0 - 8.0 */
  -webkit-animation-duration: 1.5s; /* Safari 4.0 - 8.0 */
  animation-name: shadow-show;
  animation-duration: 1.5s;

  -webkit-transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1);
  -o-transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1);
  transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1); /* custom */

  h1,
  h2,
  h4,
  h5 {
    margin: 0px;
    padding: $card_head_padding;
    font-family: "Noto Sans KR", sans-serif;
    font-size: 30px;
    color: $black;
  }

  h3 {
    margin: 0px;
    margin-top: 20px;
    padding: $card_head_padding;
    font-family: "Noto Sans KR", sans-serif;
    font-size: 20px;
    color: $black;
  }

  hr {
    display: block;
    border: none;
    height: 3px;
    background-color: $point;
    margin: 0px;

    -webkit-animation-name: line-show; /* Safari 4.0 - 8.0 */
    -webkit-animation-duration: 0.3s; /* Safari 4.0 - 8.0 */
    animation-name: line-show;
    animation-duration: 0.3s;
    -webkit-transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1);
    -o-transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1);
    transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1); /* custom */
  }

  p {
    margin: $card-padding-basis 0px 0px 0px;
    font-family: "Noto Sans KR", sans-serif;
    font-weight: 100;
    letter-spacing: -0.25px;
    line-height: 1.25;
    font-size: 16px;
    word-break: break-all;
    word-wrap: pre-wrap;
    color: $black;

    -webkit-animation-name: p-show; /* Safari 4.0 - 8.0 */
    -webkit-animation-duration: 1.5s; /* Safari 4.0 - 8.0 */
    animation-name: p-show;
    animation-duration: 1.5s;
  }

  button {
    border: none;
    background-color: $point;
    width: 50%;
    margin: 10px auto;
    margin-top: auto;
    margin-bottom: 20px;
    padding: 10px 30px;
    color: white;
    font-family: "Noto Sans KR", sans-serif;
    text-transform: uppercase;
    transition: background-color 0.3s ease;
  }
  button:hover {
  background-color: darken($point, 10%);
}

button:active {
  background-color: darken($point, 20%);
}
}

/* Safari 4.0 - 8.0 */
@-webkit-keyframes line-show {
  from {
    margin: 0px 100px;
  }
  to {
    margin: 0px;
  }
}

/* Standard syntax */
@keyframes line-show {
  from {
    margin: 0px 100px;
  }
  to {
    margin: 0px;
  }
}

/* Safari 4.0 - 8.0 */
@-webkit-keyframes p-show {
  from {
    color: white;
  }
  to {
    color: $black;
  }
}

/* Standard syntax */
@keyframes p-show {
  from {
    color: white;
  }
  to {
    color: $black;
  }
}

/* Safari 4.0 - 8.0 */
@-webkit-keyframes shadow-show {
  from {
    -webkit-box-shadow: 0px 0px 0px 0px #e0e0e0;
    box-shadow: 0px 0px 0px 0px #e0e0e0;
  }
  to {
    -webkit-box-shadow: $card-shadow;
    box-shadow: $card-shadow;
  }
}

/* Standard syntax */
@keyframes shadow-show {
  from {
    -webkit-box-shadow: 0px 0px 0px 0px #e0e0e0;
    box-shadow: 0px 0px 0px 0px #e0e0e0;
  }
  to {
    -webkit-box-shadow: $card-shadow;
    box-shadow: $card-shadow;
  }
}
</style>
