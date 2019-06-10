<template>
  <dialogform title="Nowy panel" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Tytuł" placeholder="Tytuł"></text-input>
      <text-input v-model="form.description" label="Opis" placeholder="Opis widoczny w programie konwentu"></text-input>
      <text-input v-model="form.additional" label="Dodatkowy opis" placeholder="Dodatkowy opis widoczny tylko dla obsługi"></text-input>
      <text-input v-model="form.minutes" label="Czas trwania" placeholder="W minutach"></text-input>
    </template>
  </dialogform>
</template>

<script>
import panelResource from '@/panels/resource'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        name: '',
        description: '',
        additional: '',
        minutes: ''
      })
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => panelResource(this).create({}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('panels/fetch', true)
        }
      )
    }
  }
}
</script>
