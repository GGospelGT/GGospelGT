import axios from 'axios';

// Resolve backend URL with robust localhost safeguards and optional runtime override
const getBackendUrl = () => {
  const isBrowser = typeof window !== 'undefined';
  const isLocalhost = isBrowser && window.location.hostname === 'localhost';

  // Build-time env from CRA, may be inlined; runtime override via window/localStorage if needed
  const buildEnvUrl = process.env.REACT_APP_BACKEND_URL || '';
  const runtimeOverride = isBrowser ? (window.BACKEND_URL_OVERRIDE || localStorage.getItem('BACKEND_URL_OVERRIDE') || '') : '';

  let url = runtimeOverride || buildEnvUrl;

  // Default for localhost when nothing is set
  if (!url && isLocalhost) {
    url = 'http://localhost:8001';
  }

  // Force correct port if an outdated config points to 8000
  if (isLocalhost && url && url.includes('localhost:8000')) {
    console.warn('⚠️ Detected localhost:8000 in backend URL, overriding to localhost:8001');
    url = 'http://localhost:8001';
  }

  return url;
};

const BACKEND_URL = getBackendUrl();
const API_BASE = BACKEND_URL ? `${BACKEND_URL}/api` : '/api';

console.log('🔧 API Configuration:', { BACKEND_URL, API_BASE });

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging and auth
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    
    // Add auth token if available - check both regular token and admin token
    const token = localStorage.getItem('token');
    const adminToken = localStorage.getItem('admin_token');
    
    // Use admin token for admin endpoints, regular token for others
    if (config.url?.includes('/admin') && adminToken) {
      config.headers.Authorization = `Bearer ${adminToken}`;
      console.log('🔑 Using admin token for admin endpoint');
    } else if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔑 Using regular token');
    }
    
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;