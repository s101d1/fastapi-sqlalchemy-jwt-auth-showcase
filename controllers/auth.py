from fastapi import HTTPException, status
from sqlalchemy import select

from database import session
from models.dto.auth import LoginData, SignupData
from models.user import User
from utils.auth import get_hashed_password, verify_password, create_access_token


def signup(data: SignupData):
    """
        Signup handler to create a new user and return an access token
    """

    # some validations
    existing_user = session.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already exists")

    if data.password != data.confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Confirm Password doesn't match")

    # hash the password with bcrypt
    hashed_password = get_hashed_password(data.password)

    # create the user
    new_user = User(email=data.email, password=hashed_password)
    session.add(new_user)
    session.commit()

    # generate access token for the user
    access_token = create_access_token({"email": data.email, "user_id": new_user.id})

    return {"message": "User created", "token": access_token, "user_id": new_user.id}


def login(data: LoginData):
    """
        Login handler to generate and return an access token
    """

    # retrieve the user and perform some validations
    user = session.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email or password")

    # generate access token for the user
    access_token = create_access_token({"email": data.email, "user_id": user.id})

    return {"message": "Login successful", "token": access_token, "user_id": user.id}
