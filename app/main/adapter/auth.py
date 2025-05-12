from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.shared.jwt.jwt_util import decode_access_token
from app.main.adapter.logger_adapter import logger

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        return payload  # ou carregue usuário do DB aqui
    except jwt.PyJWTError:
        logger.error("Invalid JWT token in dependency")
        raise HTTPException(status_code=401, detail="Invalid token")