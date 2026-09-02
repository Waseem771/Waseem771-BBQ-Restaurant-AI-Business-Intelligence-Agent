import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Service with all endpoints
export const api = {
  // Dashboard Endpoints
  dashboard: {
    getMetrics: () => apiClient.get('/dashboard/metrics'),
    getSalesTrend: (period = '30d') => apiClient.get(`/dashboard/sales-trend?period=${period}`),
    getProducts: () => apiClient.get('/dashboard/products'),
    getProductsByCategory: () => apiClient.get('/dashboard/products/category'),
  },

  // Analytics Endpoints
  analytics: {
    getSalesComparison: (period1, period2) =>
      apiClient.post('/analytics/compare', { period1, period2 }),
    getTrends: (metric, days = 30) =>
      apiClient.get(`/analytics/trends?metric=${metric}&days=${days}`),
    getDetailedAnalytics: () => apiClient.get('/analytics/detailed'),
  },

  // AI/Agent Endpoints
  ai: {
    chat: (message) => apiClient.post('/ai/chat', { message }),
    askQuestion: (question) => apiClient.post('/ai/ask', { question }),
    getSuggestions: () => apiClient.get('/ai/suggestions'),
  },

  // Anomalies Endpoints
  anomalies: {
    getList: () => apiClient.get('/anomalies'),
    getById: (id) => apiClient.get(`/anomalies/${id}`),
    acknowledge: (id) => apiClient.post(`/anomalies/${id}/acknowledge`),
  },

  // Forecast Endpoints
  forecast: {
    getSalesForecast: (days = 30) => apiClient.get(`/forecast/sales?days=${days}`),
    getDemandForecast: (days = 30) => apiClient.get(`/forecast/demand?days=${days}`),
  },

  // Models Endpoints
  models: {
    getStatus: () => apiClient.get('/models/status'),
    getMetrics: (modelName) => apiClient.get(`/models/${modelName}/metrics`),
    retrain: (modelName) => apiClient.post(`/models/${modelName}/retrain`),
  },

  // Health Check
  health: () => apiClient.get('/health'),
};

// Error handling interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
);

export default apiClient;
