<template>
  <div class="container center">
    <div class="card">
      <h2 class="card-title">Host: {{ host.identifier }}</h2>
      <hr />
      <p class="card-body">Status: <span :class="statusClass">{{ host.status }}</span></p>
      <h3 class="datasource-info">Datasources</h3>
      <hr />
      <div v-for="datasource in host.datasources" :key="datasource.name" class="datasource-container">
        <h4 class="datasource-name">{{ datasource.name }}</h4>
        <p class="datasource-status">Status: <span :class="datasourceStatusClass(datasource.status)">{{ datasource.status }}</span></p>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "StatusCard",
  props: {
    host: {
      type: Object,
      required: true,
    },
  },
  computed: {
    statusClass() {
      return {
        'status-online': this.host.status === 'Online',
        'status-offline': this.host.status === 'Offline'
      };
    }
  },
  methods: {
    datasourceStatusClass(status) {
      return {
        'status-online': status === 'Online',
        'status-offline': status === 'Offline'
      };
    }
  }
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
$card_shadow: -20px -20px 0px 0px $point-light;

.container {
  width: 80%;
  min-height: 100vh;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  margin-left: auto;
  margin-right: auto;
}

.center {
  align-items: center;
  justify-content: center;
}

.card {
  background-color: $card-bgcolor;
  width: $card_width;
  min-height: $card_height;
  display: flex;
  flex-direction: column;
  padding: $card_padding 30px;
  margin: $card_margin;
  box-shadow: $card_shadow;
  border-radius: $card_round;
  animation-name: shadow-show;
  animation-duration: 1.5s;
  transition-timing-function: cubic-bezier(0.795, 0, 0.165, 1);

  h2.card-title {
    font-size: 24px;
    margin-bottom: 10px;
  }

  p.card-body {
    font-weight: 500;
    margin-bottom: 10px;
  }

  h3.datasource-info {
    margin-top: 20px;
    font-size: 20px;
    color: $black;
    margin-bottom: 10px;
  }

  hr {
    margin: 10px 0;
    border: none;
    height: 3px;
    background-color: $point;
  }

  .datasource-container {
    margin-bottom: 10px;
  }

  h4.datasource-name {
    font-size: 18px;
    margin-bottom: 5px;
  }

  p.datasource-status {
    margin-left: 15px;
    font-weight: 300;
  }

  .status-online {
    color: green;
  }

  .status-offline {
    color: red;
  }
}

@keyframes shadow-show {
  from {
    box-shadow: 0px 0px 0px 0px #e0e0e0;
  }
  to {
    box-shadow: $card_shadow;
  }
}
</style>