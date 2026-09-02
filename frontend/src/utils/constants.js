// frontend/src/utils/constants.js
// Application constants and configuration

/**
 * API Configuration
 */
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
};

/**
 * Theme Configuration
 */
export const THEME_CONFIG = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto',
};

/**
 * Color Palette
 */
export const COLORS = {
  PRIMARY: '#ff6b35',
  SECONDARY: '#f7931e',
  SUCCESS: '#94d82d',
  WARNING: '#ffa94d',
  ERROR: '#ff6b6b',
  BACKGROUND: '#1a1a1a',
  CARD_BG: '#2d2d2d',
  BORDER: '#404040',
  TEXT: '#ffffff',
  TEXT_MUTED: '#b0b0b0',
};

/**
 * Dashboard Tabs
 */
export const DASHBOARD_TABS = {
  DASHBOARD: 'dashboard',
  ANALYTICS: 'analytics',
  MODELS: 'models',
  ANOMALIES: 'anomalies',
  SETTINGS: 'settings',
};

/**
 * Chart Colors
 */
export const CHART_COLORS = {
  REVENUE: '#ff6b35',
  ORDERS: '#f7931e',
  FORECAST: '#94d82d',
  ANOMALY: '#ff6b6b',
};

/**
 * Notification Types
 */
export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
};

/**
 * Alert Severity Levels
 */
export const SEVERITY_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical',
};

/**
 * Time Formats
 */
export const TIME_FORMATS = {
  SHORT_DATE: 'MMM DD',
  LONG_DATE: 'MMMM DD, YYYY',
  TIME: 'HH:mm',
  DATETIME: 'MMMM DD, YYYY HH:mm',
};

/**
 * Pagination Config
 */
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 20, 50],
};

/**
 * Debounce Delays (ms)
 */
export const DEBOUNCE_DELAYS = {
  SEARCH: 300,
  AUTO_SAVE: 1000,
  RESIZE: 500,
  SCROLL: 200,
};

/**
 * Animation Durations (ms)
 */
export const ANIMATION_DURATIONS = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
};

/**
 * Storage Keys
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'bbq_user_preferences',
  THEME: 'bbq_theme',
  SIDEBAR_STATE: 'bbq_sidebar_open',
  CACHE_TIMESTAMP: 'bbq_cache_timestamp',
};

/**
 * Default Settings
 */
export const DEFAULT_SETTINGS = {
  THEME: THEME_CONFIG.AUTO,
  AUTO_REFRESH_INTERVAL: 30000,
  ANIMATION_ENABLED: true,
  NOTIFICATIONS_ENABLED: true,
  SOUND_ENABLED: false,
};

/**
 * Regular Expressions
 */
export const REGEX_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^[\d\s\-\+\(\)]+$/,
  URL: /^https?:\/\/.+/,
  NUMBER: /^\d+$/,
  CURRENCY: /^₨?\s?[\d,]+(?:\.\d{2})?$/,
};

/**
 * Error Messages
 */
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  UNKNOWN_ERROR: 'An unexpected error occurred.',
};

/**
 * Success Messages
 */
export const SUCCESS_MESSAGES = {
  SAVED: 'Changes saved successfully.',
  DELETED: 'Item deleted successfully.',
  CREATED: 'Item created successfully.',
  UPDATED: 'Item updated successfully.',
};

export default {
  API_CONFIG,
  THEME_CONFIG,
  COLORS,
  DASHBOARD_TABS,
  CHART_COLORS,
  NOTIFICATION_TYPES,
  SEVERITY_LEVELS,
  TIME_FORMATS,
  PAGINATION,
  DEBOUNCE_DELAYS,
  ANIMATION_DURATIONS,
  STORAGE_KEYS,
  DEFAULT_SETTINGS,
  REGEX_PATTERNS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
};
