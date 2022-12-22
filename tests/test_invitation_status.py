from httpx import Response


def test_invitation_status(auth_client):
    response = auth_client.invitation_status("15IMN4")

    assert response.CustomerCode == 100029


def test_invitation_status_not_found(auth_client, respx_mock):
    respx_mock.get("").mock(return_value=Response(status_code=404))
    response = auth_client.invitation_status("15IMN4")

    assert response.status_code == 404
