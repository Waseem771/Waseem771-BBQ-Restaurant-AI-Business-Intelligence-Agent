// Frontend Settings & Configuration Management
// frontend/src/config/settings.js

/**
 * Frontend Application Settings
 * Centralized configuration for all frontend features and behavior
 */

// ============================================================================
// ENVIRONMENT DETECTION
// ============================================================================

const isDevelopment = import.meta.env.MODE === 'development';
const isProduction = import.meta.env.MODE === 'production';

// ============================================================================
// API CONFIGURATION
// ============================================================================

export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  wsURL: import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws',
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'),
  retryAttempts: isProduction ? 3 : 1,
  retryDelay: 1000,

  // Endpoints
  endpoints: {
    // Dashboard
    dashboard: '/dashboard/kpis',
    salesMonthly: '/sales/monthly',
    salesDaily: '/sales/daily',
    salesByBranch: '/sales/by-branch',

    // Products
    productsTop: '/products/top',
    productsCategories: '/products/categories',

    // Analytics
    anomalies: '/anomalies',
    forecast: '/ml/forecast',

    // AI Chat
    aiChat: '/ai/chat',
    aiHistory: '/ai/chat/history',

    // Model Management
    modelsRegister: (name) => `/models/${name}/register`,
    modelsActivate: (name, version) => `/models/${name}/${version}/activate`,
    modelsRollback: (name) => `/models/${name}/rollback`,
    modelsHistory: (name) => `/models/${name}/history`,

    // Health & Status
    health: '/health',
    metrics: '/metrics',
  }
};

// ============================================================================
// UI/UX CONFIGURATION
// ============================================================================

export const UI_CONFIG = {
  // Theme
  theme: import.meta.env.VITE_THEME || 'dark',

  // Sidebar
  sidebar: {
    collapsed: import.meta.env.VITE_SIDEBAR_COLLAPSED === 'true',
    collapsible: true,
    width: 280,
    collapsedWidth: 80,
    animationDuration: 300,
  },

  // Charts
  charts: {
    animationEnabled: import.meta.env.VITE_CHART_ANIMATION !== 'false',
    animationDuration: 800,
    responsive: true,
    maintainAspectRatio: false,
  },

  // Refresh
  autoRefreshInterval: parseInt(import.meta.env.VITE_AUTO_REFRESH_INTERVAL || '5000'),

  // Animations
  transitionDuration: 150,

  // Notifications
  notificationDuration: 5000,

  // Modals
  modalAnimationDuration: 300,

  // Toasts
  toastPosition: 'bottom-right',
  toastDuration: 4000,

  // Defaults
  itemsPerPage: 10,
  maxNotifications: 5,
};

// ============================================================================
// FEATURE FLAGS
// ============================================================================

export const FEATURES = {
  analytics: import.meta.env.VITE_ENABLE_ANALYTICS !== 'false',
  chat: import.meta.env.VITE_ENABLE_CHAT !== 'false',
  models: import.meta.env.VITE_ENABLE_MODELS !== 'false',
  realtime: import.meta.env.VITE_ENABLE_REALTIME !== 'false',
  notifications: import.meta.env.VITE_ENABLE_NOTIFICATIONS !== 'false',
  advancedAnalytics: false, // Phase 13+
  mobileApp: false, // Future
  multiTenant: false, // Phase 15+
};

// ============================================================================
// PERFORMANCE CONFIGURATION
// ============================================================================

export const PERFORMANCE_CONFIG = {
  // Caching
  caching: {
    enabled: import.meta.env.VITE_CACHE_RESPONSES !== 'false',
    maxSize: parseInt(import.meta.env.VITE_MAX_CACHE_SIZE || '50'),
    ttl: parseInt(import.meta.env.VITE_CACHE_TTL || '300000'), // 5 minutes

    // Cache strategies
    strategies: {
      dashboard: 300000, // 5 min
      products: 3600000, // 1 hour
      forecast: 86400000, // 1 day
      models: Infinity, // Never expire until update
    }
  },

  // Lazy loading
  lazyLoading: {
    enabled: import.meta.env.VITE_LAZY_LOAD_CHARTS !== 'false',
    threshold: 0.1,
  },

  // Code splitting
  codeSplitting: {
    enabled: true,
    chunks: ['vendor', 'common', 'ui'],
  },

  // Bundle optimization
  minification: isProduction,
  sourceMap: isDevelopment,
};

// ============================================================================
// DEBUG & LOGGING
// ============================================================================

export const DEBUG_CONFIG = {
  enabled: import.meta.env.VITE_DEBUG_MODE === 'true',
  logLevel: import.meta.env.VITE_LOG_LEVEL || (isDevelopment ? 'debug' : 'warn'),
  showPerformanceMetrics: import.meta.env.VITE_SHOW_PERFORMANCE_METRICS === 'true',

  // Console logging
  console: {
    api: isDevelopment,
    state: isDevelopment,
    navigation: isDevelopment,
  },

  // Performance monitoring
  monitoring: {
    enabled: isDevelopment,
    trackApiCalls: true,
    trackRenders: false,
    trackMemory: false,
  }
};

// ============================================================================
// COLOR PALETTE & STYLING
// ============================================================================

