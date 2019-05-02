def panels_routing(routing):
    routing.add("iep.panels.views.PanelsView", "panels", "/panels")
    routing.add("iep.panels.views.PanelView", "panel", "/panels/{panel_uid}")
