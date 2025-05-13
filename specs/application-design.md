# Application Design

## Architecture Overview
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  React Client │────▶│  FastAPI      │────▶│  PostgreSQL   │
│  (Frontend)   │◀────│  (Backend)    │◀────│  Database     │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     
        │                     │                     
        ▼                     ▼                     
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  YouTube      │     │  Stripe       │     │  Auth         │
│  APIs         │     │  Payment      │     │  Services     │
└───────────────┘     └───────────────┘     └───────────────┘

## Data Models

### User

User {
  id: UUID (primary key)
  username: String
  email: String (unique)
  password_hash: String
  is_premium: Boolean
  subscription_end_date: DateTime (nullable)
  created_at: DateTime
  updated_at: DateTime
}

### TranscriptionSession

TranscriptionSession {
  id: UUID (primary key)
  user_id: UUID (foreign key -> User.id)
  video_id: String (YouTube ID)
  user_transcription: Text
  correct_transcription: Text
  accuracy_score: Float
  created_at: DateTime
}

### Video

Video {
  id: UUID (primary key)
  youtube_id: String (unique)
  title: String
  description: Text
  thumbnail_url: String
  duration: Integer (seconds)
  created_at: DateTime
}

### Subscription

Subscription {
  id: UUID (primary key)
  user_id: UUID (foreign key -> User.id)
  stripe_subscription_id: String
  status: String (active, canceled, past_due)
  plan_type: String
  start_date: DateTime
  end_date: DateTime
  created_at: DateTime
  updated_at: DateTime
}

## API Endpoints

### Authentication

- POST /api/auth/register - Register new user
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout
- POST /api/auth/refresh - Refresh access token
- POST /api/auth/reset-password - Password reset

### Videos

- GET /api/videos/search - Search YouTube videos
- GET /api/videos/{id} - Get video details
- GET /api/videos/trending - Get trending videos

###  Transcriptions

- POST /api/transcriptions - Create new transcription
- GET /api/transcriptions - Get user's transcription history
- GET /api/transcriptions/{id} - Get specific transcription
- GET /api/users/me/stats - Get user transcription statistics

### Subscriptions

- GET /api/subscriptions/plans - Get available plans
- POST /api/subscriptions - Create new subscription
- GET /api/subscriptions/me - Get current subscription
- PUT /api/subscriptions/me - Update subscription
- DELETE /api/subscriptions/me - Cancel subscription

## User Interface Design

### Key Screens

#### Landing Page

- Value proposition and features
- User testimonials and sample videos
- Sign up/login buttons


#### User Dashboard

- Recent activity
- Progress statistics
- Quick search


#### Video Search Page

- Search bar with filters
- Video results grid with thumbnails
- Sort and filter options


#### Transcription Workspace

- Video player (top section)
- Transcription input area (middle)
- Results and feedback area (bottom)


#### Account Settings

- Profile management
- Subscription details
- Theme preferences
- Password change


#### Subscription Page

- Plan comparison
- Payment form
- Billing history


## Component Structure

### Frontend Components

- Header - Navigation, user menu, theme toggle
- SearchBar - Video search interface
- VideoPlayer - YouTube embedded player
- TranscriptionBox - Text input area
- FeedbackDisplay - Comparison results visualization
- SubscriptionCard - Plan details and selection
- UserDashboard - Progress and history displays
- Settings - User preference controls