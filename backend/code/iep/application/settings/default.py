from sapp.plugins.settings import PrefixedStringsDict
from decouple import config


def default():
    settings = {"paths": PrefixedStringsDict("/code/")}
    alembic(settings)
    logging(settings)
    # database(settings)
    jwt(settings)
    return settings


def logging(settings):
    settings["logging"] = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "generic": {
                "format": "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "generic",
            }
        },
        "loggers": {
            "root": {"level": "DEBUG", "handlers": ["console"]},
            "sqlalchemy": {
                "level": "ERROR",
                "handlers": ["console"],
                "qualname": "sqlalchemy.engine",
            },
            "alembic": {
                "level": "ERROR",
                "handlers": ["console"],
                "qualname": "alembic",
            },
            "iep": {"level": "DEBUG", "handlers": ["console"], "qualname": "iep"},
            "celery": {"handlers": ["console"], "level": "ERROR"},
        },
    }


def database(settings):
    settings["db:dbsession:url"] = config("BACKEND_DB_URL")
    settings["db:dbsession:default_url"] = config("BACKEND_DB_DEFAULT_URL")


def alembic(settings):
    settings["paths"]["alembic:migrations"] = "alembic"


def jwt(settings):
    settings["jwt:algorithm"] = "HS256"
    settings["jwt:secret"] = config("JWT_SECRET", "sample")
