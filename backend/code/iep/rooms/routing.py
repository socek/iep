def rooms_routing(routing):
    routing.add("iep.rooms.views.RoomsView", "rooms", "/rooms")
    routing.add("iep.rooms.views.RoomView", "room", "/rooms/{room_uid}")
