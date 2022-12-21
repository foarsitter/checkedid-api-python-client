import os

import pytest

from checkedid.client import Client


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


@pytest.fixture()
def auth_client(client: Client) -> Client:
    response = client.oauth_token(
        "password", os.getenv("CHECKEDID_USERNAME"), os.getenv("CHECKEDID_PASSWORD")
    )

    assert response.access_token

    return client
