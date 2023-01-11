from typing import Any
from typing import Optional
from typing import Type

from pydantic import BaseModel

from checkedid import models


class Endpoint:
    path: str
    request: Optional[Type[BaseModel]]
    response = Optional[Type[BaseModel]]


class DossierEndpoint(Endpoint):
    path = "/report/{dossier_number}"
    request = None
    response = models.ReportResponse

    @classmethod
    def url(cls, **kwargs: Any) -> str:
        return cls.path.format(**kwargs)
