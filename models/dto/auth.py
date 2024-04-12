from pydantic import BaseModel, EmailStr


class SignupData(BaseModel):
    """
        Signup data model
    """
    email: EmailStr
    password: str
    confirm_password: str


class LoginData(BaseModel):
    """
        Login data model
    """
    email: EmailStr
    password: str
