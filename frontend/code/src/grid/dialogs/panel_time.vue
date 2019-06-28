<template>
  <dialogform title="Dodaj panel do siatki" ref="dialog" v-model="form" @submit="onSubmit" :showButton="false">
    <template slot="content">
      <p>Panel: <strong>{{panelName}}</strong></p>
      <dropdown v-model="form.room_uid" :options="rooms" label="Pokój"></dropdown>
      <datetime-input v-model="form.begin_date" label="Początek"></datetime-input>
    </template>
  </dialogform>
</template>

<script>
import moment from 'moment'
import gridResource from '@/grid/resource'
import form from '@/forms'

export default {
  data () {
    return {
      val: '',
      panelUid: '',
      panelName: '',
      form: form({
        room_uid: {},
        begin_date: moment(this.$store.getters['conventions/isActive'].start_date).format('YYYY-MM-DD HH:mm:ss')
      })
    }
  },
  computed: {
    rooms () {
      let data = []
      for (let room of this.$store.state.rooms.rooms) {
        data.push({
          value: room.uid,
          text: room.name})
      }
      return data
    }
  },
  methods: {
    show (panelUid) {
      this.panelUid = panelUid
      this.panelName = this.$store.getters['panels/getPanel'](panelUid).name
      this.$refs.dialog.showModal()
    },
    onSubmit (form) {
      let data = form.toData()
      data.panel_uid = this.panelUid
      form.submit(
        () => gridResource(this).create({}, data),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('conventions/fetchConventions')
        }
      )
    }
  }
}
</script>
