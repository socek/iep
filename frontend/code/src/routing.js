import Vue from 'vue'
import Router from 'vue-router'

import store from '@/store'

import NotLoggedIn from '@/auth/not-logged-in'
import PanelList from '@/panels/list'
import RoomList from '@/rooms/list'

Vue.use(Router)

export function requireAuth (to, from, next) {
  if (!store.getters['auth/isAuthenticated']) {
    next({
      name: 'NotLoggedIn',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

function onlyNotLoggedIn (to, from, next) {
  if (store.getters['auth/isAuthenticated']) {
    next({
      name: 'NotLoggedIn'
    })
  } else {
    next()
  }
}

let router = new Router({
  routes: [
    {
      path: '/login',
      name: 'NotLoggedIn',
      component: NotLoggedIn,
      beforeEnter: onlyNotLoggedIn
    },
    {
      path: '/',
      name: 'PanelList',
      component: PanelList,
      beforeEnter: requireAuth
    },
    {
      path: '/rooms',
      name: 'RoomList',
      component: RoomList,
      beforeEnter: requireAuth
    }
  ]
})

export default router
