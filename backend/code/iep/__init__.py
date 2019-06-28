from iep.application.app import IAPConfigurator

import sentry_sdk

from sentry_sdk.integrations.pyramid import PyramidIntegration
sentry_sdk.init(
    dsn="https://35a3535f0c024f4d9a0518f257a42530@sentry.io/1492181",
    integrations=[PyramidIntegration()]
)

app = IAPConfigurator()
