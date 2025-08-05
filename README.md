# NutriChain Logistics - Reports Microservice

This microservice is part of the NutriChain Logistics system. Its sole responsibility is to generate and provide reports based on the data produced by other microservices (Warehouse, Store). It's a read-only service designed for performance, security, and scalability.

## Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database Connector**: SQLAlchemy
- **Database**: PostgreSQL (Designed for Supabase)
- **Server**: Uvicorn
- **Containerization**: Docker
- **Key Libraries**: Pydantic, python-jose (JWT), slowapi (Rate Limiting), fastapi-i18n.

## Features

- **JWT Security**: All endpoints are protected and require a valid Bearer token.
- **API Versioning**: All endpoints are prefixed with `/api/v1`.
- **CORS**: Production-ready CORS configuration via environment variables.
- **DTOs**: Uses Pydantic models for request and response validation, ensuring a clear data contract.
- **Service Layer**: Business logic is separated from the API layer.
- **Rate Limiting**: Protects the API from abuse.
- **Idempotency**: Prevents duplicate report generation requests via the `Idempotency-Key` header.
- **Internationalization (i18n)**: Supports English (`en`) and Spanish (`es`) for messages.
- **Logging**: Structured logging for requests and errors.
- **Dockerized**: Ready for containerized deployment.
- **SOLID & Clean Code**: The project structure follows clean architecture principles.

## Prerequisites

- Docker and Docker Compose
- A Supabase account (or any other PostgreSQL provider)

## Setup and Installation

1.  **Clone this repository:**

2.  **Set up Supabase:**
    - Create a new project on [Supabase](https://supabase.com).
    - Go to `Project Settings` > `Database`.
    - Under `Connection info`, copy the **URI** string.
    - **Important**: This service assumes that the tables (`products`, `stock_items`, `inventory_movements`, `orders`, `order_items`) already exist in your database, as they are managed by other microservices. You may need to run a seeding script or migrations to create them for testing.

3.  **Configure Environment Variables:**
    - Create a `.env` file by copying the example:
      ```bash
      cp .env.example .env
      ```
    - Edit the `.env` file and fill in the required values:
      - `DATABASE_URL`: The Supabase connection URI you copied.
      - `JWT_SECRET_KEY`: A long, random, and secret string for JWT validation.
      - `BACKEND_CORS_ORIGINS`: A JSON array of allowed frontend origins (e.g., `'["http://localhost:3000", "https://your-frontend.com"]'`).

## Running the Service

### Using Docker (Recommended)

This is the simplest way to get the service running.

```bash
docker build -t nutrichain-reports .
docker run -p 8000:8000 --env-file .env nutrichain-reports
```

The service will be available at http://localhost:8000.

## Local Development (without Docker)

1- Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2- Install dependencies:
```bash
pip install -r requirements.txt
```

3- Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation
Once the application is running, the interactive API documentation (Swagger UI) is available at:
http://localhost:8000/docs
The ReDoc documentation is available at:
http://localhost:8000/redoc

## Running Tests
To run the automated tests, use pytest:
```bash
pytest
```
