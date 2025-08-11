from time import sleep
from typing import Any, List, Type

from aws_lambda_powertools import Logger
from pydantic import BaseModel

from src.config import Config
from src.models import CredentialReport, User

logger = Logger(service="inactive-account-monitor")


# Utility function to generate pydantic models from args (normally kwargs)
def populate_model_from_args(model: Type[BaseModel], args: List[Any]):
    return model(**{field: arg for field, arg in zip(model.model_fields, args)})


def get_credential_report(iam_client) -> CredentialReport:
    iam_client.generate_credential_report()
    success = False
    retry_limit = Config.get("get_credential_report_retry_limit")
    retries = 0

    while not success and retries < retry_limit:
        try:
            iam_client.get_credential_report()
            success = True
        except Exception as e:
            logger.info(e)
            sleep(1)
        finally:
            retries = retries + 1

    if retries == retry_limit:
        raise Exception(f"Unable to get credential report after {retries} attempts")

    logger.info(f"Got credential report after {retries} attempts")

    response = iam_client.get_credential_report()
    content = response["Content"].decode("utf8").strip()
    rows = content.split("\n")
    body = rows[1:]
    users = [populate_model_from_args(User, row.split(",")) for row in body]

    return CredentialReport(users=users)
