<template>
  <dialogform title="Edytuj konwent" :fetchContent="fetchContent" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="edit"></icon>
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
  props: ['convention_uid'],

  data () {
    return {
      form: form({
        name: '',
        start_date: '',
        end_date: ''
      }),
      resource: conventResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({convention_uid: this.convention_uid})
    },
    onSubmit (form) {
      form.submit(
        () => conventResource(this).update({convention_uid: this.convention_uid}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$emit('success')
        }
      )
    }
  }
}
</script>
