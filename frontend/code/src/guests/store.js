import guestResource from '@/guests/resource'

export default {
  namespaced: true,
  state: {
    guests: [],
    dict: {},
    fetched: false
  },
  getters: {
    getGuests (state) {
      return state.guests
    },
    getGuest (state) {
      return (uid) => {
        return state.dict[uid]
      }
    }
  },
  mutations: {
    set (state, guests) {
      state.guests = guests
      state.dict = {}
      for (let guest of guests) {
        state.dict[guest.uid] = guest
      }
      state.fetched = true
    },
    clear (state) {
      state.guests = []
      state.dict = {}
      state.fetched = false
    }
  },
  actions: {
    fetch: (state, refresh) => {
      refresh = refresh || false
      let fetched = state.state.fetched
      if (refresh || !fetched) {
        let resource = guestResource(state.rootState.vue)
        resource.list().then((response) => {
          state.commit('set', response.data)
        })
      }
    }
  }
}
