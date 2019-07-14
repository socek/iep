<template>
  <datetime
    zone="UTC"
    format="yyyy-MM-dd HH:mm:ss"
    type="datetime"
    v-model="value"
    inputClass="form-control"
    :disabled="disabled"
    :readonly="schema.readonly">
  </datetime>
</template>

<script>
  import {abstractField} from "vue-form-generator/dist/vfg-core.js"
  import {Datetime} from "vue-datetime"

  export default {
    mixins: [ abstractField ],
    components: {
      Datetime
    }
  }
</script>
