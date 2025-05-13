import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import VideoCard from '../components/video/VideoCard';
import { getUserVideoHistory, getUserStats } from '../services/videoService';

/**
 * DashboardPage component - User's personal dashboard
 * Displays transcription history, statistics, and recent activity
 */
function DashboardPage() {
  const [videoHistory, setVideoHistory] = useState([]);
  const [userStats, setUserStats] = useState({
    totalTranscriptions: 0,
    averageAccuracy: 0,
    totalMinutesTranscribed: 0,
    streak: 0,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Load user video history and stats in parallel
      const [historyResponse, statsResponse] = await Promise.all([
        getUserVideoHistory(),
        getUserStats()
      ]);
      
      setVideoHistory(historyResponse.data || []);
      setUserStats(statsResponse.data || {
        totalTranscriptions: 0,
        averageAccuracy: 0,
        totalMinutesTranscribed: 0,
        streak: 0,
      });
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
      console.error('Dashboard data error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Format percentage display
  const formatPercentage = (value) => {
    return `${Math.round(value)}%`;
  };

  // Format minutes display
  const formatMinutes = (minutes) => {
    if (minutes < 60) {
      return `${minutes} min${minutes !== 1 ? 's' : ''}`;
    }
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours} hr${hours !== 1 ? 's' : ''} ${remainingMinutes} min${remainingMinutes !== 1 ? 's' : ''}`;
  };

  return (
    <Layout>
      <div className="container dashboard-page">
        <h1 className="dashboard-page__title">Your Dashboard</h1>
        
        {isLoading && (
          <div className="dashboard-page__loading">
            <div className="loader"></div>
            <p>Loading your dashboard...</p>
          </div>
        )}

        {error && (
          <div className="dashboard-page__error">
            <p>{error}</p>
            <button 
              className="button button--secondary" 
              onClick={loadDashboardData}
            >
              Try Again
            </button>
          </div>
        )}

        {!isLoading && !error && (
          <>
            <div className="dashboard-page__stats">
              <div className="stats-card">
                <div className="stats-card__value">{userStats.totalTranscriptions}</div>
                <div className="stats-card__label">Transcriptions</div>
              </div>
              <div className="stats-card">
                <div className="stats-card__value">{formatPercentage(userStats.averageAccuracy)}</div>
                <div className="stats-card__label">Avg. Accuracy</div>
              </div>
              <div className="stats-card">
                <div className="stats-card__value">{formatMinutes(userStats.totalMinutesTranscribed)}</div>
                <div className="stats-card__label">Time Transcribed</div>
              </div>
              <div className="stats-card">
                <div className="stats-card__value">{userStats.streak}</div>
                <div className="stats-card__label">Day Streak</div>
              </div>
            </div>

            <div className="dashboard-page__history">
              <div className="dashboard-page__section-header">
                <h2 className="dashboard-page__subtitle">Your Recent Activity</h2>
                <Link to="/search" className="button button--outline">Find New Videos</Link>
              </div>
              
              {videoHistory.length === 0 ? (
                <div className="dashboard-page__empty">
                  <p>You haven't transcribed any videos yet.</p>
                  <Link to="/search" className="button button--primary">
                    Get Started
                  </Link>
                </div>
              ) : (
                <div className="video-grid">
                  {videoHistory.map((video) => (
                    <VideoCard key={video.youtube_id} video={video} />
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </Layout>
  );
}

export default DashboardPage; 