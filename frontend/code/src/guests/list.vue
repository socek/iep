<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="book" /> Goście</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
          <new-dialog></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="actions" slot-scope="data">
        <edit-dialog :guest_uid="data.item.uid"></edit-dialog>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import guestResource from '@/guests/resource'
import newDialog from '@/guests/dialogs/new'
import editDialog from '@/guests/dialogs/edit'

export default {
  data () {
    return {
      isBusy: false,
      fields: [
        {key: 'name', label: 'Tytuł'},
        {key: 'kind', label: 'Typ'},
        {key: 'description', label: 'Opis'},
        {key: 'actions', label: 'Akcje'}],
      items: [],
      resource: guestResource(this)
    }
  },
  created () {
    this.$store.dispatch('guests/fetch')
  },
  computed: {
    provider () {
      return this.$store.state.guests.guests
    }
  },
  components: {
    newDialog,
    editDialog
  }
}
</script>
