import os

import pytest
from httpx import Response

from checkedid.client import Client
from checkedid.models import ErrorResponse


@pytest.fixture
def customer_code() -> str:
    return os.getenv("CHECKEDID_CUSTOMER_CODE")


@pytest.fixture
def employee_code() -> str:
    return os.getenv("CHECKEDID_EMPLOYEE_CODE")


@pytest.fixture
def client(customer_code) -> Client:
    client = Client(customer_code)
    return client


@pytest.fixture
def access_token_mock(respx_mock):
    respx_mock.post("").mock(
        return_value=Response(
            status_code=200,
            json={
                "access_token": "abc",
                "expires_in": 3600,
                "token_type": "Bearer",
                "refresh_token": "def",
            },
        )
    )


@pytest.fixture()
def auth_client(client: Client, access_token_mock) -> Client:
    response = client.oauth_token(
        "password", os.getenv("CHECKEDID_USERNAME"), os.getenv("CHECKEDID_PASSWORD")
    )

    if isinstance(response, ErrorResponse):
        raise Exception("Auth failed")

    assert response.access_token

    return client
