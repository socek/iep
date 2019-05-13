def panels_routing(routing):
    routing.add("iep.panels.views.PanelsView", "panels", "/conventions/{convention_uid}/panels")
    routing.add("iep.panels.views.PanelView", "panel", "/conventions/{convention_uid}/panels/{panel_uid}")
