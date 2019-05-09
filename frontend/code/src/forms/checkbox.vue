<template>
  <div role="group" class="form-group">
    <input
      type="checkbox"
      class="form-control"

      v-model="value.value"
      :class="inputClass()">
    <label v-if="label" class="col-form-label">{{ label }}:</label>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {extends: base}
</script>
