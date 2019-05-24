<template>
  <div class="panel">{{panel.text}}</div>
</template>

<script>
export default {
  props: ['panel'],
  data () {
    return {
    }
  }
}
</script>

<style>
.area div.panel {
  border: 1px solid black;
  background-color: green;
  color: white;
}
</style>
