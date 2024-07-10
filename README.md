# Social-Media-Management

# Project Overview
This project is a backend implementation for a social media management system built using FastAPI and PostgreSQL. It includes functionality for user authentication, image storage, and managing social media posts. The project also uses SQLAlchemy for ORM (Object-Relational Mapping) and Alembic for database migrations.

# Features
User Authentication: Secure user login and registration using OAuth2 with password hashing.
Post Management: Allows users to create, read, update, and delete social media posts.
Image Storage: Efficiently stores images as large binaries in the database.
Followers Management: Keeps track of user followers and their counts.


# Project Structure

    FASTAPI/
    │
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── utils.py
    │   ├── oauth2.py
    │   ├── email_utils.py
    │   ├── routers/
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── messages.py
    │   │   ├── users.py
    │   │   ├── votes.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   ├── security.py
    │   ├── tests/
    │   │   ├── __init__.py
    │   │   ├── test_auth.py
    │   │   ├── test_messages.py
    │   │   ├── test_users.py
    │   │   ├── test_votes.py
    │
    ├── migrations/
    │   ├── versions/
    │   │   ├── __init__.py
    │   ├── env.py
    │   ├── script.py.mako
    │   ├── alembic.ini
    │
    ├── venv/
    │   ├── ... (virtual environment files and directories)
    │
    ├── requirements.txt
    ├── README.md
    └── .env




# Prerequisites
    Python 3.9+
    PostgreSQL
    Git



# Install the dependencies:

    pip install -r requirements.txt
    Set up the database:

    Update the DATABASE_URL in app/core/config.py with your PostgreSQL credentials.

    # Run Alembic migrations to set up the database schema:



    alembic upgrade head
    Run the application:

    uvicorn app.main:app --reload


# Authentication
    Login:



    POST /login
    Request Body:
    
    json
    
    {
      "username": "user@example.com",
      "password": "yourpassword"
    }
    Response:
    
    json
    {
      "access_token": "token",
      "token_type": "bearer",
      "followers_count": 10
    }
# Posts
Create a Post:

    http
    
    POST /posts/
    Request Body:
    
    json
    
    {
      "title": "My Post",
      "content": "This is my post content.",
      "image": "base64_encoded_image_string"
    }
    Response:
    
    json
    
    {
      "id": 1,
      "title": "My Post",
      "content": "This is my post content.",
      "image_url": "http://example.com/image/1"
    }
# Error Handling
    The application uses FastAPI's built-in error handling to provide clear and consistent error messages. Common error responses include:
    
    400 Bad Request for validation errors.
    401 Unauthorized for authentication errors.
    404 Not Found for missing resources.
# Contributing
    Contributions are welcome! Please fork the repository and submit a pull request.

# License
    This project is licensed under the MIT License. See the LICENSE file for details.

# Contact
    For questions or suggestions, feel free to reach out at your-email@example.com.
