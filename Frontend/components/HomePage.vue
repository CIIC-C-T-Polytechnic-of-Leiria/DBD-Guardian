<template>
  <div class="home-container">
    <div class="welcome-title">
      <h1>Welcome To</h1>
      <h1>Cybersecurity Analytics</h1>
    </div>
    <div class="separator-line"></div>
    <div class="image-container">
      <a href="https://ciic.ipleiria.pt/" target="_blank">
        <img class="image" src="/images/ciic.png" alt="Image 1" />
      </a>
      <a href="https://trino.io/" target="_blank">
        <img class="image" src="/images/trino.png" alt="Image 2" />
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home-container {
  text-align: center;
  max-width: 100%;
  padding: 40px;
}

.welcome-title h1 {
  margin: 30px 0; /* Increase margin to add space */
  font-size: 36px;
  color: #333;
  font-weight: bold;
  letter-spacing: 2px;
}

.separator-line {
  margin: 30px 0; /* Increase margin to add space */
  width: 800px;
  height: 3px;
  background-color: rgb(1, 103, 255);
  margin: 30px auto; /* Center the line and add margin */
}

.image-container {
  display: flex;
  justify-content: center; /* Change to 'center' to reduce space between images */
  align-items: center;
  padding: 40px;
}

.image {
  width: 300px;
  height: 200px;
  object-fit: contain;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: all 0.3s ease;
  margin: 0 40px; /* Add some margin to separate the images slightly */
}

.image:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}
</style>