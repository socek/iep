import {validators} from "vue-form-generator/dist/vfg.js"

export default (guestMethod) => {
  return {
    fields: [
      {
        type: "input",
        inputType: "text",
        label: "Tytuł",
        model: "name",
        readonly: false,
        featured: false,
        disabled: false,
        required: true,
        validator: validators.string.locale({
          fieldIsRequired: "Tytuł jest wymagany!"
        })
      }, {
        type: "input",
        inputType: "text",
        label: "Opis",
        model: "description",
        readonly: false,
        featured: false,
        disabled: false,
        required: false
      }, {
        type: "input",
        inputType: "text",
        label: "Dodatkowy opis",
        model: "additional",
        readonly: false,
        featured: false,
        disabled: false,
        required: false
      }, {
        type: "input",
        inputType: "text",
        label: "Czas trwania w minutach",
        model: "minutes",
        readonly: false,
        featured: false,
        disabled: false,
        required: true
      }, {
        type: "vueMultiSelect",
        model: "guests",
        label: "Goście / Twórcy programu",
        placeholder: "Wybierz gości",
        required: false,
        validator: validators.required,
        selectOptions: {
          multiple: true,
          key: "uid",
          label: "name",
          trackBy: "uid",
          searchable: true,
          clearOnSelect: false,
          closeOnSelect: false
        },
        values: guestMethod
      }
    ]
  }
}