export const COLORS = {
  primary: '#ff6b35',
  secondary: '#f7931e',
  success: '#94d82d',
  warning: '#ffd43b',
  error: '#ff6b6b',
  info: '#339af0',

  background: '#1a1a1a',
  surface: '#2d2d2d',
  surfaceLight: '#3a3a3a',

  text: '#ffffff',
  textMuted: '#b0b0b0',
  textSecondary: '#8a8a8a',

  border: '#404040',
  divider: '#333333',

  // Status colors
  status: {
    active: '#94d82d',
    inactive: '#8a8a8a',
    pending: '#ffd43b',
    error: '#ff6b6b',
  },

  // Chart colors
  chart: {
    line1: '#ff6b35',
    line2: '#f7931e',
    bar: '#ff6b35',
    success: '#94d82d',
    warning: '#ffd43b',
    error: '#ff6b6b',
  }
};

// ============================================================================
// TYPOGRAPHY
// ============================================================================

export const TYPOGRAPHY = {
  fontFamily: {
    default: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    mono: '"IBM Plex Mono", monospace',
  },

  sizes: {
    xs: '0.75rem',     // 12px
    sm: '0.875rem',    // 14px
    base: '1rem',      // 16px
    lg: '1.125rem',    // 18px
    xl: '1.25rem',     // 20px
    '2xl': '1.5rem',   // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
  },

  weights: {
    thin: 100,
    extralight: 200,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
};

// ============================================================================
// BREAKPOINTS
// ============================================================================

export const BREAKPOINTS = {
  xs: '480px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// ============================================================================
// DATA DISPLAY CONFIGURATION
// ============================================================================

export const DATA_DISPLAY = {
  // Number formatting
  currency: {
    symbol: 'PKR',
    position: 'before', // 'before' or 'after'
    decimals: 0,
  },

  // Date formatting
  date: {
    format: 'MMM DD, YYYY',
    timeFormat: 'HH:mm:ss',
  },

  // Chart defaults
  chart: {
    defaultHeight: 300,
    minHeight: 200,
    maxHeight: 500,
    responsive: true,
  },

  // Table defaults
  table: {
    rowsPerPage: 10,
    pageSizes: [5, 10, 20, 50],
  },
};

// ============================================================================
// WEBSOCKET CONFIGURATION
// ============================================================================

export const WEBSOCKET_CONFIG = {
  enabled: FEATURES.realtime,
  reconnect: true,
  reconnectAttempts: 5,
  reconnectDelay: 3000,
  heartbeat: 30000,

  events: {
    connect: 'connect',
    disconnect: 'disconnect',
    dataUpdate: 'data:update',
    anomalyAlert: 'anomaly:alert',
    notification: 'notification:send',
  }
};

// ============================================================================
// AUTHENTICATION CONFIGURATION
// ============================================================================

export const AUTH_CONFIG = {
  enabled: false, // For future implementation
  sessionTimeout: 3600000, // 1 hour
  refreshInterval: 300000, // 5 minutes
  storageKey: 'auth_token',
};

// ============================================================================
// ERROR HANDLING
// ============================================================================

export const ERROR_HANDLING = {
  showErrorBoundary: isDevelopment,
  logErrors: true,
  retryFailedRequests: true,

  // Error messages
  messages: {
    networkError: 'Network connection failed. Please check your connection.',
    apiError: 'API request failed. Please try again.',
    validationError: 'Please check the entered data.',
    notFound: 'The requested resource was not found.',
    unauthorized: 'You are not authorized to perform this action.',
    serverError: 'Server error occurred. Please try again later.',
  }
};

// ============================================================================
// ACCESSIBILITY
// ============================================================================

export const ACCESSIBILITY = {
  focusVisible: true,
  reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  highContrast: window.matchMedia('(prefers-contrast: more)').matches,
  darkMode: window.matchMedia('(prefers-color-scheme: dark)').matches,
  fontSize: 'normal', // 'small', 'normal', 'large'
};

// ============================================================================
// APPLICATION METADATA
// ============================================================================

export const APP_META = {
  name: import.meta.env.VITE_APP_NAME || 'BBQ Restaurant AI BI',
  version: import.meta.env.VITE_APP_VERSION || '1.0.0',
  description: 'AI-powered Business Intelligence Dashboard for BBQ Restaurants',
  author: 'BBQ AI Team',
  environment: import.meta.env.VITE_ENV || 'development',

  // URLs
  urls: {
    home: '/',
    dashboard: '/dashboard',
    analytics: '/analytics',
    models: '/models',
    settings: '/settings',
  },

  // Support
  support: {
    email: 'support@bbq-ai.local',
    documentation: '/docs',
    github: 'https://github.com/bbq-ai/bbq-bi',
  }
};

// ============================================================================
// EXPORT COMPLETE CONFIG
// ============================================================================

export const CONFIG = {
  API: API_CONFIG,
  UI: UI_CONFIG,
  FEATURES,
  PERFORMANCE: PERFORMANCE_CONFIG,
  DEBUG: DEBUG_CONFIG,
  COLORS,
  TYPOGRAPHY,
  BREAKPOINTS,
  DATA: DATA_DISPLAY,
  WEBSOCKET: WEBSOCKET_CONFIG,
  AUTH: AUTH_CONFIG,
  ERROR: ERROR_HANDLING,
  ACCESSIBILITY,
  APP: APP_META,

  // Environment info
  environment: {
    isDevelopment,
    isProduction,
    mode: import.meta.env.MODE,
  }
};

export default CONFIG;
