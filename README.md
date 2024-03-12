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

## Run with Kubernetes

1. Have Kubernetes installed (I use Docker for Desktop), Postgres (I use the Postgres app), and ensure you have kubectl available.

2. Navigate to project root and deploy Postgres and Zoomies: 

    ```bash
    kubectl apply -f kube_postgres_deploy.yml
    kubectl apply -f kube_zoomies_deploy.yml
    kubectl port-forward deployment/zoomies-deploy 8000:8000
    ```

3. Verify that the app is available at `http://localhost:8000`

## Usage

See API Documentation at `http://localhost:8000/openapi` for a json version of the documentation

For incoming traffic that should be routed with a shortened url, use `http://localhost:8000/<short code>`

## Features

TBD

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


