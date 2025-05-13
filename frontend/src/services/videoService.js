import api from './api';

/**
 * Search for YouTube videos
 * @param {string} query - Search query
 * @param {number} limit - Maximum number of results (default: 10)
 * @returns {Promise<Array>} List of videos matching the query
 */
export const searchVideos = async (query, limit = 10) => {
  try {
    return await api.get('/videos/search', {
      params: { q: query, limit },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Get trending videos
 * @param {number} limit - Maximum number of results (default: 10)
 * @returns {Promise<Array>} List of trending videos
 */
export const getTrendingVideos = async (limit = 10) => {
  try {
    return await api.get('/videos/trending', {
      params: { limit },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Get details of a specific video
 * @param {string} videoId - YouTube video ID
 * @returns {Promise<Object>} Video details
 */
export const getVideoDetails = async (videoId) => {
  try {
    return await api.get(`/videos/${videoId}`);
  } catch (error) {
    throw error;
  }
};

/**
 * Get user's video history
 * @param {number} limit - Maximum number of results (default: 10)
 * @param {number} offset - Offset for pagination (default: 0)
 * @returns {Promise<Array>} List of user's previously watched videos
 */
export const getUserVideoHistory = async (limit = 10, offset = 0) => {
  try {
    return await api.get('/transcriptions', {
      params: { limit, offset },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Get user statistics
 * @returns {Promise<Object>} User statistics
 */
export const getUserStats = async () => {
  try {
    return await api.get('/users/me/stats');
  } catch (error) {
    throw error;
  }
}; 