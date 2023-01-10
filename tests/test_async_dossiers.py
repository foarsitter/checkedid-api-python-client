import pytest

from checkedid.client import ClientAsync


@pytest.mark.asyncio
async def test_dossiers(customer_code, dossier_response_200):
    client = ClientAsync(customer_code)

    with client as client:
        response = await client.dossier("999999-8888800")

        assert response.DossierNumber == "999999-8888800"
