from checkedid.models import CreateInvitationRequest


def test_invitations_create(auth_client, employee_code):
    details: CreateInvitationRequest = CreateInvitationRequest.construct()
    details.EmployeeCode = employee_code
    details.InviteeEmail = "info@jelmert.nl"
    details.InviteeFirstName = "Jelmer"
    details.InviteeLastName = "Draaijer"
    details.Validity = 20
    details.AppFlow = "10"
    details.PreferredLanguage = "nl"

    response = auth_client.invitations_create([details])

    assert response.CustomerCode == 100029
    assert len(response.Invitations) == 1

    assert auth_client.invitation_delete(response.Invitations[0].InvitationCode) is True
