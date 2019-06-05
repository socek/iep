import conventionResource from '@/conventions/resource'

export default {
  namespaced: true,
  state: {
    conventions: [],
    dict: {},
    active: null
  },
  getters: {
    isActive (state) {
      return state.dict[state.active]
    }
  },
  mutations: {
    setConventions (state, conventions) {
      state.conventions = conventions
      state.dict = {}
      for (let convention of conventions) {
        state.dict[convention.uid] = convention
      }
    },
    setActive (state, uid) {
      state.active = uid
    }
  },
  actions: {
    fetchConventions: (state) => {
      let resource = conventionResource(state.rootState.vue)
      resource.list().then((response) => {
        state.commit('setConventions', response.data)
      })
    },
    activate: ({state, commit}, uid) => {
      commit('setActive', uid)
      commit('rooms/clear', {}, {root: true})
      commit('panels/clear', {}, {root: true})
    }
  }
}
