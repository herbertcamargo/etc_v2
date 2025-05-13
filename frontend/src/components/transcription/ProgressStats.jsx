import React from 'react';
import './ProgressStats.css';

/**
 * ProgressStats component - Displays user's transcription progress statistics
 * 
 * Shows statistics cards with key metrics about the user's transcription activity
 */
const ProgressStats = ({ stats }) => {
  // Default empty stats if none provided
  const defaultStats = {
    totalTranscriptions: 0,
    averageAccuracy: 0,
    totalTime: 0, // in minutes
    streak: 0,
    wordsPerMinute: 0,
    recentAccuracy: [] // array of recent accuracy scores
  };
  
  // Merge provided stats with defaults
  const mergedStats = { ...defaultStats, ...stats };
  
  // Calculate the average accuracy percentage
  const accuracyPercentage = Math.round(mergedStats.averageAccuracy * 100);
  
  // Format the total time (convert minutes to hours if needed)
  const formatTime = (minutes) => {
    if (minutes < 60) {
      return `${minutes} min`;
    } else {
      const hours = Math.floor(minutes / 60);
      const mins = minutes % 60;
      return `${hours}h ${mins}m`;
    }
  };
  
  // Generate sparkline data points for recent accuracy trend
  const generateSparklinePoints = (data, height = 30) => {
    if (!data || data.length === 0) {
      return '';
    }
    
    const values = data.slice(-10); // Use last 10 data points
    const min = Math.min(...values);
    const max = Math.max(...values, 1); // Cap at 1.0 (100%)
    const range = max - min || 1;
    
    const points = values.map((val, i) => {
      const x = i * 10; // 10 units per data point
      const normalizedY = (val - min) / range; // Normalize to 0-1
      const y = height - (normalizedY * height); // Convert to SVG coordinates
      return `${x},${y}`;
    }).join(' ');
    
    return points;
  };
  
  const sparklinePoints = generateSparklinePoints(mergedStats.recentAccuracy);
  
  return (
    <div className="progress-stats">
      <div className="progress-stats__card">
        <div className="progress-stats__icon progress-stats__icon--transcriptions">
          <i className="icon-document"></i>
        </div>
        <div className="progress-stats__content">
          <div className="progress-stats__value">{mergedStats.totalTranscriptions}</div>
          <div className="progress-stats__label">Transcriptions</div>
        </div>
      </div>
      
      <div className="progress-stats__card">
        <div className="progress-stats__icon progress-stats__icon--accuracy">
          <i className="icon-check"></i>
        </div>
        <div className="progress-stats__content">
          <div className="progress-stats__value">{accuracyPercentage}%</div>
          <div className="progress-stats__label">Avg. Accuracy</div>
          {sparklinePoints && (
            <div className="progress-stats__trend">
              <svg width="100" height="30" className="progress-stats__sparkline">
                <polyline
                  points={sparklinePoints}
                  fill="none"
                  stroke="var(--color-primary)"
                  strokeWidth="2"
                />
              </svg>
            </div>
          )}
        </div>
      </div>
      
      <div className="progress-stats__card">
        <div className="progress-stats__icon progress-stats__icon--time">
          <i className="icon-clock"></i>
        </div>
        <div className="progress-stats__content">
          <div className="progress-stats__value">{formatTime(mergedStats.totalTime)}</div>
          <div className="progress-stats__label">Total Time</div>
        </div>
      </div>
      
      <div className="progress-stats__card">
        <div className="progress-stats__icon progress-stats__icon--streak">
          <i className="icon-fire"></i>
        </div>
        <div className="progress-stats__content">
          <div className="progress-stats__value">{mergedStats.streak}</div>
          <div className="progress-stats__label">Day Streak</div>
        </div>
      </div>
      
      <div className="progress-stats__card">
        <div className="progress-stats__icon progress-stats__icon--wpm">
          <i className="icon-speed"></i>
        </div>
        <div className="progress-stats__content">
          <div className="progress-stats__value">{mergedStats.wordsPerMinute}</div>
          <div className="progress-stats__label">Words Per Min</div>
        </div>
      </div>
    </div>
  );
};

export default ProgressStats; 