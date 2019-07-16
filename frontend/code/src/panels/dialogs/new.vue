<template>
  <ndialogform
    title="Nowy panel"
    v-model="form"
    :schema="schema"
    @submit="submitHandler">

    <icon name="plus-circle" />
  </ndialogform>
</template>

<script>
import panelResource from "@/panels/resource"
import guests from "@/panels/parts/guests"
import schema from "./schema"

export default {
  data () {
    return {
      form: {
        name: "",
        description: "",
        additional: "",
        minutes: "",
        guests: []
      },
      schema: schema(this.guestMethod)
    }
  },
  methods: {
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
      panelResource(this).create({}, form).then((response) => {
        dialog.hide()
        this.$store.dispatch("panels/fetch", true)
      })
    }
  },
  components: {
    guests
  }
}
</script>
