import datetime

from src.models import User


def has_console_access_enabled(user: User) -> bool:
    # root user is always "not_supported"
    if user.password_enabled == "not_supported":
        return False

    return user.password_enabled


def has_never_logged_in(user: User) -> bool:
    return user.password_last_used == "no_information"


def has_exceeded_inactivity_threshold(user: User, inactivity_threshold: int) -> bool:
    if isinstance(user.password_last_used, datetime.date):
        dt_since_login = datetime.datetime.now() - user.password_last_used.replace(
            tzinfo=None
        )
        days_since_login = dt_since_login.days

        return days_since_login > inactivity_threshold

    return False


def has_exceeded_password_reset_grace_period(
    user: User, reset_grace_period_threshold: int
) -> bool:
    if isinstance(user.password_last_changed, datetime.date):
        dt_since_password_reset = (
            datetime.datetime.now() - user.password_last_changed.replace(tzinfo=None)
        )
        days_since_password_reset = dt_since_password_reset.days
        return days_since_password_reset > reset_grace_period_threshold

    return False


def is_inactive(
    user: User, inactivity_threshold: int, reset_grace_period_threshold: int
):
    # Can't be inactive without a password
    if not has_console_access_enabled(user):
        return False

    # Allow users some time to login after a account creation
    if has_never_logged_in(user):
        if has_exceeded_password_reset_grace_period(user, reset_grace_period_threshold):
            return True
        return False

    if has_exceeded_inactivity_threshold(
        user, inactivity_threshold
    ) and has_exceeded_password_reset_grace_period(user, reset_grace_period_threshold):
        return True

    return False


def disable_console_access(iam_client, username: str):
    iam_client.delete_login_profile(UserName=username)


def disable_programmatic_access(iam_client, username: str):
    response = iam_client.list_access_keys(
        UserName=username,
    )

    for access_key in response["AccessKeyMetadata"]:
        iam_client.update_access_key(
            UserName=username, AccessKeyId=access_key["AccessKeyId"], Status="Inactive"
        )


def disable_user(iam_client, user: User):
    disable_console_access(iam_client, user.username)
    disable_programmatic_access(iam_client, user.username)
