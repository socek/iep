<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="shoe-prints" /> Pokoje</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
          <new-dialog></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="actions" slot-scope="data">
        <edit-dialog :room_uid="data.item.uid"></edit-dialog>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import roomResource from '@/rooms/resource'
import newDialog from '@/rooms/dialogs/new'
import editDialog from '@/rooms/dialogs/edit'

export default {
  data () {
    return {
      isBusy: false,
      fields: [
        {key: 'name', label: 'Tytuł'},
        {key: 'number', label: 'Numer'},
        {key: 'floor', label: 'Piętro'},
        {key: 'actions', label: 'Akcje'}],
      items: [],
      resource: roomResource(this)
    }
  },
  created () {
    this.$store.dispatch('rooms/fetch')
  },
  computed: {
    provider () {
      return this.$store.state.rooms.rooms
    }
  },
  components: {
    newDialog,
    editDialog
  }
}
</script>
