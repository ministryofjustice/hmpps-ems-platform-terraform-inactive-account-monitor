from src.credential_report import get_credential_report

MOCK_PASSWORD = "test_password"


def test_get_credential_report_no_users(iam_client):
    report = get_credential_report(iam_client)

    assert len(report.users) == 0


def test_get_credential_report_users(iam_client):
    iam_client.create_user(UserName="test_1")
    iam_client.create_user(UserName="test_2")
    iam_client.create_login_profile(UserName="test_2", Password=MOCK_PASSWORD)
    iam_client.create_user(UserName="test_3")
    iam_client.create_access_key(UserName="test_3")

    report = get_credential_report(iam_client)

    assert len(report.users) == 3
    assert report.users[0].username == "test_1"
    assert report.users[0].password_enabled == False
    assert report.users[1].username == "test_2"
    assert report.users[1].password_enabled == True
    assert report.users[2].username == "test_3"
    assert report.users[2].password_enabled == False
    assert report.users[2].access_key_1_active == True
