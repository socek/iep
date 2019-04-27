from iep import app


def setup(env):
    env["app"] = app
    env["ctx"] = app.create_context()
