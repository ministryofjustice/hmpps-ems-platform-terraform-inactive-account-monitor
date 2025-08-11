from typing import Any

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.config import Config
from src.credential_report import get_credential_report
from src.helpers import disable_user, is_inactive

iam_client = boto3.client("iam")
logger = Logger(service="inactive-account-monitor")
inactivity_threshold = Config.get("inactivity_threshold_days")
grace_period_threshold = Config.get("grace_period_threshold_days")
report_only = Config.get("report_only") != "false"


@logger.inject_lambda_context(log_event=True)
def handle_event(event: dict, context: LambdaContext) -> dict[Any, Any]:
    credential_report = get_credential_report(iam_client)
    users = credential_report.users

    logger.info(f"Found {len(users)} user accounts.")

    inactive_console_users = [
        user
        for user in users
        if is_inactive(user, inactivity_threshold, grace_period_threshold)
    ]

    logger.info(f"Found {len(inactive_console_users)} inactive user accounts.")

    if report_only:
        for user in inactive_console_users:
            logger.info(
                f"{user.username} is inactive, last console login: {user.password_last_used}"
            )
    else:
        for user in inactive_console_users:
            disable_user(iam_client, user)
            logger.info(
                f"{user.username} has been disabled, last console login: {user.password_last_used}"
            )

    return event
