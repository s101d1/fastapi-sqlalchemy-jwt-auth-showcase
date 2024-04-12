from fastapi import APIRouter, Response, status

from controllers.auth import signup, login
from models.dto.auth import LoginData, SignupData

router = APIRouter(prefix="/auth")


@router.post("/signup", tags=["auth"])
async def signup_route(data: SignupData, response: Response):
    """
        Signup route
    """
    response.status_code = status.HTTP_201_CREATED
    return signup(data)


@router.post("/login", tags=["auth"])
async def login_route(data: LoginData):
    """
        Login route
    """
    return login(data)
