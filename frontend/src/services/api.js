import axios from 'axios';

// Get API base URL from environment variable or use default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const { response } = error;
    
    // Handle expired tokens
    if (response && response.status === 401) {
      // If it's not the login endpoint that returned 401
      if (!error.config.url.includes('login')) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    
    // Return a structured error object
    const errorMessage = response?.data?.detail || 'Something went wrong';
    return Promise.reject({
      message: errorMessage,
      status: response?.status,
      data: response?.data
    });
  }
);

export default api; 