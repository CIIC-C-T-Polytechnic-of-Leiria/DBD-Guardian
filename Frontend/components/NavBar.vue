<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
  <div class="topnav">
    <router-link active-class="active" to="/" @click="state.activeIndex = 0">Home</router-link>

    <router-link to="/analytics" active-class="active" >Analytics</router-link>
    
   
    <div class="dropdown" @click="state.activeIndex = isConfigOpen ? state.activeIndex : 1">

    
      <button
        class="dropbtn"
        @click="isConfigOpen = !isConfigOpen"
        :class="[state.activeIndex === 1 ? 'active' : '']"
      >
        Configuration
        <i class="fa fa-caret-down"></i>
      </button>
      <div class="dropdown-content" v-show="isConfigOpen">
        <router-link to="/load">Load Config</router-link>
        <router-link to="/configuration">New Config</router-link>
      </div>
    </div>
    <router-link to="/connection" active-class="active" >Connection</router-link>
    <!-- other links -->
    <router-link to="/settings" class="gear-button" active-class="active">
      <i class="fa fa-cog gear-icon"></i> <!-- Font Awesome Gear Icon -->
    </router-link>
  </div>
</template>

<script>
import { watch, reactive } from "vue";
import { useRoute } from "vue-router";


export default {
  name: "NavBar",
  data() {
    return {
      isConfigOpen: false,
    };
  },
  setup() {
    const route = useRoute();
    const state = reactive({ activeIndex: 0 });

    watch(
      () => route.path,
      (newPath) => {
        if (newPath === "/configuration" || newPath === "/load") {
          state.activeIndex = 1;
        } else if (newPath === "/") {
          state.activeIndex = 0;
        }
        // Add more conditions here for other routes
      }
    );

    return { state };
  },
};
</script>
<style>
/* Add a black background color to the top navigation */
.topnav {
  background-color: #0963da;
  overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
  transition: background-color 0.5s ease;
}

/* Change the color of links on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
  background-color: #04aa6d;
  color: white;
  border-radius: 25px;
}
.dropbtn.active {
  /* styles for active dropbtn */
  background-color: #04aa6d;
  color: white;
  border-radius: 25px;
}
.dropbtn.dropbtn.active {
  /* styles for active dropbtn */
  background-color: #04aa6d;
  color: white;
  border-radius: 25px;
}


.dropdown {
  float: left;
  overflow: hidden;
}

.dropdown .dropbtn {
  font-size: 17px;
  border: none;
  outline: none;
  color: #f2f2f2;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.topnav a:hover,
.dropdown:hover .dropbtn {
  background-color: #ddd;
  color: black;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.dropdown:hover .dropdown-content {
  display: block;
}
.gear-button {
    position: absolute; /* Absolute positioning */
    right: 0px; /* Right alignment */
    top: 0px; /* Top alignment */
    background: transparent; /* Transparent background */
    border: none; /* No border */
    cursor: pointer; /* Pointer cursor */
    display : flex;
    align-items: center;
    transition: background-color 0.5s ease;
  }
  .gear-icon {
    color: white; /* White color for the gear icon */
    font-size: 20px; /* Adjust the size if needed */
    transition: background-color 0.5s ease;
    height: 100%;
  }
  .gear-icon:hover {
    color: #000000; /* Dark grey on mouse-over */
  }.gear-button:hover {
    background-color: #ddd; /* Dark grey on mouse-over */
  }
</style>
