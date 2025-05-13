# TranscriptV2

TranscriptV2 is a comprehensive platform for practicing and improving transcription skills using YouTube videos. This application allows users to search for videos, practice transcribing their content, and get feedback on accuracy.

## Features

- **Video Search**: Search and browse YouTube videos for transcription practice
- **Transcription System**: User-friendly interface for transcribing video content with timing and progress tracking
- **Accuracy Comparison**: Compare your transcription against reference text with detailed accuracy analysis
- **User Authentication**: Secure login and registration system
- **Progress Tracking**: Monitor your transcription history and improvement over time
- **Subscription System**: Free tier with limits and premium subscription options using Stripe
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**:
  - Python with FastAPI
  - PostgreSQL database
  - JWT authentication
  - SQLAlchemy ORM
  - Elasticsearch for search
  - Stripe for payment processing

- **Frontend**:
  - React.js with React Router
  - Context API for state management
  - Responsive CSS
  - YouTube Player API

- **Infrastructure**:
  - Docker containerization
  - Prometheus and Grafana for monitoring
  - GitHub Actions for CI/CD

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 14+ and npm (for local frontend development)
- Python 3.9+ (for local backend development)
- PostgreSQL 13+ (for local database)

### Running with Docker

The easiest way to get started is using Docker Compose:

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/transcript-v2.git
   cd transcript-v2
   ```

2. Create an environment file
   ```bash
   cp .env.example .env
   # Edit the .env file with your configuration
   ```

3. Start the application
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally

For development, you might want to run the components separately:

1. Start the backend:
   ```bash
   cd backend
   # Follow the instructions in backend/README.md
   ```

2. Start the frontend:
   ```bash
   cd frontend
   # Follow the instructions in frontend/README.md
   ```

## Project Structure

- `backend/`: FastAPI backend application
- `frontend/`: React frontend application
- `docker-compose.yml`: Development Docker Compose configuration
- `docker-compose.prod.yml`: Production Docker Compose configuration
- `monitoring/`: Prometheus and Grafana monitoring setup
- `specs/`: Project specifications and design documents
- `progress-tracking/`: Development progress tracking

## Documentation

- Backend API: http://localhost:8000/docs when running
- [Application Requirements](specs/application-requirements.md)
- [Application Design](specs/application-design.md)
- [Implementation Plan](specs/implementation-plan.md)
- [Project Structure](specs/project-directory-and-file-structure.md)

## Development Workflow

1. Create feature branches from `main`
2. Make your changes with appropriate tests
3. Submit a pull request
4. After review and CI checks, merge to `main`

## License

MIT 