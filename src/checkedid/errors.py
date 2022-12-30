from typing import Any
from typing import Dict
from typing import Optional


class CheckedIDError(Exception):
    status_code: int
    json: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        message: str,
        status_code: int,
        json: Optional[Dict[str, Any]] = None,
        *args: str
    ):
        super().__init__(message, *args)
        self.status_code = status_code
        self.json = json


class CheckedIDValidationError(CheckedIDError):
    pass


class CheckedIDNotFoundError(CheckedIDError):
    pass


class CheckedIDAuthenticationError(CheckedIDError):
    pass
