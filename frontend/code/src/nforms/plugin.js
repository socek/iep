import VueFormGenerator from "vue-form-generator/dist/vfg-core.js"
import fieldDatetime from "./datetime"
import dialogform from "./dialog"

export default {
  install (Vue, options) {
    Vue.use(VueFormGenerator)
    Vue.component("fieldDatetime", fieldDatetime)
    Vue.component("ndialogform", dialogform)
  }
}
