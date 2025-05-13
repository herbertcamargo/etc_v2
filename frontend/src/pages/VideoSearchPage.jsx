import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import SearchBar from '../components/video/SearchBar';
import VideoCard from '../components/video/VideoCard';
import { searchVideos, getTrendingVideos } from '../services/videoService';

/**
 * VideoSearchPage component - Handles video search functionality and displays results
 * Allows users to search for videos or view trending videos
 */
function VideoSearchPage() {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState(initialQuery);

  useEffect(() => {
    if (initialQuery) {
      handleSearch(initialQuery);
    } else {
      loadTrendingVideos();
    }
  }, [initialQuery]);

  const handleSearch = async (query) => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setError(null);
    setSearchQuery(query);
    
    try {
      const response = await searchVideos(query);
      setVideos(response.data || []);
    } catch (err) {
      setError('Failed to search videos. Please try again.');
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadTrendingVideos = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await getTrendingVideos();
      setVideos(response.data || []);
    } catch (err) {
      setError('Failed to load trending videos. Please try again.');
      console.error('Trending videos error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className="container search-page">
        <div className="search-page__header">
          <h1 className="search-page__title">
            {searchQuery ? `Search results for "${searchQuery}"` : 'Trending Videos'}
          </h1>
          <div className="search-page__search-container">
            <SearchBar 
              onSearch={handleSearch} 
              initialQuery={searchQuery} 
              placeholder="Search for videos to transcribe..."
            />
          </div>
        </div>

        {isLoading && (
          <div className="search-page__loading">
            <div className="loader"></div>
            <p>Loading videos...</p>
          </div>
        )}

        {error && (
          <div className="search-page__error">
            <p>{error}</p>
            <button 
              className="button button--secondary" 
              onClick={() => searchQuery ? handleSearch(searchQuery) : loadTrendingVideos()}
            >
              Try Again
            </button>
          </div>
        )}

        {!isLoading && !error && videos.length === 0 && (
          <div className="search-page__empty">
            <p>No videos found. Try a different search term.</p>
          </div>
        )}

        <div className="video-grid">
          {videos.map((video) => (
            <VideoCard key={video.youtube_id} video={video} />
          ))}
        </div>
      </div>
    </Layout>
  );
}

export default VideoSearchPage; 