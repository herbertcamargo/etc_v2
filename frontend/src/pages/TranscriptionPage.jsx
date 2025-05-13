import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import VideoPlayer from '../components/video/VideoPlayer';
import TranscriptionBox from '../components/transcription/TranscriptionBox';
import ResultComparison from '../components/transcription/ResultComparison';
import { getVideoDetails } from '../services/videoService';
import { 
  createTranscription, 
  analyzeTranscription, 
  getUserTranscriptionStats 
} from '../services/transcriptionService';
import { useAuth } from '../contexts/AuthContext';
import './TranscriptionPage.css';

/**
 * TranscriptionPage component - Displays video for transcription practice
 * Allows users to watch a video and practice transcribing its content
 */
function TranscriptionPage() {
  const { videoId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const playerControlsRef = useRef(null);
  
  const [videoDetails, setVideoDetails] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [correctTranscription, setCorrectTranscription] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [showComparison, setShowComparison] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [transcriptionSaved, setTranscriptionSaved] = useState(false);

  useEffect(() => {
    loadVideoDetails();
  }, [videoId]);

  const loadVideoDetails = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await getVideoDetails(videoId);
      setVideoDetails(response.data);
    } catch (err) {
      setError('Failed to load video details. Please try again.');
      console.error('Video details error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayerReady = (event) => {
    // Store player controls for later use
    const player = event.target;
    playerControlsRef.current = {
      play: () => player.playVideo(),
      pause: () => player.pauseVideo(),
      getCurrentTime: () => player.getCurrentTime(),
      getDuration: () => player.getDuration(),
      seekTo: (time) => player.seekTo(time, true),
    };
  };

  const handlePlayerStateChange = (event) => {
    // YouTube player states: -1 (unstarted), 0 (ended), 1 (playing), 2 (paused), 3 (buffering), 5 (video cued)
    const playerState = event.data;
    setIsPlaying(playerState === 1);
    
    if (playerState === 1) {
      // Update current time periodically while playing
      const timeUpdateInterval = setInterval(() => {
        if (playerControlsRef.current) {
          setCurrentTime(playerControlsRef.current.getCurrentTime());
        }
      }, 1000);
      
      return () => clearInterval(timeUpdateInterval);
    }
  };

  const handleTranscriptionChange = (value) => {
    setTranscription(value);
  };

  const handleCorrectTranscriptionChange = (e) => {
    setCorrectTranscription(e.target.value);
  };

  const handleSaveTranscription = async (text, stats) => {
    if (!text.trim()) {
      return;
    }
    
    setIsSaving(true);
    
    try {
      const transcriptionData = {
        video_id: videoDetails.id,
        user_transcription: text,
        correct_transcription: correctTranscription || null
      };
      
      const response = await createTranscription(transcriptionData);
      setTranscriptionSaved(true);
      
      // If we have a reference transcription, analyze it
      if (correctTranscription) {
        handleCheckAccuracy();
      }
      
      // Reset saved status after 3 seconds
      setTimeout(() => {
        setTranscriptionSaved(false);
      }, 3000);
      
    } catch (err) {
      setError('Failed to save transcription. Please try again.');
      console.error('Save transcription error:', err);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCheckAccuracy = async () => {
    if (!transcription.trim() || !correctTranscription.trim()) {
      setError('Both your transcription and the reference transcription are required.');
      return;
    }
    
    setIsAnalyzing(true);
    
    try {
      const response = await analyzeTranscription(transcription, correctTranscription);
      setComparisonResult(response.data);
      setShowComparison(true);
    } catch (err) {
      setError('Failed to analyze transcription. Please try again.');
      console.error('Analyze transcription error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleCloseComparison = () => {
    setShowComparison(false);
  };

  const handlePlayPause = () => {
    if (!playerControlsRef.current) return;
    
    if (isPlaying) {
      playerControlsRef.current.pause();
    } else {
      playerControlsRef.current.play();
    }
  };

  const handleRewind = (seconds = 5) => {
    if (!playerControlsRef.current) return;
    
    const currentTime = playerControlsRef.current.getCurrentTime();
    const newTime = Math.max(0, currentTime - seconds);
    playerControlsRef.current.seekTo(newTime);
  };

  return (
    <Layout>
      <div className="transcription-page">
        {isLoading && (
          <div className="transcription-page__loading">
            <div className="loader"></div>
            <p>Loading video...</p>
          </div>
        )}

        {error && (
          <div className="transcription-page__error">
            <p>{error}</p>
            <div className="transcription-page__error-actions">
              <button 
                className="button button--secondary" 
                onClick={() => setError(null)}
              >
                Dismiss
              </button>
              <button 
                className="button button--outline" 
                onClick={() => navigate('/search')}
              >
                Back to Search
              </button>
            </div>
          </div>
        )}

        {!isLoading && !error && videoDetails && (
          <>
            <h1 className="transcription-page__title">{videoDetails.title}</h1>
            
            <div className="transcription-page__content">
              <div className="transcription-page__video-container">
                <VideoPlayer
                  videoId={videoId}
                  onReady={handlePlayerReady}
                  onStateChange={handlePlayerStateChange}
                  controls={true}
                  height="480px"
                />
                
                <div className="transcription-page__controls">
                  <button 
                    className="button button--icon" 
                    onClick={() => handleRewind(10)}
                    aria-label="Rewind 10 seconds"
                  >
                    -10s
                  </button>
                  <button 
                    className="button button--icon" 
                    onClick={() => handleRewind(5)}
                    aria-label="Rewind 5 seconds"
                  >
                    -5s
                  </button>
                  <button 
                    className="button button--primary" 
                    onClick={handlePlayPause}
                  >
                    {isPlaying ? 'Pause' : 'Play'}
                  </button>
                </div>
              </div>
              
              <div className="transcription-page__transcription">
                <h2 className="transcription-page__subtitle">Your Transcription</h2>
                <TranscriptionBox 
                  value={transcription}
                  onChange={handleTranscriptionChange}
                  onSave={handleSaveTranscription}
                  isPlaying={isPlaying}
                  isPremium={user?.is_premium}
                />
                
                <div className="transcription-page__reference">
                  <h2 className="transcription-page__subtitle">Reference Transcription (Optional)</h2>
                  <p className="transcription-page__hint">
                    Enter a reference transcription to compare against your own.
                  </p>
                  <textarea
                    className="transcription-page__reference-textarea"
                    value={correctTranscription}
                    onChange={handleCorrectTranscriptionChange}
                    placeholder="Enter the reference transcription here..."
                    rows={4}
                  />
                  
                  <div className="transcription-page__actions">
                    <button 
                      className="button button--primary"
                      onClick={handleCheckAccuracy}
                      disabled={!transcription.trim() || !correctTranscription.trim() || isAnalyzing}
                    >
                      {isAnalyzing ? 'Analyzing...' : 'Check Accuracy'}
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            {showComparison && comparisonResult && (
              <div className="transcription-page__results">
                <ResultComparison 
                  comparisonData={comparisonResult}
                  onClose={handleCloseComparison}
                />
              </div>
            )}
            
            {transcriptionSaved && (
              <div className="transcription-page__saved-notification">
                Transcription saved successfully!
              </div>
            )}
          </>
        )}
      </div>
    </Layout>
  );
}

export default TranscriptionPage; 