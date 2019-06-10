<template>
  <dialogform title="Edytuj panel" :fetchContent="fetchContent" ref="dialog" v-model="form" @submit="onSubmit">

    <template slot="anhor">
      <icon name="edit"></icon>
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Tytuł" placeholder="Tytuł"></text-input>
      <text-input v-model="form.description" label="Opis" placeholder="Opis widoczny w programie konwentu"></text-input>
      <text-input v-model="form.additional" label="Dodatkowy opis" placeholder="Dodatkowy opis widoczny tylko dla obsługi"></text-input>
      <text-input v-model="form.minutes" label="Czas trwania" placeholder="W minutach"></text-input>
      <checkbox v-model="form.accepted" label="Zaakceptowane"></checkbox>
    </template>
  </dialogform>
</template>

<script>
import panelResource from '@/panels/resource'
import form from '@/forms'

export default {
  props: ['panel_uid'],

  data () {
    return {
      form: form({
        name: '',
        description: '',
        additional: '',
        accepted: '',
        minutes: ''}),
      resource: panelResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({panel_uid: this.panel_uid})
    },
    onSubmit (form) {
      form.submit(
        () => panelResource(this).update({panel_uid: this.panel_uid}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('panels/fetch', true)
        }
      )
    }
  }
}
</script>
