<template>
  <dialogform title="Nowy gość" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Imię i nazwisko" placeholder="Zenon Zborowiec"></text-input>
      <text-input v-model="form.kind" label="Typ" placeholder="vip, prelegent"></text-input>
      <text-input v-model="form.description" label="Opis" placeholder="Opis gościa w programie konwentu"></text-input>
    </template>
  </dialogform>
</template>

<script>
import guestResource from '@/guests/resource'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        name: '',
        kind: '',
        description: ''
      })
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => guestResource(this).create({}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('guests/fetch', true)
        }
      )
    }
  }
}
</script>
