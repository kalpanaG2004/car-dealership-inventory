import re

from pydantic import BaseModel, Field, field_validator

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(email):
            raise ValueError("Enter a valid email address")
        return email


class LoginRequest(RegisterRequest):
    pass


class UserResponse(BaseModel):
    id: str
    email: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VehicleCreate(BaseModel):
    make: str = Field(min_length=1, max_length=80)
    model: str = Field(min_length=1, max_length=80)
    category: str = Field(min_length=1, max_length=80)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class VehicleResponse(VehicleCreate):
    id: str
