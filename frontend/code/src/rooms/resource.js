export default (vue) => vue.$resource(
  'rooms{/room_uid}',
  {},
  {
    list: {method: 'GET'},
    create: {method: 'PUT'},
    update: {method: 'PATCH'}
  }
)
