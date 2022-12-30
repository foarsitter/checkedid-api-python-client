import pytest
from httpx import Response

from checkedid import errors
from checkedid.models import CreateInvitationDetails
from checkedid.models import CreateInvitationRequest


def test_invitations_create_and_delete(
    auth_client, employee_code, respx_mock, customer_code
):
    details: CreateInvitationRequest = CreateInvitationRequest.construct()
    details.EmployeeCode = employee_code
    details.InviteeEmail = "info@jelmert.nl"
    details.InviteeFirstName = "Jelmer"
    details.InviteeLastName = "Draaijer"
    details.Validity = 20
    details.AppFlow = "10"
    details.PreferredLanguage = "nl"

    respx_mock.post("").mock(
        return_value=Response(
            status_code=200,
            json=CreateInvitationDetails(
                CustomerCode=customer_code, Invitations=[details]
            ).dict(),
        )
    )

    respx_mock.delete("").mock(return_value=Response(status_code=200))

    response = auth_client.invitations_create([details])

    assert response.CustomerCode == 100029
    assert len(response.Invitations) == 1

    assert auth_client.invitation_delete(response.Invitations[0].InvitationCode) is True


def test_invitations_create_with_error(auth_client, respx_mock):
    respx_mock.post("").mock(return_value=Response(status_code=422))

    with pytest.raises(errors.CheckedIDValidationError):
        auth_client.invitations_create([CreateInvitationRequest.construct()])


def test_invitation_delete_with_error(auth_client, respx_mock):
    respx_mock.delete("").mock(return_value=Response(status_code=404))
    with pytest.raises(errors.CheckedIDNotFoundError):
        auth_client.invitation_delete("xyz")
