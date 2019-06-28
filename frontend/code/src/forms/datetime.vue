<template>
  <div role="group" class="b-form-group form-group">
    <label class="col-form-label pt-0">{{ label }}:</label>
    <datetime zone="UTC" format="yyyy-MM-dd HH:mm:ss" type="datetime" v-model="value.value" class="form-control" :class="inputClass()"></datetime>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import {Datetime} from 'vue-datetime'
  // You need a specific loader for CSS files
  import 'vue-datetime/dist/vue-datetime.css'
  // import datetime from 'vuejs-datetimepicker'
  import base from '@/forms/base'

  export default {
    extends: base,
    components: {
      Datetime
    }
  }
</script>
