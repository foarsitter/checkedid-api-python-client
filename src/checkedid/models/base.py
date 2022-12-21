from typing import List
from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int
    message: Optional[str]
    Errors: Optional[List[str]]
