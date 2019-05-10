<template>
  <dialogform title="Nowy pokój" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Tytuł" placeholder="Tytuł"></text-input>
      <text-input v-model="form.number" label="Numer" placeholder="Numer pokoju lub dodatkowy opis"></text-input>
      <text-input v-model="form.floor" label="Piętro" placeholder="Piętro lub bardziej ogólny opis miejsca"></text-input>
    </template>
  </dialogform>
</template>

<script>
import roomResource from '@/rooms/resource'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        name: '',
        number: '',
        floor: ''
      })
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => roomResource(this).create({}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$emit('success')
        }
      )
    }
  }
}
</script>
