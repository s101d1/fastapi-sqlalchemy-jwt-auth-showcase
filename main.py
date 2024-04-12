from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse

from database import engine
from models.base import Base
from models.post import Post
from models.user import User
from routes.auth import router as auth_router
from routes.posts import router as posts_router
from content_size_limit_asgi import ContentSizeLimitMiddleware


def init_db():
    """
        Initialize database by creating the tables if they don't exist yet (for development purpose only)
    """
    Base.metadata.create_all(engine)
    print("Initialized the database")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
        FastAPI lifespan manager
    """
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc):
    """
        Reformat RequestValidationError json response with message field on top
    """
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"message": exc.errors()[0]["msg"], "errors": jsonable_encoder(exc.errors())})


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(_request, exc):
    """
        Reformat ResponseValidationError json response with message field on top
    """
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"message": exc.errors()[0]["msg"], "errors": jsonable_encoder(exc.errors())})


# Add a middleware to ensure the request payload doesn't exceed 1 MB or else http error 400 response will be returned
app.add_middleware(ContentSizeLimitMiddleware, max_content_size=1024 * 1024)

app.include_router(auth_router)
app.include_router(posts_router)
