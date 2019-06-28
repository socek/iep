import Vue from 'vue'
import Vuex from 'vuex'

import auth from '@/auth/store'
import conventions from '@/conventions/store'
import grid from '@/grid/store'
import rooms from '@/rooms/store'
import panels from '@/panels/store'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    vue: null
  },
  getters: {
    vue (state) {
      return state.vue
    },
    $route (state) {
      return state.vue.$route
    }
  },
  mutations: {
    init: (state, vue) => {
      state.vue = vue
    }
  },
  modules: {
    auth,
    conventions,
    grid,
    rooms,
    panels
  }
})
