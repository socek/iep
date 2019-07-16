import {validators} from "vue-form-generator/dist/vfg.js"

export default {
  fields: [
    {
      type: "input",
      inputType: "text",
      label: "Nazwa",
      model: "name",
      readonly: false,
      featured: false,
      disabled: false,
      required: true,
      validator: validators.string.locale({
        fieldIsRequired: "Nazwa jest wymagana!"
      })
    }, {
      type: "datetime",
      label: "Początek",
      model: "start_date",
      readonly: false,
      featured: false,
      disabled: false,
      required: true,
      validator: validators.string.locale({
        fieldIsRequired: "Początek konwentu jest wymagany!"
      })
    }, {
      type: "datetime",
      label: "Zakończenie",
      model: "end_date",
      readonly: false,
      featured: false,
      disabled: false,
      required: true,
      validator: validators.string.locale({
        fieldIsRequired: "Koniec konwentu jest wymagany!"
      })
    }
  ]
}
