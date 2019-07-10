<template>
  <div v-if="isConventActive">
    <panel :panels="panels"></panel>
    <div class="area" :style="getStyle()">
      <div class="head">↓ Godziny ↓</div>
      <room
        v-for="room in rooms"
        :key="room.uid"
        :room="room">
      </room>
      <timestamp
        v-for="(timestamp, index) in timestamps"
        :key="index + timestamp"
        :timestamp="timestamp">
      </timestamp>
      <panel-time
        v-for="(panelTime, index) in panelTimes"
        :key="panelTime.uid + componentKey"
        :panelTime="panelTime"
      ></panel-time>
    </div>
  </div>
</template>

<script>
import panel from "@/grid/panel"
import timestamp from "@/grid/timestamp"
import room from "@/grid/room"
import panelTime from "@/grid/panel_time"

export default {
  data () {
    return {
      componentKey: 0
    }
  },
  mounted () {
    this.$store.dispatch("rooms/fetch")
    this.$store.dispatch("panels/fetch")
  },
  computed: {
    rooms () {
      return this.$store.state.rooms.rooms
    },
    panels () {
      return this.$store.state.panels.panels
    },
    timestamps () {
      return this.$store.state.grid.timestamps
    },
    panelTimes () {
      return this.$store.state.grid.panelTimes
    },
    isConventActive () {
      let isActive = this.$store.getters["conventions/isActive"]
      if (isActive) {
        this.$store.dispatch("grid/init")
      }
      return isActive
    }
  },
  methods: {
    getStyle () {
      return {
        gridTemplateColumns: "auto ".repeat(this.rooms.length + 1)
      }
    }
  },
  components: {
    panel,
    timestamp,
    room,
    panelTime
  },
  beforeCreate () {
    this.unsubscribe = this.$store.subscribe((action, state) => {
      if (["rooms/set", "panels/set"].includes(action.type)) {
        this.componentKey += 1
      }
    })
  },
  beforeDestroy () {
    this.unsubscribe()
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
