import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';

function VideoPlayer({ 
  videoId, 
  onReady, 
  onStateChange,
  autoplay = false,
  controls = true,
  width = '100%',
  height = '480px'
}) {
  const playerRef = useRef(null);
  const containerRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Load YouTube API if not already loaded
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
      
      window.onYouTubeIframeAPIReady = initializePlayer;
    } else {
      initializePlayer();
    }

    return () => {
      // Clean up player on unmount
      if (playerRef.current) {
        playerRef.current.destroy();
      }
    };
  }, [videoId]);

  const initializePlayer = () => {
    if (!containerRef.current) return;
    
    if (playerRef.current) {
      playerRef.current.destroy();
    }
    
    playerRef.current = new window.YT.Player(containerRef.current, {
      videoId,
      width,
      height,
      playerVars: {
        autoplay: autoplay ? 1 : 0,
        controls: controls ? 1 : 0,
        rel: 0,  // Don't show related videos
        modestbranding: 1,  // Hide YouTube logo
        origin: window.location.origin,
      },
      events: {
        onReady: (event) => {
          setIsLoaded(true);
          if (onReady) onReady(event);
        },
        onStateChange: (event) => {
          if (onStateChange) onStateChange(event);
        },
      },
    });
  };

  // Method to expose player controls to parent components
  const getPlayerControls = () => {
    if (!playerRef.current) return null;
    
    return {
      play: () => playerRef.current.playVideo(),
      pause: () => playerRef.current.pauseVideo(),
      stop: () => playerRef.current.stopVideo(),
      getCurrentTime: () => playerRef.current.getCurrentTime(),
      getDuration: () => playerRef.current.getDuration(),
      seekTo: (seconds) => playerRef.current.seekTo(seconds, true),
    };
  };

  return (
    <div className="video-player">
      <div 
        ref={containerRef} 
        className="video-player__container"
        style={{ width, height }}
      />
      {!isLoaded && (
        <div className="video-player__loading">
          <span>Loading player...</span>
        </div>
      )}
    </div>
  );
}

VideoPlayer.propTypes = {
  videoId: PropTypes.string.isRequired,
  onReady: PropTypes.func,
  onStateChange: PropTypes.func,
  autoplay: PropTypes.bool,
  controls: PropTypes.bool,
  width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
};

export default VideoPlayer; 