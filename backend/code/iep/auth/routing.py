def auth_routing(routing):
    routing.add("iep.auth.views.LoginView", "login", "/auth/login")
    routing.add("iep.auth.views.SignUpView", "sign_up", "/auth/signup")
