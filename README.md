# lms
Library management system

# API Documentation

## Setup

To set up the server, run the following Docker Compose commands to build, migrate, and start the server:

```sh
docker-compose up --build -d
```
### Base URL
```http://localhost:8000/library/api/v1/```

### Register User
Register a new user using a username and password.

- **URL:** `/api/v1/register`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "username": "new_user",
        "password": "secure_password"
    }
    ```
- **Response:**
    - Status: 201 Created
    - Body: User details (user ID)
    - Cookies: Session ID and CSRF token

### User Login
Log in using a registered username and password.

- **URL:** `/api/v1/login`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "username": "existing_user",
        "password": "existing_password"
    }
    ```
- **Response:**
    - Status: 200 OK
    - Body: User details (user ID)
    - Cookies: Session ID and CSRF token

### Books
- **Endpoint: /api/v1/books/**

    Method: GET

    Description: Retrieve a list of all books.

    Response:

    200 OK: Returns a list of books.

- **Endpoint: /api/v1/books/**

    Method: POST

    Description: Create a new book.

    Headers:

    cookies: sessionid:your_session_id

    X-CSRFToken: your_csrf_token

    Request Body:

    ```json
    {
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "YYYY-MM-DD"
    }
    ```
    Response:

    201 Created: Successfully created a book.

    400 Bad Request: Invalid input.

- **Endpoint: /api/v1/books/{id}/**

    Method: DELETE

    Description: Delete a book by ID.

    Headers:

    cookies: sessionid:your_session_id

    X-CSRFToken: your_csrf_token
    

    **Response**:

    204 book_id: Successfully deleted.
    
    404 Not Found: Book not found.

- **Endpoint: /api/v1/books/{id}/borrow/**

    Method: POST

    Description: Brrow a book.

    Headers:

    cookies: sessionid: your_session_id

    X-CSRFToken: your_csrf_token

    **Request Body**:

    ```json
    {
    "borrower_name":"Any Name"
    }
    ```

    **Response**:

    201 
    
    ```json
    {
    "id": 1,
    "borrower_name": "Ahmed",
    "borrow_date": "2024-07-08",
    "return_date": null,
    "book": 2
    }
    ```

### Use The same pattern for borrow-records