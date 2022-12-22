from httpx import Response


def test_dossier(auth_client):
    response = auth_client.dossier("100029-0000031")

    assert response.DossierNumber == "100029-0000031"


def test_dossier_with_error(auth_client, respx_mock):
    respx_mock.get("").mock(return_value=Response(status_code=404))
    response = auth_client.dossier("does-not-exist")

    assert response.status_code == 404


def test_dossier_with_scope(auth_client):
    response = auth_client.dossier_with_scope("100029-0000031", "10")

    assert response.DossierNumber == "100029-0000031"
    assert response.Authority == "Burg. van Groningen"


def test_dossier_with_scope_with_error(auth_client, respx_mock):
    respx_mock.get("").mock(return_value=Response(status_code=404))
    response = auth_client.dossier_with_scope("does-not-exist", "10")

    assert response.status_code == 404
