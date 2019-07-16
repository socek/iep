<template>
  <div>

    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-1 mr-0 btn btn-outline-primary " href="#/">Imladris Event</a>
      <ul v-if="isAuthenticated" class="nav navbar-nav col-sm-1">
        <li class="nav-item text-nowrap">
          <router-link class="nav-link" :to="{ name: 'ConventionList'}" :class="{active: isConventionListActive()}">
            <icon name="monument" /> Konwenty
          </router-link></li>
      </ul>

      <div class="nav-item col-sm-1">
        <div class="navbar-brand" v-if="isSidebarActive && activeConvention">
          Konwent: {{ activeConvention.name }}
        </div>
      </div>

      <div class="nav-item text-nowrap col-sm-8">&nbsp;</div>
      <ul class="navbar-nav px-3">
        <login v-if="isAuthenticated"></login>
        <register v-if="!isAuthenticated"></register>
      </ul>
    </nav>

    <div class="container-fluid">
      <nav class="col-sm-3 col-md-1 mr-0 d-none d-md-block bg-light sidebar" v-if="isSidebarActive">
        <div class="sidebar-sticky">
          <ul class="nav flex-column">
            <sidebar></sidebar>
          </ul>
        </div>
      </nav>

      <main role="main" class="col-md-10 ml-sm-auto" :class="{'col-lg-11': isSidebarActive, 'col-lg-12': !(isSidebarActive)}">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
  import login from "@/auth/login"
  import register from "@/auth/register"
  import sidebar from "@/sidebar/sidebar"

  export default {
    methods: {
      isConventionListActive () {
        return this.$route.name === "ConventionList"
      }
    },
    computed: {
      activeConvention () {
        return this.$store.getters["conventions/isActive"]
      },
      isAuthenticated () {
        return this.$store.getters["auth/isAuthenticated"]
      },
      isSidebarActive () {
        return this.$store.getters["auth/isAuthenticated"] && this.$store.state.conventions.active !== null
      }
    },
    beforeCreate () {
      this.$store.commit("init", this)
      this.$store.dispatch("conventions/fetchConventions")
    },
    name: "app",
    components: {
      login,
      register,
      sidebar
    }
  }
</script>
