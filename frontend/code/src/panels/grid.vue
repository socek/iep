<template>
    <div class="area">
      <div class="head">Godziny</div>
      <div class="head">Pokój A</div>
      <div class="head">Pokój B</div>
      <div class="head">Pokój C</div>
      <div class="timestamp">10:00</div>
      <div class="timestamp">10:30</div>
      <div class="timestamp">11:00</div>
      <div class="timestamp">11:30</div>
      <div class="timestamp">12:00</div>
      <div class="timestamp">12:30</div>

      <grid-element v-for="panel in panels" :panel="panel" :style="toGrid(panel)">
      </grid-element>
    </div>
</template>

<script>
import gridElement from './grid_element'
export default {
  data () {
    return {
      panels: [
        {minutes: 15, start: 1, end: 2, text: 'First Panel', room: 0},
        {minutes: 45, start: 1, end: 4, text: 'Second Panel', room: 1},
        {minutes: 45, start: 3, end: 6, text: 'Third Panel', room: 0}
      ]
    }
  },
  methods: {
    toGrid (panel) {
      let columnStart = 2
      let rowStart = 2
      return {
        gridColumnStart: columnStart + panel.room,
        gridRowStart: rowStart + panel.start,
        gridRowEnd: rowStart + panel.end
      }
    }
  },
  components: {
    gridElement
  }
}
</script>

<style>
  .area {
    display: grid;
    grid-template-columns: auto auto auto auto;
    background-color: #2196F3;
    grid-gap: 0px;
  }
  .area div {
    background-color: rgba(255, 255, 255, 0.8);
    text-align: center;
    font-size: 15px;
    border: 1px solid black;
  }
  .timestamp {
    grid-column-start: 1;
    padding: 5px 0;
    height: 60px;
  }
</style>
