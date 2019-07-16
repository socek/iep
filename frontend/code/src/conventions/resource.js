export default (vue) => vue.$resource(
  "conventions{/convention_uid}",
  {},
  {
    list: {method: "GET"},
    create: {method: "PUT"},
    update: {method: "PATCH"}
  }
)
