<template>
  <div>
    <b-button variant="success">{{panel.name}}</b-button>
  </div>
</template>

<script>
export default {
  props: ['panel']
}
</script>

<style>
  .panels div {
    margin-top: 5px;
  }
</style>
