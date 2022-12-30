from json import JSONDecodeError
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

import httpx
from httpx import Request
from httpx import Response

from . import models
from .errors import CheckedIDAuthenticationError
from .errors import CheckedIDError
from .errors import CheckedIDNotFoundError
from .errors import CheckedIDValidationError


_T = TypeVar("_T")


class Client:
    ERROR_RESPONSE_MAPPING: Dict[int, Type[CheckedIDError]] = {
        422: CheckedIDValidationError,
        403: CheckedIDAuthenticationError,
        404: CheckedIDNotFoundError,
    }

    def __init__(self, customer_code: str, base_url: str = "https://api.checkedid.eu/"):
        self.httpx = httpx.Client(base_url=base_url, auth=self.authenticate_request)
        self.access_token: Optional[str] = None
        self.customer_code = customer_code

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

    def oauth_token(
        self, grant_type: str, username: str, password: str
    ) -> Optional[models.OAuthToken]:
        response = self.httpx.post(
            "/oauth/token",
            data={"grant_type": grant_type, "username": username, "password": password},
        )

        typed_response = self.process_response(response, models.OAuthToken)

        if typed_response:
            self.access_token = typed_response.access_token

            return typed_response
        return None

    def invitation_status(self, invitation_code: str) -> Optional[models.Invitation]:
        response: Response = self.httpx.get(
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

        response: Response = self.httpx.post(
            "/invitations",
            json=obj.dict(),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

        return self.process_response(response, models.CustomerDetails)

    def invitation_delete(self, invitation_code: str) -> bool:
        response: Response = self.httpx.delete(
            f"/invitation/{self.customer_code}/{invitation_code}",
            headers={"Accept": "application/json"},
        )

        if response.status_code == 200:
            return True

        self.handle_error_response(response)

        return False

    def dossier(self, dossier_number: str) -> Optional[models.ReportResponse]:
        response = self.httpx.get(f"/report/{dossier_number}")

        return self.process_response(response, models.ReportResponse)

    def dossier_with_scope(
        self, dossier_number: str, scope: str
    ) -> Optional[models.ReportDataV3]:
        response = self.httpx.get(f"/reportdata/{dossier_number}/{scope}")

        return self.process_response(response, models.ReportDataV3)

    def handle_error_response(self, response: Response) -> None:
        if response.status_code == 400:
            raise CheckedIDValidationError(
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

    def map_exception(self, response: Response) -> Type[CheckedIDError]:
        exception_type = self.ERROR_RESPONSE_MAPPING.get(
            response.status_code, CheckedIDError
        )
        return exception_type
