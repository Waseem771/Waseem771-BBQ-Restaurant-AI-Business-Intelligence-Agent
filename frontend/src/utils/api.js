// frontend/src/utils/api.js
// Centralized API utilities for HTTP requests

import axios from 'axios';

/**
 * API Configuration
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const REQUEST_TIMEOUT = 30000; // 30 seconds

/**
 * Create axios instance with default config
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  }
});

/**
 * Request interceptor
 * Add auth token and logging
 */
apiClient.interceptors.request.use(
  config => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`📡 ${config.method.toUpperCase()} ${config.url}`, config.data);
    }

    return config;
  },
  error => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

/**
 * Response interceptor
 * Handle errors and logging
 */
apiClient.interceptors.response.use(
  response => {
    // Log successful response
    if (import.meta.env.DEV) {
      console.log(`✅ ${response.status} ${response.config.url}`, response.data);
    }
    return response.data;
  },
  error => {
    // Handle specific error cases
    if (error.response) {
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }

      if (status === 403) {
        console.error('❌ Access Forbidden:', data);
      }

      if (status >= 500) {
        console.error('❌ Server Error:', status, data);
      }

      console.error(`❌ ${status} ${error.config.url}`, data);
    } else if (error.request) {
      console.error('❌ No response from server:', error.request);
    } else {
      console.error('❌ Error:', error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * API Methods
 */
export const api = {
  // Dashboard
  getDashboardMetrics: () => apiClient.get('/dashboard/metrics'),
  getDashboardCharts: () => apiClient.get('/dashboard/charts'),

  // Sales
  getSales: (params) => apiClient.get('/sales', { params }),
  getSalesMetrics: (period) => apiClient.get(`/sales/metrics/${period}`),

  // Products
  getProducts: (params) => apiClient.get('/products', { params }),
  getProductPerformance: () => apiClient.get('/products/performance'),

  // AI Agent
  askAgent: (question) => apiClient.post('/ai/chat', { question }),
  getAgentHistory: () => apiClient.get('/ai/history'),

  // Forecasting
  getForecast: (params) => apiClient.get('/ml/forecast', { params }),

  // Anomalies
  getAnomalies: (params) => apiClient.get('/ml/anomalies', { params }),

  // Models
  getModels: () => apiClient.get('/models'),
  getModelMetrics: (modelId) => apiClient.get(`/models/${modelId}/metrics`),
  activateModel: (modelId) => apiClient.post(`/models/${modelId}/activate`),

  // Health
  getHealth: () => apiClient.get('/health'),
};

/**
 * Utility functions
 */
export const apiUtils = {
  /**
   * Retry failed requests
   */
  retry: async (fn, maxRetries = 3, delay = 1000) => {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
      }
    }
  },

  /**
   * Batch requests
   */
  batch: async (requests) => {
    return Promise.all(requests.map(req => apiClient(req)));
  },

  /**
   * Cancel pending requests
   */
  cancelPending: () => {
    const controller = new AbortController();
    return controller;
  },

  /**
   * Format error message
   */
  getErrorMessage: (error) => {
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    if (error.message) {
      return error.message;
    }
    return 'An unexpected error occurred';
  },
};

export default apiClient;
