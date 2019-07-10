import Vue from "vue"
import Router from "vue-router"

import store from "@/store"

import NotLoggedIn from "@/auth/not-logged-in"
import PanelList from "@/panels/list"
import PanelGrid from "@/grid/grid"
import RoomList from "@/rooms/list"
import ConventionList from "@/conventions/list"
import GuestList from "@/guests/list"

Vue.use(Router)

export function requireAuth (to, from, next) {
  if (to.params.convention_uid) {
    store.commit("conventions/setActive", to.params.convention_uid)
  }
  if (!store.getters["auth/isAuthenticated"]) {
    next({
      name: "NotLoggedIn",
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

function onlyNotLoggedIn (to, from, next) {
  if (store.getters["auth/isAuthenticated"]) {
    next({
      name: "NotLoggedIn"
    })
  } else {
    next()
  }
}

let router = new Router({
  routes: [
    {
      path: "/login",
      name: "NotLoggedIn",
      component: NotLoggedIn,
      beforeEnter: onlyNotLoggedIn
    },
    {
      path: "/",
      name: "ConventionList",
      component: ConventionList,
      beforeEnter: requireAuth
    },
    {
      path: "/conventions/:convention_uid/panels",
      name: "PanelList",
      component: PanelList,
      beforeEnter: requireAuth
    },
    {
      path: "/conventions/:convention_uid/rooms",
      name: "RoomList",
      component: RoomList,
      beforeEnter: requireAuth
    },
    {
      path: "/conventions/:convention_uid/panelgrid/",
      name: "PanelGrid",
      component: PanelGrid,
      beforeEnter: requireAuth
    },
    {
      path: "/conventions/:convention_uid/guests/",
      name: "GuestList",
      component: GuestList,
      beforeEnter: requireAuth
    }
  ]
})

export default router
