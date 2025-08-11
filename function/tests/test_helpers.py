import pytest
from botocore.exceptions import ClientError

from src.helpers import disable_user, is_inactive

MOCK_PASSWORD = "test_password"
MOCK_INACTIVITY_THRESHOLD = 30
MOCK_GRACE_PERIOD = 7


def test_recently_created_user_is_not_inactive(
    freeze_time, recently_created_user_with_no_logins
):
    assert (
        is_inactive(
            recently_created_user_with_no_logins,
            MOCK_INACTIVITY_THRESHOLD,
            MOCK_GRACE_PERIOD,
        )
        == False
    )


def test_not_recently_created_user_is_inactive(
    freeze_time, not_recently_created_user_with_no_logins
):
    assert (
        is_inactive(
            not_recently_created_user_with_no_logins,
            MOCK_INACTIVITY_THRESHOLD,
            MOCK_GRACE_PERIOD,
        )
        == True
    )


def test_disabled_user_is_not_inactive(freeze_time, disabled_user):
    assert (
        is_inactive(disabled_user, MOCK_INACTIVITY_THRESHOLD, MOCK_GRACE_PERIOD)
        == False
    )


def test_active_user_is_not_inactive(freeze_time, active_user):
    assert (
        is_inactive(active_user, MOCK_INACTIVITY_THRESHOLD, MOCK_GRACE_PERIOD) == False
    )


def test_inactive_user_is_inactive(freeze_time, inactive_user):
    assert (
        is_inactive(inactive_user, MOCK_INACTIVITY_THRESHOLD, MOCK_GRACE_PERIOD) == True
    )


def test_recently_reenabled_user_is_not_inactive(
    freeze_time, recently_reenabled_user_with_no_recent_login
):
    assert (
        is_inactive(
            recently_reenabled_user_with_no_recent_login,
            MOCK_INACTIVITY_THRESHOLD,
            MOCK_GRACE_PERIOD,
        )
        == False
    )


def test_disable_user_without_access_keys(iam_client, inactive_user):
    # Setup a fake user
    iam_client.create_user(UserName=inactive_user.username)
    iam_client.create_login_profile(
        UserName=inactive_user.username, Password=MOCK_PASSWORD
    )

    disable_user(iam_client, inactive_user)

    with pytest.raises(ClientError):
        iam_client.get_login_profile(UserName=inactive_user.username)

    response = iam_client.list_access_keys(UserName=inactive_user.username)

    assert len(response["AccessKeyMetadata"]) == 0


def test_disable_user_with_access_keys(iam_client, inactive_user):
    # Setup a fake user
    iam_client.create_user(UserName=inactive_user.username)
    iam_client.create_login_profile(
        UserName=inactive_user.username, Password=MOCK_PASSWORD
    )
    iam_client.create_access_key(UserName=inactive_user.username)

    disable_user(iam_client, inactive_user)

    with pytest.raises(ClientError):
        iam_client.get_login_profile(UserName=inactive_user.username)

    response = iam_client.list_access_keys(UserName=inactive_user.username)

    assert response["AccessKeyMetadata"][0]["Status"] == "Inactive"
