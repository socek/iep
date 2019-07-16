def guests_routing(routing):
    routing.add("iep.guests.views.GuestsView", "guests", "/conventions/{convention_uid}/guests")
    routing.add("iep.guests.views.GuestView", "guest", "/conventions/{convention_uid}/guests/{guest_uid}")
