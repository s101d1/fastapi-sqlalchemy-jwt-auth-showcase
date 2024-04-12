import os
from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError

from utils.auth import ALGORITHM

auth_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
        Decode and retrieve user id from the access token
    """
    try:
        payload = jwt.decode(
            token.credentials, os.environ["JWT_SECRET_KEY"], algorithms=[ALGORITHM]
        )
        exp = payload.get("exp")

        # validate the expiry date
        if datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return UUID(payload.get("user_id"))
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
