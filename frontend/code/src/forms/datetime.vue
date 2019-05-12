<template>
  <div role="group" class="b-form-group form-group">
    <label class="col-form-label pt-0">{{ label }}:</label>
    <datetime format="YYYY-MM-DD H:i:s" v-model="value.value" class="form-control" :class="inputClass()"></datetime>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import datetime from 'vuejs-datetimepicker'
  import base from '@/forms/base'

  export default {
    extends: base,
    components: {
      datetime
    }
  }
</script>
