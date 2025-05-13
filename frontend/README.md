# TranscriptV2 Frontend

Frontend application for the TranscriptV2 platform, a web application for practicing transcription skills with YouTube videos.

## Features

- User authentication (login/register)
- Video search via YouTube API
- Transcription interface
  - Video playback with custom controls
  - Transcription text entry with word counting
  - Rewind functionality (5s and 10s)
  - Reference transcription comparison
  - Accuracy visualization and statistics
- Subscription management
  - Plan selection and checkout
  - Usage tracking
  - Subscription status display
- Dark/light theme support
- Responsive design for desktop and mobile

## Requirements

- Node.js 14+
- npm 6+

## Setup

1. Clone the repository

2. Install dependencies
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:8000/api
```

4. Start the development server
```bash
npm start
```

The application will be available at http://localhost:3000

## Docker Setup

You can also run the frontend with Docker:

```bash
docker build -t transcriptv2-frontend .
docker run -p 3000:80 transcriptv2-frontend
```

Or use Docker Compose from the root directory:

```bash
docker-compose up frontend
```

## Project Structure

- `public/`: Static assets
- `src/`:
  - `components/`: Reusable UI components
    - `common/`: Shared components (Button, Input, Modal)
    - `layout/`: Layout components (Header, Footer)
    - `auth/`: Authentication components
    - `video/`: Video-related components
      - `VideoPlayer.jsx`: YouTube player with custom controls
      - `VideoCard.jsx`: Video display card with thumbnail
    - `transcription/`: Transcription-related components
      - `TranscriptionBox.jsx`: Main transcription input component
      - `ResultComparison.jsx`: Accuracy comparison visualization
      - `ProgressStats.jsx`: User progress statistics
    - `subscription/`: Subscription-related components
      - `PlanCard.jsx`: Subscription plan display
      - `SubscriptionUsage.jsx`: Usage metrics display
      - `PaymentForm.jsx`: Stripe payment integration
  - `contexts/`: React context providers
    - `AuthContext.js`: Authentication state management
    - `ThemeContext.js`: Theme switching functionality
  - `hooks/`: Custom React hooks
  - `pages/`: Top-level page components
    - `HomePage.jsx`: Landing page
    - `LoginPage.jsx`: User login
    - `RegisterPage.jsx`: User registration
    - `DashboardPage.jsx`: User dashboard with statistics
    - `VideoSearchPage.jsx`: Search and browse videos
    - `TranscriptionPage.jsx`: Transcription practice interface
    - `SubscriptionPage.jsx`: Subscription management
  - `services/`: API service functions
    - `authService.js`: Authentication API calls
    - `videoService.js`: Video search and retrieval
    - `transcriptionService.js`: Transcription management
    - `subscriptionService.js`: Subscription management
  - `styles/`: Global CSS and style variables
  - `utils/`: Utility functions
  - `App.jsx`: Main application component
  - `index.jsx`: Application entry point

## Available Scripts

- `npm start`: Start development server
- `npm test`: Run tests
- `npm run build`: Build for production
- `npm run eject`: Eject from Create React App

## Deployment

The frontend can be deployed to any static hosting provider (Netlify, Vercel, AWS S3, etc.)

1. Build the production bundle:
```bash
npm run build
```

2. Deploy the `build` directory to your hosting provider

## Docker Deployment

The Dockerfile includes a multi-stage build for production deployment:
- Build stage: Compiles the React application
- Production stage: Serves the application with Nginx

## License

MIT 