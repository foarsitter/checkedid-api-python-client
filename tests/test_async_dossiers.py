import pytest

from checkedid.client import ClientAsync


@pytest.mark.asyncio
async def test_dossiers(customer_code, dossier_response_200):
    checkedid = ClientAsync(customer_code)

    async with checkedid as client:
        response = await client.dossier("999999-8888800")

        assert response.DossierNumber == "999999-8888800"
