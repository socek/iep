<template>
  <div>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'PanelList'}" :class="{active: isPanelListActive()}">
        Panele
      </router-link>
      <new-panel-dialog></new-panel-dialog>
    </h6>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'RoomList'}" :class="{active: isRoomListActive()}">
        Pokoje
      </router-link>
      <new-room-dialog></new-room-dialog>
    </h6>
  </div>
</template>

<script>
  import newPanelDialog from '@/panels/dialogs/new'
  import newRoomDialog from '@/rooms/dialogs/new'

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
      }
    },
    components: {
      newPanelDialog,
      newRoomDialog
    }
  }
</script>
