<template>
  <dialogform title="Panel" ref="dialog" v-model="form" @submit="onSubmit" :showButton="false">
    <template slot="content">
      <dropdown v-model="form.room_uid" :options="rooms"></dropdown>
      <datetime-input v-model="form.begin_date" label="Początek"></datetime-input>
    </template>
  </dialogform>
</template>

<script>
import gridResource from '@/grid/resource'
import form from '@/forms'

export default {
  data () {
    return {
      val: '',
      form: form({
        room_uid: {},
        begin_date: '2017-02-20 10:00:00'
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
    show () {
      this.$refs.dialog.showModal()
    },
    onSubmit (form) {
      form.submit(
        () => gridResource(this).create({}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$store.dispatch('conventions/fetchConventions')
        }
      )
    }
  }
}
</script>
