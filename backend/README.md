# TranscriptV2 Backend

Backend API for the TranscriptV2 application, a platform for transcribing YouTube videos.

## Features

- User authentication with JWT
- Video search via YouTube Data API 
- Transcription management
  - Create and save transcription sessions
  - Compare user transcription against reference text
  - Calculate accuracy metrics
  - Track transcription history and statistics
- Subscription system with Stripe integration
  - Manage subscription plans (free tier and premium)
  - Handle subscription lifecycle events via webhooks
  - Track user usage against subscription limits
- PostgreSQL database with SQLAlchemy ORM
- Elasticsearch integration for advanced search

## Requirements

- Python 3.9+
- PostgreSQL 13+
- Docker (optional, for containerized development)

## Setup

1. Clone the repository

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`
```bash
cp .env.example .env
# Edit the .env file with your configuration
```

5. Initialize the database
```bash
alembic upgrade head
```

6. Start the development server
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Docker Setup

You can also run the backend with Docker:

```bash
docker build -t transcriptv2-backend .
docker run -p 8000:8000 --env-file .env transcriptv2-backend
```

Or use Docker Compose from the root directory:

```bash
docker-compose up backend
```

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Project Structure

- `app/`: Main application package
  - `api/`: API routes and dependencies
    - `endpoints/`: API endpoint definitions
    - `deps.py`: Dependency injection
  - `core/`: Core functionality (config, security)
  - `db/`: Database models and CRUD operations
    - `models/`: SQLAlchemy models
    - `crud/`: CRUD operations
    - `session.py`: Database session
  - `schemas/`: Pydantic models for request/response validation
  - `services/`: External service integrations (YouTube, payment)
    - `video/`: YouTube video service
    - `payment/`: Stripe payment service
    - `search/`: Elasticsearch service
  - `utils/`: Utility functions
    - `transcription/`: Transcription comparison utilities
  - `main.py`: Application entry point
- `alembic/`: Database migrations
- `tests/`: Test suite

## Development

### Creating database migrations

After modifying models, create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply the migration:

```bash
alembic upgrade head
```

### Running tests

```bash
pytest
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost/transcriptapp` |
| `SECRET_KEY` | JWT secret key | `<required>` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |
| `YOUTUBE_API_KEY` | YouTube Data API key | `<required>` |
| `STRIPE_API_KEY` | Stripe API key | `<required>` |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | `<required>` |
| `ELASTICSEARCH_URL` | Elasticsearch connection | `http://localhost:9200` |

## License

MIT 