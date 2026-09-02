// Utility functions for data formatting and helpers

export const formatCurrency = (value) => {
  if (!value) return '₨0';
  return `₨${(value / 1000000).toFixed(2)}M`;
};

export const formatNumber = (value) => {
  if (!value) return '0';
  return value.toLocaleString();
};

export const formatPercentage = (value) => {
  if (!value) return '0%';
  return `${(value * 100).toFixed(1)}%`;
};

export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const calculateTrend = (current, previous) => {
  if (!previous) return 0;
  return ((current - previous) / previous) * 100;
};

export const getTrendColor = (value) => {
  if (value > 0) return '#94d82d'; // Green
  if (value < 0) return '#ff6b6b'; // Red
  return '#b0b0b0'; // Gray
};

export const getTrendIcon = (value) => {
  if (value > 0) return '📈';
  if (value < 0) return '📉';
  return '➡️';
};

export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

export const throttle = (func, limit) => {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

// Chart color schemes
export const chartColors = {
  primary: '#ff6b35',
  secondary: '#f7931e',
  success: '#94d82d',
  warning: '#ffa94d',
  danger: '#ff6b6b',
  info: '#74c0fc',
};

// Severity colors for anomalies
export const severityColors = {
  high: { bg: '#ff6b6b', text: '#ffffff', border: '#ff6b6b' },
  warning: { bg: '#ffa94d', text: '#ffffff', border: '#ffa94d' },
  info: { bg: '#74c0fc', text: '#ffffff', border: '#74c0fc' },
};
