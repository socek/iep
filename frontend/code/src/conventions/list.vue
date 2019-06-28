<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="shoe-prints" /> Konwenty</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
          <new-dialog></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="actions" slot-scope="data">
        <edit-dialog :convention_uid="data.item.uid"></edit-dialog>
        <button class="btn btn-sm btn-success" @click="activate(data.item.uid)">Aktywuj</button>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import newDialog from '@/conventions/dialogs/new'
import editDialog from '@/conventions/dialogs/edit'

export default {
  data () {
    return {
      isBusy: false,
      fields: [
        {key: 'name', label: 'Nazwa'},
        {key: 'start_date', label: 'Początek'},
        {key: 'end_date', label: 'Zakończenie'},
        {key: 'actions', label: 'Akcje'}],
      items: []
    }
  },
  methods: {
    activate (uid) {
      this.$store.dispatch('conventions/activate', uid)
    }
  },
  computed: {
    provider (ctx) {
      return this.$store.state.conventions.conventions
    }
  },
  components: {
    newDialog,
    editDialog
  }
}
</script>
