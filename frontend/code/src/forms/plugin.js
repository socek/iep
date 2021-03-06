import passwordInput from "./password"
import textInput from "./text"
import ccform from "./form"
import dateInput from "./date"
import datetimeInput from "./datetime"
import dropdown from "./dropdown"
import dialogform from "./dialog_form"
import checkbox from "./checkbox"

export default {
  install (Vue, options) {
    Vue.component("text-input", textInput)
    Vue.component("ccform", ccform)
    Vue.component("password-input", passwordInput)
    Vue.component("dialogform", dialogform)
    Vue.component("date-input", dateInput)
    Vue.component("datetime-input", datetimeInput)
    Vue.component("dropdown", dropdown)
    Vue.component("checkbox", checkbox)
  }
}
