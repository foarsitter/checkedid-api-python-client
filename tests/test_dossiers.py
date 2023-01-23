import pytest
from httpx import Response

from checkedid import errors


def test_dossier(auth_client, respx_mock, dossier_response_200, dossier_number):
    response = auth_client.dossier(dossier_number)

    assert response.DossierNumber == dossier_number


def test_dossier_with_error(auth_client, respx_mock):
    respx_mock.get("").mock(return_value=Response(status_code=404))
    with pytest.raises(errors.CheckedIDError):
        auth_client.dossier("does-not-exist")


def test_dossier_with_scope(auth_client, respx_mock):
    dossier_number = "999999-8888800"
    respx_mock.get("").mock(
        return_value=Response(
            status_code=200,
            json={
                "DossierNumber": dossier_number,
                "ReportPDF": "",
                "Authority": "Burg. van Groningen",
            },
        )
    )
    response = auth_client.dossier_with_scope("100029-0000031", "10")

    assert response.DossierNumber == dossier_number
    assert response.Authority == "Burg. van Groningen"


def test_dossier_with_scope_with_error(auth_client, respx_mock):
    respx_mock.get("").mock(return_value=Response(status_code=404))

    with pytest.raises(errors.CheckedIDError):
        auth_client.dossier_with_scope("does-not-exist", "10")
