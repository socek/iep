<template>
  <div>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'PanelList'}" :class="{active: isPanelListActive()}">
        Panele
      </router-link>
      <new-dialog></new-dialog>
    </h6>
  </div>
</template>

<script>
  import newDialog from '@/panels/dialogs/new'

  export default {
    methods: {
      isPanelActive (wallet) {
        return this.$route.name === 'PanelDashboard' && this.$route.params.wallet_uid === wallet.uid
      },
      isPanelListActive () {
        return this.$route.name === 'PanelList'
      }
    },
    components: {
      newDialog
    }
  }
</script>
