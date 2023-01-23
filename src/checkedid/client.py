from json import JSONDecodeError
from types import TracebackType
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

import httpx
from httpx import Request
from httpx import Response
from httpx._types import URLTypes

from . import endpoints
from . import errors
from . import models


_T = TypeVar("_T")


class BaseClient:
    ERROR_RESPONSE_MAPPING: Dict[int, Type[errors.CheckedIDError]] = {
        422: errors.CheckedIDValidationError,
        403: errors.CheckedIDAuthenticationError,
        404: errors.CheckedIDNotFoundError,
    }

    def __init__(self, customer_code: str, base_url: str = "https://api.checkedid.eu/"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.customer_code = customer_code
        self.create_client(base_url)

    def create_client(self, base_url: URLTypes) -> None:
        raise NotImplementedError

    def authenticate_request(self, request: Request) -> Request:
        if self.access_token:
            request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request

    def process_response(
        self, response: Response, model: Type[_T], status_code_success: int = 200
    ) -> Optional[_T]:
        if response.status_code == status_code_success:
            return model(**response.json())

        self.handle_error_response(response)

        return None

    def handle_error_response(self, response: Response) -> None:
        if response.status_code == 400:
            raise errors.CheckedIDValidationError(
                response.text, status_code=response.status_code
            )

        try:
            json = response.json()
        except JSONDecodeError:
            json = {"message": response.text}

        json["status_code"] = response.status_code

        exception_type = self.map_exception(response)
        raise exception_type(
            status_code=response.status_code, json=json, message="Error from server"
        )

    def map_exception(self, response: Response) -> Type[errors.CheckedIDError]:
        exception_type = self.ERROR_RESPONSE_MAPPING.get(
            response.status_code, errors.CheckedIDError
        )
        return exception_type


class Client(BaseClient):
    client: httpx.Client

    def oauth_token(
        self, grant_type: str, username: str, password: str
    ) -> Optional[models.OAuthToken]:
        response = self.client.post(
            "/oauth/token",
            data={"grant_type": grant_type, "username": username, "password": password},
        )

        typed_response = self.process_response(response, models.OAuthToken)

        if typed_response:
            self.access_token = typed_response.access_token

            return typed_response
        return None

    def __init__(self, customer_code: str, base_url: str = "https://api.checkedid.eu/"):
        super().__init__(customer_code, base_url)

    def create_client(self, base_url: URLTypes) -> None:
        self.client = httpx.Client(base_url=base_url, auth=self.authenticate_request)

    def invitation_status(self, invitation_code: str) -> Optional[models.Invitation]:
        response: Response = self.client.get(
            f"/result/status/{invitation_code}",
            headers={"Accept": "application/json"},
        )

        return self.process_response(response, models.Invitation)

    def invitations_create(
        self, invitations: List[models.CreateInvitationRequest]
    ) -> Optional[models.CustomerDetails]:
        obj = models.CreateInvitationDetails(
            CustomerCode=self.customer_code, Invitations=invitations
        )

        response: Response = self.client.post(
            "/invitations",
            json=obj.dict(),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

        return self.process_response(response, models.CustomerDetails)

    def invitation_delete(self, invitation_code: str) -> bool:
        response: Response = self.client.delete(
            f"/invitation/{self.customer_code}/{invitation_code}",
            headers={"Accept": "application/json"},
        )

        if response.status_code == 200:
            return True

        self.handle_error_response(response)

        return False

    def dossier(self, dossier_number: str) -> Optional[models.ReportResponse]:
        response = self.client.get(f"/report/{dossier_number}")

        return self.process_response(response, models.ReportResponse)

    def dossier_with_scope(
        self, dossier_number: str, scope: str
    ) -> Optional[models.ReportDataV3]:
        response = self.client.get(f"/reportdata/{dossier_number}/{scope}")

        return self.process_response(response, models.ReportDataV3)


class ClientAsync(BaseClient):
    """for asyncio"""

    client: httpx.AsyncClient

    def __init__(self, customer_code: str, base_url: str = "https://api.checkedid.eu/"):
        super().__init__(customer_code, base_url)

    async def oauth_token(
        self, grant_type: str, username: str, password: str
    ) -> Optional[models.OAuthToken]:
        response = await self.client.post(
            "/oauth/token",
            data={"grant_type": grant_type, "username": username, "password": password},
        )

        typed_response = self.process_response(response, models.OAuthToken)

        if typed_response:
            self.access_token = typed_response.access_token

            return typed_response
        return None

    def create_client(self, base_url: URLTypes) -> None:
        self.client = httpx.AsyncClient(base_url=base_url)

    async def dossier(self, dossier_number: str) -> Optional[models.ReportResponse]:
        response = await self.client.get(
            url=endpoints.DossierEndpoint.url(dossier_number=dossier_number)
        )

        return self.process_response(response, endpoints.DossierEndpoint.response)

    async def close(self) -> None:
        if self.client:
            await self.client.aclose()

    def open(self) -> None:
        self.create_client(self.base_url)

    async def __aenter__(self) -> "ClientAsync":
        """Open the httpx client"""
        self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        """Close the httpx client"""
        await self.close()
