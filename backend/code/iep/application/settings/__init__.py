from iep.application.settings.default import default
from iep.application.settings.wsgi import wsgi_specific
from iep.application.settings.tests import tests_specific


def wsgi():
    settings = default()
    wsgi_specific(settings)
    return settings


def command():
    return default()


def tests():
    settings = default()
    wsgi_specific(settings)
    tests_specific(settings)
    return settings
