<template>
  <div class="panel" :style="toGrid()">{{panel.text}}</div>
</template>

<script>
import moment from 'moment'

const columnStart = 2
const rowStart = 2

export default {
  props: ['panel', 'timestamps', 'configuration'],
  data () {
    return {
    }
  },
  methods: {
    toGrid () {
      let gridColumnStart = columnStart + this.panel.room
      let gridRowStart = this.getGridRowStart()
      let gridRowEnd = gridRowStart + Math.ceil(this.getPanelEndMinutes(gridRowStart) / this.configuration.interval)
      let marginTop = this.getMarginTop(gridRowStart)
      let height = this.panel.minutes * this.configuration.minuteHeight + 'px'
      return {
        gridColumnStart,
        gridRowStart,
        gridRowEnd,
        marginTop,
        height
      }
    },
    getGridRowStart () {
      let index
      let before = 0
      let start = moment(this.panel.start, 'YYYY-MM-DD HH:mm')
      for (let timestamp of this.timestamps) {
        let date = moment(timestamp, 'YYYY-MM-DD HH:mm')
        if (date <= start) {
          before = this.timestamps.indexOf(timestamp)
        } else {
          break
        }
      }
      if (!index) {
        index = before
      }
      return rowStart + index
    },
    getMarginTop (gridRowStart) {
      let gridStart = moment(this.timestamps[gridRowStart - rowStart])
      let panelStart = moment(this.panel.start)
      let minutes = moment.duration(panelStart.diff(gridStart)).asMinutes()
      return minutes * this.configuration.minuteHeight + 'px'
    },
    getPanelEndMinutes (gridRowStart) {
      let gridStart = moment(this.timestamps[gridRowStart - rowStart])
      let panelStart = moment(this.panel.start)
      let minutes = moment.duration(panelStart.diff(gridStart)).asMinutes()
      return this.panel.minutes + minutes
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
