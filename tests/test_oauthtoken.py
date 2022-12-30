import pytest
from httpx import Response

from checkedid import errors
from checkedid.client import Client


def test_oauthtoken(client: Client, access_token_mock):
    response = client.oauth_token("password", "superuser", "password")

    assert response.access_token


def test_oauthtoken_with_error(client: Client, respx_mock):
    respx_mock.post("").mock(return_value=Response(status_code=403))

    with pytest.raises(errors.CheckedIDAuthenticationError):
        client.oauth_token("password", "error", "error")
