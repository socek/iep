<template>
  <div class="panel" :style="toGrid()">{{panel.text}}</div>
</template>

<script>
import moment from 'moment'
import core from '@/grid/core'

const columnStart = 2
const rowStart = 2

export default {
  props: ['panel'],
  data () {
    return {
    }
  },
  methods: {
    toGrid () {
      let gridColumnStart = this.getColumnStart()
      let gridRowStart = this.getGridRowStart()
      let gridRowEnd = gridRowStart + Math.ceil(this.getPanelEndMinutes(gridRowStart) / core.interval)
      let marginTop = this.getMarginTop(gridRowStart)
      let height = this.panel.minutes * core.minuteHeight + 'px'
      return {
        gridColumnStart,
        gridRowStart,
        gridRowEnd,
        marginTop,
        height
      }
    },
    getGridRowStart () {
      let before = 0
      let start = core.moment(this.panel.start)
      for (let timestamp of core.timestamps) {
        let date = core.moment(timestamp)
        if (date <= start) {
          before = core.timestamps.indexOf(timestamp)
        } else {
          break
        }
      }
      return rowStart + before
    },
    getMarginTop (gridRowStart) {
      let gridStart = core.moment(core.timestamps[gridRowStart - rowStart])
      let panelStart = core.moment(this.panel.start)
      let minutes = moment.duration(panelStart.diff(gridStart)).asMinutes()
      return minutes * core.minuteHeight + 'px'
    },
    getPanelEndMinutes (gridRowStart) {
      let gridStart = core.moment(core.timestamps[gridRowStart - rowStart])
      let panelStart = core.moment(this.panel.start)
      let minutes = moment.duration(panelStart.diff(gridStart)).asMinutes()
      return this.panel.minutes + minutes
    },
    getColumnStart () {
      return columnStart + core.rooms.indexOf(this.panel.room)
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
