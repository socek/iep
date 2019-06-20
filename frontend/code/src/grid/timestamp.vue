<template>
    <div class="timestamp" :style="getStyle()">{{timestamp}}</div>
</template>

<script>
import {interval, minuteHeight} from '@/grid/utils'

export default {
  props: ['timestamp'],
  methods: {
    getStyle () {
      return {
        height: interval * minuteHeight + 'px'
      }
    }
  }
}
</script>

<style>
  .timestamp {
    grid-column-start: 1;
    padding: auto 0;
  }
</style>
