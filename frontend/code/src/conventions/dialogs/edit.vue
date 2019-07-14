<template>
  <ndialogform
    title="Edytuj konwent"
    :fetchContent="fetchContent"
    ref="dialog"
    v-model="form"
    :schema="schema"
    @submit="onSubmit">
    <template slot="anhor">
      <icon name="edit"></icon>
    </template>
  </ndialogform>
</template>

<script>
import conventResource from "@/conventions/resource"

export default {
  props: ["convention_uid"],

  data () {
    return {
      form: {
        name: "",
        start_date: "",
        end_date: ""
      },
      schema: {
        fields: [{
          type: "input",
          inputType: "text",
          label: "Nazwa",
          model: "name",
          readonly: false,
          featured: false,
          disabled: false
        }, {
          type: "datetime",
          label: "Początek",
          model: "start_date",
          readonly: false,
          featured: false,
          disabled: false
        }, {
          type: "datetime",
          label: "Zakończenie",
          model: "end_date",
          readonly: false,
          featured: false,
          disabled: false
        }, {
          type: "submit",
          buttonText: "Zapisz",
          onSubmit: this.submitHandler
        }]
      },
      resource: conventResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({convention_uid: this.convention_uid})
    },
    submitHandler (data) {
      console.log(event)
      conventResource(this).update({convention_uid: this.convention_uid}, data).then((response) => {
        this.$refs.dialog.hide()
        this.$store.dispatch("conventions/fetchConventions")
      })
    }
  }
}
</script>
