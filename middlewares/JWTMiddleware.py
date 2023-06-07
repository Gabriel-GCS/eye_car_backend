from fastapi import Header, HTTPException
from services.AuthService import AuthService

authService = AuthService()

async def token_verify(authorization: str = Header(default='')):
    if not authorization.split(' ')[0] == 'Bearer':
        raise HTTPException(status_code=401, detail="Token necessary to authenticate.")

    token = authorization.split(' ')[1]

    payload = authService.decode_jwt(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    return payload