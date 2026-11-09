from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
class RefreshTokenRequest(BaseModel):
    refresh_token: str