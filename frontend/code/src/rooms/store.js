import roomResource from "@/rooms/resource"

export default {
  namespaced: true,
  state: {
    rooms: [],
    dict: {},
    fetched: false
  },
  getters: {
    getRooms (state) {
      return state.rooms
    }
  },
  mutations: {
    set (state, rooms) {
      state.rooms = rooms
      state.dict = {}
      for (let room of rooms) {
        state.dict[room.uid] = room
      }
      state.fetched = true
    },
    clear (state) {
      state.rooms = []
      state.dict = {}
      state.fetched = false
    }
  },
  actions: {
    fetch: (state, refresh) => {
      refresh = refresh || false
      let fetched = state.state.fetched
      if (refresh || !fetched) {
        let resource = roomResource(state.rootState.vue)
        resource.list().then((response) => {
          state.commit("set", response.data)
        })
      }
    }
  }
}
