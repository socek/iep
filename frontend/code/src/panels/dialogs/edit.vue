<template>
  <ndialogform
    title="Edytuj panel"
    :fetchContent="fetchContent"
    v-model="form"
    :schema="schema"
    @submit="submitHandler"
  >
      <icon name="edit"></icon>
  </ndialogform>
</template>

<script>
import panelResource from "@/panels/resource"
import schema from "./schema"

export default {
  props: ["panel_uid"],

  data () {
    return {
      form: {
        name: "",
        description: "",
        additional: "",
        minutes: "",
        guests: []
      },
      resource: panelResource(this),
      schema: schema(this.guestMethod)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({panel_uid: this.panel_uid}).then((content) => {
        let guests = []
        for (let uid of content.body.guests_uids) {
          guests.push(this.$store.getters["guests/getGuest"](uid))
        }
        content.body.guests = guests
        return content
      })
    },
    guestMethod (form) {
      return this.$store.getters["guests/getGuests"]
    },
    submitHandler (dialog, form) {
      form = Object.assign({}, form)
      let guestUids = []
      for (let guest of form.guests) {
        guestUids.push(guest.uid)
      }
      form.guests_uids = guestUids
      delete form.guests
      panelResource(this).update({panel_uid: this.panel_uid}, form).then((response) => {
        dialog.hide()
        this.$store.dispatch("panels/fetch", true)
      })
    }
  }
}
</script>
