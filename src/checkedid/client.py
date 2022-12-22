from json import JSONDecodeError
from typing import List
from typing import Optional
from typing import Union

import httpx
from httpx import Request
from httpx import Response

from . import models
from .models.generated import CustomerDetails


class Client:
    def __init__(self, customer_code: str, base_url: str = "https://api.checkedid.eu/"):
        self.httpx = httpx.Client(base_url=base_url, auth=self.authenticate_request)
        self.access_token: Optional[str] = None
        self.customer_code = customer_code

    def authenticate_request(self, request: Request) -> Request:
        if self.access_token:
            request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request

    def oauth_token(
        self, grant_type: str, username: str, password: str
    ) -> Union[models.OAuthToken, models.ErrorResponse]:
        response = self.httpx.post(
            "/oauth/token",
            data={"grant_type": grant_type, "username": username, "password": password},
        )

        if response.status_code == 200:
            typed_response = models.OAuthToken(**response.json())

            self.access_token = typed_response.access_token

            return typed_response
        else:
            return self.handle_error_response(response)

    def invitation_status(
        self, invitation_code: str
    ) -> Union[models.Invitation, models.ErrorResponse]:
        response: Response = self.httpx.get(
            f"/result/status/{invitation_code}",
            headers={"Accept": "application/json"},
        )

        if response.status_code == 200:
            return models.Invitation(**response.json())
        else:
            return self.handle_error_response(response)

    def invitations_create(
        self, invitations: List[models.CreateInvitationRequest]
    ) -> Union[CustomerDetails, models.ErrorResponse]:
        obj = models.CreateInvitationDetails(
            CustomerCode=self.customer_code, Invitations=invitations
        )

        response: Response = self.httpx.post(
            "/invitations",
            json=obj.dict(),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

        if response.status_code == 200:
            return models.CustomerDetails(**response.json())
        else:
            return self.handle_error_response(response)

    def invitation_delete(
        self, invitation_code: str
    ) -> Union[models.ErrorResponse, bool]:
        response: Response = self.httpx.delete(
            f"/invitation/{self.customer_code}/{invitation_code}",
            headers={"Accept": "application/json"},
        )

        if response.status_code == 200:
            return True
        else:
            return self.handle_error_response(response)

    def handle_error_response(self, response: Response) -> models.ErrorResponse:
        try:
            json = response.json()
        except JSONDecodeError:
            json = {"message": response.text}

        json["status_code"] = response.status_code
        return models.ErrorResponse(**json)
