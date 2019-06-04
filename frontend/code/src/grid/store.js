import moment from 'moment'
import roomResource from '@/rooms/resource'
import panelResource from '@/panels/resource'

export default {
  namespaced: true,
  state: {
    interval: 30,
    minuteHeight: 2,
    timeFormat: 'YYYY-MM-DD HH:mm',
    start: null,
    end: null,
    timestamps: undefined,
    rooms: undefined
  },
  getters: {
    moment: (state, getters, root) => (date) => {
      return moment(date, state.timeFormat)
    }
  },
  mutations: {
    // init: (state, getters, root) => {

    // }
  },
  actions: {
    init: (store) => {
      let vue = store.rootGetters.vue
      roomResource(vue).list().then((response) => {
        console.log(response)
        console.log('rooms', response.data)
      })
      panelResource(vue).list().then((response) => {
        console.log('panels', response.data)
      })
    }
  }
}
