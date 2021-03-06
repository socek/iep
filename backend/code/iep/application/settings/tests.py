from os import environ


def tests_specific(settings):
    database(settings)


def database(settings):
    settings["db:dbsession:url"] = environ["BACKEND_DB_TEST_URL"]
    settings["db:dbsession:options"] = {"pool_pre_ping": True}
