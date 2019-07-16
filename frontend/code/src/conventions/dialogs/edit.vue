<template>
  <ndialogform
    title="Edytuj konwent"
    :fetchContent="fetchContent"
    v-model="form"
    :schema="schema"
    @submit="submitHandler">

    <icon name="edit"></icon>

  </ndialogform>
</template>

<script>
import conventResource from "@/conventions/resource"
import schema from "./schema"

export default {
  props: ["convention_uid"],

  data () {
    return {
      form: {
        name: "",
        start_date: "",
        end_date: ""
      },
      resource: conventResource(this),
      schema
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({convention_uid: this.convention_uid})
    },
    submitHandler (dialog, data) {
      conventResource(this).update({convention_uid: this.convention_uid}, data).then((response) => {
        dialog.hide()
        this.$store.dispatch("conventions/fetchConventions")
      })
    }
  }
}
</script>
