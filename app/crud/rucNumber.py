from pydantic import BaseModel
from typing import Optional

class RucNumber(BaseModel):
    ruc_number: str