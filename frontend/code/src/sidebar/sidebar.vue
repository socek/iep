<template>
  <div>
    <h3 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      Planner
    </h3>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'GuestList', params: {convention_uid: convention_uid}}" :class="{active: isGuestListActive()}">
        Goście
      </router-link>
    </h6>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'PanelList', params: {convention_uid: convention_uid}}" :class="{active: isPanelListActive()}">
        Panele
      </router-link>
    </h6>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'RoomList', params: {convention_uid: convention_uid}}" :class="{active: isRoomListActive()}">
        Pokoje
      </router-link>
    </h6>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'PanelGrid', params: {convention_uid: convention_uid}}" :class="{active: isPanelGridActive()}">
        Siatka Programowa
      </router-link>
    </h6>
  </div>
</template>

<script>
  export default {
    methods: {
      isActive () {
        return false
      },
      isPanelActive (wallet) {
        return this.$route.name === 'PanelDashboard' && this.$route.params.wallet_uid === wallet.uid
      },
      isPanelListActive () {
        return this.$route.name === 'PanelList'
      },
      isRoomListActive () {
        return this.$route.name === 'RoomList'
      },
      isPanelGridActive () {
        return this.$route.name === 'PanelGrid'
      },
      isGuestListActive () {
        return this.$route.name === 'GuestList'
      }
    },
    computed: {
      convention_uid () {
        return this.$store.state.conventions.active
      }
    }
  }
</script>
