import React from 'react';
import './ResultComparison.css';

/**
 * ResultComparison component - Displays the comparison between user transcription and reference
 * 
 * Visualizes the accuracy of user's transcription with word-by-word highlighting
 * and displays overall statistics
 */
const ResultComparison = ({ comparisonData, onClose }) => {
  if (!comparisonData) {
    return null;
  }

  const { overall_accuracy, word_matches, stats } = comparisonData;

  // Format accuracy as percentage
  const formatAccuracy = (score) => {
    return `${Math.round(score * 100)}%`;
  };

  return (
    <div className="result-comparison">
      <div className="result-comparison__header">
        <h2 className="result-comparison__title">Transcription Results</h2>
        {onClose && (
          <button 
            className="result-comparison__close-btn" 
            onClick={onClose}
            aria-label="Close results"
          >
            ×
          </button>
        )}
      </div>

      <div className="result-comparison__accuracy">
        <div className="result-comparison__accuracy-meter">
          <div 
            className="result-comparison__accuracy-fill" 
            style={{ width: formatAccuracy(overall_accuracy) }}
          />
        </div>
        <div className="result-comparison__accuracy-value">
          {formatAccuracy(overall_accuracy)}
        </div>
      </div>

      <div className="result-comparison__stats">
        <div className="result-comparison__stat-item">
          <span className="result-comparison__stat-label">Correct Words:</span>
          <span className="result-comparison__stat-value">{stats.correct_words}</span>
        </div>
        <div className="result-comparison__stat-item">
          <span className="result-comparison__stat-label">Total Words:</span>
          <span className="result-comparison__stat-value">{stats.total_words}</span>
        </div>
        <div className="result-comparison__stat-item">
          <span className="result-comparison__stat-label">Missed Words:</span>
          <span className="result-comparison__stat-value">{stats.missed_words}</span>
        </div>
        <div className="result-comparison__stat-item">
          <span className="result-comparison__stat-label">Extra Words:</span>
          <span className="result-comparison__stat-value">{stats.extra_words}</span>
        </div>
      </div>

      <div className="result-comparison__text-container">
        <h3 className="result-comparison__subtitle">Detailed Comparison</h3>
        <div className="result-comparison__text-comparison">
          {word_matches.map((match, index) => {
            const [userWord, refWord, isMatch] = match;
            
            // Handle different cases
            if (!userWord && refWord) {
              // Missed word (in reference but not in user input)
              return (
                <span key={index} className="result-comparison__word result-comparison__word--missed">
                  {refWord}
                </span>
              );
            } else if (userWord && !refWord) {
              // Extra word (in user input but not in reference)
              return (
                <span key={index} className="result-comparison__word result-comparison__word--extra">
                  {userWord}
                </span>
              );
            } else if (isMatch) {
              // Word matches
              return (
                <span key={index} className="result-comparison__word result-comparison__word--correct">
                  {userWord}
                </span>
              );
            } else {
              // Word doesn't match
              return (
                <span key={index} className="result-comparison__word result-comparison__word--incorrect">
                  {userWord}
                  <span className="result-comparison__correction">
                    {refWord}
                  </span>
                </span>
              );
            }
          })}
        </div>
      </div>

      <div className="result-comparison__actions">
        <button 
          className="button button--primary" 
          onClick={onClose}
        >
          Continue Practice
        </button>
      </div>
    </div>
  );
};

export default ResultComparison; 