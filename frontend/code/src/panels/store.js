import panelResource from '@/panels/resource'

export default {
  namespaced: true,
  state: {
    panels: [],
    dict: {},
    fetched: false
  },
  getters: {
    getPanels (state) {
      return state.panels
    }
  },
  mutations: {
    set (state, panels) {
      state.panels = panels
      state.dict = {}
      for (let panel of panels) {
        state.dict[panel.uid] = panel
      }
      state.fetched = true
    },
    clear (state) {
      state.panels = []
      state.dict = {}
      state.fetched = false
    }
  },
  actions: {
    fetch: (state, refresh) => {
      refresh = refresh || false
      let fetched = state.state.fetched
      if (refresh || !fetched) {
        let resource = panelResource(state.rootState.vue)
        resource.list().then((response) => {
          state.commit('set', response.data)
        })
      }
    }
  }
}
