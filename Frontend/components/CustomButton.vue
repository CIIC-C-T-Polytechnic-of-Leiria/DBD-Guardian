<template>
  <button class="button-66" role="button">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "CustomButton",
};
</script>
<style scoped>
/* CSS */
.button-66 {
  background-color: #0a6bff;
  border-radius: 10px;
  border: 0;
  box-shadow: rgba(1, 60, 136, 0.5) 0 -1px 3px 0 inset,
    rgba(0, 44, 97, 0.1) 0 3px 6px 0;
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
  display: inherit;
  font-family: "Space Grotesk", -apple-system, system-ui, "Segoe UI", Roboto,
    Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
    "Segoe UI Symbol";
  font-size: 25px;
  width: 80px;
  height: 40px;
  font-weight: 800;
  line-height: 15px;
  margin: 0;
  margin-top: 10px;
  min-height: 30px;
  min-width: 15px;
  padding: 0px;
  position: center;
  text-align: center;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: baseline;
  transition: all 0.2s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.button-66:hover {
  background-color: #065dd8;
  transform: translateY(-2px);
}

@media (min-width: 768px) {
  .button-66 {
    padding: 10px 20px;
    min-width: 20px;
  }
}
</style>
