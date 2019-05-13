def rooms_routing(routing):
    routing.add("iep.rooms.views.RoomsView", "rooms", "/conventions/{convention_uid}/rooms")
    routing.add("iep.rooms.views.RoomView", "room", "/conventions/{convention_uid}/rooms/{room_uid}")
