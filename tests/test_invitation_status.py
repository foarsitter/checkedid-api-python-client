import pytest
from httpx import Response

from checkedid import errors


def test_invitation_status(auth_client, respx_mock):
    invitation_code = "4ZCNXF"

    respx_mock.get("").mock(
        return_value=Response(
            status_code=200,
            json={"CustomerCode": 100029, "InvitationCode": invitation_code},
        )
    )

    response = auth_client.invitation_status(invitation_code)

    assert response.CustomerCode == 100029
    assert response.InvitationCode == invitation_code


def test_invitation_status_not_found(auth_client, respx_mock):
    respx_mock.get("").mock(return_value=Response(status_code=404))

    with pytest.raises(errors.CheckedIDNotFoundError):
        auth_client.invitation_status("15IMN4")
