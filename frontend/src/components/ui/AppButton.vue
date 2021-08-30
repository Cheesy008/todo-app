<template>
  <button :class="type" :disabled="disabled">
    <slot/>
  </button>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      default: 'normal'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
}
</script>

<style scoped lang="scss">
button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  color: #333;
  background-color: #fff;
  border-radius: 4px;
  font-size: 20px;
  cursor: pointer;

  &.danger {
    background-color: #ff4949;
    border-color: #ff4949;
    color: #fff;
  }

  &.success {
    background-color: #13ce66;
    border-color: #13ce66;
    color: #fff;
  }

  &.info {
    background-color: #50bfff;
    border-color: #50bfff;
    color: #fff;
  }
}


</style>