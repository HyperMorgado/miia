from pydantic import BaseModel, EmailStr, Field

class RegisterUserDTO(BaseModel):
    name: str
    email: EmailStr
    document: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6)