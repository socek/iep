<template>
  <div class="panel" :style="toGrid()">{{panel.text}}</div>
</template>

<script>
export default {
  props: ['panel', 'timestamps', 'configuration'],
  data () {
    return {
    }
  },
  methods: {
    toGrid () {
      let columnStart = 2
      let rowStart = 2
      let gridColumnStart = columnStart + this.panel.room
      let gridRowStart = rowStart + this.timestamps.indexOf(this.panel.start)
      let gridRowEnd = gridRowStart + Math.ceil(this.panel.minutes / this.configuration.interval)
      let height = this.panel.minutes * this.configuration.minuteHeight + 'px'
      return {
        gridRowStart,
        gridColumnStart,
        gridRowEnd,
        height
      }
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
