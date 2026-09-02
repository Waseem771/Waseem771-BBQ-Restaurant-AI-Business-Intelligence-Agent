// frontend/src/hooks/useDebounce.js
// Debounce hook for performance optimization

import { useState, useEffect } from 'react';

/**
 * useDebounce Hook
 * Delays value updates to prevent excessive re-renders
 * @param {any} value - Value to debounce
 * @param {number} delay - Delay in milliseconds (default: 500)
 * @returns {any} - Debounced value
 */
export const useDebounce = (value, delay = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};

export default useDebounce;
