from typing import Optional
from pydantic import BaseModel
from src.domain.v1.type.AccountValueType import (
    AccountId
)


class AuthorizationToken(BaseModel):
    sub: str
    iss: str
    aud: str
    exp: int
    iat: int
    scope: Optional[str] = None
    jti: Optional[str] = None
    nonce: Optional[str] = None


class AuthorizationCode(BaseModel):
    code: str
    client_id: str
    state: str
    scope: Optional[str] = None


class Credential(BaseModel):
    account_id: AccountId
    scope: Optional[str] = None
    token: str