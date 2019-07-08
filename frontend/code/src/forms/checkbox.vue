<template>
  <div role="group" class="form-group">
    <b-form-checkbox
      v-model="value.value"
      :class="inputClass()"
      value="true"
      unchecked-value="false">
        {{ label }}
      </b-form-checkbox>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {extends: base}
</script>
