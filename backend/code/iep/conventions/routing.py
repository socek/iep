def conventions_routing(routing):
    routing.add("iep.conventions.views.ConventionsView", "conventions", "/conventions")
    routing.add("iep.conventions.views.ConventionView", "convencion", "/conventions/{convention_uid}")
