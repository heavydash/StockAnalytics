import datetime

import jwt

from config import settings


def create_jwt_token(user_id: int, email: str, secret_key: str = settings.JWT_SECRET_KEY) -> str:
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_LIFETIME)
    }

    token = jwt.encode(payload, secret_key, settings.JWT_ALGORITHM)

    return token
