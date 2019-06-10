<template>
  <div>
    <panel :panels="panels"></panel>
    <div class="area" :style="getStyle()">
      <div class="head">↓ Godziny ↓</div>
      <room
        v-for="room in rooms"
        :key="room.uid"
        :room="room">
      </room>
      <timestamp
        v-for="(timestamp, index) in core.timestamps"
        :key="index + timestamp"
        :timestamp="timestamp">
      </timestamp>
    </div>
  </div>
</template>

<script>
import panel from '@/grid/panel'
import timestamp from '@/grid/timestamp'
import room from '@/grid/room'
import core from '@/grid/core'
import gridResource from '@/grid/resource'

export default {
  data () {
    core.init(this)
    gridResource(this).list().then(() => {})
    return {
      core,
      panelTimes: [
        {minutes: 15, start: '2017-02-20 10:21', text: 'Pierwszy Panel (start o 10:21, trwa 15 min)', room: 'Jeszcze jeden pokój'},
        {minutes: 45, start: '2017-02-20 10:00', text: 'Drugi Panel (start o 10:00, trwa 45 min)', room: 'Pokój Nauczycielski'},
        {minutes: 60, start: '2017-02-20 12:00', text: 'Trzeci Panel  (start o 12:00, trwa 60 min)', room: 'Pokój C'},
        {minutes: 60, start: '2017-02-20 13:00', text: 'Czwarty Panel  (start o 13:00, trwa 60 min)', room: 'Pokój C'}
      ]
    }
  },
  created () {
    this.$store.dispatch('rooms/fetch')
    this.$store.dispatch('panels/fetch')
  },
  computed: {
    rooms () {
      return this.$store.state.rooms.rooms
    },
    panels () {
      return this.$store.state.panels.panels
    }
  },
  methods: {
    getStyle () {
      return {
        gridTemplateColumns: 'auto '.repeat(this.rooms.length + 1)
      }
    }
  },
  components: {
    panel,
    timestamp,
    room
  }
}
</script>

<style>
  .area {
    display: grid;
    grid-template-columns: auto auto auto auto auto;
    background-color: #2196F3;
    grid-gap: 0px;
  }
  .area div {
    background-color: rgba(255, 255, 255, 0.8);
    text-align: center;
    font-size: 15px;
    border: 1px solid black;
  }
</style>
