def panel_times_routing(routing):
    routing.add("iep.grid.views.PanelTimesView", "panel_times", "/conventions/{convention_uid}/panel_times")
    routing.add("iep.grid.views.PanelTimeView", "panel_time", "/conventions/{convention_uid}/panel_times/{panel_uid}")
