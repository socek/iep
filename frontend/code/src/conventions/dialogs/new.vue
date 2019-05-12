<template>
  <dialogform title="Nowy konwent" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Nazwa" placeholder="Imladris"></text-input>
      <datetime-input v-model="form.start_date" label="Początek"></datetime-input>
      <datetime-input v-model="form.end_date" label="Koniec"></datetime-input>
    </template>
  </dialogform>
</template>

<script>
import conventResource from '@/conventions/resource'
import form from '@/forms'

export default {
  data () {
    return {
      val: '',
      form: form({
        name: '',
        start_date: '',
        end_date: ''
      })
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => conventResource(this).create({}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$emit('success')
        }
      )
    }
  }
}
</script>
