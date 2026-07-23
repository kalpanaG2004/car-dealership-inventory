from typing import Any

import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pymongo.database import Database

from app.config import get_settings
from app.database import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), database: Database = Depends(get_database)
) -> dict[str, Any]:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            get_settings().jwt_secret_key,
            algorithms=[get_settings().jwt_algorithm],
        )
        subject = payload.get("sub")
        if not subject:
            raise credentials_error
        user_id = ObjectId(subject)
    except (jwt.PyJWTError, TypeError, ValueError):
        raise credentials_error

    user = database.users.find_one({"_id": user_id})
    if user is None:
        raise credentials_error

    return user
