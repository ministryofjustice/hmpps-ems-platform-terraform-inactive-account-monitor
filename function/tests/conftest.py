import datetime
import os
from dataclasses import dataclass
from unittest.mock import MagicMock

import boto3
import pytest
from moto import mock_aws

from src.models import User


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
        aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

    return LambdaContext()


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def iam_client(aws_credentials):
    """
    Return a mocked S3 client
    """
    with mock_aws():
        yield boto3.client("iam", region_name="eu-west-2")


@pytest.fixture
def recently_created_user_with_no_logins():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time=datetime.datetime.fromisoformat("2023-08-04T00:00:00+00:00"),
        password_enabled=True,
        password_last_used="no_information",
        password_last_changed=datetime.datetime.fromisoformat(
            "2023-08-04T00:00:00+00:00"
        ),
        password_next_rotation="N/A",
        mfa_active=False,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def not_recently_created_user_with_no_logins():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time=datetime.datetime.fromisoformat("2023-01-01T00:00:00+00:00"),
        password_enabled=True,
        password_last_used="no_information",
        password_last_changed=datetime.datetime.fromisoformat(
            "2023-01-01T00:00:00+00:00"
        ),
        password_next_rotation="N/A",
        mfa_active=False,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def disabled_user():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time=datetime.datetime.fromisoformat("2023-08-04T00:00:00+00:00"),
        password_enabled=False,
        password_last_used=datetime.datetime.fromisoformat("2023-08-04T00:00:00+00:00"),
        password_last_changed="N/A",
        password_next_rotation="N/A",
        mfa_active=True,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def active_user():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time=datetime.datetime.fromisoformat("2023-07-01T00:00:00+00:00"),
        password_enabled=True,
        password_last_used=datetime.datetime.fromisoformat("2023-08-04T00:00:00+00:00"),
        password_last_changed=datetime.datetime.fromisoformat(
            "2023-07-02T00:00:00+00:00"
        ),
        password_next_rotation="N/A",
        mfa_active=True,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def recently_reenabled_user_with_no_recent_login():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time=datetime.datetime.fromisoformat("2023-07-01T00:00:00+00:00"),
        password_enabled=True,
        password_last_used=datetime.datetime.fromisoformat("2023-07-03T00:00:00+00:00"),
        password_last_changed=datetime.datetime.fromisoformat(
            "2023-08-03T00:00:00+00:00"
        ),
        password_next_rotation="N/A",
        mfa_active=True,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def inactive_user():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time=datetime.datetime.fromisoformat("2023-06-01T00:00:00+00:00"),
        password_enabled=True,
        password_last_used=datetime.datetime.fromisoformat("2023-06-02T00:00:00+00:00"),
        password_last_changed=datetime.datetime.fromisoformat(
            "2023-06-01T00:00:00+00:00"
        ),
        password_next_rotation="N/A",
        mfa_active=True,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def root_user():
    return User(
        username="<root_account>",
        arn="arn:aws:iam::132044171362:root",
        user_creation_time=datetime.datetime.fromisoformat("2023-06-01T00:00:00+00:00"),
        password_enabled=True,
        password_last_used=datetime.datetime.fromisoformat("2023-06-02T00:00:00+00:00"),
        password_last_changed=datetime.datetime.fromisoformat(
            "2023-06-01T00:00:00+00:00"
        ),
        password_next_rotation="N/A",
        mfa_active=True,
        access_key_1_active=False,
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active=False,
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active=False,
        cert_1_last_rotated="N/A",
        cert_2_active=False,
        cert_2_last_rotated="N/A",
    )


# Freeze time to 2023-08-01 00:00 to enable repeatable datetime comparisons
@pytest.fixture
def freeze_time(monkeypatch):
    now = datetime.datetime(2023, 8, 1, 0, 0, 0)
    dt_mock = MagicMock(wraps=datetime.datetime)
    dt_mock.now.return_value = now
    monkeypatch.setattr(datetime, "datetime", dt_mock)
