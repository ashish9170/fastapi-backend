from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TwoFAVerifySchema(BaseModel):
    email: EmailStr
    code: str