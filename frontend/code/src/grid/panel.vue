<template>
  <div class="panels">
    <dropdown v-model="value" :options="options" @input="sendUpdate()"></dropdown>
    <panel-time ref="panelTime"></panel-time>
  </div>
</template>

<script>
import panelTime from '@/grid/dialogs/panel_time'

export default {
  props: ['panels'],
  data () {
    return {
      value: {}
    }
  },
  methods: {
    sendUpdate () {
      console.log(this.value)
      this.value = {}
      this.$refs.panelTime.show()
    }
  },
  computed: {
    options () {
      let data = []
      for (let panel of this.panels) {
        data.push({
          value: panel.uid,
          text: panel.name})
      }
      return data
    }
  },
  components: {
    panelTime
  }
}
</script>

<style>
  .panels {
    margin: 10px;
  }
</style>
