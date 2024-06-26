from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt
from jwt import PyJWTError
from config import settings

class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if any(request.url.path.startswith(path) for path in settings.AUTH_FREE_PATHS):
            return await call_next(request)
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != 'bearer':
                    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                request.state.user = payload
            except (PyJWTError, ValueError):
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization header missing.")

        response = await call_next(request)
        return response
