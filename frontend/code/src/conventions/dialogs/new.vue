<template>
  <ndialogform
    title="Nowy konwent"
    v-model="form"
    :schema="schema"
    @submit="submitHandler"
  >
    <icon name="plus-circle" />
  </ndialogform>
</template>

<script>
import conventResource from "@/conventions/resource"
import schema from "./schema"

export default {
  data () {
    return {
      form: {
        name: "",
        start_date: "",
        end_date: ""
      },
      schema
    }
  },
  methods: {
    submitHandler (dialog, data) {
      conventResource(this).create({}, data).then((response) => {
        dialog.hide()
        this.$store.dispatch("conventions/fetchConventions")
      })
    }
  }
}
</script>
