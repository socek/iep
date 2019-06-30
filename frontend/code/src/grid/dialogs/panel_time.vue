<template>
  <dialogform
    title="Dodaj panel do siatki"
    ref="dialog"
    v-model="form"
    @submit="onSubmit"
    :showButton="false"
    :fetchContent="fetchContent"
    @afterFetchContent="afterFetchContentHandler">
    <template slot="content">
      <b-alert v-if="is_conflict" show variant="danger">W tym czasie i pokoju jest już inny panel!</b-alert>
      <p>Panel: <strong>{{panelName}}</strong></p>
      <dropdown ref="room" v-model="form.room_uid" :options="rooms" label="Pokój"></dropdown>
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
      is_conflict: false,
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
      this.val = ''
      this.form.room_uid.value = ''
      this.form.begin_date.value = ''
      this.$refs.dialog.showModal()
    },
    fetchContent () {
      return gridResource(this).get({panel_uid: this.panelUid}).then((response) => {
        return {
          body: {
            room_uid: response.body.room_uid,
            begin_date: response.body.begin_date
          }
        }
      })
    },
    afterFetchContentHandler () {
      this.$refs.room.setValue(this.form.room_uid.value)
    },
    onSubmit (form) {
      let data = form.toData()
      data.panel_uid = this.panelUid
      form.submit(
        () => {
          this.is_conflict = false
          return gridResource(this).create({}, data)
        },
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('conventions/fetchConventions')
        },
        (response) => {
          if (response.status === 409) {
            this.is_conflict = true
          } else {
            console.log('Unhandled exception', response)
          }
        }
      )
    }
  }
}
</script>
