<template>
  <dialogform title="Edytuj pokój" :fetchContent="fetchContent" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="edit"></icon>
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
  props: ['room_uid'],
  data () {
    return {
      form: form({
        name: '',
        number: '',
        floor: ''
      }),
      resource: roomResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({room_uid: this.room_uid})
    },
    onSubmit (form) {
      form.submit(
        () => roomResource(this).update({room_uid: this.room_uid}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('rooms/fetch', true)
        }
      )
    }
  }
}
</script>
