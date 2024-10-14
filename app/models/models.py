from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_superuser: bool = False
    is_active: bool = True
    is_staff: bool = False
    is_admin: bool = False
    date_joined: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str
    iat: int
    exp: int