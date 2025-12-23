import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

SECRET = "my-secret"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

def sign_jwt(user_id: int) -> TokenResponse:
    now = time.time()
    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": str(user_id),
        "aud": "curso-fastapi",
        "exp": now + (60 * 30),
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return TokenResponse(access_token=token)


async def decode_jwt(token: str) -> AccessToken | None:
    try:
        decoded = jwt.decode(token, SECRET, audience="curso-fastapi", algorithms=[ALGORITHM],)
        payload = AccessToken.model_validate(decoded)
        return payload if payload.exp >= time.time() else None
    except Exception as e:
        print("JWT decode error:", e)
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        credentials = await super().__call__(request)

        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Schema de autenticação inválido!")
        payload = await decode_jwt(credentials.credentials)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado.")
        print("Authorization header:", request.headers.get("Authorization"))
        return payload


async def get_current_user(token: Annotated[AccessToken, Depends(JWTBearer())]) -> dict[str, int]:
    return {"user_id": int(token.sub)}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    return current_user