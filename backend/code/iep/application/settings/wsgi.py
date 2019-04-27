from decouple import config


def wsgi_specific(settings):
    settings["pyramid.reload_templates"] = True
    settings["session_secret"] = config("SESSION_SECRET", "this is not a secret")
    settings["secret"] = config("SECRET", "this is not a secret")
