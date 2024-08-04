# Book Review Project

## Overview

Book Review is a Django-based web application

## Features

-   **User Creation**: Users can register for an account.
-   **Authentication and Authorization**: Secure login and access control.
-   **CRUD Operations for Reviews**: Users can create, read, update, and delete book reviews.
-   **Unit Testing**: Each app includes unit tests to verify functionality.

## Installation Guide

Follow these steps to set up and run the Book Review project locally.

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)

### Steps

1. Clone the Repository

    ```bash
    git clone https://github.com/shyarnis/bookReview.git
    cd bookReview
    ```

2. Create a Virtual Environment
    ```bash
    python3 -m venv venv
    ```
3. Activate the Virtual Environment
    - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
    - On macOS and Linux
    ```bash
    source venv/bin/activate
    ```
4. Install Requirements
    ```bash
    pip install -r requirements.txt
    ```
5. Generate a Secret Key
    ```bash
    python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_urlsafe()}')" > .env
    ```
6. Make Migrations
    ```bash
    python3 manage.py makemigrations
    ```
7. Migrate the Database
    ```bash
    python3 manage.py migrate
    ```
8. Run the Server
    ```bash
    python3 manage.py runserver
    ```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser to view the application.

## Runing Tests

To run unit tests for the project, use the following command:

```bash
./manage.py <app_name>.tests
```

More about running tests on [official documentation.](https://docs.djangoproject.com/en/5.0/topics/testing/overview/#running-tests)
