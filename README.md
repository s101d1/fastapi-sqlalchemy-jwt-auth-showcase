# <b>FastAPI + SQLAlchemy 2.0 + MySQL + JWT Authentication + Memory Caching</b>

A demonstration of a Python REST API server with JWT Authentication and Memory Caching using FastAPI framework.

Database connection is handled by SQLAlchemy 2.0.x library.

JWT authentication is handled by [python-jose](https://pypi.org/project/python-jose/) library.

The caching is handled by [cachetools](https://pypi.org/project/cachetools/) library.

## <b> Getting Started </b>

### Requirements

* Python v3.10.x or newer.
* MySQL database v8.0 or newer with an empty database/schema prepared.

### How to run the app

* Initialize and activate virtual environment inside the project folder:
    ```bash
    $ python3 -m venv venv
    $ . venv/bin/activate
    ```
* Install the required libraries:

    ```bash
    $ pip3 install -r requirements.txt
    ```

* Modify the `DB_URL` environment variable in `.env` file according to your database.

* Run the server:
    ```bash
    $ uvicorn main:app --reload
    ```
    The server will run at http://localhost:8000

    The swagger API docs can be accessed at http://localhost:8000/docs

    The tables in database will be created automatically if they don't exist yet when the server starts or reloaded.

## Endpoints information

1. `POST /auth/signup` (Signup endpoint)
   * Accepts `email`, `password`, and `confirm_password` values.
   * Returns a token (JWT) with 1 hour expiry time if successful.

2. `POST /auth/login` (Login endpoint)
   * Accepts `email` and `password` values.
   * Returns a token (JWT) with 1 hour expiry time if successful.

3. `POST /posts` (Add New Post endpoint)
   * Endpoint is protected by JWT authentication (`Bearer <token>` header is required).
   * Accepts `text` value, and it will create a new Post that belongs to the authenticated User if successful.
   * Payload size is limited to 1 MB.

4. `GET /posts` (Get Posts endpoint)
   * Endpoint is protected by JWT authentication (`Bearer <token>` header is required).
   * Returns all user's posts.
   * Successful response is cached for 5 minutes for the authenticated user. Cache will be invalidated if user adds a new post or deletes a post.

5. `DELETE /posts/:id` (Delete Post endpoint)
   * Endpoint is protected by JWT authentication (`Bearer <token>` header is required).
   * Deletes a Post by the id that belongs to the authenticated User.
