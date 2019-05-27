<template>
    <div class="timestamp" :style="getStyle()">{{timestamp}}</div>
</template>

<script>
import core from '@/grid/core'

export default {
  props: ['timestamp'],
  methods: {
    getStyle () {
      return {
        height: core.interval * core.minuteHeight + 'px'
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
