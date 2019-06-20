import {moment, interval, timeFormat} from '@/grid/utils'
import gridResource from '@/grid/resource'

export default {
  namespaced: true,
  state: {
    timestamps: null,
    panelTimes: null
  },
  getters: {
  },
  mutations: {
    createTimestamps: function (state, {startDate, endDate}) {
      state.timestamps = []
      endDate = moment(endDate)
      let current = moment(startDate)

      while (current <= endDate) {
        state.timestamps.push(current.format(timeFormat))
        current = current.add(interval, 'm')
      }
    },
    setPanelTimes: function (state, panelTimes) {
      state.panelTimes = panelTimes
    }
  },
  actions: {
    init: (store) => {
      let resource = gridResource(store.rootGetters.vue)
      let startDate = store.rootGetters['conventions/startDate']
      let endDate = store.rootGetters['conventions/endDate']
      if (!(startDate && endDate)) {
        return
      }

      resource.list().then((result) => {
        store.commit('createTimestamps', {startDate, endDate})
        store.commit('setPanelTimes', result.body)
      })
    }
  }
}
