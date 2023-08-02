from fastapi import status, HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

from app.settings import settings

auth_header = HTTPBearer()


async def verify_token(token: HTTPAuthorizationCredentials = Security(auth_header)):
    if token.credentials != settings.AAPI_TOKEN.get_secret_value():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return token
