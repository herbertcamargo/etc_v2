import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Context providers
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import VideoSearchPage from './pages/VideoSearchPage';
import TranscriptionPage from './pages/TranscriptionPage';
import SubscriptionPage from './pages/SubscriptionPage';
import SubscriptionSuccessPage from './pages/SubscriptionSuccessPage';

// Private route component
import PrivateRoute from './components/auth/PrivateRoute';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Protected routes */}
          <Route path="/dashboard" element={
            <PrivateRoute>
              <DashboardPage />
            </PrivateRoute>
          } />
          <Route path="/search" element={
            <PrivateRoute>
              <VideoSearchPage />
            </PrivateRoute>
          } />
          <Route path="/transcribe/:videoId" element={
            <PrivateRoute>
              <TranscriptionPage />
            </PrivateRoute>
          } />
          <Route path="/subscription" element={
            <PrivateRoute>
              <SubscriptionPage />
            </PrivateRoute>
          } />
          <Route path="/subscription/success" element={
            <PrivateRoute>
              <SubscriptionSuccessPage />
            </PrivateRoute>
          } />
        </Routes>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 