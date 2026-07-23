from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.database import get_database
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, database: Database = Depends(get_database)) -> UserResponse:
    users = database.users
    users.create_index("email", unique=True)

    try:
        result = users.insert_one(
            {
                "email": payload.email,
                "password_hash": hash_password(payload.password),
                "role": "user",
            }
        )
    except DuplicateKeyError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from error

    return UserResponse(id=str(result.inserted_id), email=payload.email, role="user")


@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest, database: Database = Depends(get_database)) -> TokenResponse:
    user = database.users.find_one({"email": payload.email})
    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return TokenResponse(access_token=create_access_token(str(user["_id"]), user["role"]))
