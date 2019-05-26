<template>
    <div class="area">
      <div class="head">Godziny</div>
      <div class="head">Pokój A</div>
      <div class="head">Pokój B</div>
      <div class="head">Pokój C</div>
      <div class="timestamp":style="configuration.timestampStyle()"  v-for="timestamp in timestamps">{{timestamp}}</div>

      <grid-element v-for="panel in panels" :panel="panel" :timestamps="timestamps" :configuration="configuration">
      </grid-element>
    </div>
</template>

<script>
import gridElement from './grid_element'
import moment from 'moment'

export default {
  data () {
    let configuration = {
      interval: 30,
      minuteHeight: 2,
      timestampStyle: function () {
        return {height: this.interval * this.minuteHeight + 'px'}
      }
    }

    let start = moment('2017-02-20 10:00', 'YYYY-MM-DD HH:mm')
    let end = moment('2017-02-22 14:00', 'YYYY-MM-DD HH:mm')
    let current = start
    let timestamps = []
    while (current <= end) {
      timestamps.push(current.format('YYYY-MM-DD HH:mm'))
      current = current.add(configuration.interval, 'm')
    }

    return {
      timestamps,
      configuration,
      panels: [
        {minutes: 15, start: '2017-02-20 10:17', text: 'First Panel', room: 0},
        {minutes: 45, start: '2017-02-20 10:00', text: 'Second Panel', room: 1},
        {minutes: 45, start: '2017-02-20 12:00', text: 'Third Panel', room: 0}
      ]
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
    padding: auto 0;
  }
</style>
