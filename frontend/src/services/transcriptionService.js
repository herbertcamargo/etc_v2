/**
 * Transcription Service
 * 
 * This module provides functions for interacting with the transcription API endpoints.
 * It handles creating, retrieving, analyzing, and managing transcription sessions.
 */
import api from './api';

/**
 * Create a new transcription session
 * 
 * @param {Object} transcriptionData - Data for the new transcription
 * @param {string} transcriptionData.video_id - UUID of the video
 * @param {string} transcriptionData.user_transcription - User's transcription text
 * @param {string} [transcriptionData.correct_transcription] - Optional reference transcription
 * @returns {Promise} Promise resolving to the created transcription
 */
export const createTranscription = async (transcriptionData) => {
  return api.post('/transcriptions', transcriptionData);
};

/**
 * Get all transcription sessions for the current user
 * 
 * @param {Object} options - Query options
 * @param {number} [options.skip=0] - Number of items to skip
 * @param {number} [options.limit=10] - Maximum number of items to return
 * @returns {Promise} Promise resolving to an array of transcription sessions
 */
export const getUserTranscriptions = async ({ skip = 0, limit = 10 } = {}) => {
  return api.get(`/transcriptions?skip=${skip}&limit=${limit}`);
};

/**
 * Get a specific transcription session
 * 
 * @param {string} id - UUID of the transcription session
 * @returns {Promise} Promise resolving to the transcription session
 */
export const getTranscription = async (id) => {
  return api.get(`/transcriptions/${id}`);
};

/**
 * Update a transcription session
 * 
 * @param {string} id - UUID of the transcription session
 * @param {Object} updateData - Data to update
 * @returns {Promise} Promise resolving to the updated transcription
 */
export const updateTranscription = async (id, updateData) => {
  return api.put(`/transcriptions/${id}`, updateData);
};

/**
 * Delete a transcription session
 * 
 * @param {string} id - UUID of the transcription session to delete
 * @returns {Promise} Promise resolving when deletion is complete
 */
export const deleteTranscription = async (id) => {
  return api.delete(`/transcriptions/${id}`);
};

/**
 * Analyze and compare transcription texts without saving
 * 
 * @param {string} userText - User's transcription text
 * @param {string} referenceText - Reference/correct transcription text
 * @returns {Promise} Promise resolving to analysis results
 */
export const analyzeTranscription = async (userText, referenceText) => {
  return api.post('/transcriptions/analyze', { user_text: userText, reference_text: referenceText });
};

/**
 * Get user's transcription statistics
 * 
 * @returns {Promise} Promise resolving to user stats
 */
export const getUserTranscriptionStats = async () => {
  return api.get('/users/me/stats');
}; 