from pydantic import BaseModel, EmailStr, Field

class RegistrationIntiate(BaseModel):
    email: EmailStr

class RegistrationComplete(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

class TokenResponse(BaseModel):
    success: bool
    access_token: str
    token_type: str = "bearer"
    onboarding_complete: bool