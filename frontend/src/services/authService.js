import api from './api';

/**
 * Register a new user
 * @param {Object} userData - User data containing username, email, and password
 * @returns {Promise<Object>} The newly created user data
 */
export const registerUser = async (userData) => {
  try {
    return await api.post('/auth/register', userData);
  } catch (error) {
    throw error;
  }
};

/**
 * Login a user
 * @param {Object} credentials - Object containing username and password
 * @returns {Promise<Object>} Authentication token data
 */
export const loginUser = async (credentials) => {
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  try {
    // Login endpoint requires form data, not JSON
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response;
  } catch (error) {
    throw error;
  }
};

/**
 * Get current user data
 * @returns {Promise<Object>} Current user data
 */
export const getCurrentUser = async () => {
  try {
    return await api.get('/auth/me');
  } catch (error) {
    throw error;
  }
};

/**
 * Logout the current user
 * Note: Since we're using JWT tokens, we don't need to make a server call
 * Just clearing the token on the client side is enough
 */
export const logoutUser = () => {
  // This function doesn't need to do anything server-side
  // The actual logout is handled in the AuthContext by removing the token
  return true;
}; 