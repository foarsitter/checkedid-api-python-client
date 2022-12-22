def test_invitation_status(auth_client):
    response = auth_client.invitation_status("15IMN4")

    assert response.CustomerCode == 100029
