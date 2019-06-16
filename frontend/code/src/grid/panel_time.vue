<template>
  <div class="panel" :style="style()">{{panel.text}}</div>
</template>

<script>
import {moment, interval, minuteHeight} from '@/grid/utils'

const columnStart = 2
const rowStart = 2

export default {
  props: ['panel'],
  data () {
    return {
    }
  },
  methods: {
    style () {
      let gridColumnStart = this.getColumnStart()
      let gridRowStart = this.getGridRowStart()
      let gridRowEnd = gridRowStart + Math.ceil(this.getPanelEndMinutes(gridRowStart) / interval)
      let marginTop = this.getMarginTop(gridRowStart)
      let height = this.panel.minutes * minuteHeight + 'px'
      return {
        gridColumnStart,
        gridRowStart,
        gridRowEnd,
        marginTop,
        height
      }
    },
    getGridRowStart () {
      return
      let before = 0
      let start = moment(this.panel.start)
      for (let timestamp of core.timestamps) {
        let date = moment(timestamp)
        if (date <= start) {
          before = core.timestamps.indexOf(timestamp)
        } else {
          break
        }
      }
      return rowStart + before
    },
    getMarginTop (gridRowStart) {
      let gridStart = moment(core.timestamps[gridRowStart - rowStart])
      let panelStart = moment(this.panel.start)
      let minutes = moment.duration(panelStart.diff(gridStart)).asMinutes()
      return minutes * minuteHeight + 'px'
    },
    getPanelEndMinutes (gridRowStart) {
      let gridStart = moment(core.timestamps[gridRowStart - rowStart])
      let panelStart = moment(this.panel.start)
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
