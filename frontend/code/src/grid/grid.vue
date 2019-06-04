<template>
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
      <panel
        v-for="(panel, index) in panels"
        :key="index + panel"
        :panel="panel">
      </panel>
    </div>
</template>

<script>
import panel from '@/grid/panel'
import timestamp from '@/grid/timestamp'
import room from '@/grid/room'
import core from '@/grid/core'

export default {
  data () {
    core.init(this)

    this.$store.dispatch('grid/init')

    return {
      core,
      panels: [
        {minutes: 15, start: '2017-02-20 10:21', text: 'Pierwszy Panel (start o 10:21, trwa 15 min)', room: 'Pokój A'},
        {minutes: 45, start: '2017-02-20 10:00', text: 'Drugi Panel (start o 10:00, trwa 45 min)', room: 'Pokój C'},
        {minutes: 60, start: '2017-02-20 12:00', text: 'Trzeci Panel  (start o 12:00, trwa 60 min)', room: 'Pokój C'},
        {minutes: 60, start: '2017-02-20 13:00', text: 'Czwarty Panel  (start o 13:00, trwa 60 min)', room: 'Pokój C'}
      ]
    }
  },
  created () {
    this.$store.dispatch('rooms/fetch')
  },
  computed: {
    rooms () {
      return this.$store.state.rooms.rooms
    }
  },
  methods: {
    getStyle () {
      return {
        gridTemplateColumns: 'auto '.repeat(core.rooms.length + 1)
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
