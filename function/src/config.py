import os

from aws_lambda_powertools import Logger

logger = Logger(service="inactive-account-monitor")


class Config:
    __conf = {
        "inactivity_threshold_days": 30,
        "default_region": "eu-west-2",
        "grace_period_threshold_days": 7,
        "get_credential_report_retry_limit": 5,
    }

    @staticmethod
    def get(name):
        value = None

        logger.debug("Retrieving config value for key {0}".format(name))
        if name in Config.__conf:
            value = Config.__conf[name]

        value = os.environ.get(name, value)

        if value is None:
            raise KeyError(
                "Could not retrieve configuration value for [{0}]".format(name)
            )

        return value
