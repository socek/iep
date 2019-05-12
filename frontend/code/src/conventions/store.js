import conventionResource from '@/conventions/resource'

export default {
  namespaced: true,
  state: {
    conventions: [],
    dict: {},
    active: null
  },
  getters: {},
  mutations: {
    setConventions (state, conventions) {
      state.conventions = conventions
      state.dict = {}
      for (let convention of conventions) {
        state.dict[convention.uid] = convention
      }
    },
    setActive (state, uid) {
      if (uid) {
        state.active = state.dict[uid]
      } else {
        state.active = null
      }
    }
  },
  actions: {
    fetchConventions: (state) => {
      let resource = conventionResource(state.rootState.vue)
      resource.list().then((response) => {
        state.commit('setConventions', response.data)
      })
    }
  }
}
