import os

from checkedid.client import Client


def test_oauthtoken(client: Client):
    response = client.oauth_token(
        "password", os.getenv("CHECKEDID_USERNAME"), os.getenv("CHECKEDID_PASSWORD")
    )

    assert response.access_token


def test_oauthtoken_with_error(client: Client):
    response = client.oauth_token("password", "error", "error")

    assert response.status_code == 400
