import React, { useState, useEffect, useRef } from 'react';
import './TranscriptionBox.css';

/**
 * TranscriptionBox component - Input area for transcribing video content
 * 
 * Provides a textarea for users to type their transcription with automatic
 * word counting and session timing functionality.
 */
const TranscriptionBox = ({ 
  value, 
  onChange, 
  onSave, 
  isPlaying,
  isPremium = false,
  placeholder = "Type what you hear..."
}) => {
  const [wordCount, setWordCount] = useState(0);
  const [sessionTime, setSessionTime] = useState(0);
  const [isTimerActive, setIsTimerActive] = useState(false);
  const timerRef = useRef(null);
  const textareaRef = useRef(null);

  // Handle word count calculation whenever value changes
  useEffect(() => {
    if (!value) {
      setWordCount(0);
      return;
    }
    
    // Count words by splitting on whitespace and filtering empty strings
    const words = value.trim().split(/\s+/).filter(word => word.length > 0);
    setWordCount(words.length);
  }, [value]);

  // Handle session timing based on typing activity
  useEffect(() => {
    // Start timer when playing and user starts typing
    if (isPlaying && value && !isTimerActive) {
      setIsTimerActive(true);
    }
    
    // Start or stop timer based on active state
    if (isTimerActive && !timerRef.current) {
      timerRef.current = setInterval(() => {
        setSessionTime(prevTime => prevTime + 1);
      }, 1000);
    } else if (!isTimerActive && timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    
    // Clean up timer on unmount
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isPlaying, isTimerActive, value]);

  // Format time display (MM:SS)
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleTextChange = (e) => {
    const newValue = e.target.value;
    
    // For non-premium users, limit to 500 words
    if (!isPremium) {
      const wordArray = newValue.trim().split(/\s+/).filter(word => word.length > 0);
      if (wordArray.length > 500) {
        // Don't update if over limit
        return;
      }
    }
    
    onChange(newValue);
    
    // Activate timer if not already active
    if (!isTimerActive && newValue.trim()) {
      setIsTimerActive(true);
    }
  };

  const handleSave = () => {
    if (onSave) {
      onSave(value, { wordCount, sessionTime });
    }
  };

  const handleKeyDown = (e) => {
    // Allow Ctrl+S for saving
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      handleSave();
    }
  };

  return (
    <div className="transcription-box">
      <div className="transcription-box__header">
        <div className="transcription-box__stats">
          <span className="transcription-box__word-count">
            Words: {wordCount}
            {!isPremium && wordCount >= 450 && 
              <span className="transcription-box__limit-warning">
                ({500 - wordCount} words remaining)
              </span>
            }
          </span>
          <span className="transcription-box__time">
            Time: {formatTime(sessionTime)}
          </span>
        </div>
      </div>
      
      <textarea
        ref={textareaRef}
        className="transcription-box__textarea"
        value={value}
        onChange={handleTextChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        rows={10}
      />
      
      <div className="transcription-box__footer">
        <button 
          className="button button--primary" 
          onClick={handleSave}
          disabled={!value.trim()}
        >
          Save
        </button>
        {!isPremium && (
          <div className="transcription-box__premium-note">
            Premium required for transcriptions over 500 words
          </div>
        )}
      </div>
    </div>
  );
};

export default TranscriptionBox; 