export default (vue) => vue.$resource(
  'panels{/panel_uid}',
  {},
  {
    list: {method: 'GET'},
    create: {method: 'PUT'},
    update: {method: 'PATCH'}
  }
)
