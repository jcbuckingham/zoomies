# Zoomies

A URL-shortening service.  

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jcbuckingham/zoomies.git
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

6. Access the application in your browser at `http://localhost:8000`.

## Usage

See API Documentation at `http://localhost:8000/swagger` for authentication usage and CRUD for short_urls

For incoming traffic that should be routed with a shortened url, use `http://localhost:8000/<short code>`

## Features

TBD

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


