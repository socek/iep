<template>
  <dialogform title="Edytuj panel" :fetchContent="fetchContent" ref="dialog" v-model="form" @submit="onSubmit" @afterFetchContent="afterFetchContent">

    <template slot="anhor">
      <icon name="edit"></icon>
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Tytuł" placeholder="Tytuł"></text-input>
      <text-input v-model="form.description" label="Opis" placeholder="Opis widoczny w programie konwentu"></text-input>
      <text-input v-model="form.additional" label="Dodatkowy opis" placeholder="Dodatkowy opis widoczny tylko dla obsługi"></text-input>
      <text-input v-model="form.minutes" label="Czas trwania" placeholder="W minutach"></text-input>
      <guests ref="guests" v-model="form.guests_uids" />
    </template>
  </dialogform>
</template>

<script>
import panelResource from "@/panels/resource"
import form from "@/forms"
import guests from "@/panels/parts/guests"

export default {
  props: ["panel_uid"],

  data () {
    return {
      form: form({
        name: "",
        description: "",
        additional: "",
        // accepted: "",
        minutes: "",
        guests_uids: []
      }),
      resource: panelResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({panel_uid: this.panel_uid})
    },
    afterFetchContent (body) {
      this.$refs.guests.setGuests(body.guests_uids)
    },
    onSubmit (form) {
      form.submit(
        () => panelResource(this).update({panel_uid: this.panel_uid}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch("panels/fetch", true)
        }
      )
    }
  },
  components: {
    guests
  }
}
</script>
