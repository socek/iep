<template>
  <div class="panel" :style="style()">{{panelTime.panel.name}}</div>
</template>

<script>
import {moment, interval, minuteHeight} from '@/grid/utils'
import {duration} from 'moment'

const columnStart = 2
const rowStart = 2

export default {
  props: ['panelTime'],
  data () {
    console.log(this.panelTime)
    return {
      rooms: this.$store.state.rooms.rooms,
      panels: this.$store.state.panels.panels,
      timestamps: this.$store.state.grid.timestamps
    }
  },

  methods: {
    style () {
      let beginDate = moment(this.panelTime.begin_date)
      let endDate = moment(this.panelTime.end_date)

      let gridColumnStart = this.getColumnStart()
      let gridRowStart = this.getGridRowStart(beginDate)
      let gridRowEnd = this.getGridRowEnd(beginDate, endDate, gridRowStart)
      let marginTop = this.getMarginTop(beginDate, gridRowStart)

      let height = this.getHeight(beginDate, endDate)
      let result = {
        gridColumnStart,
        gridRowStart,
        gridRowEnd,
        height,
        marginTop
      }
      console.log(this.panelTime.panel.name, '|', gridRowEnd, result)
      return result
    },
    getGridRowStart (beginDate) {
      let before = 0
      for (let timestamp of this.timestamps) {
        let date = moment(timestamp)
        if (date <= beginDate) {
          before = this.timestamps.indexOf(timestamp)
        } else {
          break
        }
      }
      return rowStart + before
    },
    getMarginTop (beginDate, gridRowStart) {
      let gridStart = moment(this.timestamps[gridRowStart - rowStart])
      let minutes = duration(beginDate.diff(gridStart)).asMinutes()
      return minutes * minuteHeight + 'px'
    },
    getPanelEndMinutes (beginDate, gridRowStart) {
      let gridStart = moment(this.timestamps[gridRowStart - rowStart])
      let minutes = duration(beginDate.diff(gridStart)).asMinutes()
      return beginDate.minutes() + minutes
    },
    getColumnStart () {
      for (let index = 0; index < this.rooms.length; index++) {
        let roomUid = this.rooms[index].uid
        if (roomUid === this.panelTime.room_uid) {
          return columnStart + index
        }
      }
      return 0
    },
    getHeight (beginDate, endDate) {
      let minutes = duration(endDate.diff(beginDate)).asMinutes()
      return (minutes * minuteHeight) + 'px'
    },
    getGridRowEnd (beginDate, endDate, gridRowStart) {
      let minutes = duration(endDate.diff(beginDate)).asMinutes()
      minutes += beginDate.minutes()
      let rows = Math.ceil(minutes / interval)
      return gridRowStart + rows
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
