<template>
  <dialogModal ref="dialogModal" title="Czy na pewno?" variant="outline-danger" @ok="okHandler">
    <template slot="anhor">
      <icon name="trash" />
    </template>
    <template slot="content">
      Czy jesteś pewien, że chcesz usunąć panel "{{panelTime.panel.name}}" z kalendarza?
    </template>
  </dialogModal>
</template>

<script>
import dialogModal from '@/common/dialog'
import gridResource from '@/grid/resource'

export default {
  props: ['panelTime'],
  methods: {
    okHandler () {
      gridResource(this).delete({
        panel_uid: this.panelTime.panel_uid,
        room_uid: this.panelTime.room_uid
      })
      this.$store.dispatch('conventions/fetchConventions')
    }
  },
  components: {
    dialogModal
  }
}
</script>
