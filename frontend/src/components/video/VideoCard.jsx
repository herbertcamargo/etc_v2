import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

function VideoCard({ video }) {
  // Format duration from seconds to mm:ss format
  const formatDuration = (durationInSeconds) => {
    if (!durationInSeconds) return '0:00';
    
    const minutes = Math.floor(durationInSeconds / 60);
    const seconds = durationInSeconds % 60;
    
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  // Truncate title or description if too long
  const truncateText = (text, maxLength) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="video-card">
      <Link to={`/transcribe/${video.youtube_id}`} className="video-card__link">
        <div className="video-card__thumbnail">
          <img 
            src={video.thumbnail_url} 
            alt={video.title} 
            className="video-card__image"
          />
          {video.duration && (
            <span className="video-card__duration">
              {formatDuration(video.duration)}
            </span>
          )}
        </div>
        <div className="video-card__content">
          <h3 className="video-card__title">{truncateText(video.title, 60)}</h3>
          {video.description && (
            <p className="video-card__description">
              {truncateText(video.description, 120)}
            </p>
          )}
        </div>
      </Link>
    </div>
  );
}

VideoCard.propTypes = {
  video: PropTypes.shape({
    youtube_id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string,
    thumbnail_url: PropTypes.string,
    duration: PropTypes.number,
  }).isRequired,
};

export default VideoCard; 