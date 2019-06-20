export default (vue) => vue.$resource(
  'conventions/{convention_uid}/panel_times{/panel_uid}{/room_uid}',
  {
    convention_uid: vue.$route.params.convention_uid
  },
  {
    list: {method: 'GET'},
    create: {method: 'PUT'},
    update: {method: 'PATCH'}
  }
)
