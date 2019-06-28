<template>
  <div class="panel" :style="style" :key="componentKey">
    {{panelTime.panel.name}}
    <b-btn size="sm" variant="outline-warning" @click="editHandler(panelTime)"><icon name="tools" /></b-btn>
    <delete-dialog :panelTime="panelTime" />
    <panel-time ref="panelTime"></panel-time>
  </div>
</template>

<script>
import {moment, interval, minuteHeight} from '@/grid/utils'
import {duration} from 'moment'
import deleteDialog from '@/grid/dialogs/delete'
import panelTime from '@/grid/dialogs/panel_time'

const columnStart = 2
const rowStart = 2

export default {
  props: ['panelTime'],
  data () {
    return {
      componentKey: 0,
      rooms: this.$store.getters['rooms/getRooms'],
      panels: this.$store.getters['panels/getPanels'],
      timestamps: this.$store.getters['grid/getTimestamps']
    }
  },
  methods: {
    editHandler (panelTime) {
      this.$refs.panelTime.show(panelTime.panel_uid)
    },
    deleteHandler () {
      console.log('delete')
    }
  },
  computed: {
    style () {
      let getGridRowStart = (beginDate) => {
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
      }

      let getMarginTop = (beginDate, gridRowStart) => {
        let gridStart = moment(this.timestamps[gridRowStart - rowStart])
        let minutes = duration(beginDate.diff(gridStart)).asMinutes()
        return minutes * minuteHeight + 'px'
      }

      let getColumnStart = () => {
        for (let index = 0; index < this.rooms.length; index++) {
          let roomUid = this.rooms[index].uid
          if (roomUid === this.panelTime.room_uid) {
            return columnStart + index
          }
        }
        return 0
      }

      let getHeight = (beginDate, endDate) => {
        let minutes = duration(endDate.diff(beginDate)).asMinutes()
        return (minutes * minuteHeight) + 'px'
      }

      let getGridRowEnd = (beginDate, endDate, gridRowStart) => {
        let minutes = duration(endDate.diff(beginDate)).asMinutes()
        minutes += beginDate.minutes()
        let rows = Math.ceil(minutes / interval)
        return gridRowStart + rows
      }

      let beginDate = moment(this.panelTime.begin_date)
      let endDate = moment(this.panelTime.end_date)

      let gridColumnStart = getColumnStart()
      let gridRowStart = getGridRowStart(beginDate)
      let gridRowEnd = getGridRowEnd(beginDate, endDate, gridRowStart)
      let marginTop = getMarginTop(beginDate, gridRowStart)

      let height = getHeight(beginDate, endDate)
      let result = {
        gridColumnStart,
        gridRowStart,
        gridRowEnd,
        height,
        marginTop
      }
      return result
    }
  },
  components: {
    deleteDialog,
    panelTime
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
