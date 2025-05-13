# Project Directory and File Structure

## Frontend Structure (React)

frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── assets/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   └── Modal.jsx
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── video/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── VideoCard.jsx
│   │   │   └── VideoPlayer.jsx
│   │   ├── transcription/
│   │   │   ├── TranscriptionBox.jsx
│   │   │   ├── ResultComparison.jsx
│   │   │   └── ProgressStats.jsx
│   │   └── subscription/
│   │       ├── PlanCard.jsx
│   │       └── PaymentForm.jsx
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── VideoSearchPage.jsx
│   │   ├── TranscriptionPage.jsx
│   │   ├── SettingsPage.jsx
│   │   └── SubscriptionPage.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useTranscription.js
│   │   └── useYouTubeAPI.js
│   ├── contexts/
│   │   ├── AuthContext.js
│   │   └── ThemeContext.js
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── videoService.js
│   │   └── subscriptionService.js
│   ├── utils/
│   │   ├── validation.js
│   │   ├── textComparison.js
│   │   └── formatters.js
│   ├── styles/
│   │   ├── global.css
│   │   ├── themes.js
│   │   └── variables.css
│   ├── App.jsx
│   ├── index.jsx
│   └── routes.js
├── package.json
├── .env.example
└── README.md

## Backend Structure (FastAPI/Python)

backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── videos.py
│   │   │   ├── transcriptions.py
│   │   │   └── subscriptions.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── videos.py
│   │       ├── transcriptions.py
│   │       └── subscriptions.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── videos.py
│   │   ├── transcriptions.py
│   │   └── subscriptions.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── youtube.py
│   │   ├── transcription.py
│   │   └── payment.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── text_comparison.py
│   └── main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_videos.py
│   ├── test_transcriptions.py
│   └── test_subscriptions.py
├── requirements.txt
├── .env.example
└── README.md