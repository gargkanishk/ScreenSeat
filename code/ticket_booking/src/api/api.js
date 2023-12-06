// api.js

import axios from 'axios';

// Create a new Axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api/', // Your backend API base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add an interceptor to automatically include the Authorization header
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('user_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Add an interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle expired token - redirect to login or home page
      console.log('Token expired. Redirect to login or home page.');
      // For example, to redirect to the home page:
      window.location.href = '/';
      return Promise.reject(error);
    }
    return Promise.reject(error);
  }
);

export default api;
