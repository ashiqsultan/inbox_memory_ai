import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'https://api.kbhelper.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API endpoints
export const authAPI = {
  // Login - send OTP to email
  login: async (email: string) => {
    const response = await api.post('/auth/login', { email });
    return response.data;
  },

  // Signup - create account and send OTP
  signup: async (email: string, name: string) => {
    const response = await api.post('/auth/signup', { email, name });
    return response.data;
  },

  // Verify OTP
  verifyOTP: async (email: string, otp: string) => {
    const response = await api.post('/auth/verify-otp', { email, otp });
    return response.data;
  },

  // Logout
  logout: () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  },
};

// Export the axios instance for other custom API calls
export default api;

// Email API endpoints
export const emailAPI = {
  // Get list of emails for the authenticated user
  getEmailList: async () => {
    const response = await api.get('/kb/');
    return response.data;
  },

  // Get specific email by ID
  getEmailById: async (emailId: string) => {
    const response = await api.get(`/kb/${emailId}`);
    return response.data;
  },

  // Ask question about emails (QA)
  askQuestion: async (question: string) => {
    const response = await api.post('/kb/qa', { question });
    return response.data;
  },
};
