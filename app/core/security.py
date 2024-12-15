from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_jwt(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    return jwt.encode(payload=to_encode, key=settings.secret_jwt, algorithm=settings.algorithm_jwt)


def decode_jwt(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(jwt=token, key=settings.secret_jwt, algorithms=settings.algorithm_jwt)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token signature doesn't match",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_user_from_token(payload: dict = Depends(decode_jwt)) -> str:
    return payload["sub"]