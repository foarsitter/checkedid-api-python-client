from typing import Type

from pydantic import BaseModel

from checkedid import models


class Endpoint:
    path: str
    request: Type[BaseModel]
    response = Type[BaseModel]


class DossierEndpoint(Endpoint):
    path = "/report/{dossier_number}"
    request = None
    response = models.ReportResponse

    @classmethod
    def url(cls, **kwargs):
        return cls.path.format(**kwargs)
